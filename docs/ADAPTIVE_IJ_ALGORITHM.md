# Adaptive I/J Selection Algorithm for SAPO

**Novel Contribution for Master's Thesis**

## 🎯 Core Idea

The SAPO paper uses **fixed I/J ratios** (e.g., 4 local / 4 external). This document proposes **adaptive I/J selection** that changes during training based on performance signals.

**Hypothesis**: Optimal I/J ratio changes over training phases:
- **Early training**: High J (learn from diverse swarm)
- **Mid training**: Balanced I/J (consolidate learning)
- **Late training**: High I (specialize, avoid interference)

---

## 📊 Algorithm Design

### **Version 1: Reward-Based Adaptation** (Simplest)

```python
class AdaptiveIJSelector:
    def __init__(self, total_samples=8, window=10, threshold=0.05):
        self.total = total_samples  # I + J = 8 (fixed)
        self.window = window        # Moving average window
        self.threshold = threshold  # Reward improvement threshold

        # State
        self.current_I = 4  # Start balanced
        self.current_J = 4
        self.reward_history = []

    def update(self, round_reward):
        """Called after each round with average reward"""
        self.reward_history.append(round_reward)

        # Wait for enough history
        if len(self.reward_history) < self.window:
            return self.current_I, self.current_J

        # Compute trend
        recent = np.mean(self.reward_history[-self.window:])
        previous = np.mean(self.reward_history[-(2*self.window):-self.window])
        improvement = (recent - previous) / (previous + 1e-8)

        # Adaptation rules
        if improvement > self.threshold:
            # Learning well → maintain or reduce external
            self.current_J = max(0, self.current_J - 1)
            self.current_I = self.total - self.current_J
        elif improvement < -self.threshold:
            # Struggling → increase external help
            self.current_J = min(self.total, self.current_J + 1)
            self.current_I = self.total - self.current_J
        # else: no change

        return self.current_I, self.current_J
```

**Pros**:
- Simple to implement
- Clear logic: struggling → more help, succeeding → more independence
- Easy to analyze

**Cons**:
- May oscillate
- Doesn't detect "aha moments" explicitly

---

### **Version 2: Gradient-Based Adaptation** (Better)

```python
class GradientAdaptiveIJ:
    def __init__(self, total_samples=8, adaptation_rate=0.1):
        self.total = total_samples
        self.alpha = adaptation_rate  # Learning rate for J

        # State
        self.J_continuous = 4.0  # Continuous value
        self.baseline_reward = 0.0
        self.baseline_alpha = 0.95  # EMA for baseline

    def update(self, round_reward):
        """Update J based on reward gradient"""
        # Update baseline (EMA)
        self.baseline_reward = (self.baseline_alpha * self.baseline_reward +
                                (1 - self.baseline_alpha) * round_reward)

        # Compute advantage
        advantage = round_reward - self.baseline_reward

        # Update J (gradient ascent)
        # If advantage > 0 with current J → increase J slightly
        # If advantage < 0 with current J → decrease J
        self.J_continuous += self.alpha * advantage

        # Clip to valid range
        self.J_continuous = np.clip(self.J_continuous, 0, self.total)

        # Discretize
        J = int(np.round(self.J_continuous))
        I = self.total - J

        return I, J
```

**Pros**:
- Smooth adaptation
- Doesn't oscillate as much
- Theoretically grounded (gradient ascent)

**Cons**:
- Harder to interpret
- Requires hyperparameter tuning (alpha)

---

### **Version 3: Multi-Signal Adaptation** (Most Sophisticated)

```python
class MultiSignalAdaptiveIJ:
    def __init__(self, total_samples=8):
        self.total = total_samples
        self.current_I = 4
        self.current_J = 4

        # Multiple signals
        self.reward_history = []
        self.variance_history = []
        self.swarm_quality_history = []

    def update(self, round_data):
        """
        round_data = {
            'my_reward': float,
            'my_variance': float,  # Variance across generations
            'swarm_avg_reward': float,  # Average from swarm rollouts
            'swarm_quality': float  # % of swarm rollouts with advantage > 0
        }
        """
        self.reward_history.append(round_data['my_reward'])
        self.variance_history.append(round_data['my_variance'])
        self.swarm_quality_history.append(round_data['swarm_quality'])

        # Signal 1: Reward trend
        reward_trend = self._compute_trend(self.reward_history)

        # Signal 2: Learning stability
        variance_trend = self._compute_trend(self.variance_history)

        # Signal 3: Swarm quality
        swarm_quality = np.mean(self.swarm_quality_history[-10:]) if len(self.swarm_quality_history) >= 10 else 0.5

        # Decision logic
        if reward_trend > 0.05 and variance_trend < 0:
            # Learning well and stable → reduce J (more independence)
            self.current_J = max(0, self.current_J - 1)
        elif reward_trend < -0.05 or variance_trend > 0.1:
            # Struggling or unstable → increase J if swarm is good
            if swarm_quality > 0.3:
                self.current_J = min(self.total, self.current_J + 1)
        elif swarm_quality < 0.2:
            # Swarm quality poor → reduce J
            self.current_J = max(0, self.current_J - 1)

        self.current_I = self.total - self.current_J

        return self.current_I, self.current_J

    def _compute_trend(self, history, window=10):
        if len(history) < window * 2:
            return 0
        recent = np.mean(history[-window:])
        previous = np.mean(history[-(2*window):-window])
        return (recent - previous) / (abs(previous) + 1e-8)
```

**Pros**:
- Uses multiple signals (robust)
- Detects swarm quality degradation
- Can handle complex scenarios

**Cons**:
- Most complex
- Requires instrumentation for all signals
- Many hyperparameters

---

## 🧪 Implementation Plan

### **For Master's Thesis: Recommend Version 2 (Gradient-Based)**

**Why**:
1. **Simple enough** to implement and debug
2. **Sophisticated enough** to be a contribution
3. **Theoretically motivated** (easy to justify)
4. **Smooth adaptation** (better for analysis)

### **Implementation Steps**

**Step 1**: Modify `swarm_launcher.py`
```python
# Add adaptive mode flag
ADAPTIVE_MODE = os.environ.get('ADAPTIVE_IJ', 'False').lower() == 'true'

if ADAPTIVE_MODE:
    from rgym_exp.utils.adaptive_ij import GradientAdaptiveIJ
    ij_selector = GradientAdaptiveIJ(
        total_samples=NUM_TRAIN_SAMPLES + NUM_TRANSPLANT_TREES,
        adaptation_rate=float(os.environ.get('ADAPTIVE_RATE', '0.1'))
    )
```

**Step 2**: Create `rgym_exp/utils/adaptive_ij.py`
```python
# Full implementation of GradientAdaptiveIJ class
```

**Step 3**: Modify `manager.py` to use adaptive I/J
```python
def _hook_after_round_advanced(self):
    # ... existing code ...

    if hasattr(self, 'ij_selector'):
        # Get average reward this round
        round_reward = self._get_average_round_reward()

        # Update I/J
        new_I, new_J = self.ij_selector.update(round_reward)

        # Update data manager
        self.data_manager.update_sample_sizes(new_I, new_J)

        # Log adaptation
        logger.info(f"Adaptive I/J: Round {self.state.round} → I={new_I}, J={new_J}, reward={round_reward:.3f}")
```

**Step 4**: Log I/J trajectory
```python
# Save to GDrive for analysis
ij_log = {
    'round': self.state.round,
    'I': new_I,
    'J': new_J,
    'reward': round_reward,
    'J_continuous': self.ij_selector.J_continuous
}
self.gdrive_logger.log_ij_adaptation(ij_log)
```

---

## 📊 Experimental Design

### **Experiment Set**

| Name | I | J | Description |
|------|---|---|-------------|
| **baseline** | 4 | 0 | No swarm (reference) |
| **fixed_4_4** | 4 | 4 | Fixed balanced (paper's best) |
| **adaptive_v2** | adaptive | adaptive | Gradient-based adaptation |

### **Hypotheses**

**H1**: Adaptive outperforms fixed 4/4 in cumulative reward
- **Measure**: Total cumulative reward over 2000 rounds
- **Test**: t-test between adaptive and fixed_4_4

**H2**: Adaptive shows different I/J ratios in different phases
- **Measure**: Plot J over rounds
- **Expected**: J starts high, decreases over time

**H3**: Adaptive is more stable than 1/3 config
- **Measure**: Variance of rewards, oscillation count
- **Test**: Compare variance(adaptive) vs variance(1/3)

### **Metrics to Collect**

**Primary**:
- Cumulative reward (sum over all rounds)
- Final model performance (pass@1 on held-out test set)

**Secondary**:
- I/J trajectory (plot over rounds)
- Adaptation frequency (how often I/J changes)
- Reward variance (stability measure)

**Analysis**:
- Correlation between J and reward improvement
- Phase analysis (early/mid/late training patterns)
- Swarm quality vs J (does high J require high swarm quality?)

---

## 📈 Expected Results

### **Optimistic Scenario** (Thesis success)

```
Cumulative Rewards (2000 rounds, GPT-2):
  Baseline (4/0):     250
  Fixed (4/4):        600  (+140%)
  Adaptive (v2):      720  (+188%)  ✅ BEST
```

**I/J Trajectory**:
- Rounds 0-500: J=6-7 (learn from swarm)
- Rounds 500-1500: J=3-5 (balanced)
- Rounds 1500-2000: J=1-2 (specialize)

**Conclusion**: Adaptive beats fixed by +20%, validates hypothesis

---

### **Neutral Scenario** (Still publishable)

```
Cumulative Rewards:
  Baseline (4/0):     250
  Fixed (4/4):        600  (+140%)
  Adaptive (v2):      580  (+132%)  ⚠️ Slightly worse
```

**I/J Trajectory**: Oscillates, no clear pattern

**Conclusion**:
- Adaptation doesn't hurt much (-3%)
- Analysis shows why: swarm quality varied, no single strategy optimal
- Contribution: Understanding when adaptation helps vs hurts
- **Still a complete thesis** with negative result analysis

---

### **Pessimistic Scenario** (Debugging needed)

```
Cumulative Rewards:
  Baseline (4/0):     250
  Fixed (4/4):        600  (+140%)
  Adaptive (v2):      400  (+60%)   ❌ Much worse
```

**Diagnosis**:
- Check if adaptation is too aggressive (reduce alpha)
- Check if baseline estimation is wrong
- Check if swarm quality too low for high J

**Recovery**:
- Try Version 1 (simpler, more robust)
- Add constraints (J ∈ [2,6] instead of [0,8])
- Analyze failures to understand why

---

## 🔧 Hyperparameters to Tune

**For GradientAdaptiveIJ**:

| Parameter | Range | Default | Notes |
|-----------|-------|---------|-------|
| `adaptation_rate` | 0.01 - 0.5 | 0.1 | Higher = faster adaptation |
| `baseline_alpha` | 0.9 - 0.99 | 0.95 | Higher = slower baseline update |
| `initial_J` | 0 - 8 | 4 | Starting value |
| `clip_min` | 0 - 2 | 0 | Minimum J allowed |
| `clip_max` | 6 - 8 | 8 | Maximum J allowed |

**Tuning Strategy**:
1. Run 3-5 short experiments (100 rounds each) with different `adaptation_rate`
2. Pick best performer
3. Run full 2000-round experiment with best hyperparameters

---

## 📝 Thesis Chapter Outline (Chapter 5)

**Chapter 5: Adaptive I/J Selection**

**5.1 Motivation** (2-3 pages)
- Why fixed ratios suboptimal
- Different training phases need different strategies
- Cite multi-stage curriculum learning papers

**5.2 Algorithm Design** (3-4 pages)
- Describe GradientAdaptiveIJ
- Justify gradient-based approach
- Derivation from policy gradient perspective

**5.3 Implementation** (2 pages)
- Code snippets
- Integration with SAPO
- Logging infrastructure

**5.4 Experimental Setup** (2 pages)
- Baseline vs Fixed vs Adaptive comparison
- Hyperparameter choices
- Evaluation metrics

**5.5 Results** (5-6 pages)
- Cumulative reward comparison
- I/J trajectory plots
- Phase analysis
- Statistical significance tests

**5.6 Analysis** (3-4 pages)
- Why does adaptation help (or not)?
- When does high J work?
- Failure mode analysis

**5.7 Summary** (1 page)

**Total**: 18-24 pages (substantial contribution)

---

## 🚀 Timeline for Implementation

**Week 7-8**: Design & Implementation
- Day 1-3: Implement `GradientAdaptiveIJ` class
- Day 4-5: Integrate into `swarm_launcher.py` and `manager.py`
- Day 6-7: Add logging and testing

**Week 9**: Hyperparameter Tuning
- Run 5 short experiments (100 rounds each)
- Pick best `adaptation_rate`
- Document tuning process

**Week 10-12**: Full Experiments
- Run adaptive (2000 rounds) × 3 seeds
- Run fixed 4/4 (2000 rounds) × 3 seeds (if not done in Phase 1)
- Total: 6 × 21 hours = 126 hours (~5 days GPU time)

**Week 13**: Analysis
- Plot I/J trajectories
- Compute statistics
- Write Chapter 5

---

## 📚 Related Work to Cite

**Curriculum Learning**:
- Bengio et al. (2009) - Curriculum Learning
- Graves et al. (2017) - Automated Curriculum Learning

**Adaptive Methods**:
- Schaul et al. (2015) - Prioritized Experience Replay
- Andrychowicz et al. (2017) - Hindsight Experience Replay

**Multi-stage RL**:
- Silver et al. (2017) - AlphaGo Zero (different strategies in opening/mid/endgame)

---

## ✅ Success Criteria

**Minimum (Pass)**:
- ✅ Adaptive method implemented and runs
- ✅ Compared to fixed 4/4
- ✅ Analysis of results (even if negative)

**Good**:
- ✅ All of above
- ✅ Adaptive matches or beats fixed 4/4
- ✅ Clear I/J trajectory patterns

**Excellent**:
- ✅ All of above
- ✅ Adaptive beats fixed by >10%
- ✅ Theoretical justification for trajectory patterns
- ✅ Ablation studies showing importance of components

---

**Document Version**: 1.0
**Created**: 2025-01-16
**Author**: Claude (Anthropic)
**For**: Master's Thesis - Adaptive SAPO
