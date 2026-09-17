/-
Phase 3, Level 2 (scoped): kernel-checked proof that the Schwarzschild metric
satisfies R_tt = 0 and R_rr = 0.

Scope honesty: this verifies the ALGEBRAIC identity obtained after applying the
Ricci-tensor formula to the Christoffel symbols (which were extracted from the
sympy Level-1 computation, not from memory). Rational functions in (r, M) are
implemented as exact bivariate integer polynomials; the kernel (via
native_decide) recomputes the polynomial arithmetic and confirms the numerators
are the zero polynomial. This is NOT a formalization of differential geometry
from first principles (that requires Mathlib's manifold library); it is a
machine-checked certificate for the algebraic core of the verification.

R_tt = ∂_r Γ^r_tt + (Γ^ρ_ρr) Γ^r_tt − 2 Γ^t_tr Γ^r_tt
R_rr = ∂_r Γ^r_rr − ∂_r (Γ^ρ_ρr) + (Γ^ρ_ρr) Γ^r_rr
       − ( (Γ^t_tr)² + (Γ^r_rr)² + (Γ^θ_rθ)² + (Γ^φ_rφ)² )
where Γ^ρ_ρr = Γ^t_tr + Γ^r_rr + Γ^θ_rθ + Γ^φ_rφ, and
  Γ^t_tr = M / (r² − 2Mr)          Γ^r_tt = M(r − 2M) / r³
  Γ^r_rr = M / (2Mr − r²)          Γ^θ_rθ = Γ^φ_rφ = 1 / r
-/

namespace Schwarzschild

/-- Bivariate polynomial in (r, M): `p[i][j]` = coefficient of r^i M^j. -/
abbrev Poly := List (List Int)

def trimL : List Int → List Int := fun l => l.reverse.dropWhile (· == 0) |>.reverse

def trimP : Poly → Poly := fun p =>
  (p.map trimL).reverse.dropWhile (· == []) |>.reverse

def addL : List Int → List Int → List Int
  | [], ys => ys
  | xs, [] => xs
  | x :: xs, y :: ys => (x + y) :: addL xs ys

def addP : Poly → Poly → Poly
  | [], q => q
  | p, [] => p
  | c :: p, d :: q => addL c d :: addP p q

def negP : Poly → Poly := fun p => p.map fun c => c.map (· * (-1))

def subP (p q : Poly) : Poly := addP p (negP q)

def mulL : List Int → List Int → List Int
  | [], _ => []
  | x :: xs, ys => addL (ys.map (· * x)) (0 :: mulL xs ys)

def mulP : Poly → Poly → Poly
  | [], _ => []
  | c :: p, q => addP (q.map (mulL c)) ([] :: mulP p q)

/-- d/dr of Σᵢ cᵢ rⁱ = Σᵢ (i+1) cᵢ₊₁ rⁱ. -/
def derivR : Poly → Poly := fun p =>
  (p.drop 1).zipIdx.map fun (c, j) => c.map (· * ((j : Int) + 1))

/-- Rational function in (r, M). -/
structure Rat2 where
  num : Poly
  den : Poly

def Rat2.add (a b : Rat2) : Rat2 :=
  ⟨addP (mulP a.num b.den) (mulP b.num a.den), mulP a.den b.den⟩

def Rat2.sub (a b : Rat2) : Rat2 :=
  ⟨subP (mulP a.num b.den) (mulP b.num a.den), mulP a.den b.den⟩

def Rat2.mul (a b : Rat2) : Rat2 := ⟨mulP a.num b.num, mulP a.den b.den⟩

def Rat2.neg (a : Rat2) : Rat2 := ⟨negP a.num, a.den⟩

def Rat2.derivR (a : Rat2) : Rat2 :=
  ⟨subP (mulP (_root_.Schwarzschild.derivR a.num) a.den)
        (mulP a.num (_root_.Schwarzschild.derivR a.den)),
   mulP a.den a.den⟩

def constP (n : Int) : Poly := [[n]]
def rP : Poly := [[], [1]]   -- the variable r
def mP : Poly := [[0, 1]]    -- the variable M

/-- Γ^t_tr = M / (r² − 2Mr) -/
def Gtr : Rat2 := ⟨mP, subP (mulP rP rP) (mulP (mulP (constP 2) mP) rP)⟩

/-- Γ^r_tt = M(r − 2M) / r³ -/
def Gtt : Rat2 :=
  ⟨mulP mP (subP rP (mulP (constP 2) mP)), mulP rP (mulP rP rP)⟩

/-- Γ^r_rr = M / (2Mr − r²) -/
def Grr : Rat2 := ⟨mP, subP (mulP (mulP (constP 2) mP) rP) (mulP rP rP)⟩

/-- Γ^θ_rθ = Γ^φ_rφ = 1 / r -/
def G1r : Rat2 := ⟨constP 1, rP⟩

/-- Γ^ρ_ρr = Γ^t_tr + Γ^r_rr + Γ^θ_rθ + Γ^φ_rφ -/
def traceR : Rat2 := ((Gtr.add Grr).add G1r).add G1r

/-- R_tt numerator: ∂_r Γ^r_tt + (Γ^ρ_ρr) Γ^r_tt − 2 Γ^t_tr Γ^r_tt -/
def Rtt : Rat2 :=
  (Gtt.derivR.add (traceR.mul Gtt)).sub
    ⟨mulP (constP 2) (Gtr.mul Gtt).num, (Gtr.mul Gtt).den⟩

/-- R_rr: ∂_r Γ^r_rr − ∂_r(Γ^ρ_ρr) + (Γ^ρ_ρr) Γ^r_rr
    − (Γ^t_tr² + Γ^r_rr² + Γ^θ_rθ² + Γ^φ_rφ²) -/
def Rrr : Rat2 :=
  (((Grr.derivR.sub traceR.derivR).add (traceR.mul Grr)).sub
    (Gtr.mul Gtr)).sub
    ((((Grr.mul Grr).add (G1r.mul G1r)).add (G1r.mul G1r)))

theorem Rtt_vacuum : trimP Rtt.num = [] := by native_decide

theorem Rrr_vacuum : trimP Rrr.num = [] := by native_decide

#print axioms Rtt_vacuum
#print axioms Rrr_vacuum

end Schwarzschild
