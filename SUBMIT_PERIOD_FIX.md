# Reward Submission Frequency Fix

## What Was Fixed

**Changed hardcoded 3-hour reward submission to configurable environment variable.**

### Before (Broken)
```python
# manager.py:114 (hardcoded)
self.submit_period = 3.0  # hours
```

**Result:**
- Rewards folder empty for first 3 hours
- Looked like a bug (caused confusion)
- No benefit in Google Drive mode (legacy from blockchain)

### After (Fixed)
```python
# Now configurable via environment variable
SUBMIT_PERIOD_HOURS=0.0  # Default: submit every round
```

**Result:**
- ✅ Rewards folder populated immediately
- ✅ Better debugging visibility
- ✅ No more confusion about empty folders
- ✅ Backward compatible (can still set to 3.0 if desired)

---

## How To Use

### Default Behavior (Submit Every Round)

**No changes needed!** Default is now every round:

```python
# In your notebook Cell 2, nothing to add:
# SUBMIT_PERIOD_HOURS defaults to 0.0 automatically
```

**Result:**
- `/experiments/{EXPERIMENT_NAME}/rewards/round_0/`
- `/experiments/{EXPERIMENT_NAME}/rewards/round_1/`
- `/experiments/{EXPERIMENT_NAME}/rewards/round_2/`
- ... (created immediately)

### Old Behavior (Submit Every 3 Hours)

**If you want the old 3-hour batching:**

```python
# In notebook Cell 12, add to environment variables:
env['SUBMIT_PERIOD_HOURS'] = '3.0'
```

### Custom Frequency

**Any interval you want:**

```python
# Submit every 10 minutes (0.167 hours)
env['SUBMIT_PERIOD_HOURS'] = '0.167'

# Submit every hour
env['SUBMIT_PERIOD_HOURS'] = '1.0'

# Submit every 10 rounds (depends on round duration)
# For ~1 min/round: 10 rounds = 10 min = 0.167 hours
env['SUBMIT_PERIOD_HOURS'] = '0.167'
```

---

## Important Notes

### This Does NOT Fix Adaptive I/J Cold-Start

**The rewards folder issue was UNRELATED to your J=0 problem!**

Two separate systems:

| System | Purpose | Location | Frequency |
|--------|---------|----------|-----------|
| **Rewards folder** | Legacy debugging | `/rewards/` | Now configurable |
| **Adaptive I/J** | Algorithm input | `round_rewards_accumulator` | Every round (always) |

**Your J=0 problem is caused by:**
- Starting with `initial_J=0` (no swarm data to evaluate)
- Baseline tracking learning so closely that advantage ≈ 0
- Algorithm can't measure benefit of swarm it hasn't tried

**Solution for J=0:**
```python
# In your notebook Cell 2:
ADAPTIVE_IJ_INITIAL_J = 4  # Start with swarm enabled
# OR increase adaptation rate:
ADAPTIVE_IJ_ALPHA = 0.5    # Faster response to reward signals
```

---

## Technical Details

### What Changed

**1. swarm_launcher.py (line 84-87)**
```python
# NEW: Read environment variable with sensible default
submit_period_hours = float(os.environ.get('SUBMIT_PERIOD_HOURS', '0.0'))
# 0.0 = submit every round
# Old default was 3.0
```

**2. swarm_launcher.py (line 312)**
```python
# NEW: Pass to game manager
game_manager = SwarmGameManager(
    ...,
    submit_period_hours=submit_period_hours  # NEW parameter
)
```

**3. manager.py (line 41)**
```python
# NEW: Accept parameter in __init__
def __init__(
    ...,
    submit_period_hours: float = 0.0,  # NEW parameter with default
    **kwargs,
):
```

**4. manager.py (line 115)**
```python
# CHANGED: Use parameter instead of hardcoded value
self.submit_period = submit_period_hours  # Was: 3.0
```

### Why This Was Needed

**Original design (Gensyn blockchain mode):**
- Submit to blockchain = gas fee ($0.50 per transaction)
- 2000 rounds × $0.50 = **$1000 total cost**
- Submit every 3 hours (once per ~180 rounds) = **$11 total cost**
- 99% cost reduction!

**Current design (Google Drive mode):**
- Submit to Google Drive = free (just write JSON file)
- No gas fees = no reason to batch
- Batching only causes confusion ("Why is rewards folder empty?")

---

## Verification

**Check that it's working:**

```python
# In your Colab, after starting experiment:
import os
import time

# Wait 1 minute for first round to complete
time.sleep(60)

# Check rewards folder
rewards_path = f"{GDRIVE_BASE_PATH}/experiments/{EXPERIMENT_NAME}/rewards"
rounds = os.listdir(rewards_path)
print(f"Found {len(rounds)} reward submissions")
print(f"Rounds: {sorted(rounds)}")

# Expected with default (0.0):
# Found 1 reward submissions
# Rounds: ['round_0']

# After 5 minutes:
# Found 5 reward submissions
# Rounds: ['round_0', 'round_1', 'round_2', 'round_3', 'round_4']
```

---

## Troubleshooting

### Rewards folder still empty after 5 rounds

**Check environment variable:**
```python
# In notebook Cell 12, verify:
print(env.get('SUBMIT_PERIOD_HOURS', 'NOT SET'))
# Should print: 0.0 (or your custom value)
```

**Check if code is updated:**
```bash
# Pull latest changes:
%cd /content/rl-swarm
!git pull origin main
```

### Want to disable reward submissions entirely

**Set to a very large number:**
```python
env['SUBMIT_PERIOD_HOURS'] = '999999.0'  # Effectively disabled
```

**Why you might want this:**
- Rewards folder not needed for your analysis
- Saves disk space (tiny amount)
- Slightly faster (negligible difference)

---

## Summary

✅ **Fixed**: Rewards now submit every round by default
✅ **Configurable**: Set `SUBMIT_PERIOD_HOURS` env var
✅ **Backward compatible**: Can restore old behavior
✅ **No breaking changes**: Existing experiments unaffected

⚠️ **Does NOT fix**: Adaptive I/J cold-start (separate issue)
⚠️ **Does NOT affect**: Rollout sharing or adaptive algorithm

**For adaptive I/J cold-start, see:** `ADAPTIVE_IJ_FIXES.md`
