# Complete Derivations for Key Optimization Concepts

---

# 1. Secant Condition — Full Derivation

We want to approximate the Hessian \( \nabla^2 f(x) \) using updates of the form:
\[
B_{k+1} \approx \nabla^2 f(x_{k+1}).
\]

From Taylor expansion of the gradient:
\[
\nabla f(x_{k+1}) \approx \nabla f(x_k) + B_{k+1}(x_{k+1} - x_k).
\]

Define:
\[
s_k = x_{k+1} - x_k,
\qquad
y_k = \nabla f(x_{k+1}) - \nabla f(x_k).
\]

Substitute into the approximation:
\[
y_k \approx B_{k+1} s_k.
\]

This is the **secant condition**:
\[
\boxed{ B_{k+1} s_k = y_k }.
\]

This condition must be satisfied by any quasi-Newton update.

---

# 2. SR1 Update — Full Derivation

We want a rank-1 correction:
\[
B_{k+1} = B_k + u u^T.
\]

Impose the secant condition:
\[
(B_k + u u^T)s_k = y_k.
\]

Expand:
\[
B_k s_k + u(u^T s_k) = y_k.
\]

Rearrange:
\[
u(u^T s_k) = y_k - B_k s_k.
\]

Let:
\[
r_k = y_k - B_k s_k.
\]

We must solve:
\[
u(u^T s_k) = r_k.
\]

Choose:
\[
u = \frac{r_k}{\sqrt{r_k^T s_k}}.
\]
so that:
\[
u^T s_k = \sqrt{r_k^T s_k}.
\]

Then:
\[
u(u^T s_k) = \frac{r_k}{\sqrt{r_k^T s_k}} \sqrt{r_k^T s_k} = r_k.
\]

Therefore:
\[
\boxed{
B_{k+1} = B_k +
\frac{(y_k - B_k s_k)(y_k - B_k s_k)^T}{(y_k - B_k s_k)^T s_k}.
}
\]

This is the **SR1 update**.

---

# 3. BFGS Inverse Update — Full Derivation

We approximate the inverse Hessian \(H_k \approx B_k^{-1}\).

We require the inverse secant condition:
\[
H_{k+1} y_k = s_k.
\]

BFGS chooses a rank-2 symmetric update:
\[
H_{k+1} = H_k + U + V.
\]

The BFGS solution that satisfies:

- secant condition  
- symmetry  
- positive definiteness  

is:
\[
\boxed{
H_{k+1} =
(I - \rho_k s_k y_k^T) H_k (I - \rho_k y_k s_k^T) + \rho_k s_k s_k^T
}
\]
where:
\[
\rho_k = \frac{1}{y_k^T s_k}.
\]

This is derived by solving a constrained minimum-change optimization problem in matrix space.

---

# 4. Descent Direction Condition — Full Derivation

A direction \(p\) is descent if:
\[
\frac{d}{d\alpha} f(x + \alpha p)\big|_{\alpha=0} < 0.
\]

Compute:
\[
\frac{d}{d\alpha} f(x + \alpha p)
= \nabla f(x + \alpha p)^T p.
\]

At \(\alpha = 0\):
\[
\boxed{
\nabla f(x)^T p < 0.
}
\]

This is the standard descent condition.

---

# 5. Steepest Descent Direction — Full Derivation

We want the direction \(p\) of unit length that decreases the objective fastest.

Solve:
\[
\min_{\|p\|=1} \nabla f(x)^T p.
\]

By Cauchy-Schwarz:
\[
\nabla f(x)^T p \ge -\|\nabla f(x)\|.
\]

Equality achieved when:
\[
p = -\frac{\nabla f(x)}{\|\nabla f(x)\|}.
\]

Thus the steepest descent direction is:
\[
\boxed{
p_k = -\nabla f(x_k).
}
\]

---

# 6. Exact Line Search for Quadratics — Full Derivation

Given a quadratic:
\[
f(x) = \frac12 x^T Q x - b^T x,
\qquad Q = Q^T \succ 0.
\]

At iterate \(x_k\), direction \(p_k = -\nabla f(x_k)\), we solve:
\[
\min_{\alpha \ge 0} f(x_k + \alpha p_k).
\]

Define:
\[
\phi(\alpha) = f(x_k + \alpha p_k).
\]

Expand:
\[
\phi(\alpha)
= \frac12 (x_k + \alpha p_k)^T Q (x_k + \alpha p_k)
- b^T(x_k + \alpha p_k).
\]

Expand terms fully:
\[
\phi(\alpha)
= \frac12 x_k^T Q x_k
+ \alpha x_k^T Q p_k
+ \frac12 \alpha^2 p_k^T Q p_k
- b^T x_k
- \alpha b^T p_k.
\]

Use \(Qx_k - b = \nabla f(x_k)\):
\[
x_k^T Q p_k - b^T p_k = \nabla f(x_k)^T p_k.
\]

Thus:
\[
\phi(\alpha)
= f(x_k) + \alpha \nabla f(x_k)^T p_k + \frac12 \alpha^2 p_k^T Q p_k.
\]

Differentiate:
\[
\phi'(\alpha)
= \nabla f(x_k)^T p_k + \alpha p_k^T Q p_k.
\]

Set to zero:
\[
\alpha_k
=
- \frac{\nabla f(x_k)^T p_k}{p_k^T Q p_k}.
\]

But steepest descent uses:
\[
p_k = -\nabla f(x_k).
\]

Thus:
\[
\boxed{
\alpha_k
= \frac{\|\nabla f(x_k)\|^2}{\nabla f(x_k)^T Q \nabla f(x_k)}.
}
\]

---

# 7. Quadratic Functions — Gradient and Stationarity

Given:
\[
f(x) = \frac12 x^T Q x - b^T x.
\]

Differentiate:

### Gradient
\[
\nabla f(x) = Qx - b.
\]

### Stationary point
Solve:
\[
Qx = b.
\]

If \(Q \succ 0\), this solution is the unique global minimizer.

---

# 8. Exact Minimization Along a Ray — Full Step-by-Step Derivation

Let:
\[
f(x) = \frac12 x^T Q x - b^T x,
\qquad Q = Q^T \succ 0.
\]

Search along a ray:
\[
x(\alpha) = x_k + \alpha p_k.
\]

Define:
\[
\phi(\alpha) = f(x_k + \alpha p_k).
\]

Expand fully:

\[
\phi(\alpha)
= \frac12 (x_k + \alpha p_k)^T Q (x_k + \alpha p_k)
- b^T (x_k + \alpha p_k)
\]

\[
= \frac12 x_k^T Q x_k
+ \alpha x_k^T Q p_k
+ \frac12 \alpha^2 p_k^T Q p_k
- b^T x_k
- \alpha b^T p_k.
\]

Group terms:

\[
\phi(\alpha)
= f(x_k)
+ \alpha (\underbrace{x_k^T Q p_k - b^T p_k}_{=\nabla f(x_k)^T p_k})
+ \frac12 \alpha^2 p_k^T Q p_k.
\]

Thus:
\[
\phi(\alpha)
= f(x_k) + \alpha \nabla f(x_k)^T p_k + \frac12 \alpha^2 p_k^T Q p_k.
\]

Derivative:
\[
\phi'(\alpha)
= \nabla f(x_k)^T p_k + \alpha p_k^T Q p_k.
\]

Set to zero:
\[
\alpha_k = -\frac{\nabla f(x_k)^T p_k}{p_k^T Q p_k}.
\]

For steepest descent \(p_k = -\nabla f(x_k)\):
\[
\boxed{
\alpha_k = \frac{\|\nabla f(x_k)\|^2}{\nabla f(x_k)^T Q \nabla f(x_k)}.
}
\]

This fully matches the derivation shown in your UI screenshots.

---

# End of Complete Derivation File
