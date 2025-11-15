# Conditioning

**Type:** Concept  
**Domain:** Numerical Analysis  
**Prerequisites:** Matrix Norms, Linear Systems, Error Analysis  
**Related Nodes:** Forward_Error, Backward_Error, Stability, Jacobi_Method, Gauss_Seidel_Method  

---

## 1. Definition

The **conditioning** of a problem measures its sensitivity to perturbations in input.

For solving \(Ax = b\):

\[
\kappa(A) = \|A\| \|A^{-1}\|
\]

- \(\kappa(A) \approx 1\): **well-conditioned**
- \(\kappa(A) \gg 1\): **ill-conditioned**

---

## 2. Why Conditioning Matters

Even if the algorithm is perfect, a poorly conditioned problem amplifies errors:

\[
\frac{\|\delta x\|}{\|x\|} \approx \kappa(A) \frac{\|\delta b\|}{\|b\|}
\]

Thus conditioning governs **how large the solution error can become**.

---

## 3. Conditioning & Iterative Methods

Affects convergence of:

- Jacobi method  
- Gauss–Seidel method  
- Krylov subspace solvers  

---

## 4. Cross Links

- **Matrix_Norms → defines → Conditioning**  
- **Vector_Norms → used_in → Conditioning**  
- **Conditioning → amplifies → Forward_Error**  
- **Conditioning → affects_convergence → Jacobi_Method**  
- **Conditioning → affects_convergence → Gauss_Seidel_Method**

---

## 5. References

- Higham — *Accuracy and Stability of Numerical Algorithms*  
- Trefethen & Bau — *Numerical Linear Algebra*
