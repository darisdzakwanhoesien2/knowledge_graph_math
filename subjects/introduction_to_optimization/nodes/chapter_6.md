# Chapter 6 — Trust Region Methods for Unconstrained Optimization  
**Clean Markdown Conversion**

Trust region methods solve unconstrained optimization problems by repeatedly solving *constrained* quadratic subproblems. Surprisingly, they can outperform line-search methods even though the original problem is unconstrained.

---

## 1. Motivation

Consider the unconstrained minimization problem (2.1):

$$
\min_{x \in \mathbb{R}^n} f(x).
$$

Trust region methods use **second-order Taylor models** of \(f\) and solve *restricted* minimization problems around the current point \(x_k\).

Second-degree Taylor expansion around \(x_k\):

$$
f(x_k + p)
= f_k + g_k^T p + \frac12 p^T \nabla^2 f(x_k + t p)p,\quad t\in(0,1),
$$

where:

- \( f_k = f(x_k) \)  
- \( g_k = \nabla f(x_k) \)

We approximate the Hessian by some matrix \(B_k\), giving the **quadratic model**:

$$
m_k(p) = f_k + g_k^T p + \frac12 p^T B_k p. \tag{51}
$$

For exact Hessian \(B_k = \nabla^2 f(x_k)\), the approximation error satisfies:

$$
|f(x_k + p) - m_k(p)| = O(\|p\|^3).
$$

---

## 2. Trust Region Subproblem

At iteration \(k\), the next iterate is obtained by solving:

$$
\min_{p \in \mathbb{R}^n} m_k(p)
\quad \text{s.t.} \quad \|p\| \le \Delta_k, \tag{52}
$$

where:

- \(p_k\) = proposed step  
- \(\Delta_k > 0\) = trust-region radius (controls how far the quadratic model is trusted)

### Comparison with line search
- Line search picks **direction + step size separately**  
- Trust region chooses them **simultaneously**  
- Uses the same information (gradient + Hessian/approximation)

---

## 3. Adjusting the Trust Region Radius

After solving the subproblem with some guessed radius \(\hat{\Delta}\), compute the **ratio of actual reduction to predicted reduction**:

$$
\rho_k
=
\frac{f(x_k) - f(x_k + p_k)}
     {m_k(0) - m_k(p_k)}. \tag{53}
$$

Interpretation:

- \(\rho_k \approx 1\): model is accurate → **accept** step, possibly enlarge \(\Delta_k\)
- \(\rho_k < 0\): model is poor → **reject** step, shrink \(\Delta_k\)
- Standard rules in Algorithm 4.1 (book p. 69)

If accepted:

$$
x_{k+1} = x_k + p_k.
$$

---

## 4. Using KKT to Solve the Trust Region Subproblem

The trust-region constraint is the single inequality:

$$
\|p\|^2 \le \Delta^2.
$$

Lagrangian:

$$
L(p,\lambda)
=
m(p) - \lambda(\Delta^2 - \|p\|^2).
$$

KKT conditions:

- Stationarity:

  $$
  \nabla_p L = g + Bp + 2\lambda p = 0,
  $$

- Dual feasibility: \( \lambda \ge 0 \)
- Primal feasibility: \( \Delta^2 - \|p\|^2 \ge 0 \)
- Complementarity:

  $$
  \lambda(\Delta^2 - \|p\|^2) = 0
  $$

### Case 1 — Constraint inactive (\(\lambda = 0\))

Solve:

$$
Bp = -g. \tag{55}
$$

Check if \( \|p\| \le \Delta \).  
If yes → accept as solution.

### Case 2 — Constraint active (\(\lambda > 0\))

Solve:

$$
(B + 2\lambda I)p = -g, \tag{54}
$$

together with:

$$
\|p\| = \Delta. \tag{56}
$$

This is an \((n+1)\)-equation system.  
Solvable with Newton’s method — but too expensive in practice.

---

## 5. Practical Approximation Strategy

Suppose solving \(Bp = -g\) yields a step outside the trust region:

$$
\|p\| > \Delta.
$$

We cannot afford solving (54)+(56) exactly, so we restrict \(p\) to a **2-dimensional Krylov subspace**:

$$
p \in \operatorname{span}\{ g,\ B^{-1}g \}. \tag{57}
$$

Compute an orthonormal basis:

$$
[q,\ \tilde{q}]
$$

and write:

$$
p = [q\ \ \tilde{q}] 
\begin{bmatrix}
\alpha \\ \beta
\end{bmatrix}. \tag{58}
$$

Then:

$$
\|p\|^2 = \alpha^2 + \beta^2.
$$

Solve reduced 2D problem:

$$
\min_{\alpha, \beta}
f_k
+ \hat{g}^T
\begin{bmatrix}
\alpha \\ \beta
\end{bmatrix}
+
\frac12
\begin{bmatrix}
\alpha \\ \beta
\end{bmatrix}^T
\hat{B}
\begin{bmatrix}
\alpha \\ \beta
\end{bmatrix}
\quad
\text{s.t. } \alpha^2 + \beta^2 \le \Delta_k,
$$

where:

- \( \hat{g}^T = g^T [q\;\tilde{q}] \)
- \( \hat{B} = [q\;\tilde{q}]^T B [q\;\tilde{q}] \)

Use the solution to form \(p\), perform ratio test (53), and adjust radius.

This is a **dimension-reduction strategy** that uses inexpensive quadratic solves.

---

## 6. Krylov Subspace Interpretation

The subspace:

$$
\operatorname{span}\{g,\ B^{-1}g\}
$$

is the first two vectors of the **Krylov sequence**:

$$
\{ g,\ B^{-1} g,\ B^{-2}g,\ \dots \}.
$$

Better approximations can be achieved by expanding to:

$$
\operatorname{span}\{g,\ B^{-1}g,\ \dots,\ B^{-j}g\}.
$$

This is computationally feasible because:

- We already factored \(B\)
- Applying \(B^{-1}\) repeatedly is cheap

---

## 7. Convergence (High-Level Note)

A mathematically rigorous convergence theory exists in:

> Nocedal & Wright, *Numerical Optimization*, Chapter 4.2.

The argument is technical and omitted in this course.  
Instructor’s remark: trust region methods often outperform line search in practice.

---

## 8. Transition to Next Chapter

The chapter concludes:

> Having KKT conditions available is essential for analyzing constrained optimization.  
> Next: **Second-order conditions for constrained optimization**.

---

# End of Chapter 6  
*(Based on textbook pp. 66–70 and the discussion around equation (4.17) on p. 76.)*
