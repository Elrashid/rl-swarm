"""
Cumulative Reward Progress Monitoring for SAPO Experiments

This module provides real-time monitoring of total_cumulative_reward
(the primary SAPO paper metric) across all nodes in an experiment.
"""

import os
import json
import time
from typing import Dict, List, Tuple
from rgym_exp.vendor.genrl.logging_utils.global_defs import get_logger


def get_live_cumulative_rewards(gdrive_base_path: str, experiment_name: str) -> Tuple[float, Dict[str, float], int]:
    """
    Get live cumulative reward metrics from all nodes.

    Args:
        gdrive_base_path: Base path in Google Drive
        experiment_name: Name of experiment

    Returns:
        Tuple of (total_cumulative_reward, per_node_rewards, current_round)
    """
    exp_path = os.path.join(gdrive_base_path, 'experiments', experiment_name)
    logs_dir = os.path.join(exp_path, 'logs')

    if not os.path.exists(logs_dir):
        return 0.0, {}, 0

    cumulative_rewards = {}
    latest_round = 0

    try:
        # Read cumulative metrics from each node
        for node_dir in os.listdir(logs_dir):
            cumulative_file = os.path.join(logs_dir, node_dir, 'cumulative_metrics.jsonl')

            if not os.path.exists(cumulative_file):
                continue

            # Read last line (most recent cumulative value)
            with open(cumulative_file, 'r') as f:
                lines = f.readlines()
                if lines:
                    try:
                        last_entry = json.loads(lines[-1])
                        peer_id = last_entry.get('peer_id', node_dir)
                        cumulative_rewards[peer_id] = last_entry.get('cumulative_reward', 0.0)

                        # Track latest round
                        node_round = last_entry.get('round', 0)
                        if node_round > latest_round:
                            latest_round = node_round

                    except json.JSONDecodeError:
                        continue

    except Exception as e:
        get_logger().error(f"Error reading cumulative rewards: {e}")
        return 0.0, {}, 0

    total_cumulative = sum(cumulative_rewards.values())

    return total_cumulative, cumulative_rewards, latest_round


def display_cumulative_progress(gdrive_base_path: str, experiment_name: str,
                                max_rounds: int = None, baseline_reward: float = None):
    """
    Display cumulative reward progress in a clear format.

    Args:
        gdrive_base_path: Base path in Google Drive
        experiment_name: Name of experiment
        max_rounds: Maximum rounds (for progress %)
        baseline_reward: Baseline cumulative reward (for improvement %)
    """
    total, per_node, current_round = get_live_cumulative_rewards(gdrive_base_path, experiment_name)

    print("="*70)
    print("TOTAL CUMULATIVE REWARD PROGRESS (SAPO Paper Metric)")
    print("="*70)
    print(f"Experiment: {experiment_name}")
    print(f"Round: {current_round}", end="")
    if max_rounds:
        progress_pct = (current_round / max_rounds) * 100
        print(f" / {max_rounds} ({progress_pct:.1f}%)")
    else:
        print()
    print()

    print(f"📊 TOTAL CUMULATIVE REWARD: {total:8.2f}")
    print()

    if baseline_reward and baseline_reward > 0:
        improvement = ((total - baseline_reward) / baseline_reward) * 100
        print(f"Improvement vs Baseline:")
        print(f"  Baseline: {baseline_reward:8.2f}")
        print(f"  Current:  {total:8.2f}")
        print(f"  Change:   {improvement:+7.1f}%")
        print()

    if per_node:
        print(f"Per-Node Breakdown ({len(per_node)} nodes):")
        for node_id in sorted(per_node.keys()):
            reward = per_node[node_id]
            pct = (reward / total * 100) if total > 0 else 0
            print(f"  {node_id:10s}: {reward:7.2f} ({pct:5.1f}%)")
        print()

    # Paper comparison
    print("SAPO Paper Benchmarks (Qwen2.5-0.5B, 2000 rounds):")
    print("  Baseline (8/0):    562")
    print("  Config 1 (6/2):    854 (+52%)")
    print("  Config 2 (4/4):  1,093 (+94%) ⭐ BEST")
    print("  Config 3 (2/6):    946 (+68%)")
    print("="*70)


def get_cumulative_history(gdrive_base_path: str, experiment_name: str) -> List[Dict]:
    """
    Get full cumulative reward history for plotting.

    Args:
        gdrive_base_path: Base path in Google Drive
        experiment_name: Name of experiment

    Returns:
        List of dicts with round-by-round cumulative rewards
    """
    exp_path = os.path.join(gdrive_base_path, 'experiments', experiment_name)
    logs_dir = os.path.join(exp_path, 'logs')

    if not os.path.exists(logs_dir):
        return []

    # Aggregate all cumulative metrics from all nodes
    all_entries = []

    try:
        for node_dir in os.listdir(logs_dir):
            cumulative_file = os.path.join(logs_dir, node_dir, 'cumulative_metrics.jsonl')

            if not os.path.exists(cumulative_file):
                continue

            with open(cumulative_file, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        all_entries.append(entry)
                    except json.JSONDecodeError:
                        continue

    except Exception as e:
        get_logger().error(f"Error reading cumulative history: {e}")
        return []

    # Group by round and sum across nodes
    round_totals = {}

    for entry in all_entries:
        round_num = entry.get('round', 0)
        cumulative = entry.get('cumulative_reward', 0.0)
        peer_id = entry.get('peer_id', 'unknown')

        if round_num not in round_totals:
            round_totals[round_num] = {}

        round_totals[round_num][peer_id] = cumulative

    # Convert to sorted list
    history = []
    for round_num in sorted(round_totals.keys()):
        total = sum(round_totals[round_num].values())
        history.append({
            'round': round_num,
            'total_cumulative_reward': total,
            'num_nodes': len(round_totals[round_num]),
            'per_node': round_totals[round_num]
        })

    return history


def compare_experiments(gdrive_base_path: str, experiment_names: List[str]) -> Dict:
    """
    Compare total cumulative rewards across multiple experiments.

    Args:
        gdrive_base_path: Base path in Google Drive
        experiment_names: List of experiment names to compare

    Returns:
        Dictionary with comparison data
    """
    comparison = {}

    for exp_name in experiment_names:
        total, per_node, current_round = get_live_cumulative_rewards(gdrive_base_path, exp_name)

        comparison[exp_name] = {
            'total_cumulative_reward': total,
            'current_round': current_round,
            'num_nodes': len(per_node),
            'avg_per_node': total / len(per_node) if per_node else 0.0
        }

    return comparison


def display_experiment_comparison(gdrive_base_path: str, experiment_names: List[str]):
    """
    Display side-by-side comparison of experiments.

    Args:
        gdrive_base_path: Base path in Google Drive
        experiment_names: List of experiment names
    """
    comparison = compare_experiments(gdrive_base_path, experiment_names)

    print("="*70)
    print("EXPERIMENT COMPARISON - Total Cumulative Rewards")
    print("="*70)
    print()

    # Sort by total cumulative reward
    sorted_exps = sorted(comparison.items(), key=lambda x: x[1]['total_cumulative_reward'], reverse=True)

    for exp_name, data in sorted_exps:
        total = data['total_cumulative_reward']
        round_num = data['current_round']
        num_nodes = data['num_nodes']

        print(f"{exp_name}:")
        print(f"  Total Cumulative: {total:8.2f}")
        print(f"  Round: {round_num}")
        print(f"  Nodes: {num_nodes}")
        print(f"  Avg per node: {total/num_nodes:7.2f}")
        print()

    # Calculate improvements vs first (baseline)
    if len(sorted_exps) > 1:
        baseline_name, baseline_data = sorted_exps[-1]  # Lowest score (likely baseline)
        baseline_total = baseline_data['total_cumulative_reward']

        print("Improvements vs Baseline:")
        for exp_name, data in sorted_exps:
            if exp_name == baseline_name:
                print(f"  {exp_name}: {data['total_cumulative_reward']:8.2f} (baseline)")
            else:
                improvement = ((data['total_cumulative_reward'] - baseline_total) / baseline_total) * 100
                print(f"  {exp_name}: {data['total_cumulative_reward']:8.2f} ({improvement:+6.1f}%)")

    print("="*70)
