# Chapter 3 — Line Search Methods for Unconstrained Optimization  
**Clean Markdown Conversion**

This chapter introduces line search methods, their convergence properties, Newton’s method connections, and quasi-Newton updates.

---

## 1. Setup of Line Search Methods

Line search methods iteratively improve the current iterate \(x_k\) by:

1. **Choosing a descent direction** \(p_k\)
2. **Finding a step length** \(\alpha_k > 0\) via:

   $$
   \min_{\alpha > 0} f(x_k + \alpha p_k). \tag{7}
   $$

The new iterate is:

$$
x_{k+1} = x_k + \alpha_k p_k. \tag{8}
$$

An exact minimizer for \(\alpha\) is rarely computed; an approximate \(\alpha_k\) suffices.

---

## 2. Choosing the Descent Direction \(p_k\)

Using Taylor expansion at \(x_k\):

Let \(\phi(\alpha) = f(x_k + \alpha p_k)\). Then:

$$
\phi'(0) = \nabla f(x_k)^T p_k. \tag{9}
$$

For descent, we require:

$$
\nabla f(x_k)^T p_k < 0.
$$

### Steepest Descent Direction

Choosing:

$$
p_k = -\nabla f(x_k)
$$

gives:

$$
f(x_k + \alpha p_k) 
= f(x_k) - \alpha \| \nabla f(x_k) \|^2 + O(\alpha^2). \tag{10}
$$

### General Descent Direction

A general family:

$$
p_k = - B_k^{-1} \nabla f(x_k), \tag{11}
$$

where \(B_k\) is **positive definite**, ensures descent.

---

## 3. Newton’s Method as a Line Search Method

To solve \(\nabla f(x) = 0\), Newton’s update is:

$$
x_{k+1} = x_k - (\nabla^2 f(x_k))^{-1} \nabla f(x_k),
$$

i.e., \(B_k = \nabla^2 f(x_k)\) and \(\alpha = 1\).

### Example: Newton’s Method

Minimize:

$$
(x_1 - 2)^4 + (x_1 - 2x_2)^2.
$$

Gradient:

$$
\nabla f(x)=
\begin{bmatrix}
4(x_1 - 2)^3 + 2(x_1 - 2x_2) \\
-4(x_1 - 2x_2)
\end{bmatrix},
$$

Hessian:

$$
\nabla^2 f(x)=
\begin{bmatrix}
12(x_1 - 2)^2 + 2 & -4 \\
-4 & 8
\end{bmatrix}.
$$

Stationary point: \(x_1 = 2,\ x_2 = 1\).

Newton converges quadratically **only if** the initial guess is close.

---

## 4. Cost of Newton’s Method

For large \(n\), forming the Hessian and solving:

$$
\nabla^2 f(x_k) p_k = -\nabla f(x_k) \tag{12}
$$

is expensive.

Thus, approximations to the Hessian are preferred → **quasi-Newton methods**.

---

## 5. Steepest Descent Analysis on Quadratics

Consider the quadratic model:

$$
f(x) = \frac{1}{2} x^T Q x - b^T x. \tag{6}
$$

Stationary point solves \(Qx = b\).

Steepest descent direction:

$$
p_k = -\nabla f(x_k) = -(Qx_k - b).
$$

Optimal step length (for quadratics):

$$
\alpha_k = \frac{\|\nabla f(x_k)\|^2}{\nabla f(x_k)^T Q \nabla f(x_k)}.
$$

Define the \(Q\)-norm:

$$
\|x\|_Q = (x^T Q x)^{1/2}. \tag{13}
$$

Using spectral analysis, steepest descent satisfies:

$$
\|x_{k+1} - x^*\|_Q 
\le \frac{\kappa(Q)-1}{\kappa(Q)+1}
\|x_k - x^*\|_Q,
$$

where:

$$
\kappa(Q) = \frac{\lambda_{\max}(Q)}{\lambda_{\min}(Q)}.
$$

Thus:

- Convergence is **linear**
- Convergence is **slow** if \(\kappa(Q)\) is large  
  (e.g., \(\kappa=800 \Rightarrow C=0.9975\)) → thousands of iterations.

Rule of thumb:

> If steepest descent stagnates, switch method or better initialize.

---

## 6. Quasi-Newton Methods

Goal: approximate \(\nabla^2 f(x_k)\) cheaply and achieve **superlinear convergence**.

A generic quasi-Newton update:

$$
B_{k+1} = B_k + F_k, \tag{15}
$$

where \(F_k\) is **low rank** (rank ≤ 2).

This allows efficient updates via **Sherman–Morrison** formulas:

If \(F_k = U_k V_k^T\), then

$$
B_{k+1}^{-1}
= B_k^{-1} - B_k^{-1} U_k (I + V_k^T B_k^{-1} U_k)^{-1} V_k^T B_k^{-1}.
$$

---

## 7. Secant Condition

Using Taylor approximation:

$$
\nabla f(x) \approx \nabla f(x_k)
+ \nabla^2 f(x_k)(x - x_k).
$$

At \(x_{k+1}\):

$$
\nabla^2 f(x_k)(x_{k+1}-x_k)
\approx
\nabla f(x_{k+1}) - \nabla f(x_k). \tag{16}
$$

Quasi-Newton methods impose:

$$
B_{k+1}(x_{k+1}-x_k)
= \nabla f(x_{k+1}) - \nabla f(x_k). \tag{17}
$$

Define:

- \(s_k = x_{k+1} - x_k\)
- \(y_k = \nabla f(x_{k+1}) - \nabla f(x_k)\)

---

## 8. SR1 Update (Symmetric Rank-1)

Assume:

$$
B_{k+1} = B_k + v_k v_k^T.
$$

From (17):

$$
B_k s_k + (v_k^T s_k) v_k = y_k. \tag{18}
$$

Thus:

$$
v_k = \theta (y_k - B_k s_k)
$$

for some scalar \(\theta\).

Final SR1 update:

$$
B_{k+1}
=
B_k
+
\frac{(y_k - B_k s_k)(y_k - B_k s_k)^T}
     {(y_k - B_k s_k)^T s_k}.
$$

The method **fails** if the denominator is zero or tiny; in that case, skip update.

---

## 9. Rank-2 Update (BFGS Mention)

If rank-2 updates are used, the optimal choice leads to the **BFGS method**, a standard quasi-Newton method with excellent performance.

---

## 10. Step-Length Selection

Given descent direction \(p_k\), define:

$$
\phi(\alpha) = f(x_k + \alpha p_k).
$$

Stationary points satisfy:

$$
\nabla f(x_k + \alpha p_k)^T p_k = 0. \tag{19}
$$

### Bisection Method for Step Length

Since:

- \(\phi'(0) = \nabla f(x_k)^T p_k < 0\)
- Find \(\hat{\alpha} > 0\) with \(\phi'(\hat{\alpha}) > 0\)

By continuity, a zero exists in \([0,\hat{\alpha}]\).

Iteratively bisect:

1. Let \(c = \hat{\alpha}/2\)
2. Compute \(\phi'(c)\)
3. Update interval accordingly
4. Repeat until interval is sufficiently small

This gives an approximate solution for \(\alpha_k\).

---

# End of Chapter 3
**Based on Chapter 3.3 and pp. 41–45 of the textbook.**

---
