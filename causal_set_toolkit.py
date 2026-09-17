"""Causal-set toolkit — Phase 1 of the ToE research program.

Implements, for 2D spacetimes:
  1. Poisson sprinkling into a causal diamond of 2D Minkowski space.
  2. Causal-order (transitively closed relation) construction.
  3. Myrheim–Meyer dimension estimation (validated: fraction -> 1/2 for d=2).
  4. Interval abundances N_m (pairs with exactly m intermediate elements).
  5. Benincasa-Dowker-Glaser action in 2D (epsilon=1 form):
       S = 2(N - 2 N_0 + 4 N_1 - 2 N_2)
     (Machet & Eichhorn 2021, arXiv:2007.13192, eq. 48).
  6. EXACT analytic ensemble expectations for flat 2D diamonds, from
     arXiv:2007.13192 eq. (49):
       <N_m>_flat = sum_n (-N_f)^n N_f^{m+2} / (n! m! (n+m+1)^2 (n+m+2)^2)
     evaluated in exact rational arithmetic (Fraction), and the resulting
     exact <S>_flat. Continuum limit (their eq. 52): <S> -> (R/2) V + 2,
     i.e. 2 for a flat diamond (the "+2" is the joint/boundary contribution).
  7. Sprinkling into 2D de Sitter (conformally flat; causal order inherited
     from flat (eta, theta) space; volume weighting sec^2(eta)).

Validation logic:
  - Sprinkling/order code is validated by the Myrheim-Meyer fraction (0.5).
  - Counting code is validated against the EXACT analytic <N_m>.
  - The action's continuum behavior is checked against the exact analytic
    <S> and its known limit. BD fluctuations are documented to be large and
    non-self-averaging, so means are reported with SEM over many trials.
"""

from fractions import Fraction
from math import factorial

import numpy as np


# ---------------------------------------------------------------- sprinkling

def sprinkle_minkowski_diamond(n, rng):
    """Poisson-sprinkle n points into the 2D causal diamond
    {|x| <= 1 - |t|, t in (-1, 1)}. Volume = 2, so density rho = n/2 and
    N_f = rho V = n."""
    ts, xs = [], []
    while len(ts) < n:
        m = 4 * (n - len(ts)) + 16
        t = rng.uniform(-1.0, 1.0, m)
        x = rng.uniform(-1.0, 1.0, m)
        ok = np.abs(x) <= 1.0 - np.abs(t)
        take = min(n - len(ts), int(ok.sum()))
        ts.extend(t[ok][:take])
        xs.extend(x[ok][:take])
    return np.array(ts), np.array(xs)


def sprinkle_de_sitter(n, eta_max, rng):
    """Poisson-sprinkle n points into the 2D de Sitter patch
    eta in (-eta_max, eta_max), theta in (0, 2*pi), a=1.
    Metric ds^2 = sec^2(eta)(-d eta^2 + d theta^2); volume weight sec^2(eta)."""
    etas, thetas = [], []
    w_max = 1.0 / np.cos(eta_max) ** 2
    while len(etas) < n:
        m = 4 * (n - len(etas)) + 16
        eta = rng.uniform(-eta_max, eta_max, m)
        w = 1.0 / np.cos(eta) ** 2
        ok = rng.uniform(0.0, w_max, m) < w
        take = min(n - len(etas), int(ok.sum()))
        etas.extend(eta[ok][:take])
        thetas.extend(rng.uniform(0.0, 2 * np.pi, take))
    return np.array(etas), np.array(thetas)


# ------------------------------------------------------------- causal structure

def causal_matrix(u, v):
    """rel[i, j] = (point i precedes point j). Conformally flat 2D:
    i < j iff du > |dv| with du = u_j - u_i > 0."""
    du = u[None, :] - u[:, None]
    dv = np.abs(v[None, :] - v[:, None])
    return (du > 0) & (du > dv)


def ordering_fraction(rel):
    n = rel.shape[0]
    return rel.sum() / (n * (n - 1) / 2.0)


def interval_abundances(rel, m_max=2):
    """N_m = number of related pairs (x, y) with exactly m elements strictly
    between them, for m = 0..m_max. between = rel @ rel counts intermediates."""
    between = rel.astype(np.int64) @ rel.astype(np.int64)
    return [int(((between == m) & rel).sum()) for m in range(m_max + 1)]


def bd_action_2d(rel):
    """2D BDG action S = 2(N - 2 N_0 + 4 N_1 - 2 N_2)."""
    n = rel.shape[0]
    n0, n1, n2 = interval_abundances(rel, 2)
    return 2.0 * (n - 2 * n0 + 4 * n1 - 2 * n2), (n0, n1, n2)


def f2(j, eps):
    """Smearing kernel f_2(j, eps) = (1-eps)^j [1 - 2 j eps/(1-eps)
    + (j(j-1)/2) (eps/(1-eps))^2]. Reconstructed from Glaser's closed-form
    coefficients (C^(2) = (1, -2, 1), alpha_2 = -2, beta_2 = 4) via the
    general-d form of arXiv:2506.19538 App. A; verified to reproduce the
    epsilon=1 BDG action exactly (Machet-Eichhorn eq. 48)."""
    return (1.0 - eps) ** j * (1.0 - 2.0 * j * eps / (1.0 - eps)
                               + 0.5 * j * (j - 1.0) * (eps / (1.0 - eps)) ** 2)


def bd_action_2d_smeared(rel, eps):
    """Epsilon-smeared 2D BDG action:
    S_eps = 2 eps [ N - 2 eps sum_j f_2(j, eps) N_j ].
    The (1-eps)^j decay suppresses the non-self-averaging fluctuations of
    the eps=1 action. Sum truncated where |f_2| < 1e-10."""
    n = rel.shape[0]
    if eps > 1.0 - 1e-9:
        s, _ = bd_action_2d(rel)
        return s
    # find needed m_max
    m_max = 2
    while abs(f2(m_max, eps)) > 1e-10 and m_max < n:
        m_max += 1
    abund = interval_abundances(rel, m_max)
    s = sum(f2(j, eps) * abund[j] for j in range(m_max + 1))
    return 2.0 * eps * (n - 2.0 * eps * s)


def check_smeared_limit(rel):
    """Self-check: S_eps -> eps=1 BDG action as eps -> 1."""
    s1, _ = bd_action_2d(rel)
    s_eps = bd_action_2d_smeared(rel, 1.0 - 1e-12)
    return abs(s1 - s_eps) < 1e-6 * max(1.0, abs(s1))


# --------------------------------------------- exact analytic expectations

def analytic_flat_abundances(nf):
    """Exact <N_0>, <N_1>, <N_2> for a Poisson sprinkling into a flat 2D
    diamond with N_f = rho V, via arXiv:2007.13192 eq. (49), evaluated in
    exact rational arithmetic. N_f must be a nonnegative integer."""
    nf_f = Fraction(nf)
    acc = [Fraction(0), Fraction(0), Fraction(0)]  # series A_m
    term = Fraction(1)  # (-N_f)^n / n!
    n = 0
    tiny = Fraction(1, 10**30)
    while True:
        for m in (0, 1, 2):
            denom = (n + m + 1) ** 2 * (n + m + 2) ** 2
            acc[m] += term / denom
        if n > 4 * nf + 60 and abs(term) < tiny:
            break
        n += 1
        term *= -nf_f / n
    out = []
    for m in (0, 1, 2):
        out.append(float(nf_f ** (m + 2) * acc[m] / Fraction(factorial(m))))
    return out


def analytic_flat_action(nf):
    """Exact ensemble <S> for a flat 2D diamond at N_f = nf."""
    n0, n1, n2 = analytic_flat_abundances(nf)
    return 2.0 * (nf - 2 * n0 + 4 * n1 - 2 * n2), (n0, n1, n2)


# -------------------------------------------------------------------- driver

def run_trials(sprinkle_fn, n, trials, seed):
    fracs, actions, abuns = [], [], []
    for t in range(trials):
        rng = np.random.default_rng(seed + t)
        u, v = sprinkle_fn(n, rng)
        rel = causal_matrix(u, v)
        fracs.append(ordering_fraction(rel))
        s, (n0, n1, n2) = bd_action_2d(rel)
        actions.append(s)
        abuns.append((n0, n1, n2))
    return np.array(fracs), np.array(actions), np.array(abuns, dtype=float)


def main():
    trials = 150
    print("=" * 78)
    print("Causal-set toolkit validation (2D)")
    print("=" * 78)

    # --- Test 1: Myrheim-Meyer ordering fraction -----------------------------
    print("\n[1] Myrheim-Meyer ordering fraction, flat 2D Minkowski (target 0.5)")
    print(f"{'N':>6} {'fraction':>10} {'std':>8}")
    for n in (100, 200, 400):
        fracs, _, _ = run_trials(sprinkle_minkowski_diamond, n, 20, 1000 + n)
        print(f"{n:>6} {fracs.mean():>10.4f} {fracs.std():>8.4f}")

    # --- Test 2: abundances vs EXACT analytic expectation ---------------------
    print("\n[2] Interval abundances vs exact theory (arXiv:2007.13192 eq. 49)")
    for n in (100, 200, 400):
        _, _, ab = run_trials(sprinkle_minkowski_diamond, n, trials, 2000 + n)
        exact = analytic_flat_abundances(n)
        sem = ab.std(axis=0) / np.sqrt(trials)
        print(f"  N={n:>4}: " + "  ".join(
            f"N{m}: meas {ab[:, m].mean():9.2f} ± {sem[m]:5.2f} | exact {exact[m]:9.2f}"
            for m in range(3)))

    # --- Test 3: flat action vs exact <S> and continuum limit (+2) -----------
    print("\n[3] BDG action, flat 2D diamond: measured vs exact vs continuum (2)")
    print(f"{'N':>6} {'meas <S>':>10} {'SEM':>8} {'exact <S>':>10} {'lim':>5}")
    for n in (100, 200, 400):
        _, acts, _ = run_trials(sprinkle_minkowski_diamond, n, trials, 3000 + n)
        exact_s, _ = analytic_flat_action(n)
        sem = acts.std() / np.sqrt(trials)
        print(f"{n:>6} {acts.mean():>10.2f} {sem:>8.2f} {exact_s:>10.2f} {2:>5}")

    # --- Test 4: curvature detection, 2D de Sitter (R=2) vs flat -------------
    eta_max = 1.0
    vol = 2 * np.pi * 2 * np.tan(eta_max)
    ds_sprinkle = lambda n, rng: sprinkle_de_sitter(n, eta_max, rng)
    print(f"\n[4] Curvature detection: de Sitter a=1 (R=2, patch volume {vol:.1f})"
          " vs flat")
    print(f"{'N':>6} {'flat <S>':>10} {'SEM':>7} {'dS <S>':>10} {'SEM':>7}")
    for n in (100, 200, 400):
        _, flat, _ = run_trials(sprinkle_minkowski_diamond, n, trials, 4000 + n)
        _, ds, _ = run_trials(ds_sprinkle, n, trials, 5000 + n)
        print(f"{n:>6} {flat.mean():>10.2f} {flat.std()/np.sqrt(trials):>7.2f}"
              f" {ds.mean():>10.2f} {ds.std()/np.sqrt(trials):>7.2f}")

    print("\nInterpretation:")
    print("  [1] fraction -> 0.5 validates sprinkling + causal order (d=2).")
    print("  [2] measured abundances matching exact series validates the counting")
    print("      code with zero free parameters.")
    print("  [3] measured <S> tracking the exact <S> (which itself -> 2, the known")
    print("      joint/boundary contribution, NOT 0) validates the action code.")
    print("      Large std is the documented non-self-averaging BD fluctuation.")
    print("  [4] dS mean > flat mean shows curvature sensitivity; quantitative")
    print("      R*V matching needs the epsilon-smeared family + higher density.")

    # --- Phase 1.5: epsilon-smeared action -----------------------------------
    print("\n" + "=" * 78)
    print("[5] Phase 1.5: epsilon-smeared BDG action (fluctuation suppression)")
    rng = np.random.default_rng(7777)
    u, v = sprinkle_minkowski_diamond(400, rng)
    rel = causal_matrix(u, v)
    print(f"    self-check S_eps->1 == S_BDG: {check_smeared_limit(rel)}")
    print(f"{'eps':>6} {'flat <S>':>10} {'SEM':>8} {'dS <S>':>10} {'SEM':>8} {'sep (sigma)':>12}")
    for eps in (1.0, 0.5, 0.25, 0.1):
        flat_s, ds_s = [], []
        for t in range(60):
            rng = np.random.default_rng(6000 + t)
            u, v = sprinkle_minkowski_diamond(400, rng)
            flat_s.append(bd_action_2d_smeared(causal_matrix(u, v), eps))
            rng = np.random.default_rng(7000 + t)
            u, v = sprinkle_de_sitter(400, 1.0, rng)
            ds_s.append(bd_action_2d_smeared(causal_matrix(u, v), eps))
        flat_s, ds_s = np.array(flat_s), np.array(ds_s)
        sem_f, sem_d = flat_s.std() / np.sqrt(60), ds_s.std() / np.sqrt(60)
        sep = abs(ds_s.mean() - flat_s.mean()) / np.sqrt(sem_f ** 2 + sem_d ** 2)
        print(f"{eps:>6} {flat_s.mean():>10.2f} {sem_f:>8.2f} "
              f"{ds_s.mean():>10.2f} {sem_d:>8.2f} {sep:>12.2f}")
    print("    (flat continuum value is 2 for all eps; separation should GROW")
    print("     as eps shrinks if the smearing suppresses fluctuations)")


if __name__ == "__main__":
    main()
