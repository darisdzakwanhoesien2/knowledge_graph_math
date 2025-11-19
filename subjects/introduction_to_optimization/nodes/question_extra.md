# Introduction to Optimization  
**Collection of Old Exam Problems & Selected Solutions**

## Some Tasks from Old Exams (English)

### 1. Newton method (unconstrained)
$$
\min_{x \in \mathbb{R}^2} x_1^2 + x_2^2 + e^{x_1 - x_2}.
$$
Starting point \(x^{(0)} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}\). Compute two iterations.

### 2. Conjugate gradient method
$$
\min_{x \in \mathbb{R}^2} 2x_1^2 - 2x_1 x_2 + 4x_2^2 - x_1 - 2x_2,
\quad x^{(0)} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}.
$$

### 3. Conjugate gradient method
$$
\min_{x \in \mathbb{R}^2} 2x_1^2 + x_1 x_2 + x_2^2 - 4x_1 + x_2,
\quad x^{(0)} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}.
$$

### 4. KKT conditions
$$
\min \quad x_1^2 + x_1 x_2 + 2x_2^2 - 2x_1
$$
subject to
$$
x_1 - x_2 - 2 \leq 0, \quad x_1 \leq 2.
$$

### 5. KKT conditions
$$
\min \quad x_1 - 2x_2
$$
subject to
$$
x_1 - x_2^2 + 1 \geq 0, \quad x_2 \geq 0.
$$

### 6–7. Dual function and dual problem
6. \(\min \quad 2x_1^2 + x_2^2 - x_1 x_2 - x_2 \quad \text{s.t.} \quad 2x_1 + x_2 \leq -2\).

7. \(\min \quad 2x_1^2 + x_2^2 - x_1 x_2 - x_1 \quad \text{s.t.} \quad 2x_1 + x_2 \leq -1\).

### 8. Uzawa algorithm (two iterations, \(\rho = \frac{1}{7}\))
$$
\min \quad x_1^2 + x_2^2 + x_1 x_2 - 3x_2 \quad \text{s.t.} \quad -x_1 + 2x_2 - 2 \leq 0.
$$

## Selected Solutions (from various old exams)

### Newton method on \(f(x) = e^{-x_1-x_2} + x_1^2 + x_2^2\)
$$
x^{(0)} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}, \;
x^{(1)} = \begin{bmatrix} 1/4 \\ 1/4 \end{bmatrix}, \;
x^{(2)} \approx \begin{bmatrix} 0.2832 \\ 0.2832 \end{bmatrix}.
$$

### Conjugate gradient (one of the quadratics)
Optimal solution \(x^* = \begin{bmatrix} -1/2 \\ -1 \end{bmatrix}\), minimum value \(-\frac{4}{7}\).

### KKT example
Only feasible KKT point: \(x^* = \begin{bmatrix} 8/7 \\ -2/7 \end{bmatrix}\), \(\lambda^* = (0,0)\).

### Dual example (primal with single inequality)
Both problems lead to dual \( \max_{u \geq 0} G(u) = -\frac{8}{7}u^2 + cu - \frac{d}{7} \) (c, d differ slightly between 6 and 7).

## Final Exam 22.10.2015 – Solutions

1. Newton on \(f(x)=e^{-x_1-x_2}+x_1^2+x_2^2\) → iterations given above.

2. Conjugate gradient → optimal \(x^{(2)} = \begin{bmatrix} -1/2 \\ -1 \end{bmatrix}\).

3. KKT on exponential problem → \(x_1=0\), \(x_2=\ln 19\), \(\lambda_1=1/361\), \(\lambda_2=20/361\).

4. Lagrangian & dual derivation for box-constrained quadratic.

## Loppukoe / Exam 18.1.2016 (bilingual)

### 1. LP problem
$$
\min -x_1 + 2x_2 - 5x_3 \quad \text{s.t.} \quad Ax = b,\; x \geq 0
$$
$$
A = \begin{bmatrix} -2 & -2 & 1 & -1 & 0 \\ 1 & -1 & 2 & 0 & -1 \\ 1 & 0 & 0 & 0 & -1 \end{bmatrix}, \;
b = \begin{bmatrix} -2 \\ 4 \\ -2 \end{bmatrix}.
$$

### 2. Dual of constrained problem
$$
\min x_1^2 + x_1 x_2 + x_2^2 - 4x_1 + x_2 \quad \text{s.t.} \quad 2x_1 + x_2 \leq 2.
$$
Find optimal primal and dual solutions.

### 3. Conjugate gradient
$$
\min 3x_1^2 - 2x_1 x_3 + 3x_3^2 - x_1 - 3x_2, \quad x^{(0)} = 0.
$$

### 4. KKT + Uzawa algorithm (two iterations, \(u_0 = 7.5\), \(\rho = 4\))
$$
\min e^{x_1} + e^{x_2} \quad \text{s.t.} \quad x_1 + x_2 \geq 4.
$$

(All problems are now cleanly formatted in LaTeX, bilingual titles preserved where applicable, and minor OCR errors corrected for mathematical accuracy.)