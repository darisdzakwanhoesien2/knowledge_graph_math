# Chapter 8 — Linear Programming (LP) and the Simplex Method  
**Clean Markdown Conversion**

Linear Programming (LP) is a foundational class of constrained optimization problems where both the objective and the constraints are *linear*. This chapter introduces LP standard form, canonical form, basic feasible solutions, and the simplex method with worked examples.

---

# 1. Introduction to Linear Programming

We consider the constrained optimization problem:

$$
\min c^T x \quad \text{s.t.} \quad Ax = b,\; x \ge 0. \tag{64}
$$

Here:

- \(c \in \mathbb{R}^n\) is the cost vector  
- \(A \in \mathbb{R}^{m \times n}\) with **linearly independent rows**  
- \(m < n\)

This is the **standard form** of a linear program.

### Why “linear program”?

- All functions involved (objective and constraints) are linear.
- Many real-world optimization problems can be written this way.

---

# 2. Canonical Form and Slack Variables

A more general LP form is:

$$
\min c^T x \quad \text{s.t.} \quad Ax \le b,\; x \ge 0. \tag{65}
$$

To convert this to standard form, introduce **slack variables** \(z \ge 0\):

$$
Ax + Iz = b.
$$

Thus:

$$
\begin{bmatrix} A & I \end{bmatrix}
\begin{bmatrix} x \\ z \end{bmatrix}
= b. \tag{66}
$$

The new variable vector \((x, z)\) has dimension \(n + m\).

---

# 3. KKT Conditions for Linear Programming

The Lagrangian:

$$
L(x, \lambda) = c^T x - \lambda^T (Ax - b) - s^T x.
$$

KKT conditions:

1. **Stationarity**  
   $$
   \nabla_x L = c - A^T \lambda - s = 0.
   $$
2. **Primal feasibility**  
   $$
   Ax = b,\quad x \ge 0.
   $$
3. **Dual feasibility**  
   $$
   s \ge 0.
   $$
4. **Complementarity**  
   $$
   s \circ x = 0.
   $$

Solving KKT directly is inefficient → simplex avoids this.

---

# 4. Geometry and Vertices

LP feasible set \( \Omega \) (from (65)) is a polytope: intersection of half-spaces.

For \(n=3\), it appears as a **polygonal region** (Fig. 13.2 in textbook).

Key fact:

> The minimum of a linear function over a polytope is always attained at a **vertex** (corner).

Thus the simplex method moves *from vertex to vertex*.

---

# 5. Basic Feasible Solutions (BFS)

A **basic feasible solution** for (64) corresponds to:

- Selecting \(m\) linearly independent columns of \(A\) → matrix \(B\)
- Setting the remaining \(n-m\) variables to zero
- Solving \(Bx_B = b\)

If \(x_B \ge 0\), the solution is feasible.

Terminology:

- **Basic variables:** components of \(x_B\)  
- **Nonbasic (free) variables:** the remaining variables, equal to zero

Simplex moves from one BFS to another along edges of the feasible polytope.

---

# 6. Simple Example Demonstrating Vertices

Consider the LP:

$$
\min 7x_3 - x_4 - 3x_5
$$

subject to:

$$
\begin{aligned}
x_1 + x_3 + 6x_4 + 2x_5 &= 8, \\
x_2 + x_3 + 3x_5 &= 9.
\end{aligned} \tag{67}
$$

Initial BFS:

- \(x_1 = 8,\ x_2 = 9\) (basic)  
- \(x_3 = x_4 = x_5 = 0\) (free)  

Cost involves only free variables.

### Choosing the entering variable
Free variable with **most negative** cost coefficient enters:

- Candidates: \(x_4\) (–1), \(x_5\) (–3)  
- Entering variable → **\(x_5\)**

### Ratio test (to determine leaving variable)

Solve:

- From eq. 1: \(x_1 + 2x_5 = 8\) → \(x_1 = 8 - 2x_5\), reaches zero at \(x_5 = 4\)
- From eq. 2: \(x_2 + 3x_5 = 9\), reaches zero at \(x_5 = 3\)

Smallest positive ratio ⇒ **\(x_2\)** leaves, **\(x_5=3\)**.

New BFS:

- \(x_1 = 2,\ x_5 = 3,\ x_2 = 0,\ x_3 = x_4 = 0\)

Continue by pivoting and repeating (details in text).

This process illustrates:

- How entering vs leaving variables are chosen  
- Descent of cost function  
- Movement from corner to corner

---

# 7. Tableau Form of Simplex

Initial tableau (68):

$$
\begin{bmatrix}
A & b \\
c^T & 0
\end{bmatrix}
$$

Reorder columns so basic variables come first:

$$
A = [B\ N],\quad c = (c_B,\ c_N).
$$

Transform by multiplying constraints by \(B^{-1}\):

$$
\begin{bmatrix}
I & B^{-1}N & B^{-1}b \\
c_B^T & c_N^T & 0
\end{bmatrix}.
$$

Eliminate \(c_B\)-terms from bottom row:

Resulting simplex tableau (70):

$$
\begin{bmatrix}
I & B^{-1}N & B^{-1}b \\
0 & c_N^T - c_B^T B^{-1} N & - c_B^T B^{-1} b
\end{bmatrix}.
$$

Cost becomes:

$$
c^T x = \big(c_N - N^T B^{-1} c_B\big)^T x_N + c_B^T B^{-1}b.
$$

The vector:

$$
s = c_N - N^T B^{-1} c_B
$$

tells whether descent is possible.

---

# 8. The Simplex Step (Algorithm)

Let:

- \(B\) = current basis matrix  
- \(N\) = matrix of nonbasic columns  
- \(x_B = B^{-1}b\) = basic variables  
- \(x_N = 0\) = nonbasic variables  
- \(s = c_N - N^T B^{-1} c_B\) = reduced costs

### Step 1 — Stop or choose entering variable
If:

- \(s \ge 0\): optimal  
- Otherwise: choose \(x_j\) with most negative \(s_j\) as **entering variable**

Let \(u\) = \(j\)-th column of \(N\).

### Step 2 — Ratio test (leaving variable)

Compute:

$$
\min_i \frac{(B^{-1}b)_i}{(B^{-1}u)_i} \tag{71}
$$

over **positive** components of \(B^{-1}u\).

- Smallest ratio → **leaving variable**

If **no positive** entries exist → unbounded LP.

### Step 3 — Pivot  
Replace the leaving column of \(B\) with \(u\).  
Update \(B^{-1}\), recompute reduced costs, repeat.

---

# 9. Large Example (Standard Form)

Given the LP:

$$
\min -12x_1 - 9x_2
$$

subject to:

$$
\begin{aligned}
x_1 &\le 1000, \\
x_2 &\le 1500, \\
x_1 + x_2 &\le 1750, \\
4x_1 + 2x_2 &\le 4800,
\end{aligned} \tag{72}
$$

Introduce slack variables \(x_3,\ldots,x_6\):

$$
Ax = b,\quad x \ge 0.
$$

Initial BFS:

$$
x_3 = 1000,\ x_4 = 1500,\ x_5 = 1750,\ x_6 = 4800,
$$

with \(x_1 = x_2 = 0\).

Reduced costs:

$$
s = c_N = (-12, -9),
$$

entering variable → \(x_1\).

Ratio test yields leaving variable \(x_3\).

Updated BFS:

$$
x_1 = 1000,\ x_4 = 1500,\ x_5 = 750,\ x_6 = 800.
$$

Continue simplex iterations until optimum is reached.

---

# 10. Complexity of Simplex

Worst-case number of steps:

$$
\binom{n}{m}
$$

can be exponential.

Example:

- “Factory allocation problem” had  
  \( 38! / (14! 24!) \) possible bases.

In practice:

- Simplex is extremely efficient.  
- Typical number of steps is \(2m\) or \(3m\).  
- Modern implementations are highly optimized.

---

# 11. Summary of the Simplex Method (Compact)

1. Start from a BFS (Phase I if necessary).  
2. Compute reduced costs  
   \( s = c_N - N^T B^{-1} c_B \).  
3. If \(s \ge 0\): stop — optimal BFS.  
4. Choose entering variable with most negative \(s_j\).  
5. Compute \(d = B^{-1} u\).  
6. If \(d \le 0\): LP is unbounded.  
7. Use ratio test to choose leaving variable.  
8. Pivot (update basis).  
9. Repeat.

---

# 12. Transition to Chapter 9

Next chapter introduces **duality**, requiring convexity assumptions.  
We consider:

$$
\min f(x) \quad \text{s.t.} \quad c(x) \le 0, \tag{73}
$$

where:

- \(f\) is convex  
- each \(-c_j\) is convex (i.e., each \(c_j\) concave)

This ensures Lagrangian convexity in \(x\).

---

# End of Chapter 8  
*(Based on textbook pp. 355–371.)*
