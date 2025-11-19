# Introduction to Optimization  
**Old Exam Solutions (collection)**

### 1.
$$
x^{(0)} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}, \quad
x^{(1)} = \begin{bmatrix} -1/3 \\ 1/2 \end{bmatrix}, \quad
x^{(2)} = \begin{bmatrix} -0.3561 \\ 0.5 \end{bmatrix}.
$$

### 2.
The function is quadratic:
$$
f(x) = \frac{1}{2} x^{\top} A x - b^{\top} x, \quad
A = \begin{bmatrix} 4 & -2 \\ -2 & 8 \end{bmatrix}, \quad
b^{\top} = \begin{bmatrix} 1 & 2 \end{bmatrix}.
$$

Conjugate gradient method starting from \( x^{(0)} = \begin{bmatrix} 0 \\ 0 \end{bmatrix} \):

$$
r^{(0)} = d_0 = \begin{bmatrix} 1 \\ 2 \end{bmatrix}, \quad \beta_0 = 0, \quad \alpha_0 = \frac{5}{28},
$$
$$
x^{(1)} = \begin{bmatrix} \frac{5}{28} \\ \frac{5}{14} \end{bmatrix}, \quad
r^{(1)} = \begin{bmatrix} 1 \\ -1/2 \end{bmatrix}.
$$

Next iteration:
$$
\beta_1 = \frac{1}{4}, \quad d_1 = \begin{bmatrix} 5/4 \\ 0 \end{bmatrix}, \quad \alpha_1 = \frac{1}{5},
$$
$$
x^{(2)} = \begin{bmatrix} 3/7 \\ 5/14 \end{bmatrix}, \quad r^{(2)} = \begin{bmatrix} 0 \\ 0 \end{bmatrix}.
$$

Thus \( x^{(2)} \) is the optimal solution and \( f(x^{(2)}) = -4/7 \).

### 3.
$$
x_{\min} = \begin{bmatrix} 9/7 \\ -8/7 \end{bmatrix}.
$$

### 4.
Constrained problem
$$
\min \quad x_1^2 + x_1 x_2 + 2x_2^2 - 2x_1
$$
$$
\text{s.t.} \quad x_1 - x_2 - 2 \leq 0, \quad x_1 - 2 \leq 0.
$$

Lagrangian
$$
L(x,\lambda) = x_1^2 + x_1 x_2 + 2x_2^2 - 2x_1 + \lambda_1 (x_1 - x_2 - 2) + \lambda_2 (x_1 - 2).
$$

KKT conditions
$$
\begin{align*}
2x_1 + x_2 - 2 + \lambda_1 + \lambda_2 &= 0, \\
x_1 + 4x_2 - \lambda_1 &= 0, \\
\lambda_1 (x_1 - x_2 - 2) &= 0, \\
\lambda_2 (x_1 - 2) &= 0, \\
\lambda_1, \lambda_2 &\geq 0.
\end{align*}
$$

The only point that satisfies the KKT conditions is
$$
x^* = \begin{bmatrix} 8/7 \\ -2/7 \end{bmatrix}, \quad \lambda_1^* = \lambda_2^* = 0.
$$

### 5.
The point \( [x, u] = [0 \quad 1 \quad 1 \quad 0]^{\top} \).

### 6–7.
Primal problem
$$
\min \quad 2x_1^2 + x_2^2 - x_1 x_2 - x_2 \quad \text{s.t.} \quad 2x_1 + x_2 + 2 \leq 0.
$$

Lagrangian
$$
L(x,u) = 2x_1^2 + x_2^2 - x_1 x_2 - x_2 + u(2x_1 + x_2 + 2).
$$

Unconstrained minimizer of Lagrangian:
$$
x_1(u) = -\frac{5}{7}u + \frac{1}{7}, \quad x_2(u) = -\frac{6}{7}u + \frac{4}{7}.
$$

Dual function
$$
G(u) = -\frac{8}{7}u^2 + \frac{20}{7}u - \frac{2}{7}.
$$

Dual problem: \( \max_{u \geq 0} G(u) \).

(Slightly different linear terms appear in problem 7, yielding \( G(u) = -\frac{8}{7}u^2 + \frac{12}{7}u - \frac{1}{7} \), with maximum at \( u = 3/4 \), giving primal solution \( x_1 = -1/4 \), \( x_2 = -1/2 \).)

### 8.
Constrained problem
$$
\min \quad x_1^2 + x_2^2 + x_1 x_2 - 3x_2 \quad \text{s.t.} \quad -x_1 + 2x_2 \leq 2.
$$

Quadratic form:
$$
f(x) = \frac{1}{2} x^{\top} \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix} x - \begin{bmatrix} 0 \\ 3 \end{bmatrix}^{\top} x.
$$

Uzawa algorithm with \( \lambda^{(0)} = 1 \), \( \rho = 1/7 \):
$$
x^{(0)} = \begin{bmatrix} 1/3 \\ 1/3 \end{bmatrix}.
$$

Subsequent iterations yield the values shown in the original solution sheet.