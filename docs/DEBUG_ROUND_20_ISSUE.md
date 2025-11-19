# Debugging: Training Stops at Round 20 (MAX_ROUNDS=2000)

## Investigation Summary

I analyzed the codebase and found **NO CODE that uses `ROLLOUT_KEEP_LAST_N_ROUNDS` or `ROLLOUT_CLEANUP_ENABLED` as a stopping condition**.

The rollout cleanup only deletes old rollout files - it does NOT stop training.

## Possible Causes

### 1. **Environment Variable Not Being Passed (MOST LIKELY)**

The notebook Cell 12 sets environment variables PER PROCESS:

```python
env['MAX_ROUNDS'] = str(MAX_ROUNDS)  # ← Must be set BEFORE launching
```

**Check:** Did you change `MAX_ROUNDS` in Cell 2 but NOT re-run Cell 12?

**Solution:**
1. Change `MAX_ROUNDS = 2000` in Cell 2
2. **MUST re-run Cell 12** to launch with new value
3. Kill old processes first if they're still running

### 2. **Testing Mode Still Enabled**

In the notebook Cell 2, check this line:

```python
MAX_ROUNDS = 10              # Testing: 10 rounds
# MAX_ROUNDS = 2000          # ← Is this COMMENTED OUT?
```

**Check:** Is `MAX_ROUNDS = 2000` still commented out?

**Solution:** Uncomment the production line:
```python
# MAX_ROUNDS = 10            # Comment out testing mode
MAX_ROUNDS = 2000            # Uncomment this
```

### 3. **Round Numbering Confusion (Bug #3 Double Increment)**

If Bug #3 (double round increment) is still present:
- Actual round 10 → Displayed as "round_20" in filesystem
- Actual round 20 → Displayed as "round_40" in filesystem

**Check:** Look at your rollout folders. Do you have:
- `round_0`, `round_2`, `round_4`, ..., `round_20` (only even numbers)?
- OR `round_0`, `round_1`, `round_2`, ..., `round_20` (sequential)?

If EVEN NUMBERS ONLY:
- Bug #3 is still active
- "round_20" = actual round 10
- Training stopped correctly at round 10 (MAX_ROUNDS=10 was still set)

### 4. **Multiple Experiments Confusion**

**Check:** Are you looking at the RIGHT experiment?

List your experiments:
```bash
ls /path/to/gdrive/rl-swarm/experiments/
```

Each experiment stores its own config.yaml with its MAX_ROUNDS value.

### 5. **Config.yaml Override (UNLIKELY but possible)**

Although the code doesn't read config.yaml, check if you have an old config:

```bash
cat /path/to/gdrive/experiments/YOUR_EXPERIMENT/config.yaml
```

If it shows `training.max_round: 10`, you need to:
1. Delete the old experiment folder
2. Re-run Cell 10 (init_experiment) with MAX_ROUNDS=2000
3. Re-run Cell 12 (launch)

## Diagnostic Script

Run this in your Colab notebook to check actual values:

```python
import os
import json

print("="*70)
print("DIAGNOSTIC: MAX_ROUNDS Configuration")
print("="*70)
print()

# Check Python variable
print(f"1. Python variable MAX_ROUNDS = {MAX_ROUNDS}")
print()

# Check what would be passed to subprocess
print(f"2. Environment variable would be: '{MAX_ROUNDS}'")
print()

# Check experiment config.yaml
import yaml
config_path = f"{GDRIVE_BASE_PATH}/experiments/{EXPERIMENT_NAME}/config.yaml"
try:
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    print(f"3. Config file {config_path}:")
    print(f"   training.max_round: {config.get('training.max_round', 'NOT SET')}")
except FileNotFoundError:
    print(f"3. Config file not found: {config_path}")
except Exception as e:
    print(f"3. Error reading config: {e}")
print()

# Check current state
state_path = f"{GDRIVE_BASE_PATH}/experiments/{EXPERIMENT_NAME}/state/current_state.json"
try:
    with open(state_path, 'r') as f:
        state = json.load(f)
    print(f"4. Current state {state_path}:")
    print(f"   Round: {state.get('round', 'NOT SET')}")
    print(f"   Updated at: {state.get('updated_at', 'NOT SET')}")
except FileNotFoundError:
    print(f"4. State file not found: {state_path}")
except Exception as e:
    print(f"4. Error reading state: {e}")
print()

# Check rollout directories
rollouts_path = f"{GDRIVE_BASE_PATH}/experiments/{EXPERIMENT_NAME}/rollouts"
try:
    import os
    rounds = [d for d in os.listdir(rollouts_path) if d.startswith('round_')]
    rounds_sorted = sorted(rounds, key=lambda x: int(x.split('_')[1]))
    print(f"5. Rollout folders found: {len(rounds)}")
    print(f"   First 5: {rounds_sorted[:5]}")
    print(f"   Last 5:  {rounds_sorted[-5:]}")

    # Check for Bug #3 (double increment)
    round_nums = [int(d.split('_')[1]) for d in rounds]
    is_sequential = all(round_nums[i] == round_nums[i-1] + 1 for i in range(1, min(5, len(round_nums))))
    is_even_only = all(num % 2 == 0 for num in round_nums[:10])

    if is_even_only:
        print(f"   ⚠️  BUG #3 DETECTED: Only even-numbered rounds!")
        print(f"   Actual rounds completed: {max(round_nums) // 2 + 1}")
    elif is_sequential:
        print(f"   ✓ Sequential numbering (Bug #3 fixed)")
        print(f"   Actual rounds completed: {max(round_nums) + 1}")

except FileNotFoundError:
    print(f"5. Rollouts directory not found: {rollouts_path}")
except Exception as e:
    print(f"5. Error checking rollouts: {e}")
print()

print("="*70)
print("RECOMMENDATIONS:")
print("="*70)
if MAX_ROUNDS <= 20:
    print("❌ MAX_ROUNDS is set to TESTING mode ({})".format(MAX_ROUNDS))
    print("   → Change MAX_ROUNDS = 2000 in Cell 2")
    print("   → Re-run Cell 10 (init_experiment)")
    print("   → Re-run Cell 12 (launch)")
else:
    print("✓ MAX_ROUNDS looks correct ({})".format(MAX_ROUNDS))
    print("   Check config.yaml and rollout folders above")
```

## Solution Steps

1. **Check your Cell 2 configuration:**
   ```python
   MAX_ROUNDS = 2000  # ← Is this the actual value?
   ```

2. **Delete old experiment (if needed):**
   ```python
   import shutil
   exp_path = f"{GDRIVE_BASE_PATH}/experiments/{EXPERIMENT_NAME}"
   if os.path.exists(exp_path):
       shutil.rmtree(exp_path)
       print(f"Deleted: {exp_path}")
   ```

3. **Re-run these cells IN ORDER:**
   - Cell 2 (set MAX_ROUNDS=2000)
   - Cell 10 (init_experiment)
   - Cell 12 (launch nodes)

4. **Monitor progress:**
   - Use Cell 7 (monitor)
   - Check `/experiments/{EXPERIMENT_NAME}/state/current_state.json`

## Expected Behavior

With `MAX_ROUNDS=2000`:
- Training should run until round 1999 (0-indexed)
- Rollout folders: `round_0` through `round_1999` (if Bug #3 fixed)
- OR `round_0`, `round_2`, ..., `round_3998` (if Bug #3 still present)
- Logs should continue until coordinator reaches round 2000

## Still Not Working?

If training still stops at round 20 after these checks, please share:
1. Output of the diagnostic script above
2. Contents of `/experiments/{EXPERIMENT_NAME}/config.yaml`
3. Last 20 lines of `/experiments/{EXPERIMENT_NAME}/logs/node_0/stdout.log`
4. List of rollout folders: `ls /experiments/{EXPERIMENT_NAME}/rollouts/`

This will help identify the exact issue.
