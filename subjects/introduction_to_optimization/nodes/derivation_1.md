# Derivations — Chapters 1–9 (Comprehensive)
Clean Markdown Conversion with LaTeX Equations

---

# Chapter 1 — Taylor Expansion, Gradients, Newton (1D & Multivariate)

## 1. First-Order Taylor Expansion (1D)
For \(f:\mathbb{R} \to \mathbb{R}\):
$$
f(x) = f(x_0) + f'(x_0)(x - x_0) + \frac12 f''(\xi)(x - x_0)^2.
$$

## 2. Gradient Orthogonality to Level Sets
Let \(f:\mathbb{R}^n \to \mathbb{R}\) and \(\gamma(t)\) a curve on a level set.
$$
0 = \frac{d}{dt} f(\gamma(t))\Big|_{t=0}
  = \nabla f(x)^T \gamma'(0)
$$
Thus, \(\nabla f(x)\) is orthogonal to the tangent plane.

## 3. Newton’s Method (1D)
Equation:
$$
r(x)=0.
$$
Taylor expansion:
$$
r(x) \approx r(x_k) + r'(x_k)(x - x_k).
$$
Solve for zero:
$$
x_{k+1} = x_k - \frac{r(x_k)}{r'(x_k)}.
$$

### Quadratic Convergence
Under smoothness and \(r'(x^*)\neq 0\):
$$
|x_{k+1}-x^*| \le C |x_k - x^*|^2.
$$

## 4. Newton’s Method (Multivariate)
Solve \(\nabla f(x)=0\):
$$
x_{k+1} = x_k - \left( \nabla^2 f(x_k) \right)^{-1} \nabla f(x_k).
$$

---

# Chapter 2 — First/Second Order Conditions (Unconstrained)

## 1. First-Order Necessary Condition
For local minimizer \(x^*\):
$$
\nabla f(x^*) = 0.
$$

## 2. Second-Order Necessary Condition
If \(f\in C^2\) and \(x^*\) is a local minimizer:
$$
\nabla^2 f(x^*) \succeq 0.
$$

## 3. Second-Order Sufficient Condition
If:
$$
\nabla f(x^*) = 0, \qquad \nabla^2 f(x^*) \succ 0,
$$
then \(x^*\) is a strict local minimizer.

## 4. Quadratic Functions
For:
$$
f(x) = \frac12 x^T Qx - b^T x
$$
gradient:
$$
\nabla f = Qx - b.
$$
Stationary point:
$$
Qx = b.
$$

---

# Chapter 3 — Line Search, Steepest Descent, Quasi-Newton

## 1. Descent Direction Condition
Direction \(p\) is descent if:
$$
\nabla f(x)^T p < 0.
$$

## 2. Steepest Descent
Direction:
$$
p_k = -\nabla f(x_k).
$$

## 3. Exact Line Search for Quadratics
Given \(p_k=-\nabla f(x_k)\):
$$
\alpha_k = \frac{\|\nabla f(x_k)\|^2}{\nabla f(x_k)^T Q \nabla f(x_k)}.
$$

## 4. Linear Convergence Rate (Quadratic Case)
Condition number \(\kappa=\lambda_{\max}/\lambda_{\min}\):
$$
\|x_{k+1}-x^*\|_Q
\le
\frac{\kappa-1}{\kappa+1}
\|x_k-x^*\|_Q.
$$

---

# Chapter 3 — Secant Condition, SR1, BFGS

## 1. Secant Condition
$$
B_{k+1} s_k = y_k,
$$
where:
- \(s_k = x_{k+1}-x_k\)
- \(y_k = \nabla f(x_{k+1}) - \nabla f(x_k)\)

## 2. SR1 Update
$$
B_{k+1} = 
B_k +
\frac{(y_k - B_k s_k)(y_k - B_k s_k)^T}
     {(y_k - B_k s_k)^T s_k}.
$$

## 3. BFGS Inverse Update
$$
H_{k+1}
=
(I - \rho_k s_k y_k^T) H_k (I - \rho_k y_k s_k^T)
+ \rho_k s_k s_k^T,
$$
where
$$
\rho_k = \frac{1}{y_k^T s_k}.
$$

---

# Chapter 4 — Nonlinear Least Squares & Gauss–Newton

## 1. Objective
$$
f(x) = \frac12 \|r(x)\|^2.
$$

## 2. Gradient
$$
\nabla f(x) = J(x)^T r(x).
$$

## 3. Hessian (Exact)
$$
\nabla^2 f(x)
=
J(x)^T J(x)
+
\sum_{j=1}^m r_j(x)\,\nabla^2 r_j(x).
$$

## 4. Gauss–Newton Approximation
Drop second term:
$$
\nabla^2 f(x) \approx J(x)^T J(x).
$$
Gauss–Newton direction:
$$
J(x_k)^T J(x_k) p_k = - J(x_k)^T r(x_k).
$$

---

# Chapter 5 — Constrained Optimization, KKT

## 1. Lagrangian
For:
$$
\min f(x)
\quad s.t.\quad c_i(x)=0,\ c_i(x)\le 0,
$$
Lagrangian:
$$
L(x,\lambda,\mu)
=
f(x) - \sum_{i\in E} \mu_i c_i(x)
  - \sum_{i\in I} \lambda_i c_i(x).
$$

## 2. KKT Conditions
- **Stationarity**  
  $$
  \nabla_x L(x^*,\lambda^*,\mu^*)=0
  $$
- **Primal feasibility**  
  $$
  c_i(x^*) = 0, \quad c_i(x^*) \le 0
  $$
- **Dual feasibility**  
  $$
  \lambda_i^* \ge 0
  $$
- **Complementarity**  
  $$
  \lambda_i^* c_i(x^*) = 0
  $$

---

# Chapter 6 — Trust Region Subproblem & KKT

## 1. Trust Region Model
$$
m(p) = f_k + g_k^T p + \frac12 p^T B_k p.
$$
Constraint:
$$
\|p\| \le \Delta_k.
$$

## 2. Lagrangian
$$
\mathcal{L}(p,\lambda) = g^T p + \frac12 p^T Bp - \lambda(\Delta^2 - \|p\|^2).
$$

## 3. Stationarity
$$
g + Bp + 2\lambda p = 0.
$$

## 4. Complementarity
$$
\lambda(\Delta^2 - \|p\|^2)=0.
$$

---

# Chapter 7 — Second-Order Conditions (Constrained)

## 1. Critical Cone
Let \(A\) be matrix of gradients of active constraints with positive multipliers.  
Critical cone:
$$
C(x^*,\lambda^*) = \{ w \mid A^T w = 0 \}.
$$

## 2. Second-Order Necessary Condition (SONC)
For all \(w\in C(x^*,\lambda^*)\):
$$
w^T \nabla^2_{xx} L(x^*,\lambda^*) w \ge 0.
$$

## 3. Second-Order Sufficient Condition (SOSC)
For all nonzero \(w\in C(x^*,\lambda^*)\):
$$
w^T \nabla^2_{xx} L(x^*,\lambda^*) w > 0.
$$

---

# Chapter 8 — Linear Programming, Simplex, Dual

## 1. Reduced Costs
Partition \(A=[B\ N]\), \(x=(x_B,x_N)\).  
Reduced costs:
$$
s = c_N - N^T B^{-T} c_B.
$$

## 2. Ratio Test (Leaving Variable)
For entering column \(u\):
$$
d = B^{-1}u,
$$
$$
\theta = \min_{i: d_i>0} \frac{(B^{-1}b)_i}{d_i}.
$$

## 3. Simplex Optimality Condition
If:
$$
s \ge 0,
$$
then BFS is optimal.

---

# Chapter 9 — Duality & Dual Derivations

## 1. Dual Function
$$
q(\lambda) = \inf_x L(x,\lambda).
$$

## 2. Weak Duality
For any feasible \(x\) and any \(\lambda\ge0\):
$$
q(\lambda) \le f(x).
$$

## 3. LP Dual (Explicit)
Primal:
$$
\min c^T x \quad s.t.\quad Ax - b \le 0.
$$
Dual becomes:
$$
\max_{\lambda\ge0} \lambda^T b
\quad s.t.\quad A^T \lambda = c.
$$

## 4. Quadratic Programming Dual
Primal:
$$
\min \frac12 x^T Qx - b^T x \quad s.t.\ Cx \le d.
$$
Stationarity:
$$
Qx - b + C^T \lambda = 0 \quad\Rightarrow\quad x = Q^{-1}(b - C^T\lambda).
$$
Dual:
$$
q(\lambda)
= -\frac12 (b - C^T\lambda)^T Q^{-1}(b - C^T\lambda)
  - d^T \lambda.
$$

---

# End of Comprehensive Derivations
