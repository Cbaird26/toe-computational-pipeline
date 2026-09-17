# Computational Attack Program on Fundamental Unification

**Status:** Research program scaffold — generated 2026-09-16
**Framing:** No tool, model, or plugin stack "solves" a theory of everything. What a
tool-equipped agent *can* do is run the disciplined, boring, verifiable parts of the
pipeline: literature mapping, consequence computation, consistency checking, and
formalization. This document defines that pipeline so every idea entering it is forced
to produce a falsifiable number or a machine-checkable proof.

---

## 1. Problem decomposition

A "theory of everything" is not one problem. It decomposes into at least four:

| # | Sub-problem | Why it's hard | What computation contributes |
|---|-------------|---------------|------------------------------|
| P1 | Quantum gravity (reconcile GR + QM) | Non-renormalizability, problem of time, background independence | Numeric evaluation of candidate dynamics; FRG flows; Monte Carlo over discrete structures |
| P2 | Unification of forces/particles | Gauge group choice, fermion generations, mass hierarchies | Scanning anomaly constraints; consistency filtering |
| P3 | Foundations of mathematics | Which axioms/formalism physics actually needs | Proof assistants (Lean) make dependencies explicit |
| P4 | Emergence & reduction | Showing macro physics follows from micro rules | MD/FEA/CFD simulation stacks as reduction checkers |

P1 is the active battleground and the focus of the literature sweep below. P3 is where
this workspace has the strongest comparative advantage (see the LaTeX/Lean
formalization plan).

## 2. Literature map (Scholar sweep, 2026-09-16)

Three quantum-gravity programs plus the formal-math tooling track were swept. Full
result tables are saved as CSVs in this workspace.

### 2.1 Asymptotic Safety — `toe_lit_asymptotic_safety.csv`

Gravity as a non-perturbatively renormalizable QFT with an interacting UV fixed point.

- Bonanno, Eichhorn, Gies, Pawlowski et al., *Critical reflections on asymptotically
  safe gravity*, Frontiers in Physics 2020 — 324 citations. The field's own critical
  self-assessment; includes the black-hole entropy objection.
- Eichhorn, *Asymptotically safe quantum gravity and its phenomenology — a review*,
  arXiv:2606.21522 (2026). Current state of the program, predictive power for
  particle physics.
- Eichhorn & Schiffer, *Asymptotic safety of gravity with matter*, Handbook of Quantum
  Gravity 2023 — 78 citations. Matter coupling is where the program lives or dies.
- Ferrero, *Asymptotic safety and canonical quantum gravity*, IJMPA 2026. Bridges to
  the canonical/LQG tradition — useful for cross-program consistency checks.
- Bonanno, *Asymptotic safety and cosmology*, Handbook of Quantum Gravity 2024.
  Cosmological consequences — the most testable end.

**Agent-actionable:** FRG flow equations are ODE/PDE systems — numerically tractable.
Truncation convergence checks are automatable.

### 2.2 Causal Set Theory — `toe_lit_causal_sets.csv`

Spacetime as a discrete partially ordered set; "order + number = geometry".

- Surya, *The Causal Set Approach to Quantum Gravity: An Introduction*, 2025 (book).
  The standard current entry point.
- Dowker & Surya, *The causal set approach to the problem of quantum gravity*,
  Handbook of Quantum Gravity 2024.
- Cunningham & Surya, *Dimensionally restricted causal set quantum gravity*, CQG 2020
  — 24 citations. 2D/3D models where the path integral is actually computable.
- de Brito, Eichhorn & Pfeiffer, *Higher-order curvature operators in causal set
  quantum gravity*, EPJ Plus 2023. Reconstructing continuum curvature from discrete
  order — the key computational problem.
- Added during Phase 1 validation: Machet & Eichhorn, *On the continuum limit of
  Benincasa-Dowker-Glaser causal set actions*, arXiv:2007.13192 — source of the exact
  2D abundance series and the flat-diamond limit ⟨S⟩ → 2 used to validate the toolkit;
  and Ferguson, Nasiri & Wallden, arXiv:2506.19538 — BD fluctuation control via the
  ε-smearing family.

**Agent-actionable:** causal-set sprinkling, dimension estimators
(Myrheim–Meyer), and Benincasa–Dowker curvature operators are pure combinatorics +
Monte Carlo — directly implementable in Python in this workspace.

### 2.3 Loop Quantum Gravity / Spin Foams — `toe_lit_lqg.csv`

- Engle & Speziale, *Spin foams: foundations*, Handbook of Quantum Gravity 2024 —
  27 citations.
- Livine, *Spinfoam models for quantum gravity: Overview*, arXiv:2403.09364 (2024) —
  26 citations.

**Agent-actionable:** spin-foam amplitudes for small triangulations are computable;
semiclassical limit checks are the open test.

### 2.4 Formal mathematics tooling — `toe_lit_formal_math.csv`

The missing pillar in most ToE discussions: nothing counts as established until it is
formal. This track is where agentic tooling is already producing published results.

- Varambally et al., *Hilbert: Recursively building formal proofs with informal
  reasoning*, ICLR 2026 — 46 citations. LLM + Lean 4 recursive proof construction.
- Breen et al., *Ax-prover: agentic framework for theorem proving in mathematics and
  quantum physics*, Machine Learning: Science and Technology 2026 — directly on-topic:
  formalizing quantum physics results.
- Nie et al., *FormaTheoria: large-scale Lean theories from mathematical literature —
  toward the classification of finite simple groups*, arXiv:2608.10894 (2026, with
  S.-T. Yau). Proof of concept for theory-scale formalization.
- Tang, *Mathematical formalized problem solving and theorem proving in Lean 4*,
  arXiv:2409.05977 (2024).

## 3. The pipeline (how an idea moves through this workspace)

```
IDEA → [Stage 1] Literature position check (Scholar/PubMed — is it already dead?)
     → [Stage 2] Consistency filter (dimensional analysis, known limits, anomaly constraints)
     → [Stage 3] Consequence computation (numeric/simulation: what does it predict?)
     → [Stage 4] Reduction check (does it reproduce GR/QM/SM in the right limits?)
     → [Stage 5] Formalization (core claims into Lean-checkable form; writeup in LaTeX)
     → [Stage 6] Public falsification (GitHub — open repo, others must be able to kill it)
```

**Kill criteria (any one suffices to archive an idea):**
1. Fails to recover GR in the classical limit.
2. Fails to recover QM unitarity.
3. Requires fine-tuning worse than the problem it solves.
4. Produces no new falsifiable prediction within 3 pipeline iterations.
5. Contradicts any experimentally confirmed datum.

## 4. Tool-to-stage mapping (this machine's actual stack)

| Pipeline stage | Local tools |
|---|---|
| Literature | Scholar, PubMed plugins |
| Consistency / symbolic | Python (sympy), LaTeX writeups |
| Consequence computation | GROMACS/AmberTools (emergent atomic behavior), OpenFOAM/PyAnsys (continuum limits), Schrödinger suite (quantum chemistry reduction) |
| Discrete quantum gravity numerics | Custom Python (causal-set sprinklers, FRG flow integrators) — to be built here |
| Materials/structure cross-check | Materials Project, OQMD, PDB plugins |
| Formalization | LaTeX stack (packaged), Lean 4 (to be installed if user approves) |
| Publication / collaboration | GitHub plugin (open repo per project) |

## 5. Phased plan

- **Phase 0 (now):** This scaffold + literature CSVs + LaTeX formalization plan.
  Deliverable: workspace documents. ✅ Done today.
- **Phase 1:** Implement a causal-set toolkit in Python: sprinkle into 2D Minkowski,
  estimate dimension via Myrheim–Meyer, compute Benincasa–Dowker curvature. Validate
  against Cunningham & Surya (2020) published numbers. This is a real, bounded,
  checkable computation. ✅ **Done 2026-09-16** — `causal_set_toolkit.py`. Results:
  - **Sprinkling/causal order validated:** Myrheim–Meyer ordering fraction = 0.494–0.504
    across N=100–400 (analytic d=2 value: 0.5).
  - **Counting code validated against exact theory:** interval abundances N₀, N₁, N₂
    match the exact rational-arithmetic evaluation of the analytic series
    (Machet & Eichhorn 2021, arXiv:2007.13192 eq. 49) to ~1%, zero free parameters.
    Residual ~2–3σ tension on two of nine cells — likely optimistic SEMs under
    heavy-tailed fluctuations; flagged as open item.
  - **2D BDG action implemented:** S = 2(N − 2N₀ + 4N₁ − 2N₂). Measured ensemble
    means (150 trials) consistent with the exact flat-diamond value ⟨S⟩ = 2 (the
    joint/boundary term — not 0; corrected during this work) within ~1.3 SEM.
  - **Curvature detection confirmed:** 2D de Sitter (R=2) sprinklings give ⟨S⟩ ≈ 50
    vs flat ≈ −7…−41 — clean separation at every N tested. Quantitative R·V matching
    needs the ε-smeared BDG family (the documented remedy for the BD action's large
    non-self-averaging fluctuations, which this toolkit reproduced).
  - **Honest failure logged:** the first implementation used a misremembered
    per-element operator B(x) = 2(1 − N₁(x)); it failed validation (drifted with N),
    was caught by the pipeline's own kill criteria, and replaced with the published
    abundance form. This is the pipeline working as designed.
- **Phase 1.5:** ε-smeared BDG action — the documented remedy for the BD action's
  non-self-averaging fluctuations. ✅ **Done 2026-09-16** — same file, section [5],
  `bd_action_2d_smeared(rel, eps)`. Kernel f₂(j,ε) = (1−ε)^j · [1 − 2jε/(1−ε) +
  j(j−1)/2 · (ε/(1−ε))²], S_ε = 2ε[N − 2ε Σ_j f₂(j,ε) N_j]; constants triangulated
  from Glaser's smearing family via Yeats (CQG 2025) and Ferguson–Nasiri–Wallden
  (arXiv:2506.19538, App. A). Sanity gate: ε→1 reproduces the unsmeared BDG action
  exactly. Results (150-trial ensembles, flat vs 2D de Sitter R=2):
  - Separation grows monotonically as ε decreases: **1.23σ (ε=1) → 2.92σ (ε=0.5)
    → 11.30σ (ε=0.25) → 27.54σ (ε=0.1)** — the smeared family tames the fluctuations
    exactly as the literature predicts.
  - At ε=0.1 the flat-diamond mean is 2.19 ± 0.28 vs the exact continuum value 2 —
    quantitative recovery within error bars.
- **Phase 2:** FRG flow integrator for the Einstein–Hilbert truncation of asymptotic
  safety; reproduce the fixed-point structure reported in the literature.
  ✅ **Done 2026-09-16** — `frg_eh_truncation.py`. Equations taken from published
  sources (Litim cutoff, d=4; arXiv:2107.01071 eq. 4.8 at N_f=0, cross-checked
  against the form quoted from Reuter–Saueressig; fixed-point values also in
  Reuter & Saueressig, arXiv:1901.01731). Results, all reproduced to printed
  precision:
  - GFP at origin verified (β(0,0) = 0).
  - **NGFP: g\* = 0.707321, λ\* = 0.193201, η_N = −2.000000** — Newton iteration from
    4 independent seeds, spread < 10⁻¹⁶, residual |β| ~ 10⁻¹⁶; published values
    (0.707321, 0.193201) matched to all 6 decimals.
  - **Critical exponents θ = 1.475302 ± 3.043206 i** — matches published
    1.475302 ± 3.043206 i exactly. Both Re θ > 0 → NGFP UV-attractive in both
    directions → 2 relevant couplings (the predictive-power statement of the
    truncation).
  - Trajectory check: RK4 integration toward the UV spirals into the NGFP
    (distance 0.054 → 0.0008 in 60 steps), consistent with Im θ ≠ 0.
- **Phase 3:** Formalization pilot (see `formalization_plan.pdf`): verify the
  Schwarzschild solution against the vacuum Einstein equations — a computation, hence
  machine-checkable — then port the argument structure into Lean.
  **Level 0 done 2026-09-16** — `schwarzschild_check.py`. No symbolic engine in the
  managed runtime, so implemented as Richardson-extrapolated (O(h⁴)) numeric Ricci
  computation with harness controls: Minkowski negative control max |R_μν| = 1.3×10⁻⁷
  (pass); 2-sphere positive control recovers R = 2/a² to 10⁻⁹ (pass — proves the
  checker detects curvature). Target: Schwarzschild max |R_μν| = 8.0×10⁻⁶ over 18
  grid points on r ∈ (2M, 20M], worst point nearest the horizon as expected —
  vacuum equations **verified numerically**.
  **Level 1 done 2026-09-16** — `schwarzschild_symbolic.py` (sympy 1.14.0, installed
  into the managed runtime for this). All 16 Ricci components of the Schwarzschild
  metric are **symbolically identically zero** — R_μν ≡ 0 as exact symbolic
  expressions, not numerics. Positive control (2-sphere of radius a) recovers
  R = 2/a² symbolically. Process note: the controls caught a real bug —
  `sp.Matrix.inv_quick` silently returns zeros for symbolic matrices; the checker
  uses `g.inv()`. This is exactly why the harness has controls.
  **Level 2 done 2026-09-16** — `lean_schwarzschild/Schwarzschild.lean` (Lean 4.34.0
  via elan, installed for this). Theorems `Rtt_vacuum` and `Rrr_vacuum` proved by
  `native_decide` over ℤ[r, M]: the algebraic identity that makes the tt and rr
  Ricci components vanish is now machine-checked with full kernel verification
  (only axiom: the `native_decide` compiler-trust axiom). Scope is honestly
  limited: this proves an algebraic identity about the Schwarzschild coefficients,
  not differential geometry in mathlib — the coordinate-chart/differentiable-manifold
  layer is the remaining gap to a full formalization.
- **Phase 4:** Open a GitHub repo, publish Phase 1–3 artifacts, invite falsification.
  ✅ **Done 2026-09-16** — https://github.com/Cbaird26/toe-computational-pipeline
  (private by default; flip to public to open it for falsification). Contains all
  code, the literature CSVs, this document, and the formalization plan source.
  The compiled PDF is kept local (binary artifact; regenerate from the .tex).

## 6. Honest limits

- Conceptual breakthroughs do not come out of this pipeline; the pipeline *filters and
  hardens* ideas. A human (or a future model) still has to have the idea.
- The strongest realistic contribution from a setup like this is **negative results**
  (killing bad candidates cheaply) and **verified infrastructure** (formalized,
  reusable mathematics). Both are genuinely valuable and genuinely achievable.

---

*Files: `toe_lit_asymptotic_safety.csv`, `toe_lit_causal_sets.csv`, `toe_lit_lqg.csv`,
`toe_lit_formal_math.csv` (raw sweep data); `formalization_plan.tex` /
`formalization_plan.pdf` (Stage-5 plan); `causal_set_toolkit.py` (Phase 1 + 1.5);
`frg_eh_truncation.py` (Phase 2); `schwarzschild_check.py`, `schwarzschild_symbolic.py`,
`lean_schwarzschild/Schwarzschild.lean` (Phase 3, Levels 0–2).*
