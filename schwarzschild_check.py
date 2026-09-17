"""Phase 3, Level 0 (numeric): verify that the Schwarzschild metric solves the
vacuum Einstein equations R_mn = 0 for r > 2M.

No symbolic engine available in this runtime, so derivatives are computed by
Richardson-extrapolated central differences (error O(h^4) at each of two
derivative levels). This is a *numeric* verification, weaker than the planned
sympy/Lean levels, but the harness itself is validated by two controls:

  Negative control: Minkowski in spherical coordinates -> R_mn = 0 (must pass)
  Positive control: unit 2-sphere -> Ricci scalar R = 2 (checker must detect
                    nonzero curvature; proves the harness is not trivially
                    returning zeros)

Then the target:
  Schwarzschild (M=1) -> all 10 components of R_mn ~ 0 on a grid r in (2M, 20M].

All metrics diagonal; general-diagonal formulas used throughout.
"""

import numpy as np


def make_metric(kind, **kw):
    """Return g(x) -> 1D array of diagonal components, x = coords tuple."""
    if kind == "minkowski":  # (t, r, th, ph), spherical
        return lambda x: np.array([-1.0, 1.0, x[1] ** 2, x[1] ** 2 * np.sin(x[2]) ** 2])
    if kind == "sphere2":  # (th, ph), radius a
        a = kw.get("a", 1.0)
        return lambda x: np.array([a ** 2, a ** 2 * np.sin(x[0]) ** 2])
    if kind == "schwarzschild":  # (t, r, th, ph), G = c = 1
        M = kw.get("M", 1.0)
        def g(x):
            r = x[1]
            f = 1.0 - 2.0 * M / r
            return np.array([-f, 1.0 / f, r ** 2, r ** 2 * np.sin(x[2]) ** 2])
        return g
    raise ValueError(kind)


def deriv(f, x, i, h):
    """Richardson-extrapolated central difference of f wrt coordinate i."""
    xp, xm = list(x), list(x)
    xp[i] += h
    xm[i] -= h
    d1 = (f(tuple(xp)) - f(tuple(xm))) / (2 * h)
    xp2, xm2 = list(x), list(x)
    xp2[i] += h / 2
    xm2[i] -= h / 2
    d2 = (f(tuple(xp2)) - f(tuple(xm2))) / h
    return d2 + (d2 - d1) / 3.0  # O(h^4)


def christoffel(g, x, h=1e-4):
    """Gamma[up][lo1][lo2] at point x for diagonal metric g."""
    dim = len(x)
    gv = g(x)
    dg = np.stack([deriv(g, x, k, h) for k in range(dim)])  # dg[k][mu]
    Gamma = np.zeros((dim, dim, dim))
    for up in range(dim):
        for lo1 in range(dim):
            for lo2 in range(dim):
                Gamma[up, lo1, lo2] = 0.5 / gv[up] * (
                    dg[lo1][up] * (1 if up == lo2 else 0)
                    + dg[lo2][up] * (1 if up == lo1 else 0)
                    - dg[up][lo1] * (1 if lo1 == lo2 else 0)
                )
    return Gamma


def ricci(g, x, h=1e-3):
    """Ricci tensor R[mu][nu] at x. Derivatives of Gamma via Richardson."""
    dim = len(x)

    def gamma_at(y):
        return christoffel(g, y)

    dG = np.zeros((dim, dim, dim, dim))  # dG[rho][up][lo1][lo2]
    for rho in range(dim):
        dG[rho] = deriv(gamma_at, x, rho, h)

    G = christoffel(g, x)
    R = np.zeros((dim, dim))
    for mu in range(dim):
        for nu in range(dim):
            s = 0.0
            for rho in range(dim):
                s += dG[rho][rho][nu][mu] - dG[nu][rho][rho][mu]
                for lam in range(dim):
                    s += G[rho][rho][lam] * G[lam][nu][mu] - G[rho][nu][lam] * G[lam][rho][mu]
            R[mu, nu] = s
    return R


def ricci_scalar(g, x):
    gv = g(x)
    R = ricci(g, x)
    return float(sum(R[i, i] / gv[i] for i in range(len(x))))


def main():
    print("=" * 72)
    print("Phase 3 Level 0: vacuum Einstein equation check (numeric, Richardson O(h^4))")
    print("=" * 72)

    # Negative control: Minkowski in spherical coords
    gm = make_metric("minkowski")
    worst = 0.0
    for r in (1.5, 3.0, 10.0):
        for th in (0.4, 1.1, 1.5):
            R = ricci(gm, (0.0, r, th, 0.7))
            worst = max(worst, np.abs(R).max())
    print(f"\n[-] Minkowski (negative control): max |R_mn| = {worst:.2e}  "
          f"{'PASS' if worst < 1e-6 else 'FAIL'}")

    # Positive control: 2-sphere of radius a, Ricci scalar = 2/a^2
    ok = True
    for a in (1.0, 2.5):
        gs = make_metric("sphere2", a=a)
        for th in (0.5, 1.2):
            val = ricci_scalar(gs, (th, 0.9))
            exp = 2.0 / a ** 2
            err = abs(val - exp) / exp
            ok &= err < 1e-5
            print(f"[+] 2-sphere a={a}: R = {val:.8f}, expected {exp:.8f}, "
                  f"rel err {err:.1e}")
    print(f"    positive control: {'PASS' if ok else 'FAIL'}")

    # Target: Schwarzschild
    gsch = make_metric("schwarzschild", M=1.0)
    worst = 0.0
    where = None
    for r in (2.05, 2.2, 3.0, 5.0, 10.0, 20.0):
        for th in (0.3, 1.0, 1.55):
            R = ricci(gsch, (0.0, r, th, 1.2))
            w = np.abs(R).max()
            if w > worst:
                worst, where = w, (r, th)
    print(f"\n[*] Schwarzschild (M=1), 18 grid points, r in (2M, 20M]:")
    print(f"    max |R_mn| = {worst:.3e} at r={where[0]}, theta={where[1]}")
    print(f"    vacuum Einstein equations R_mn = 0: "
          f"{'VERIFIED (numeric)' if worst < 1e-5 else 'FAIL'}")


if __name__ == "__main__":
    main()
