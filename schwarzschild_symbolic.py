"""Phase 3, Level 1: SYMBOLIC verification that the Schwarzschild metric
solves the vacuum Einstein equations R_mn = 0 (r > 2M), using sympy.

Unlike the Level-0 numeric check, this is exact symbolic algebra: every
Christoffel symbol and Ricci component is computed symbolically from the
metric and simplified to zero. Controls first:
  negative: Minkowski (spherical coords) -> R_mn = 0 symbolically
  positive: 2-sphere radius a -> R_mn = (1/a^2) g_mn symbolically (i.e.
            Ricci scalar = 2/a^2), proving the machinery detects curvature
"""

import sympy as sp


def christoffel_symbols(g, coords):
    dim = len(coords)
    ginv = g.inv()  # NB: sympy 1.14 sp.inv_quick is broken for symbolic
                    # entries (returns zeros) — caught by positive control
    dg = [[sp.diff(g[i, j], coords[k]) for k in range(dim)]
          for i in range(dim) for j in range(dim)]
    Gamma = [[[0] * dim for _ in range(dim)] for _ in range(dim)]
    for up in range(dim):
        for lo1 in range(dim):
            for lo2 in range(dim):
                expr = sum(
                    ginv[up, rho] * (
                        sp.diff(g[rho, lo2], coords[lo1])
                        + sp.diff(g[rho, lo1], coords[lo2])
                        - sp.diff(g[lo1, lo2], coords[rho])
                    )
                    for rho in range(dim)
                )
                Gamma[up][lo1][lo2] = sp.simplify(expr / 2)
    return Gamma


def ricci_tensor(Gamma, coords):
    dim = len(coords)
    R = sp.zeros(dim)
    for mu in range(dim):
        for nu in range(dim):
            expr = sum(
                sp.diff(Gamma[rho][nu][mu], coords[rho])
                - sp.diff(Gamma[rho][rho][mu], coords[nu])
                + sum(
                    Gamma[rho][rho][lam] * Gamma[lam][nu][mu]
                    - Gamma[rho][nu][lam] * Gamma[lam][rho][mu]
                    for lam in range(dim)
                )
                for rho in range(dim)
            )
            R[mu, nu] = sp.simplify(expr)
    return R


def main():
    print("=" * 72)
    print("Phase 3 Level 1: symbolic vacuum Einstein check (sympy", sp.__version__, ")")
    print("=" * 72)

    # ---- negative control: Minkowski, spherical coords ----------------------
    t, r, th, ph, M, a = sp.symbols("t r th ph M a", positive=True)
    coords4 = (t, r, th, ph)
    g_mink = sp.diag(-1, 1, r**2, r**2 * sp.sin(th) ** 2)
    R = ricci_tensor(christoffel_symbols(g_mink, coords4), coords4)
    worst = max(sp.simplify(x) for x in R)
    print(f"\n[-] Minkowski: all Ricci components simplify to zero: "
          f"{all(sp.simplify(x) == 0 for x in R)}  "
          f"{'PASS' if all(sp.simplify(x) == 0 for x in R) else 'FAIL'}")

    # ---- positive control: 2-sphere ------------------------------------------
    coords2 = (th, ph)
    g_s2 = sp.diag(a**2, a**2 * sp.sin(th) ** 2)
    R2 = ricci_tensor(christoffel_symbols(g_s2, coords2), coords2)
    ratio = sp.simplify(R2[0, 0] / g_s2[0, 0])
    print(f"[+] 2-sphere: R_mn / g_mn = {ratio} (expect 1/a^2); "
          f"Ricci scalar = {sp.simplify(sum(R2[i, i] / g_s2[i, i] for i in range(2)))}"
          f" (expect 2/a^2)  {'PASS' if sp.simplify(ratio - 1 / a**2) == 0 else 'FAIL'}")

    # ---- target: Schwarzschild -------------------------------------------------
    f = 1 - 2 * M / r
    g_schw = sp.diag(-f, 1 / f, r**2, r**2 * sp.sin(th) ** 2)
    Gamma = christoffel_symbols(g_schw, coords4)
    R_schw = ricci_tensor(Gamma, coords4)
    results = {f"R_{coords4[i]}{coords4[j]}": sp.simplify(R_schw[i, j])
               for i in range(4) for j in range(4)}
    all_zero = all(v == 0 for v in results.values())
    print(f"\n[*] Schwarzschild: all 16 Ricci components simplify to 0: {all_zero}")
    for k, v in results.items():
        print(f"    {k} = {v}")
    print(f"\n    vacuum Einstein equations R_mn = 0: "
          f"{'PROVEN SYMBOLICALLY (r > 2M)' if all_zero else 'FAIL'}")


if __name__ == "__main__":
    main()
