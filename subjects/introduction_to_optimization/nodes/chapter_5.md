# Chapter 5 — Theory of Constrained Optimization: First-Order Conditions  
**Clean Markdown Conversion**

This chapter introduces the geometric ideas, tangent cones, active sets, constraint qualifications, and the Karush–Kuhn–Tucker (KKT) conditions for constrained optimization.

---

## 1. Review: Unconstrained Minimization

For an unconstrained problem, necessary and sufficient conditions were:

- **Necessary:**  
  \( \nabla f(x^*) = 0 \) and \( \nabla^2 f(x^*) \) positive semidefinite.

- **Sufficient:**  
  If \( \nabla f(x^*) = 0 \) and \( \nabla^2 f(x^*) \succ 0 \), then \(x^*\) is a *strict* local minimizer.

These ideas extend to constrained optimization, but with more structure.

---

## 2. General Constrained Optimization Problem

Let equality constraints \( c_i(x) = 0 \) for \( i \in E \)  
and inequality constraints \( c_i(x) \le 0 \) for \( i \in I \).

Define the feasible set:

$$
\Omega = \{ x \in \mathbb{R}^n \mid c_i(x)=0,\ i\in E,\ \ c_i(x)\le0,\ i\in I \}.
$$

We consider:

$$
\min_{x \in \Omega} f(x). \tag{27}
$$

Local minimizer \(x^*\):  
There exists a neighborhood \(N_r(x^*)\) such that:

$$
f(x^*) \le f(x) \quad \forall x \in N_r(x^*) \cap \Omega.
$$

---

## 3. Tangent Cone and Admissible Directions

Even though we cannot move arbitrarily (constraints restrict feasible directions), the basic idea remains:

> We want points where no feasible descent direction exists.

### Tangent Cone \(T_\Omega(x)\)

Definition (non-computational):

A vector \( d \) is in the tangent cone if there exists feasible \( z_k \to x \) such that:

$$
d = \lim_{k\to\infty} \alpha_k (z_k - x), \quad \alpha_k > 0.
$$

The tangent cone depends **only** on geometry of \( \Omega \), not the constraint functions.

### Example 1: Single Equality Constraint

For:

$$
\Omega = \{ x \in \mathbb{R}^2 \mid c_1(x) = x_1^2 + x_2^2 - 2 = 0 \},
$$

the tangent cone is the tangent line:

$$
T_\Omega(x) = \{ d \in \mathbb{R}^2 \mid \nabla c_1(x)^T d = 0 \}. \tag{28}
$$

### Example 2: Disk Interior Constraint

$$
\Omega = \{ x \in \mathbb{R}^2 \mid 2 - x_1^2 - x_2^2 \ge 0 \}.
$$

If:

- **Interior point:** \(T_\Omega(x)=\mathbb{R}^2\)  
- **Boundary point:** Tangent cone is the half-space pointing inward.

### Example 3: Non-smooth Boundary

For:

$$
\Omega = \{ (x_1, x_2) \mid x_2 \ge -x_1^2 \},
$$

at \(x=(0,0)\):

$$
T_\Omega(0,0) = \{ (d_1, d_2) \mid d_2 \ge 0 \}.
$$

---

## 4. First-Order Necessary Condition via Tangent Cone

Theorem 12.3 (book p. 325):

> If \(x^*\) is a local minimizer, then for every \(d \in T_\Omega(x^*)\),
> \[
> \nabla f(x^*)^T d \ge 0.
> \]

This ensures no feasible descent direction exists.

However, this is not computationally useful → motivates KKT.

---

## 5. Active Constraints and the Active Set

Define:

$$
A(x) = E \cup \{ i \in I \mid c_i(x) = 0 \}.
$$

- Equality constraints are **always** active.
- Inequality constraints active only when binding: \(c_i(x)=0\).

Inactive constraints impose **no restrictions** locally.

---

## 6. Single Equality Constraint Example

Problem:

$$
\min\ x_1 + x_2 \quad \text{s.t. } c_1(x)=x_1^2 + x_2^2 - 2 = 0. \tag{29}
$$

Feasible directions satisfy:

$$
\nabla c_1(x)^T d = 0.
$$

Descent is possible if:

$$
\nabla f(x)^T d < 0.
$$

If no such \(d\) exists → gradients are parallel:

$$
\nabla f(x) = \lambda \nabla c_1(x). \tag{30}
$$

This is equivalent to:

$$
\nabla_x L(x,\lambda) = 0, \tag{33}
$$

where:

$$
L(x,\lambda) = f(x) - \lambda c_1(x). \tag{32}
$$

Solutions: \( (\pm 1, \pm 1) \), only \((-1,-1)\) is minimizer.

---

## 7. Single Inequality Constraint Example

Problem:

$$
\min\ x_1 + x_2 \quad \text{s.t. } c_1(x) = 2 - x_1^2 - x_2^2 \ge 0.
$$

Two cases:

### Case 1 — Constraint inactive

Then \(T_\Omega(x)=\mathbb{R}^2\) and:

$$
\nabla f(x)=0
$$

is necessary (unconstrained scenario).

### Case 2 — Constraint active

Feasible descent requires:

$$
\nabla f(x)^T d < 0, 
\quad \nabla c_1(x)^T d \ge 0. \tag{34}
$$

No feasible descent exists iff:

$$
\nabla f(x) = \lambda \nabla c_1(x),\quad \lambda \ge 0. \tag{35}
$$

Plus complementarity:

$$
\lambda\, c_1(x)=0. \tag{36}
$$

---

## 8. Two Inequality Constraints Example

Constraints:

$$
c_1(x)=2 - x_1^2 - x_2^2,\qquad c_2(x)=x_2.
$$

Feasible descent direction must satisfy:

$$
\nabla f(x)^T d < 0,\quad
\nabla c_1(x)^T d \ge 0,\quad 
\nabla c_2(x)^T d \ge 0. \tag{38}
$$

Define Lagrangian:

$$
L(x,\lambda) = f(x) - \lambda_1 c_1(x) - \lambda_2 c_2(x). \tag{39}
$$

Necessary condition:

$$
\nabla_x L(x,\lambda)=0,\quad \lambda_1,\lambda_2 \ge 0. \tag{40}
$$

Complementarity:

- \( \lambda_i = 0 \) if constraint inactive  
- \( \lambda_i c_i(x)=0 \) if constraint active

---

## 9. Linear Independence Constraint Qualification (LICQ)

To avoid pathological cases:

- At a feasible point \(x\), the gradients of **active constraints** must be **linearly independent**.

LICQ ensures:

$$
T_\Omega(x) = F(x),
$$

where \(F(x)\) = cone of linearized feasible directions.

In practice:

- Form matrix of active gradients  
- Check rank (e.g., via SVD)

---

## 10. KKT Conditions (First-Order Necessary Conditions)

Given LICQ holds, KKT for problem (27):

1. **Stationarity**  
   \( \nabla_x L(x,\lambda)=0 \)

2. **Primal feasibility**  
   \( c_i(x)=0,\ i\in E;\quad c_i(x)\le0,\ i\in I \)

3. **Dual feasibility**  
   \( \lambda_i \ge 0,\ i\in I \)

4. **Complementarity**  
   \( \lambda_i c_i(x)=0,\ i\in I \)

5. **Active constraints enforced**  
   Equality constraints always active.

KKT conditions generalize:

- Unconstrained stationary points  
- Equality constrained Lagrange multipliers  
- Inequality constrained multiplier signs

---

## 11. Example: Solving KKT System

For problem:

$$
\min x_1+x_2 \quad 
\text{s.t.}\ 
2 - x_1^2 - x_2^2 \ge 0,\ x_2 \ge 0,
$$

Lagrangian:

$$
L(x,\lambda)=x_1+x_2 - \lambda_1(2-x_1^2-x_2^2) - \lambda_2 x_2.
$$

Stationarity:

$$
\nabla_x L =
\begin{bmatrix}
1 + 2\lambda_1 x_1 \\
1 + 2\lambda_1 x_2 - \lambda_2
\end{bmatrix}
=0. \tag{42}
$$

Feasibility:

$$
2 - x_1^2 - x_2^2 \ge 0,\quad x_2 \ge 0,
$$

Complementarity:

$$
\lambda_1(2 - x_1^2 - x_2^2)=0,\quad
\lambda_2 x_2 =0. \tag{43}
$$

Solving yields:

$$
x^* = (-\sqrt{2},\ 0).
$$

This point satisfies LICQ → it is the global minimizer.

---

## 12. Quadratic Programming Example

Consider:

$$
\min\ \tfrac12 x^T Q x - b^T x \quad 
\text{s.t.}\ Cx - d \le 0. \tag{44}
$$

Lagrangian:

$$
L(x,\lambda)=\tfrac12 x^T Q x - b^T x - \lambda^T(d - Cx).
$$

Stationarity:

$$
Qx - b - C^T \lambda = 0. \tag{45}
$$

Thus:

$$
x = Q^{-1}(b + C^T \lambda).
$$

Complementarity:

$$
\lambda \circ (d - Cx) = 0 \quad (\text{elementwise}). \tag{46}
$$

All **\(2^m\)** patterns of active/inactive constraints may need checking.

---

## 13. Farkas’ Lemma

Let:

- \(B\) = gradients of active inequality constraints  
- \(C\) = gradients of equality constraints  

Define cone:

$$
K = \{ By + Cw \mid y \ge 0,\ w \in \mathbb{R}^p \}.
$$

Then for any \(g\):

- Either \(g \in K\),  
- Or there exists \(d\) such that:

  $$
  g^T d < 0,\quad B^T d \ge 0,\quad C^T d = 0. \tag{47}
  $$

Applying this with \(g=\nabla f(x^*)\) and LICQ → KKT conditions follow.

---

## 14. Classical Eigenvalue Example

Problem:

$$
\min_{x} x^T Q x \quad \text{s.t. } \|x\|=1. \tag{48}
$$

Lagrangian:

$$
L(x,\lambda)=x^T Q x - \lambda(\|x\|^2-1).
$$

Stationarity:

$$
Qx=\lambda x,
$$

→ **Eigenvalue problem**  
→ Solutions = eigenvectors, minimizer corresponds to smallest eigenvalue.

---

## 15. Norm-Constrained Quadratic Optimization

Problem:

$$
\min\ a + b^T x + \tfrac12 x^T Q x,\quad \|x\|\le4. \tag{50}
$$

Lagrangian:

$$
L(x,\lambda)=a + b^T x + \tfrac12 x^T Q x - \lambda(16 - \|x\|^2).
$$

Stationarity:

$$
(Q + 2\lambda I)x = -b.
$$

Two cases:

### Case 1 — Inactive constraint

\(\lambda = 0\):

$$
x = -Q^{-1} b.
$$

Accept only if \(\|x\|\le4\).

### Case 2 — Active constraint

Solve simultaneously:

$$
(Q + 2\lambda I)x = -b,\quad
\|x\|=4.
$$

Diagonalize \(Q = U \operatorname{diag}(s_1,s_2) U^T\).  
Let \(y = U^T x\), \(c = U^T b\). Then:

$$
y_i = -\frac{c_i}{s_i + 2\lambda}.
$$

Constraint becomes:

$$
\left(\frac{c_1}{s_1+2\lambda}\right)^2 +
\left(\frac{c_2}{s_2+2\lambda}\right)^2
= 16.
$$

Solve a quartic polynomial in \(\lambda\); accept positive roots.

Companion matrix trick:

Given monic:

$$
p(z)=z^m + a_{m-1}z^{m-1} + \cdots + a_1 z + a_0,
$$

roots = eigenvalues of:

$$
A=\begin{bmatrix}
0 & 0 & \cdots & -a_0 \\
1 & 0 & \cdots & -a_1 \\
0 & 1 & \cdots & -a_2 \\
\vdots & & \ddots & \vdots \\
0 & 0 & \cdots & -a_{m-1}
\end{bmatrix}.
$$

---

# End of Chapter 5  
*(Based on textbook pages 305–329)*

