# Chapter 1 — Introduction to Optimization  
**Lecture Notes (Clean Markdown Conversion)**

## Overview
This course is about optimization. We follow book **[3]**, which contains extensive background material (over 600 pages).  
Because this is a seven-week course, only selected parts are covered.  
These notes assume you have access to the book.

Useful additional resource: **NEOS Optimization Guide**  
https://neos-guide.org/  
Recommended starting sections: *Case Studies*, *Optimization*.

---

## Background

- Book [3] includes a large appendix on basic mathematical tools (pp. 598–633).
- Continuous optimization involves problems of the form:

  $$
  \min_{x \in \mathbb{R}^n} f(x)
  $$

  with constraints  
  \( c_i : \mathbb{R}^n \to \mathbb{R} \).

- In **discrete optimization**, the domain is a discrete set (e.g., number of cars, humans).

- Smooth optimization relies on:
  - Gradients  
  - Taylor’s theorem  
  - Linear algebra  
  - Geometric intuition (drawing)

- Many real-world tasks can be framed as optimization, but they may not be easy to solve.

---

## Level Sets

For a function \( f : \mathbb{R}^n \to \mathbb{R} \), level sets are defined as:

$$
L_c(f) = \{ x \in \mathbb{R}^n \mid f(x) = c \}.
$$

- These typically have dimension \( n-1 \).
- When \( n = 2 \), level sets are *curves* (contours).

### Gradient direction
A key fact from calculus:

> At any point on a level set, \( \nabla f(x) \) is **orthogonal** to the tangent plane of that level set.

---

## Example: Tangent to a Level Set

Let:

$$
f(x_1, x_2) = (x_1 - 2)^2 + (x_2 - 1)^2.
$$

Find the tangent line at point \( (1, 2) \).

### Method 1 — Implicit Differentiation

Start with:

$$
f(x_1, x_2) = 2.
$$

Differentiate:

$$
2(x_1 - 2) + 2(x_2 - 1)x_2'(x_1) = 0.
$$

Thus:

$$
x_2'(x_1) = -\frac{x_1 - 2}{x_2 - 1}.
$$

At point (1, 2):

$$
x_2' = 1.
$$

Tangent line:

$$
x_2 = x_1 + 1.
$$

### Method 2 — Gradient

$$
\nabla f(1, 2) = (-2, 2)
$$

An orthogonal direction is \( (1, 1) \), giving the same tangent line.

---

## Relationship Between Objective and Constraints

The optimizer depends on **both**:

- the objective function \( f \)
- the constraints (feasible region)

Illustrated in Figure 1.1 (book p. 3).

---

## Linear Programming (LP)

Consider problem (1.3 a–d):

- Objective and constraints are linear.
- Feasible region is a **convex polygon**.
- LP is a major field in optimization theory.

---

## Classification of Optimization Problems

Two main categories:

- **Unconstrained optimization**
- **Constrained optimization**

NEOS provides finer classifications.

This course focuses on:

- **Convex optimization**
- **Nonconvex optimization**

Excluded:

- Discrete optimization  
- Optimization under uncertainty  

---

## Convexity

Convexity of a function \( f \) on a convex set \( S \subseteq \mathbb{R}^n \):

Intuition:

> The function is "bowl-shaped".

For smooth functions:

$$
f \text{ is convex } \iff \nabla^2 f(x) \text{ is positive semidefinite } \forall x \in S.
$$

### Example

Let \( S = \mathbb{R}^2 \):

- \( f(x_1, x_2) = x_1^4 + x_2^6 \) is convex.
- \( g(x_1, x_2) = x_1^2 x_2^2 \) is **not** convex.

Evidence:  
The Hessian of \( g \) at (1,1) has eigenvalues 6 and −2 → not PSD.

---

## Optimization Algorithms

Optimization algorithms are often **iterative**:

$$
x^{(k+1)} \quad \text{improves over} \quad x^{(k)}.
$$

Characteristics:

- computational cost  
- storage cost  
- convergence speed  

Starting point \( x^{(0)} \) must be chosen.

---

## Convergence Order

An iterative method has order \( p \) if:

$$
\| x - x^{(k+1)} \| \le C \| x - x^{(k)} \|^p.
$$

- \( p = 1 \): linear  
- \( p = 2 \): quadratic  
- \( p = 3 \): cubic  

Quadratic convergence example:  
\( 10^{-1} \to 10^{-2} \to 10^{-4} \to 10^{-8} \).

---

## Newton’s Method

Solves:

$$
r(x) = 0.
$$

### 1D Newton

$$
x^{(k+1)} = x^{(k)} - \frac{r(x^{(k)})}{r'(x^{(k)})}.
$$

### Multivariate Newton

$$
x^{(k+1)} = x^{(k)} - J(x^{(k)})^{-1} r(x^{(k)}),
$$

where \( J \) is the Jacobian.

Under standard assumptions → **quadratic convergence**.

---

# Chapter 2 — Fundamentals of Unconstrained Optimization

Unconstrained optimization problem:

$$
\min f(x)
$$

with full domain \( \mathbb{R}^n \).

Maximization:

$$
\max f(x) \quad \equiv \quad \min (-f(x)).
$$

---
