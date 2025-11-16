"""
Adaptive I/J Selection Algorithm (Version 2: Gradient-Based)

This module implements the gradient-based adaptive algorithm for dynamically
selecting the optimal ratio of local (I) to external (J) rollouts during
SAPO training.

Algorithm Design:
- Maintains continuous J value with gradient updates
- Uses exponential moving average baseline for advantage estimation
- Clips J to valid range [0, total_samples]
- Rounds to nearest integer for actual sampling

References:
- ADAPTIVE_IJ_ALGORITHM.md - Full algorithm documentation
- SAPO paper (arXiv:2509.08721) - Fixed I/J baseline results
"""

import numpy as np
from typing import Tuple, Dict, Any
import logging

logger = logging.getLogger(__name__)


class GradientAdaptiveIJ:
    """
    Gradient-based adaptive I/J selection using policy gradient approach.

    This algorithm treats J as a continuous parameter and updates it using
    gradient ascent on the reward signal. It maintains a baseline using
    exponential moving average to reduce variance.

    Key features:
    - Continuous J optimization with gradient updates
    - Baseline-adjusted advantage for variance reduction
    - Smooth adaptation with configurable learning rate
    - Automatic clipping to valid range

    Args:
        total_samples: Total rollouts per round (I + J), typically 8
        adaptation_rate: Learning rate for gradient updates (alpha), default 0.1
        baseline_alpha: EMA smoothing for baseline, default 0.95
        initial_J: Starting value for J (default: total_samples / 2)
        min_J: Minimum allowed J value (default: 0)
        max_J: Maximum allowed J value (default: total_samples)

    Example:
        >>> adapter = GradientAdaptiveIJ(total_samples=8, adaptation_rate=0.1)
        >>> I, J = adapter.get_current_ij()
        >>> print(f"Round 0: I={I}, J={J}")
        Round 0: I=4, J=4
        >>>
        >>> # After training round with reward=0.65
        >>> I, J = adapter.update(round_reward=0.65)
        >>> print(f"Round 1: I={I}, J={J}")
        Round 1: I=4, J=4  # May change based on advantage
    """

    def __init__(
        self,
        total_samples: int = 8,
        adaptation_rate: float = 0.1,
        baseline_alpha: float = 0.95,
        initial_J: float = None,
        min_J: int = 0,
        max_J: int = None
    ):
        self.total_samples = total_samples
        self.alpha = adaptation_rate
        self.baseline_alpha = baseline_alpha

        # Initialize J to middle of range by default
        if initial_J is None:
            initial_J = total_samples / 2.0
        self.initial_J = float(initial_J)  # Save for reset()
        self.J_continuous = float(initial_J)

        # Set valid range
        self.min_J = min_J
        self.max_J = max_J if max_J is not None else total_samples

        # Baseline reward (exponential moving average)
        self.baseline_reward = 0.0
        self.rounds_completed = 0

        # History tracking for analysis
        self.history = {
            'rounds': [],
            'rewards': [],
            'baselines': [],
            'advantages': [],
            'J_continuous': [],
            'J_discrete': [],
            'I_discrete': []
        }

        logger.info(
            f"Initialized GradientAdaptiveIJ: "
            f"total={total_samples}, alpha={adaptation_rate}, "
            f"baseline_alpha={baseline_alpha}, initial_J={initial_J:.2f}"
        )

    def get_current_ij(self) -> Tuple[int, int]:
        """
        Get current I/J values without updating.

        Returns:
            (I, J): Current integer values for local and external rollouts
        """
        J = self._discretize_J()
        I = self.total_samples - J
        return I, J

    def update(self, round_reward: float) -> Tuple[int, int]:
        """
        Update J based on round reward and return new I/J values.

        Args:
            round_reward: Reward achieved in the completed round (e.g., accuracy)

        Returns:
            (I, J): Updated integer values for next round
        """
        # Update baseline using exponential moving average
        if self.rounds_completed == 0:
            # First round: initialize baseline to first reward
            self.baseline_reward = round_reward
        else:
            self.baseline_reward = (
                self.baseline_alpha * self.baseline_reward +
                (1 - self.baseline_alpha) * round_reward
            )

        # Compute advantage (reward - baseline)
        advantage = round_reward - self.baseline_reward

        # Gradient update: J ← J + α * advantage
        self.J_continuous += self.alpha * advantage

        # Clip to valid range
        self.J_continuous = np.clip(self.J_continuous, self.min_J, self.max_J)

        # Discretize for actual use
        J = self._discretize_J()
        I = self.total_samples - J

        # Record history
        self.rounds_completed += 1
        self.history['rounds'].append(self.rounds_completed)
        self.history['rewards'].append(round_reward)
        self.history['baselines'].append(self.baseline_reward)
        self.history['advantages'].append(advantage)
        self.history['J_continuous'].append(self.J_continuous)
        self.history['J_discrete'].append(J)
        self.history['I_discrete'].append(I)

        logger.info(
            f"Round {self.rounds_completed}: "
            f"reward={round_reward:.4f}, baseline={self.baseline_reward:.4f}, "
            f"advantage={advantage:+.4f}, J_cont={self.J_continuous:.2f} → "
            f"I={I}, J={J}"
        )

        return I, J

    def _discretize_J(self) -> int:
        """Convert continuous J to integer using rounding."""
        return int(np.round(self.J_continuous))

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get current statistics for monitoring/logging.

        Returns:
            Dictionary with current state and summary statistics
        """
        I, J = self.get_current_ij()

        stats = {
            'rounds_completed': self.rounds_completed,
            'current_I': I,
            'current_J': J,
            'J_continuous': float(self.J_continuous),
            'baseline_reward': float(self.baseline_reward),
            'total_samples': self.total_samples,
            'adaptation_rate': self.alpha,
        }

        # Add summary statistics if we have history
        if self.rounds_completed > 0:
            stats['mean_reward'] = float(np.mean(self.history['rewards']))
            stats['std_reward'] = float(np.std(self.history['rewards']))
            stats['mean_J'] = float(np.mean(self.history['J_discrete']))
            stats['std_J'] = float(np.std(self.history['J_discrete']))

        return stats

    def get_history(self) -> Dict[str, list]:
        """
        Get complete adaptation history for analysis.

        Returns:
            Dictionary with lists of all tracked values over time
        """
        return self.history.copy()

    def reset(self):
        """Reset the adapter to initial state (useful for multiple experiments)."""
        self.J_continuous = self.initial_J  # Use saved initial value
        self.baseline_reward = 0.0
        self.rounds_completed = 0
        self.history = {
            'rounds': [],
            'rewards': [],
            'baselines': [],
            'advantages': [],
            'J_continuous': [],
            'J_discrete': [],
            'I_discrete': []
        }
        logger.info("GradientAdaptiveIJ reset to initial state")


# Convenience function for easy integration
def create_adaptive_ij(
    total_samples: int = 8,
    adaptation_rate: float = 0.1,
    **kwargs
) -> GradientAdaptiveIJ:
    """
    Factory function to create GradientAdaptiveIJ instance with sensible defaults.

    Args:
        total_samples: Total rollouts per round (default: 8)
        adaptation_rate: Learning rate for updates (default: 0.1)
        **kwargs: Additional arguments passed to GradientAdaptiveIJ

    Returns:
        Configured GradientAdaptiveIJ instance
    """
    return GradientAdaptiveIJ(
        total_samples=total_samples,
        adaptation_rate=adaptation_rate,
        **kwargs
    )
