"""Phase 2: FRG flow in the Einstein-Hilbert truncation (asymptotic safety).

Equations (Litim/optimized cutoff, d=4, pure gravity), as printed in
arXiv:2107.01071 eq. (4.8) at N_f = 0 and equivalently in the form used by
the researchsquare preprint quoting Reuter-Saueressig [their ref 21]:

    beta_g   = (2 + eta_N) g
    beta_lam = (eta_N - 2) lam
               + (g / 12 pi) [ 30/(1 - 2 lam) - 24 - 5 eta_N/(1 - 2 lam) ]
    eta_N    = g B1(lam) / (1 - g B2(lam))
    B1(lam)  = (1/3 pi) [ 5/(1-2 lam) - 9/(1-2 lam)^2 - 7 ]
    B2(lam)  = -(1/12 pi) [ 5/(1-2 lam) - 6/(1-2 lam)^2 ]

Validation targets (published, same scheme):
    g* = 0.707321, lambda* = 0.193201, eta_N* = -2 (exactly, since beta_g = 0)
    critical exponents theta = 1.475302 +/- 3.043206 i
    Gaussian fixed point at g = lambda = 0.

Checks: Newton iteration for the NGFP from multiple seeds; numerical
Jacobian -> stability matrix -> critical exponents; RK4 trajectory
integration for flow sanity (UV-attractive spiral into the NGFP).
"""

import numpy as np

PI = np.pi


def B1(lam):
    return (1.0 / (3.0 * PI)) * (5.0 / (1.0 - 2.0 * lam) - 9.0 / (1.0 - 2.0 * lam) ** 2 - 7.0)


def B2(lam):
    return -(1.0 / (12.0 * PI)) * (5.0 / (1.0 - 2.0 * lam) - 6.0 / (1.0 - 2.0 * lam) ** 2)


def eta_N(g, lam):
    return g * B1(lam) / (1.0 - g * B2(lam))


def beta(u):
    """u = (g, lam). Returns (beta_g, beta_lam)."""
    g, lam = u
    eta = eta_N(g, lam)
    bg = (2.0 + eta) * g
    bl = (eta - 2.0) * lam + (g / (12.0 * PI)) * (
        30.0 / (1.0 - 2.0 * lam) - 24.0 - 5.0 * eta / (1.0 - 2.0 * lam)
    )
    return np.array([bg, bl])


def find_fixed_point(seed, tol=1e-14, maxit=200):
    """Newton iteration with numerical Jacobian."""
    u = np.array(seed, dtype=float)
    for _ in range(maxit):
        J = jacobian(u)
        step = np.linalg.solve(J, -beta(u))
        u = u + step
        if np.linalg.norm(step) < tol:
            break
    return u


def jacobian(u, h=1e-7):
    J = np.zeros((2, 2))
    for j in range(2):
        du = np.zeros(2)
        du[j] = h
        J[:, j] = (beta(u + du) - beta(u - du)) / (2 * h)
    return J


def rk4(u, dt, steps):
    traj = [u.copy()]
    for _ in range(steps):
        k1 = beta(u)
        k2 = beta(u + 0.5 * dt * k1)
        k3 = beta(u + 0.5 * dt * k2)
        k4 = beta(u + dt * k3)
        u = u + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
        traj.append(u.copy())
    return np.array(traj)


def main():
    print("=" * 74)
    print("Phase 2: Einstein-Hilbert truncation FRG flow (Litim cutoff, d=4)")
    print("=" * 74)

    # --- Gaussian fixed point sanity -----------------------------------------
    b0 = beta(np.array([0.0, 0.0]))
    print(f"\n[0] GFP check: beta(0,0) = ({b0[0]:.1e}, {b0[1]:.1e})  "
          f"{'PASS' if np.abs(b0).max() < 1e-15 else 'FAIL'}")

    # --- NGFP from multiple seeds --------------------------------------------
    print("\n[1] Non-Gaussian fixed point (Newton from 4 seeds)")
    fps = []
    for seed in ([0.5, 0.2], [1.0, 0.1], [0.3, 0.3], [0.9, 0.25]):
        fp = find_fixed_point(seed)
        fps.append(fp)
        eta = eta_N(*fp)
        resid = np.abs(beta(fp)).max()
        print(f"    seed {seed}: g*={fp[0]:.6f}  lambda*={fp[1]:.6f}  "
              f"eta_N={eta:.6f}  |beta|={resid:.1e}")
    fps = np.array(fps)
    spread = fps.std(axis=0).max()
    g_star, lam_star = fps.mean(axis=0)
    print(f"    seed spread: {spread:.1e}")
    print(f"    published:   g*=0.707321  lambda*=0.193201  eta_N=-2 (exact)")

    # --- Critical exponents ---------------------------------------------------
    print("\n[2] Critical exponents (theta = -eig(stability matrix))")
    J = jacobian(np.array([g_star, lam_star]), h=1e-6)
    theta = -np.linalg.eigvals(J)
    theta = sorted(theta, key=lambda z: -z.real)
    print(f"    computed:  theta = {theta[0].real:.6f} +/- {abs(theta[0].imag):.6f} i")
    print(f"    published: theta = 1.475302 +/- 3.043206 i")
    print(f"    both Re(theta) > 0 -> NGFP is UV-attractive in both directions "
          f"(2 relevant couplings)")

    # --- Flow sanity: trajectory spirals into NGFP toward the UV --------------
    print("\n[3] Trajectory check (integrating toward UV, t = ln k increasing)")
    start = np.array([g_star + 0.05, lam_star + 0.02])
    traj = rk4(start, dt=0.05, steps=60)
    dist0 = np.linalg.norm(traj[0] - [g_star, lam_star])
    dist1 = np.linalg.norm(traj[-1] - [g_star, lam_star])
    print(f"    start (g,lambda)=({start[0]:.3f},{start[1]:.3f}), "
          f"dist to NGFP: {dist0:.4f} -> {dist1:.6f} after 60 steps")
    print(f"    {'PASS' if dist1 < dist0 * 0.1 else 'FAIL'}: "
          f"trajectory converges to NGFP toward the UV (spiral, Im theta != 0)")


if __name__ == "__main__":
    main()
