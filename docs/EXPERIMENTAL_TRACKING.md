# Experimental Tracking Sheet

**Thesis**: Adaptive Swarm Sampling for Decentralized RL
**Student**: [Your Name]
**Last Updated**: 2025-01-16

---

## 📊 Experiment Overview

| Phase | Experiments | Total Rounds | GPU Hours | Status |
|-------|-------------|--------------|-----------|--------|
| **Phase 1: Validation** | 4 | 8,000 | 84h | ⏳ Pending |
| **Phase 2: Adaptive** | 3 | 6,000 | 63h | ⏳ Pending |
| **Phase 3: Ablations** | 2 | 4,000 | 42h | ⏳ Pending |
| **TOTAL** | **9** | **18,000** | **189h** | **0% Complete** |

---

## 🎯 Phase 1: Validation Experiments

**Goal**: Replicate paper's findings on GPT-2

### Experiment 1.1: Baseline (4/0)
- **Status**: ⏳ Not Started
- **Priority**: 🔴 CRITICAL - Run this FIRST
- **Config**: I=4, J=0, G=8
- **Rounds**: 2000
- **Started**: ___________
- **Completed**: ___________
- **GPU Time**: _____ hours
- **Result**: Cumulative reward = _______
- **Notes**:
  - This is your reference point for all comparisons
  - Save the cumulative reward number!
  - Verify logs are being saved to GDrive
- **Notebook**: `EX12.14a.SAPO_gpt2_Baseline_4loc0ext.ipynb`
- **Files**:
  - [ ] Logs saved to GDrive
  - [ ] Metrics CSV exported
  - [ ] Cumulative reward recorded
  - [ ] Plot generated

---

### Experiment 1.2: Config 1 (3/1)
- **Status**: ⏳ Not Started
- **Priority**: 🟡 Medium
- **Config**: I=3, J=1, G=8
- **Rounds**: 2000
- **Started**: ___________
- **Completed**: ___________
- **GPU Time**: _____ hours
- **Result**: Cumulative reward = _______
- **Improvement vs Baseline**: _______ %
- **Paper Improvement**: +52%
- **Notes**:
- **Notebook**: `EX12.14b.SAPO_gpt2_Config1_3loc1ext.ipynb` (need to create)
- **Files**:
  - [ ] Logs saved
  - [ ] Metrics exported
  - [ ] Comparison plot vs baseline

---

### Experiment 1.3: Config 2 (4/4) **BEST**
- **Status**: ⏳ Not Started
- **Priority**: 🔴 HIGH - Run after baseline
- **Config**: I=4, J=4, G=8
- **Rounds**: 2000
- **Started**: ___________
- **Completed**: ___________
- **GPU Time**: _____ hours
- **Result**: Cumulative reward = _______
- **Improvement vs Baseline**: _______ %
- **Paper Improvement**: +94%
- **Hypothesis**: GPT-2 should show +110-150% (weaker model benefits more)
- **Notes**:
- **Notebook**: `EX12.14c.SAPO_gpt2_Config2_4loc4ext.ipynb`
- **Files**:
  - [ ] Logs saved
  - [ ] Metrics exported
  - [ ] Comparison plot vs baseline
  - [ ] Hypothesis test results

---

### Experiment 1.4: Config 3 (1/3)
- **Status**: ⏳ Not Started
- **Priority**: 🟡 Medium
- **Config**: I=1, J=3, G=8
- **Rounds**: 2000
- **Started**: ___________
- **Completed**: ___________
- **GPU Time**: _____ hours
- **Result**: Cumulative reward = _______
- **Improvement vs Baseline**: _______ %
- **Paper Improvement**: +68%
- **Notes**:
  - Watch for oscillations (paper showed instability)
- **Notebook**: `EX12.14d.SAPO_gpt2_Config3_1loc3ext.ipynb` (need to create)
- **Files**:
  - [ ] Logs saved
  - [ ] Metrics exported
  - [ ] Oscillation analysis

---

## 🚀 Phase 2: Adaptive Experiments

**Goal**: Test novel adaptive I/J algorithm

### Experiment 2.1: Adaptive Baseline (α=0.1)
- **Status**: ⏳ Not Started
- **Priority**: 🔴 HIGH
- **Config**: I=adaptive, J=adaptive, G=8, α=0.1
- **Rounds**: 2000
- **Started**: ___________
- **Completed**: ___________
- **GPU Time**: _____ hours
- **Result**: Cumulative reward = _______
- **Improvement vs Fixed 4/4**: _______ %
- **Hypothesis**: Should beat fixed 4/4 by +10-20%
- **Notes**:
- **Notebook**: `EX12.15.SAPO_Adaptive_alpha0.1.ipynb` (need to create)
- **Files**:
  - [ ] I/J trajectory plot
  - [ ] Adaptation log CSV
  - [ ] Comparison vs fixed 4/4
  - [ ] Phase analysis (early/mid/late)

---

### Experiment 2.2: Adaptive Low α (α=0.05)
- **Status**: ⏳ Not Started
- **Priority**: 🟢 Low
- **Config**: I=adaptive, J=adaptive, G=8, α=0.05
- **Purpose**: Test slower adaptation
- **Rounds**: 2000
- **Started**: ___________
- **Completed**: ___________
- **Result**: Cumulative reward = _______
- **Notes**:
  - Compare trajectory smoothness vs α=0.1

---

### Experiment 2.3: Adaptive High α (α=0.2)
- **Status**: ⏳ Not Started
- **Priority**: 🟢 Low
- **Config**: I=adaptive, J=adaptive, G=8, α=0.2
- **Purpose**: Test faster adaptation
- **Rounds**: 2000
- **Started**: ___________
- **Completed**: ___________
- **Result**: Cumulative reward = _______
- **Notes**:
  - Watch for instability

---

## 🔬 Phase 3: Ablation Studies (Optional)

**Goal**: Understand what makes adaptive work

### Experiment 3.1: Constrained Adaptive (J ∈ [2,6])
- **Status**: ⏳ Not Started
- **Config**: Adaptive with J clipped to [2,6]
- **Purpose**: Test if constraints help
- **Rounds**: 2000
- **Result**: _______

### Experiment 3.2: Random I/J Baseline
- **Status**: ⏳ Not Started
- **Config**: Randomly sample I/J each round
- **Purpose**: Control for variability vs fixed
- **Rounds**: 2000
- **Result**: _______

---

## 📈 Results Summary Table

| Experiment | Config | Cumulative Reward | vs Baseline | vs Paper | Status |
|------------|--------|-------------------|-------------|----------|--------|
| **1.1 Baseline** | 4/0 | _______ | - | 562 | ⏳ |
| **1.2 Config 1** | 3/1 | _______ | _____% | +52% | ⏳ |
| **1.3 Config 2** | 4/4 | _______ | _____% | +94% | ⏳ |
| **1.4 Config 3** | 1/3 | _______ | _____% | +68% | ⏳ |
| **2.1 Adaptive** | adaptive | _______ | _____% | N/A | ⏳ |
| **2.2 Adaptive (slow)** | adaptive | _______ | _____% | N/A | ⏳ |
| **2.3 Adaptive (fast)** | adaptive | _______ | _____% | N/A | ⏳ |

---

## 🎯 Hypothesis Testing Checklist

### Hypothesis 1: Weaker models benefit more
- [ ] Run: Baseline (GPT-2)
- [ ] Run: Config 2 (GPT-2)
- [ ] Compute: Improvement %
- [ ] Compare: GPT-2 improvement vs paper's Qwen2.5 (+94%)
- [ ] Expected: GPT-2 shows +110-150% (higher than paper)
- [ ] Result: _________ % ← FILL THIS IN
- [ ] Conclusion: [ ] Confirmed [ ] Rejected

### Hypothesis 2: Adaptive beats fixed
- [ ] Run: Config 2 (fixed 4/4)
- [ ] Run: Adaptive (α=0.1)
- [ ] Compute: Improvement %
- [ ] Statistical test: t-test (p < 0.05)
- [ ] Result: _________ % improvement, p = _______
- [ ] Conclusion: [ ] Confirmed [ ] Rejected

### Hypothesis 3: I/J changes across phases
- [ ] Plot: J trajectory over rounds
- [ ] Analyze: Early (0-500), Mid (500-1500), Late (1500-2000)
- [ ] Expected: J high early → balanced mid → low late
- [ ] Result: Early J = ____, Mid J = ____, Late J = ____
- [ ] Conclusion: [ ] Confirmed [ ] Partial [ ] Rejected

---

## 📅 Weekly Progress Tracker

### Week 1: Setup & Baseline
- [ ] **Day 1-2**: Create baseline notebook, run testing mode (10 rounds)
- [ ] **Day 3**: Start baseline production (2000 rounds)
- [ ] **Day 4-7**: While baseline runs, write Chapter 2 (background)
- [ ] **Deliverable**: Baseline complete, cumulative reward = _______

### Week 2: Config 2
- [ ] **Day 1**: Start Config 2 (4/4)
- [ ] **Day 2-7**: While running, continue Chapter 2 + start Chapter 3
- [ ] **Deliverable**: Config 2 complete, improvement = _______%, H1 tested

### Week 3-4: Configs 1 & 3
- [ ] Week 3: Run Config 1
- [ ] Week 4: Run Config 3
- [ ] **Deliverable**: All validation done, Chapter 4 data collected

### Week 5-6: Adaptive Design
- [ ] Implement adaptive algorithm
- [ ] Run hyperparameter tuning (100 rounds × 5 configs)
- [ ] **Deliverable**: Best α selected, code ready

### Week 7-9: Adaptive Experiments
- [ ] Week 7: Adaptive α=0.1
- [ ] Week 8: Adaptive α=0.05
- [ ] Week 9: Adaptive α=0.2
- [ ] **Deliverable**: All adaptive results, H2 & H3 tested

### Week 10-12: Analysis & Chapter 5
- [ ] Generate all plots
- [ ] Statistical tests
- [ ] Write Chapter 5
- [ ] **Deliverable**: Chapter 5 draft complete

### Week 13-16: Writing Chapters 1, 3, 4, 6
- [ ] Week 13: Chapters 1 & 3
- [ ] Week 14: Chapter 4
- [ ] Week 15: Chapter 6
- [ ] Week 16: Chapter 7 + revision
- [ ] **Deliverable**: Complete thesis draft

### Week 17-20: Revision & Finalization
- [ ] Incorporate advisor feedback
- [ ] Polish figures
- [ ] Proofread
- [ ] **Deliverable**: Final thesis

---

## 💾 Data Management

### File Organization
```
Google Drive/
├── rl-swarm/
│   ├── experiments/
│   │   ├── sapo_gpt2_baseline_4loc0ext/
│   │   ├── sapo_gpt2_config1_3loc1ext/
│   │   ├── sapo_gpt2_config2_4loc4ext/
│   │   ├── sapo_gpt2_config3_1loc3ext/
│   │   ├── sapo_gpt2_adaptive_alpha0.1/
│   │   ├── sapo_gpt2_adaptive_alpha0.05/
│   │   └── sapo_gpt2_adaptive_alpha0.2/
│   ├── thesis_data/
│   │   ├── raw_metrics/
│   │   ├── processed_results/
│   │   ├── plots/
│   │   └── statistical_tests/
│   └── thesis_writing/
│       ├── chapters/
│       ├── figures/
│       └── references/
```

### Backup Strategy
- [ ] GDrive primary storage (all experiments)
- [ ] Local backup (metrics CSVs)
- [ ] GitHub (code + notebooks)
- [ ] Weekly backup to external drive

---

## 🚨 Troubleshooting Log

### Issue 1: OOM Crashes
- **Date**: __________
- **Experiment**: __________
- **Solution**:
- **Notes**:

### Issue 2: Slow Training
- **Date**: __________
- **Experiment**: __________
- **Solution**:
- **Notes**:

### Issue 3: Poor Results
- **Date**: __________
- **Experiment**: __________
- **Solution**:
- **Notes**:

---

## ✅ Final Checklist (Before Submission)

### Experiments
- [ ] All 9 experiments completed
- [ ] All data backed up in 3 locations
- [ ] All plots generated (high resolution)
- [ ] Statistical tests performed
- [ ] Results tables complete

### Thesis
- [ ] All 7 chapters written
- [ ] Abstract complete
- [ ] References formatted (BibTeX)
- [ ] Figures numbered and captioned
- [ ] Tables formatted
- [ ] Appendices (if needed)

### Code
- [ ] All code pushed to GitHub
- [ ] README updated
- [ ] Notebooks runnable
- [ ] Adaptive algorithm documented

### Submission
- [ ] Advisor approval
- [ ] Department format check
- [ ] Plagiarism check
- [ ] PDF generated
- [ ] Submitted!

---

**Progress**: ____ / 9 experiments complete (____ %)

**Next Action**: __________________________________________

**Blockers**: __________________________________________

**Notes**: __________________________________________

---

**Document Version**: 1.0
**Created**: 2025-01-16
**Purpose**: Track all thesis experiments and maintain progress
