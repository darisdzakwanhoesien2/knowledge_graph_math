# Matrix Norms

**Type:** Concept  
**Domain:** Numerical Matrix Analysis  
**Prerequisites:** Vector Norms, Linear Algebra, Induced Norms  
**Related Nodes:** Conditioning, Stability, Matrix_Exponential, LU_Factorization  

---

## 1. Definition

A **matrix norm** is a function  
\[
\|\cdot\| : \mathbb{R}^{m \times n} \to \mathbb{R}
\]  
satisfying:

1. **Non-negativity:** \(\|A\| \ge 0\)
2. **Definiteness:** \(\|A\| = 0 \iff A = 0\)
3. **Homogeneity:** \(\|\alpha A\| = |\alpha| \|A\|\)
4. **Triangle inequality:** \(\|A + B\| \le \|A\| + \|B\|\)
5. **Submultiplicativity:**  
   \[
   \|AB\| \le \|A\| \cdot \|B\|
   \]

---

## 2. Induced (Operator) Matrix Norms

Given a vector norm \(\|\cdot\|\) on \(\mathbb{R}^n\), the **induced matrix norm** is:

\[
\|A\| = \max_{x \neq 0} \frac{\|Ax\|}{\|x\|}
\]

### Key examples:

- **1-norm:**  
  \[
  \|A\|_1 = \max_j \sum_i |a_{ij}|
  \]
- **∞-norm:**  
  \[
  \|A\|_\infty = \max_i \sum_j |a_{ij}|
  \]
- **2-norm (spectral norm):**  
  \[
  \|A\|_2 = \sqrt{\lambda_{\max}(A^\top A)}
  \]

---

## 3. Properties

- Submultiplicative  
- Compatible with the vector norm  
- Used to bound stability and error  
- Determines conditioning: \(\kappa(A) = \|A\|\|A^{-1}\|\)

---

## 4. Applications

- Stability analysis of linear systems
- Convergence of iterative solvers
- Sensitivity of matrix functions
- Error propagation in numerical algorithms
- Bounding LU/QR/SVD factorization errors

---

## 5. Cross Links

- **Vector_Norms** → induces → **Matrix_Norms**  
- **Matrix_Norms** → defines → **Conditioning**  
- **Matrix_Norms** → influences → **Stability**  
- **Matrix_Norms** → used_in → **Matrix_Exponential**  
- **Matrix_Norms** → analyzes → **LU_Factorization**

---

## 6. References

- Trefethen & Bau — *Numerical Linear Algebra*  
- Golub & Van Loan — *Matrix Computations*
