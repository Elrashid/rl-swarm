# Rewards Logging Fixes

## Issues Fixed

### 1. Incorrect Stage Value in Round-Level Logging
**Problem:** When logging rewards after all stages complete, `self.state.stage` was used, but this value had already been incremented past the last stage, making the logged stage number incorrect.

**Fix:** Changed to use `stage=0` when logging round-level summaries (in `_get_my_rewards()`), with a clear comment indicating this is a round-level metric.

**Location:** `rgym_exp/src/manager.py:214`

### 2. Missing Comprehensive Reward Statistics
**Problem:** Only logged basic metrics (`my_reward`, `total_agents`, `peer_id`), lacking detailed statistics for analysis.

**Fix:** Added comprehensive reward metrics including:
- **Distribution statistics**: mean, std, min, max, median
- **Ranking information**: my_rank, percentile
- **Comparison context**: how this node compares to others in the swarm

**Benefits:**
- Better visibility into training progress
- Easier to identify "aha moments" (when one node suddenly improves)
- Can track swarm dynamics and identify lagging/leading nodes
- Essential for thesis analysis and plots

**Location:** `rgym_exp/src/manager.py:193-209`

### 3. Missing Per-Stage Reward Breakdown
**Problem:** Only logged round-level totals, making it impossible to see which stages contributed more/less to the total reward.

**Fix:** Added per-stage reward logging in `_hook_after_rewards_updated()` that logs:
- `stage_reward`: Total reward for this specific stage
- `num_samples`: Number of samples processed in this stage
- `avg_reward_per_sample`: Average reward per sample
- `is_stage_detail`: Flag to distinguish from round summaries

**Benefits:**
- Can analyze reward progression within each round
- Identify which stages are most/least effective
- Debug issues with specific stages
- Granular data for research analysis

**Location:** `rgym_exp/src/manager.py:262-290`

### 4. Missing Informative Log Messages
**Problem:** Reward logging was silent (only to JSON files), making it hard to monitor training in real-time.

**Fix:** Added informative log message that displays:
```
Round X rewards - My: Y (rank Z/N), Mean: M, Range: [min, max]
```

**Benefits:**
- Real-time visibility during training
- Easy to spot when rewards improve/degrade
- Human-readable format in stdout.log files
- Helps identify training issues immediately

**Location:** `rgym_exp/src/manager.py:218-224`

## New Metrics Logged

### Round-Level Metrics (stage=0)
These are logged once per round after all stages complete:

| Metric | Description |
|--------|-------------|
| `my_reward` | Total reward for this node (all stages) |
| `total_agents` | Number of nodes in the swarm |
| `mean_reward` | Average reward across all nodes |
| `std_reward` | Standard deviation of rewards |
| `min_reward` | Minimum reward across all nodes |
| `max_reward` | Maximum reward across all nodes |
| `median_reward` | Median reward across all nodes |
| `my_rank` | This node's ranking (1=best) |
| `percentile` | Percentage of nodes with lower rewards |
| `peer_id` | Node identifier |

### Stage-Level Metrics (stage=0,1,...)
These are logged for each stage within a round:

| Metric | Description |
|--------|-------------|
| `stage_reward` | Total reward for this specific stage |
| `num_samples` | Number of samples/rollouts processed |
| `avg_reward_per_sample` | Average reward per sample |
| `peer_id` | Node identifier |
| `is_stage_detail` | Flag (True) to distinguish from round summaries |

## Example Log Output

### JSON Metrics (saved to Google Drive)

**Round summary (stage=0):**
```json
{
  "timestamp": 1699999999.0,
  "round": 10,
  "stage": 0,
  "node_id": "worker_1",
  "experiment": "sapo_gpt2_config2",
  "my_reward": 142.7,
  "total_agents": 5,
  "mean_reward": 112.96,
  "std_reward": 20.5,
  "min_reward": 88.1,
  "max_reward": 142.7,
  "median_reward": 110.2,
  "my_rank": 1,
  "percentile": 80.0,
  "peer_id": "worker_1"
}
```

**Stage detail (stage=0,1,...):**
```json
{
  "timestamp": 1699999999.0,
  "round": 10,
  "stage": 0,
  "node_id": "worker_1",
  "experiment": "sapo_gpt2_config2",
  "stage_reward": 71.3,
  "num_samples": 32,
  "avg_reward_per_sample": 2.23,
  "peer_id": "worker_1",
  "is_stage_detail": true
}
```

### Console Log Output (stdout.log)
```
[manager] 2024-11-16 10:30:45 INFO: Round 10 rewards - My: 142.7000 (rank 1/5), Mean: 112.9600, Range: [88.1000, 142.7000]
```

## Impact on Thesis Work

### For Validation Experiments (Option 1)
- ✅ Can now generate proper learning curves (reward over time)
- ✅ Can calculate statistical significance between configs
- ✅ Can identify when "aha moments" propagate through swarm
- ✅ Can create comprehensive comparison tables

### For Adaptive Algorithm (Option 2)
- ✅ Can track how adaptive I/J affects reward distribution
- ✅ Can measure swarm dynamics (variance, spread)
- ✅ Can identify when to trigger I/J adjustments
- ✅ Can compare adaptive vs fixed strategies with rich data

### Example Analysis Queries

**1. Which node learned fastest?**
```python
df = pd.read_json('metrics.jsonl', lines=True)
round_summary = df[df['stage'] == 0]  # Round-level only
round_summary.groupby('node_id')['my_reward'].sum()
```

**2. Did rewards converge across nodes?**
```python
convergence = round_summary.groupby('round')['std_reward'].mean()
plt.plot(convergence)  # Should decrease if swarm is working
```

**3. Which stages contribute most to learning?**
```python
stage_detail = df[df.get('is_stage_detail', False) == True]
stage_detail.groupby('stage')['stage_reward'].mean()
```

## Testing

### Unit Test
✅ Reward calculation logic tested successfully
✅ Ranking and percentile calculations verified
✅ Log message formatting validated
✅ Syntax check passed

### Integration Test
To verify in a real experiment:
1. Run baseline experiment (10 rounds)
2. Check `metrics.jsonl` contains both round summaries and stage details
3. Verify `stdout.log` contains reward log messages
4. Confirm all new metrics are present and valid

## Files Modified
- `rgym_exp/src/manager.py`: Enhanced `_get_my_rewards()` and `_hook_after_rewards_updated()`

## Backward Compatibility
✅ All existing metrics still logged (my_reward, peer_id, total_agents)
✅ Additional metrics are additive (won't break existing analysis)
✅ Stage value fix (0 for round summaries) is semantic correction, not breaking change

## Next Steps
1. ✅ Commit and push changes
2. Run test experiment to verify logging works
3. Update analysis notebooks to use new metrics
4. Create visualization utilities for new reward statistics
