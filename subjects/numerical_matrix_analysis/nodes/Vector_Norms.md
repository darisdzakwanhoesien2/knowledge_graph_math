# Vector Norms

**Type:** Concept  
**Domain:** Numerical Matrix Analysis  
**Prerequisites:** Linear Algebra, Inner Products, Basic Analysis  
**Related Nodes:** Matrix_Norms, Conditioning, Stability, Induced_Matrix_Norms  

---

## 1. Definition

A **vector norm** is a function  
\[
\|\cdot\| : \mathbb{R}^n \to \mathbb{R}
\]  
that assigns a non-negative length or magnitude to a vector, satisfying:

1. **Positive definiteness**  
   \[
   \|x\| \ge 0,\quad \|x\| = 0 \iff x = 0
   \]

2. **Homogeneity**  
   \[
   \|\alpha x\| = |\alpha|\,\|x\|
   \]

3. **Triangle inequality**  
   \[
   \|x+y\| \le \|x\| + \|y\|
   \]

These axioms make norms fundamental tools in numerical analysis, error analysis, and iterative methods.

---

## 2. Common Norms in \(\mathbb{R}^n\)

### ### 2.1 **1-Norm (Manhattan norm)**

\[
\|x\|_1 = \sum_{i=1}^n |x_i|
\]

**Geometric interpretation:** diamond shape in 2D.

**Applications:**  
- Sparse optimization  
- Basis pursuit  
- LASSO regularization  

---

### 2.2 **2-Norm (Euclidean norm)**

\[
\|x\|_2 = \left( \sum_{i=1}^n x_i^2 \right)^{1/2}
\]

Equivalent to the standard geometric length.

Key property:

\[
\|x\|_2 = \sqrt{x^\top x}
\]

---

### 2.3 **p-Norm (General case)**

\[
\|x\|_p = \left( \sum_{i=1}^n |x_i|^p \right)^{1/p},\qquad p \ge 1
\]

As \(p \to \infty\):

---

### 2.4 **∞-Norm (Max norm)**

\[
\|x\|_\infty = \max_{1 \le i \le n} |x_i|
\]

Describes the maximum coordinate magnitude.

Used in:  
- Uniform error bounds  
- Gershgorin circle theorem  
- Stability analysis  

---

## 3. Properties of p-Norms

### 3.1 Monotonicity  
\[
p \le q \quad \Rightarrow \quad \|x\|_q \le \|x\|_p \le n^{1/p - 1/q}\|x\|_q
\]

### 3.2 Norm Equivalence (Finite Dimensions)

All norms satisfy:

\[
\exists c_1, c_2 > 0 : \quad c_1 \|x\|_a \le \|x\|_b \le c_2 \|x\|_a
\]

---

## 4. Geometric Interpretation

| Norm | Unit Ball Shape |
|------|------------------|
| \(\|\cdot\|_1\) | Diamond |
| \(\|\cdot\|_2\) | Circle |
| \(\|\cdot\|_\infty\) | Square |
| \(\|\cdot\|_p, p>2\) | Rounded square |
| \(\|\cdot\|_p, p<2\) | Rounded diamond |

---

## 5. Relation to Matrix Norms

Matrix norms induced by vector norms satisfy:

\[
\|A\| = \max_{x \ne 0} \frac{\|Ax\|}{\|x\|}
\]

Examples:

- Induced 1-norm: column-sum norm  
- Induced ∞-norm: row-sum norm  
- Induced 2-norm: spectral norm  

---

## 6. Applications in Numerical Analysis

- Error bounds for linear solvers  
- Stability of iterative methods  
- Conditioning of linear systems  
- Convergence of Krylov methods  
- Sensitivity of eigenvalues  

---

## 7. Examples

### Example 1  
\[
x = (3, -4, 1)
\]

\[
\|x\|_1 = 3 + 4 + 1 = 8
\]

\[
\|x\|_2 = \sqrt{26}
\]

\[
\|x\|_\infty = 4
\]

---

## 8. Cross-Links

- See *Matrix_Norms* for induced norms  
- See *Conditioning* for how vector norms influence condition numbers  
- See *Stability* for numerical error propagation  

---

## 9. References

- Trefethen & Bau — *Numerical Linear Algebra*  
- Horn & Johnson — *Matrix Analysis*
