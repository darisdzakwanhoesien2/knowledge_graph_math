# Chapter 9 — Duality  
**Clean Markdown Conversion**

Duality is one of the most important theoretical topics in optimization.  
This chapter introduces the dual function, the dual problem, weak/strong duality, and examples for LP and quadratic programming.

We consider constrained convex optimization problems where convexity of the Lagrangian is essential.

---

# 1. Convex Constrained Optimization Problem

We study:

$$
\min f(x)
\quad \text{s.t.} \quad
c(x) =
\begin{bmatrix}
c_1(x) \\ c_2(x) \\ \vdots \\ c_m(x)
\end{bmatrix}
\le 0, \tag{73}
$$

under the assumptions:

- \(f\) is **convex**
- each \(-c_j\) is **convex** (equivalently: each \(c_j\) is concave)
- all functions are **smooth** enough (continuously differentiable)

Define the **Lagrangian**:

$$
L(x,\lambda) = f(x) - \lambda^T c(x),
\quad \lambda \ge 0.
$$

For fixed \(\lambda \ge 0\), \(L(x,\lambda)\) is **convex in \(x\)**.

---

# 2. The Dual Function

The **dual objective function** is:

$$
q(\lambda) = \inf_x L(x,\lambda), \tag{74}
$$

defined only for those \(\lambda \ge 0\) for which the infimum is finite (otherwise \(q(\lambda) = -\infty\)).

Thanks to convexity:

- Minimizing \(L(x,\lambda)\) over \(x\) is often tractable
- The result is a concave function \(q(\lambda)\)

---

## Example: Simple Quadratic with Inequality Constraint

Problem:

$$
\min\ \frac12 (x_1^2 + x_2^2)
\quad \text{s.t.} \quad
x_1 - 1 \le 0. \tag{75}
$$

Lagrangian:

$$
L(x,\lambda) = \tfrac12(x_1^2 + x_2^2) - \lambda(x_1 - 1).
$$

Compute critical point for fixed \(\lambda \ge 0\):

$$
\nabla_x L =
\begin{bmatrix}
x_1 - \lambda \\ x_2
\end{bmatrix}
= 0
\quad \Rightarrow \quad
x = (\lambda, 0).
$$

Insert:

$$
q(\lambda)
= \tfrac12 \lambda^2 - \lambda(\lambda - 1)
= -\tfrac12 \lambda^2 + \lambda.
$$

Dual problem:

$$
\max_{\lambda \ge 0} q(\lambda). \tag{76}
$$

Both primal and dual attain value **\(1/2\)** → **strong duality**.

---

# 3. Weak Duality

For any feasible \(x\) and any \(\lambda \ge 0\):

$$
q(\lambda)
= \inf_{u} (f(u) - \lambda^T c(u))
\le f(x) - \lambda^T c(x)
\le f(x). \tag{77}
$$

Thus:

> Dual objective always gives a **lower bound** to the primal objective.

Consequences:

- Dual optimum ≤ primal optimum  
- If equality occurs → both are optimal

---

# 4. Strong Duality (Motivation)

If for some feasible \(x\) and some \(\lambda \ge 0\):

$$
q(\lambda) = f(x),
$$

then:

- \(x\) is primal optimal  
- \(\lambda\) is dual optimal  

This motivates solving the dual problem as a way to bound or solve the primal.

---

# 5. Example: Linear Programming Dual

Given LP:

$$
\min c^T x
\quad \text{s.t.} \quad
Ax - b \le 0. \tag{78}
$$

Lagrangian:

$$
L(x,\lambda)
= c^T x - \lambda^T(Ax - b)
= (c - A^T\lambda)^T x + \lambda^T b.
$$

Dual function:

- Finite only if:  
  $$
  c - A^T \lambda = 0.
  $$
- Otherwise \(q(\lambda) = -\infty\)

Thus, when feasible:

$$
q(\lambda) = \lambda^T b.
$$

Dual LP (79):

$$
\max_{\lambda \ge 0} \ \lambda^T b
\quad \text{s.t.} \quad
A^T \lambda = c. \tag{79}
$$

This converts one LP into another.

---

# 6. Convexity Properties

- Dual function \(q(\lambda)\) is **concave**, regardless of primal convexity.
- The function \(-q\) is **convex** — see Theorem 12.10.

Dual feasible set:

- \(\lambda \ge 0\)
- (plus any additional constraints ensuring finiteness)

---

# 7. Strong Duality via KKT

Theorem 12.12 (p. 346):

If:

- \(x^*\) solves the primal problem (73)  
- functions \(f, -c_j\) are convex and differentiable  
- \((x^*,\lambda^*)\) satisfy KKT conditions  

then \(\lambda^*\) solves the dual problem (76).

Important notes:

- LICQ or differentiability of constraints **not required** here  
- Proof uses convexity of the Lagrangian + weak duality  
- Concludes \(q(\lambda^*) = f(x^*)\) → optimality

---

# 8. Practical Use of Duality (How to Solve Problems)

Duality is often used **backwards**:

1. Form the dual (easier, smaller dimension, or simpler structure)
2. Solve the dual for \(\lambda^*\)
3. Solve the KKT conditions for \(x\) using the computed \(\lambda^*\)
4. Check strong-duality condition:  
   $$
   q(\lambda^*) = f(x)
   $$

If true → both are optimal.

This avoids enumerating all \(2^m\) active/inactive patterns in inequality-constrained KKT systems.

---

# 9. Quadratic Programming Example (Revisited from Chapter 5)

Quadratic program:

$$
\min \tfrac12 x^T Q x - b^T x
\quad \text{s.t.} \quad
Cx - d \le 0. \tag{44}
$$

Assume \(Q \succ 0\) → convex.

Lagrangian:

$$
L(x,\lambda)
= \tfrac12 x^T Q x - b^T x - \lambda^T(d - Cx).
$$

Set gradient to zero:

$$
\nabla_x L = Qx - b + C^T\lambda = 0
\quad \Rightarrow \quad
x = Q^{-1}(b - C^T\lambda).
$$

Insert into L to obtain dual:

$$
q(\lambda)
=
\tfrac12 (b - C^T \lambda)^T Q^{-1}(b - C^T \lambda)
- d^T \lambda.
$$

Dual problem:

$$
\max_{\lambda \ge 0}
\ \tfrac12 (b - C^T \lambda)^T Q^{-1}(b - C^T \lambda)
- d^T \lambda.
$$

Still includes inequalities → may not be simpler.

---

# 10. Inequality Constraints and Active-Set Difficulty

For problem (44):

- There are \(m\) inequality constraints
- For KKT, need to test **all \(2^m\)** active sets  
- This is computationally infeasible for large \(m\)  
- LP avoids this via standard form and simplex pivots  
- For general convex programs → **interior-point methods** are preferred

Interior-point methods avoid enumerating active sets and handle large numbers of inequalities efficiently.

---

# 11. Summary of Duality Principles

1. Dual function:
   $$
   q(\lambda) = \inf_x L(x,\lambda)
   $$
2. Always:
   $$
   q(\lambda) \le f(x) \quad \text{for all feasible } x,\ \lambda \ge 0
   $$
   (weak duality)
3. If:
   $$
   q(\lambda^*) = f(x^*)
   $$
   both are optimal (strong duality)
4. KKT links primal and dual optimizers  
5. Duality is especially clean in LP and convex quadratic programming  
6. Interior-point methods rely heavily on duality theory

---

# End of Chapter 9  
*(Based on textbook pp. 345–349.)*
