# Chapter 4 — Nonlinear Least Squares  
**Clean Markdown Conversion**

Nonlinear least squares problems arise when one wants to solve systems of nonlinear equations approximately, by minimizing the sum of squared residuals. This chapter covers the formulation, linear case, nonlinear extensions, Jacobians, Gauss–Newton method, and connections to trust-region approaches.

---

# 1. From Equation Solving to Optimization

Given a nonlinear system:

$$
r_j(x) = 0, \qquad j = 1, \ldots, m,
$$

it may be impossible to solve it exactly. Instead, define:

$$
f(x) = \frac12 \sum_{j=1}^m r_j(x)^2. \tag{21}
$$

Minimizing \(f(x)\):

- Converts root-finding into an optimization problem.
- If the global minimizer satisfies \(f(x^*) = 0\), then all equations are exactly solved.

---

# 2. Linear Regression as the Most Important Example

We have measurements \((t_j, y_j)\) and want to fit:

$$
y(t) = x_1 + x_2 t.
$$

Residuals:

$$
r_j(x) = x_1 + x_2 t_j - y_j, \qquad j = 1,\ldots,m.
$$

This is a **linear least squares problem**, where:

$$
f(x) = \frac12 \|Jx - y\|^2 = \frac12 (Jx - y)^T(Jx - y),
$$

with \(J \in \mathbb{R}^{m \times n}\).

### Critical point (normal equations)

Taking gradient:

$$
\nabla f(x) = J^T(Jx - y) = 0,
$$

giving the **normal equations**:

$$
J^T J x = J^T y. \tag{22}
$$

### More stable solution via QR factorization

Use:

$$
J = QR,
$$

so that:

$$
Rx = Q^T y,
$$

avoiding forming \(J^T J\) explicitly, preventing numerical instabilities.

---

# 3. General Nonlinear Least Squares Structure

Define vector of residuals:

$$
r(x) = (r_1(x), \ldots, r_m(x))^T, \qquad r : \mathbb{R}^n \to \mathbb{R}^m.
$$

Jacobian:

$$
J(x)
=
\begin{bmatrix}
\nabla r_1(x)^T \\
\nabla r_2(x)^T \\
\vdots \\
\nabla r_m(x)^T
\end{bmatrix}.
$$

### Gradient

Using chain rule:

$$
\nabla f(x) = J(x)^T r(x). \tag{23}
$$

### Hessian

$$
\nabla^2 f(x)
=
J(x)^T J(x)
+
\sum_{j=1}^m r_j(x)\, \nabla^2 r_j(x). \tag{24}
$$

---

# 4. Linear vs Nonlinear Cases

### Linear least squares

- \(r(x) = Jx - y\)
- \(\nabla^2 r_j(x) = 0\)
- Thus:

  $$
  \nabla^2 f(x) = J^T J.
  $$

### Nonlinear case

- Hessian includes extra second-derivative terms
- Provides motivation for **Gauss–Newton** as a quasi-Newton simplification

---

# 5. Gauss–Newton Method

Newton’s method for minimizing \(f\):

$$
\nabla^2 f(x_k)\, p_k = -\nabla f(x_k)
= -J(x_k)^T r(x_k).
$$

But computing \(\nabla^2 r_j(x)\) is expensive.  
Gauss–Newton **drops the second-order terms** in (24), giving the approximation:

$$
\nabla^2 f(x_k) \approx J(x_k)^T J(x_k). \tag{26}
$$

Thus solve:

$$
J(x_k)^T J(x_k) p_k
= -J(x_k)^T r(x_k). \tag{25}
$$

### Properties

- Requires only Jacobian \(J(x_k)\)
- Computationally cheaper than Newton
- Produces a **descent direction**:

  $$
  p_k^T \nabla f(x_k)
  = -\| J(x_k) p_k \|^2 \le 0
  $$

---

# 6. Why Dropping the Second-Order Terms Makes Sense

From Hessian expression:

$$
\nabla^2 f(x)
= J^T J + \sum_{j=1}^m r_j(x)\, \nabla^2 r_j(x),
$$

the omitted term is:

- weighted by \(r_j(x)\)
- small near a solution (residuals get small)
- therefore typically negligible in practice

This supports using Gauss–Newton as a quasi-Newton method.

---

# 7. Computational Advantages

When evaluating \(\nabla f(x)\), we already compute:

$$
J(x)^T r(x).
$$

Having \(J(x)\) makes it easy to compute:

$$
J(x)^T J(x),
$$

without additional evaluations of second derivatives.

Thus Gauss–Newton has:

- low computational cost
- simpler implementation
- strong performance on least-squares problems

---

# 8. Levenberg–Marquardt Method (Brief Mention)

The **Levenberg–Marquardt** method is another algorithm for nonlinear least squares.

It belongs to the class of **trust-region methods**, which are covered after the constrained optimization chapters.

---

# End of Chapter 4  
*(Based on textbook pp. 245–254.)*
