# Chapter 2 — Fundamentals of Unconstrained Optimization  
**Clean Markdown Conversion**

This chapter continues from Newton's method and introduces the foundations of smooth unconstrained optimization.

---

## 1. Newton’s Method (Closing Notes from Previous Chapter)

Given an approximation \( x_k \), Taylor expansion gives:

$$
r(x) = r(x_k) + r'(x_k)(x - x_k) + O(|x - x_k|^2).
$$

Setting \( r(x) = 0 \):

$$
x = x_k - \frac{r(x_k)}{r'(x_k)} + \frac{O(|x - x_k|^2)}{r'(x_k)}. \tag{2}
$$

Newton's update drops the second-order term:

$$
x_{k+1} = x_k - \frac{r(x_k)}{r'(x_k)}. \tag{3}
$$

Subtracting (3) from (2) yields quadratic convergence:

$$
|x - x_{k+1}| \le C |x - x_k|^2.
$$

For \( n > 1 \):

$$
x_{k+1} = x_k - J(x_k)^{-1} r(x_k),
$$

where \( J(x_k) \) is the Jacobian.

---

# 2. Fundamentals of Unconstrained Optimization

Unconstrained optimization concerns:

$$
\min_{x \in \mathbb{R}^n} f(x),
$$

i.e., the feasible region is the entire space.

Maximization is equivalent to minimizing \( -f \).

---

## 2.1 Basic Concepts

### Neighborhood  
A neighborhood of \( x \in \mathbb{R}^n \):

$$
N_r(x) = \{ v \in \mathbb{R}^n \mid \|v - x\| < r \}. \tag{4}
$$

### Local vs Global Minimizers

- **Global minimizer**:  
  \( f(x^*) \le f(x) \) for all \( x \in \Omega \subseteq \mathbb{R}^n \).

- **Local minimizer**:  
  \( f(x^*) \le f(x) \) for all \( x \) in a neighborhood of \( x^* \).

- **Strict local minimizer**:  
  \( f(x^*) < f(x) \) for all \( x \ne x^* \) near \( x^* \).

Local minima may not be global (see Fig. 2.2 in the book).

### Convex Case  
If **f is convex**, any local minimizer is global → the problem is “easy.”

---

## 2.2 Taylor’s Theorem and Minimizers

Theorem 2.1 (book p. 14) provides several Taylor expansions:

- Directional slope  
- Integral representation  
- Quadratic approximation

These are foundational for deriving necessary and sufficient conditions.

---

## 2.3 Geometry: Hyperplanes

Fix a vector \( v \in \mathbb{R}^n \). The hyperplane:

$$
H_v = \{ x \in \mathbb{R}^n \mid v^T x = 0 \} \tag{5}
$$

If \( v = \nabla f(x^*) \):

- On the **positive side**: \( f \) increases  
- On the **negative side**: \( f \) decreases  

---

## 2.4 First-Order Necessary Condition (Stationary Points)

Theorem 2.2 (p. 15):

If \( x^* \) is a local minimizer and \( f \) is smooth:

$$
\nabla f(x^*) = 0.
$$

Such points are **stationary** or **critical** points.

---

## 2.5 Second-Order Conditions

Matrix reminder:

- \( A \) positive semidefinite ⇔ all eigenvalues ≥ 0  
- \( A \) positive definite ⇔ all eigenvalues > 0  

### Second-Order Necessary Condition

If \( x^* \) is a local minimizer and \( \nabla f(x^*) = 0 \):

$$
\nabla^2 f(x^*) \succeq 0.
$$

### Second-Order Sufficient Condition

If:

- \( \nabla f(x^*) = 0 \)
- \( \nabla^2 f(x^*) \succ 0 \)

then \( x^* \) is a **strict local minimizer**.

Important nuance:

A point with \( \nabla f = 0 \) and semidefinite Hessian **may or may not** be a minimum.

Example:  
\( f(x) = x^4 \) has a minimizer at \( x = 0 \) but Hessian = 0.

---

## 2.6 Quadratic Functions

Consider:

$$
f(x) = \frac{1}{2} x^T Q x - b^T x. \tag{6}
$$

Stationary point solves:

$$
Qx = b.
$$

If \( Q \succ 0 \), this is a global minimizer.

Quadratics are fundamental because:

- simple  
- analytically solvable  
- used as approximations (Newton, trust region, etc.)

---

## 2.7 Example: Stationary Points

Given:

$$
f(x) = x_1(x_1^2 - 1) + x_2^2,
$$

gradient:

$$
\nabla f(x) = (3x_1^2 - 1,\; 2x_2).
$$

Solve \( \nabla f = 0 \):

- \( x_1 = \pm \frac{1}{\sqrt{3}} \)
- \( x_2 = 0 \)

Hessian:

$$
\nabla^2 f(x) =
\begin{bmatrix}
6x_1 & 0 \\
0 & 2
\end{bmatrix}.
$$

Thus:

- \( ( +\frac{1}{\sqrt{3}}, 0 ) \) → **strict local minimum**  
- \( ( -\frac{1}{\sqrt{3}}, 0 ) \) → **saddle point**

---

## 2.8 Convexity and Simplification

Theorem 2.5 (p. 16):

If **f is convex and smooth**, then:

- The stationary point is the **global minimizer**.
- Solving \( \nabla f(x) = 0 \) is the entire task.

---

## 2.9 What Comes Next

Two families of methods for unconstrained optimization:

- **Line search methods**  
- **Trust region methods**

Intro: pp. 18–26 in the book.

---

# 3. Line Search Methods for Unconstrained Optimization

In line search, the update is:

1. Choose a **descent direction** \( p_k \).
2. Choose step length \( \alpha > 0 \) that solves:

   $$
   \min_{\alpha > 0} f(x_k + \alpha p_k). \tag{7}
   $$

Notes:

- Descent direction ensures \( f \) decreases.
- Step length selection is a **1D optimization problem**.
- Exact solution may not be easy; practical methods use approximations.

---
