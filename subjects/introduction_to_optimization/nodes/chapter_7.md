# Chapter 7 — Second-Order Conditions of Constrained Optimization  
**Clean Markdown Conversion**

Second-order conditions extend the KKT framework to determine whether a KKT point is a **local minimizer** by analyzing curvature along the feasible directions. This chapter builds upon tangent cones, active sets, and the Lagrangian.

---

## 1. From KKT to Second-Order Analysis

The KKT conditions ensure that the **first-order necessary condition** holds:

- No feasible descent direction exists  
  \( \Rightarrow \) corresponds to Theorem 12.3.

However, KKT alone does **not** guarantee that the point is a local minimizer.  
Just like unconstrained optimization needs the Hessian test, constrained optimization needs **second-order conditions**.

After identifying a point \(x^*\) and its Lagrange multipliers \(\lambda^*\), the question is:

> Is \(x^*\) a local minimizer?

To answer this, we must examine the behaviour of **second derivatives along feasible directions**.

---

## 2. Critical Directions and the Critical Cone

Suppose:

- \(x^*\) satisfies KKT,  
- with multipliers \(\lambda^* = (\hat{\lambda}, \tilde{\lambda})\),  
- \(\hat{\lambda}_i \ge 0\) for inequality constraints.

Let:

- \(B\) = gradients of active *inequality* constraints  
- \(C\) = gradients of *equality* constraints  

For a feasible direction \(w\):

- \(B^T w \ge 0\)  
- \(C^T w = 0\)

At a KKT point, using stationarity:

$$
\nabla f(x^*) = B\hat{\lambda} + C\tilde{\lambda}.
$$

Then:

$$
0 = \nabla f(x^*)^T w = \hat{\lambda}^T (B^T w).
$$

Thus, whenever \(\hat{\lambda}_i > 0\), the corresponding component of \(B^T w\) must be zero.

### Critical Cone

The **critical cone** \(C(x^*, \lambda^*)\) consists of directions where:

- Constraints with positive multipliers behave like equalities.
- The first-order directional derivative is zero.

These are the only directions where second-order curvature determines minimizers.

---

## 3. Example 12.7 (Book p. 331)

Problem:

$$
\min x_1 
\quad \text{s.t.} \quad 
c_1(x) = x_2 \ge 0,
\quad
c_2(x) = 1 - (x_1 - 1)^2 - x_2^2 \ge 0. \tag{59}
$$

KKT solutions: \((0,0)\) and \((2,0)\).

At \((0,0)\):

- \(\lambda_2^* = \tfrac12\), \(\lambda_1^* = 0\)
- active constraints: \(c_1\) and \(c_2\)

Critical cone:

- From \(c_2\): \( \nabla c_2(0,0) = (2,0) \Rightarrow w_1 = 0 \)
- From \(c_1\): requirement \( (0,1)^T w \ge 0 \Rightarrow w_2 \ge 0 \)

Thus:

$$
C((0,0),\lambda^*) = \{ (0, w_2) \mid w_2 \ge 0 \}.
$$

---

## 4. Second-Order Behaviour via the Lagrangian

For directions in the critical cone, the behaviour of \(f\) matches that of the **Lagrangian**:

$$
L(x, \lambda^*) = f(x) - \sum_i \lambda^*_i c_i(x).
$$

Why?

- Active constraints behave like equalities.
- Inactive constraints play no role.
- Constraints with positive multipliers remain at equality along feasible directions.

Thus, instead of studying \(f\) along complicated manifolds, we study:

$$
w^T \nabla^2_{xx} L(x^*, \lambda^*) w.
$$

This is the **second variation** restricted to the critical cone.

---

## 5. Two-Dimensional Illustration

Let \(f:\mathbb{R}^2 \to \mathbb{R}\) and one active constraint:

$$
c_1(x_1, x_2) = 0, \quad \lambda_1^* \ne 0.
$$

Solve the constraint locally:

- Assume we can write \(x_2 = g(x_1)\) near \(x^*\)
- On the constraint manifold, define:

  $$
  F(x_1) = f(x_1, g(x_1)).
  $$

Using derivatives:

$$
F'(x_1) 
= f_{x_1} + f_{x_2} g'(x_1),
$$

$$
F''(x_1)
=
\begin{bmatrix}
1 \\ g'(x_1)
\end{bmatrix}^T
\nabla^2 f
\begin{bmatrix}
1 \\ g'(x_1)
\end{bmatrix}
+
f_{x_2} g''(x_1). \tag{60}
$$

Do the same for the constraint:

$$
C_1(x_1) = 0,
$$

and differentiate twice to obtain:

$$
C_1''(x_1) = 0. \tag{61}
$$

Using the KKT relation:

$$
f_{x_2}(x^*) = \lambda_1^* c_{1,x_2}(x^*),
$$

Subtract (61) multiplied by \(\lambda_1^*\) from (60):

$$
F''(x_1)
=
\begin{bmatrix}
1 \\ g'(x_1)
\end{bmatrix}^T
\nabla^2_{xx} L(x^*,\lambda^*)
\begin{bmatrix}
1 \\ g'(x_1)
\end{bmatrix}. \tag{62}
$$

Thus:

- \(F''(x_1) \ge 0\): **necessary** for minimizer  
- \(F''(x_1) > 0\): **sufficient**

This generalizes to higher dimensions via the critical cone.

---

## 6. Higher-Dimensional Second-Order Conditions

Let the Hessian of the Lagrangian be:

$$
\nabla^2_{xx} L(x^*, \lambda^*).
$$

### **Second-Order Necessary Condition (SONC)**

If \(x^*\) is a local minimizer:

$$
w^T \nabla^2_{xx} L(x^*, \lambda^*) w \ge 0
\quad \forall w \in C(x^*, \lambda^*). 
$$

### **Second-Order Sufficient Condition (SOSC)**

If:

$$
w^T \nabla^2_{xx} L(x^*, \lambda^*) w > 0
\quad \forall w \in C(x^*, \lambda^*),\ w \ne 0,
$$

then \(x^*\) is a **strict local minimizer**.

If the Hessian is positive definite on all of \(\mathbb{R}^n\), the SOSC holds automatically.

---

## 7. How to Compute the Critical Cone in Practice

If the active constraints with **positive multipliers** are:

$$
c_{j_1}, c_{j_2}, \dots, c_{j_\ell},
$$

collect their gradients into matrix \(A \in \mathbb{R}^{n \times \ell}\).

Then:

- The **critical cone** is the **null space** of \(A^T\):

  $$
  C(x^*,\lambda^*) = \{ w \mid A^T w = 0,\ w \ne 0 \}.
  $$

This reduces the second-order test to checking positive (semi)definiteness on this subspace.

---

## 8. Simple Cases

### Case A — Linear Constraints

If constraints are linear:

- \(c_j(x) = c_j^T x + b_j\)
- Their Hessians vanish
- The Hessian of the Lagrangian reduces to the Hessian of the objective:

$$
\nabla^2_{xx} L(x^*,\lambda^*) = \nabla^2 f(x^*).
$$

If \(\nabla^2 f(x^*)\) is positive definite, \(x^*\) is a strict local minimizer.

---

### Case B — Linear Objective

If \(f\) is linear:

- \(\nabla^2 f(x) = 0\)

Consider example (29):

$$
L(x,\lambda) = x_1 + x_2 - \lambda(2 - x_1^2 - x_2^2).
$$

KKT solutions:

- \((-1,-1)\) with \(\lambda = 1/2\)  
- \((1,1)\) with \(\lambda = -1/2\)

Hessian of the Lagrangian:

$$
\nabla^2_{xx}L = 
\begin{bmatrix}
2\lambda & 0 \\
0 & 2\lambda
\end{bmatrix}.
$$

- Negative definite for \(\lambda = -1/2\) → discard \((1,1)\)  
- Positive definite for \(\lambda = 1/2\) → \((-1,-1)\) is a (global) minimizer

---

### Case C — Eigenvalue Problem Revisited

Eigenvalue problem:

$$
\min_{x} x^T Q x \quad \text{s.t. } \|x\| = 1. \tag{48}
$$

KKT gives:

$$
Qx = \lambda x.
$$

Lagrangian:

$$
L(x,\lambda) = x^T Q x - \lambda(\|x\|^2 - 1).
$$

Second-order condition:

$$
\nabla^2_{xx}L = 2(Q - \lambda I).
$$

Critical cone = orthogonal complement of eigenvector \(x^*\):

$$
C(x^*,\lambda^*) = \{ w \mid x^{*T} w = 0 \}.
$$

Evaluate:

$$
w^T (Q - \lambda I) w. \tag{63}
$$

Interpretation:

- If \(\lambda\) is **not** the smallest eigenvalue → expression becomes negative → discard  
- If \(\lambda\) is the smallest eigenvalue and eigenvalue has multiplicity 1 → SOSC holds → \(x^*\) is a strict local minimizer  
- If multiplicity > 1 → semidefinite → still a candidate

---

# End of Chapter 7  
*(Based on textbook pp. 330–336.)*
