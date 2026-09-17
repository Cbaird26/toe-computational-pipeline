# ToE Computational Pipeline

Validated computational artifacts from an agent-assisted research program on
quantum gravity / fundamental unification. Every artifact here passed an
explicit validation gate against published results or exact analytic theory
before inclusion. See `ToE_Research_Program.md` for the full pipeline design,
kill criteria, and phase plan.

## Contents

| File | What it is | Validation |
|---|---|---|
| `causal_set_toolkit.py` | 2D causal-set toolkit: Poisson sprinkling (Minkowski diamond + de Sitter), Myrheim–Meyer dimension, interval abundances, ε-smeared Benincasa–Dowker–Glaser action | Abundances match exact analytic series (arXiv:2007.13192 eq. 49) to ~1%; flat-diamond ⟨S⟩ = 2.19 ± 0.28 vs continuum 2 at ε=0.1; de Sitter separated at 27σ |
| `frg_eh_truncation.py` | FRG flow integrator, Einstein–Hilbert truncation (Litim cutoff) | Reproduces Reuter fixed point g\* = 0.707321, λ\* = 0.193201 and critical exponents θ = 1.475302 ± 3.043206i to all published digits |
| `schwarzschild_check.py` | Numeric (Richardson O(h⁴)) Ricci-tensor checker with positive/negative controls | Schwarzschild max \|R_μν\| = 8×10⁻⁶ on 18-point grid |
| `schwarzschild_symbolic.py` | Exact symbolic verification via sympy | All 16 Ricci components ≡ 0; controls pass (2-sphere recovers R = 2/a²) |
| `lean_schwarzschild/Schwarzschild.lean` | Lean 4 kernel-checked algebraic core (rational-function arithmetic over ℤ[r, M]) | `Rtt_vacuum`, `Rrr_vacuum` proved; only axiom is native_decide compiler trust |
| `formalization_plan.tex` | Phase-3 formalization plan (builds with any LaTeX) | — |
| `toe_lit_*.csv` | Literature sweep raw data (Scholar, 2026-09-16) | — |

## Honest limits

- Nothing here is new physics. This is validated infrastructure: the kind of
  cheap, checkable machinery that filters candidate ideas.
- The Lean proof verifies the algebraic identity after the Ricci formula is
  applied to (sympy-extracted) Christoffel symbols — not differential geometry
  from first principles.
- BD action fluctuations are huge and non-self-averaging (documented in the
  literature and reproduced here); only ensemble means are meaningful.

Generated with Kimi Work, 2026-09-16.
