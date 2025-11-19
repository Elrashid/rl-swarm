# Master's Thesis Proposal

**Title**: Adaptive Swarm Sampling for Decentralized Reinforcement Learning: Validating and Extending SAPO

**Student**: [Your Name]
**Advisor**: [Advisor Name]
**Program**: Master of AI
**Expected Duration**: 4-5 months
**Expected Completion**: [Date]

---

## 1. Motivation

Recent advances in reinforcement learning (RL) for language models have shown remarkable improvements in reasoning capabilities (DeepSeek-R1, GPT-4). However, scaling RL training requires significant computational resources, often necessitating large GPU clusters with tight synchronization.

The SAPO algorithm (Swarm sAmpling Policy Optimization, arXiv:2509.08721) proposes a decentralized alternative where heterogeneous nodes share **decoded rollouts** instead of gradients, enabling:
- Asynchronous training without synchronization
- Heterogeneous models and hardware
- Resilience to node failures
- Reduced communication overhead

**Key finding from paper**: Balanced sharing (4 local / 4 external rollouts) achieves **+94% improvement** over no-sharing baseline.

**Open question**: Paper uses **fixed ratios** (4/4, 6/2, etc.). Could **adaptive selection** of local vs external rollouts improve performance?

---

## 2. Research Questions

**RQ1 (Validation)**: Can SAPO be replicated on consumer hardware (single GPU) with different models (GPT-2 vs paper's Qwen2.5)?

**RQ2 (Hypothesis)**: Do weaker models benefit **more** from swarm collaboration than stronger models?

**RQ3 (Novel)**: Can adaptive I/J selection outperform fixed ratios?

**RQ4 (Analysis)**: What is the optimal I/J trajectory during training? Does it change across training phases?

---

## 3. Proposed Approach

### Part 1: Validation (Chapters 1-4)

**Replicate paper's experiments on modified setup:**
- Hardware: Single A100 80GB (vs paper's 8 GPUs)
- Model: GPT-2 (124M params) vs paper's Qwen2.5 (500M)
- Configs: Baseline (4/0), Config 1 (3/1), Config 2 (4/4), Config 3 (1/3)
- Dataset: ReasoningGYM (same as paper)
- Rounds: 2000 (same as paper)

**Expected outcome**: Validate that:
- SAPO works on consumer hardware
- GPT-2 shows >94% improvement (weaker models benefit more)
- Trends match paper's findings

### Part 2: Novel Contribution (Chapter 5)

**Develop adaptive I/J selection algorithm:**

```python
Algorithm: Gradient-Based Adaptive I/J

Initialize: J = 4 (balanced)
For each round:
  1. Observe round reward
  2. Compute advantage vs baseline (EMA)
  3. Update J ← J + α × advantage
  4. Clip J to [0, 8]
  5. Set I = 8 - J
```

**Hypothesis**:
- Early training: High J (learn from swarm diversity)
- Mid training: Balanced I/J (consolidate learning)
- Late training: High I (specialize, avoid interference)

**Expected outcome**: Adaptive beats fixed 4/4 by **10-20%** additional improvement

### Part 3: Analysis (Chapter 6)

**Comprehensive analysis:**
- When does adaptation help vs hurt?
- Correlation between swarm quality and optimal J
- Failure modes and limitations
- Design guidelines for practitioners

---

## 4. Contributions

1. **First independent validation** of SAPO outside Gensyn
2. **Democratization study**: Show SAPO works on single GPU (vs 8 GPUs)
3. **Weaker model analysis**: Systematic study of GPT-2 vs paper's Qwen2.5
4. **Novel algorithm**: Adaptive I/J selection with theoretical justification
5. **Empirical insights**: When to use fixed vs adaptive, optimal trajectories

---

## 5. Experimental Plan

### Phase 1: Validation (4-6 weeks)
| Experiment | Config | Rounds | GPU Hours | Purpose |
|------------|--------|--------|-----------|---------|
| Baseline | 4/0 | 2000 | 21 | Reference |
| Config 1 | 3/1 | 2000 | 21 | Low sharing |
| Config 2 | 4/4 | 2000 | 21 | Balanced (paper's best) |
| Config 3 | 1/3 | 2000 | 21 | High sharing |
| **Total** | - | **8000** | **84** | **Validation** |

### Phase 2: Novel Work (6-8 weeks)
| Experiment | Config | Rounds | GPU Hours | Purpose |
|------------|--------|--------|-----------|---------|
| Adaptive v1 | adaptive | 2000 | 21 | Main algorithm |
| Adaptive v2 | adaptive (α=0.05) | 2000 | 21 | Hyperparameter tuning |
| Adaptive v3 | adaptive (α=0.2) | 2000 | 21 | Hyperparameter tuning |
| **Total** | - | **6000** | **63** | **Novel contribution** |

### Phase 3: Writing (4-6 weeks)
- Draft chapters 1-7
- Generate all figures
- Statistical analysis
- Revision

**Total Timeline**: 14-20 weeks (3.5-5 months)

**Total GPU Time**: ~150 hours (~$75-100 on Colab Pro+)

---

## 6. Expected Results

### Validation (RQ1, RQ2)
```
Paper (Qwen2.5-0.5B, 8 nodes):
  Baseline: 562
  Config 2: 1093 (+94%)

Ours (GPT-2, 5 nodes):
  Baseline: 250-350
  Config 2: 550-700 (+110-150%)  ← HYPOTHESIS: Higher % improvement
```

**Conclusion for RQ2**: Weaker models benefit MORE ✅

### Novel Work (RQ3, RQ4)

**Optimistic**:
```
  Baseline (4/0):    300
  Fixed (4/4):       650 (+117%)
  Adaptive:          780 (+160%)  ← +20% over fixed
```

**Neutral** (still publishable):
```
  Baseline (4/0):    300
  Fixed (4/4):       650 (+117%)
  Adaptive:          620 (+107%)  ← Slightly worse but insights gained
```

---

## 7. Thesis Outline

**Chapter 1: Introduction** (10-15 pages)
- Motivation, problem statement, research questions, contributions

**Chapter 2: Background** (20-25 pages)
- RL for LMs (RLHF, RLVR, GRPO)
- Multi-agent methods
- Distributed RL
- SAPO algorithm

**Chapter 3: Methodology** (15-20 pages)
- Experimental setup
- Dataset, models, metrics
- Implementation details

**Chapter 4: Validation Experiments** (20-25 pages)
- Replication results
- GPT-2 vs Qwen2.5 comparison
- Infrastructure analysis

**Chapter 5: Adaptive I/J Selection** (20-25 pages)
- Algorithm design
- Implementation
- Results and analysis

**Chapter 6: Discussion** (10-15 pages)
- Key findings
- Implications
- Limitations

**Chapter 7: Conclusion** (5-10 pages)
- Summary, future work

**Total**: 100-135 pages

---

## 8. Risk Mitigation

**Risk 1**: Can't reproduce paper results
- **Mitigation**: Focus on relative improvements (%), not absolute values
- **Backup**: Validation alone is publishable contribution

**Risk 2**: Adaptive doesn't beat fixed
- **Mitigation**: Analyze why (still publishable negative result)
- **Backup**: Try simpler adaptation (Version 1 instead of Version 2)

**Risk 3**: Experiments take too long
- **Mitigation**: Prioritize Baseline + Config 2 first
- **Backup**: Reduce to 1000 rounds if needed (still meaningful)

**Risk 4**: GPU costs exceed budget
- **Mitigation**: Use Colab Pro+ ($50/month) instead of cloud GPUs
- **Backup**: Request department GPU access

---

## 9. Timeline

```
Month 1 (Weeks 1-4):   Setup + Baseline + Config 2
Month 2 (Weeks 5-8):   Config 1 + Config 3 + Design adaptive
Month 3 (Weeks 9-12):  Implement adaptive + Run experiments
Month 4 (Weeks 13-16): Analysis + Writing Chapters 1-5
Month 5 (Weeks 17-20): Writing Chapters 6-7 + Revision
```

**Milestones**:
- End of Month 1: Validation data collected (Baseline + Config 2)
- End of Month 2: All validation done + Adaptive designed
- End of Month 3: All experiments complete
- End of Month 4: Complete draft ready
- End of Month 5: Final thesis submitted

---

## 10. Resources Required

**Computational**:
- GPU: A100 80GB via Colab Pro+ ($50/month × 3 months = $150)
- Storage: Google Drive (15 GB free tier sufficient)

**Software** (all free/open-source):
- Python, PyTorch, HuggingFace Transformers
- ReasoningGYM dataset
- Modified RL-Swarm codebase (fork of Gensyn's repo)

**References**:
- Access to academic databases (university library)
- SAPO paper (arXiv:2509.08721)
- Related RL/LM papers

---

## 11. Success Criteria

**Minimum (Pass)**:
- ✅ Validated SAPO on GPT-2 (2+ configs)
- ✅ Implemented adaptive algorithm
- ✅ Analysis of results (even if negative)
- ✅ 80+ page thesis

**Good (Strong Pass)**:
- ✅ All 4 configs validated
- ✅ Adaptive matches fixed performance
- ✅ Statistical analysis + clear insights
- ✅ 100+ page thesis

**Excellent (Honors/Publication)**:
- ✅ All of above
- ✅ Adaptive beats fixed by >10%
- ✅ Workshop paper submitted
- ✅ Open-source contribution to original repo

---

## 12. References (Key Papers)

1. Gensyn AI Team (2025). SAPO: Swarm sAmpling Policy Optimization. arXiv:2509.08721
2. DeepSeek AI (2025). DeepSeek-R1-Zero.
3. Shao et al. (2024). DeepSeek-Math: GRPO for reasoning.
4. Schulman et al. (2017). Proximal Policy Optimization.
5. Ziegler et al. (2020). Fine-Tuning Language Models from Human Preferences.

---

**Signatures**:

Student: __________________ Date: __________

Advisor: __________________ Date: __________

---

**Approval**: [ ] Approved [ ] Revisions Required

**Comments**:


---

**Document Version**: 1.0
**Created**: 2025-01-16
**Status**: Draft - Awaiting Advisor Review
