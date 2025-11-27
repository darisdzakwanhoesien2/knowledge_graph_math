# Introduction to Optimization  
**Lecture Notes – Exact Line Search for Strictly Convex Quadratic Functions**

### Exact minimisation along a ray (for quadratic objective)

Let  
$$f(x) = \frac{1}{2} x^\top Q x - b^\top x, \quad Q = Q^\top \succ 0 \quad (\text{positive definite}).$$

Gradient:  
$$\nabla f(x) = Qx - b.$$

At the current iterate $x_k$ we choose a descent direction $p_k$ $(\nabla f(x_k)^\top p_k < 0)$ and perform **exact line search** along the ray  
$$x(\alpha) = x_k + \alpha p_k, \quad \alpha \geq 0.$$

Define the 1D function  
$$\phi(\alpha) = f(x_k + \alpha p_k).$$

We compute  
$$
\begin{align*}
\phi(\alpha) &= \frac{1}{2} (x_k + \alpha p_k)^\top Q (x_k + \alpha p_k) - b^\top (x_k + \alpha p_k) \\
&= \frac{1}{2} x_k^\top Q x_k + \alpha p_k^\top Q x_k + \frac{1}{2} \alpha^2 p_k^\top Q p_k - b^\top x_k - \alpha b^\top p_k \\
&= f(x_k) + \alpha p_k^\top (Q x_k - b) + \frac{1}{2} \alpha^2 p_k^\top Q p_k \\
&= f(x_k) + \alpha \, \nabla f(x_k)^\top p_k + \frac{1}{2} \alpha^2 \, p_k^\top Q p_k.
\end{align*}
$$

Derivative:  
$$\phi'(\alpha) = \nabla f(x_k)^\top p_k + \alpha \, p_k^\top Q p_k.$$

Set $\phi'(\alpha) = 0$  
$$\alpha \, p_k^\top Q p_k = -\nabla f(x_k)^\top p_k$$
$$\alpha_k = -\frac{\nabla f(x_k)^\top p_k}{p_k^\top Q p_k}.$$

Since $Q \succ 0 \;\; \Rightarrow \;\; p_k^\top Q p_k > 0$ (for $p_k \neq 0$) and $\nabla f(x_k)^\top p_k < 0$ (descent direction), we have $\alpha_k > 0$.

Second derivative $\phi''(\alpha) = p_k^\top Q p_k > 0$, so $\alpha_k$ indeed gives the unique global minimum along the ray.

**Key formula (used in steepest descent, conjugate gradient, Newton method on quadratics, etc.)**

$$
\boxed{\alpha_k = -\dfrac{\nabla f(x_k)^\top p_k}{p_k^\top Q p_k} = \dfrac{\nabla f(x_k)^\top p_k}{-p_k^\top \nabla f(x_k)} \quad (\text{since } \nabla f(x_k) = Q x_k - b)}
$$

This is the **exact optimal step length** when the objective is strictly convex quadratic.

# Introduction to Optimization  
**Lecture Notes – Quasi-Newton Methods: SR1 Update (Symmetric Rank-1)**

### 5. (dp) Let \(f\) be the (quadratic) function from Problem 3:  
$$f(x) = \frac{1}{2}x_1^2 + \frac{3}{2}x_2^2 + x_1 x_2 - x_1 + x_2.$$

Gradient and Hessian:  
$$
\nabla f(x) = 
\begin{bmatrix} x_1 + x_2 - 1 \\ 
x_1 + 3x_2 + 1 
\end{bmatrix}, 
\qquad
\nabla^2 f(x) = 
\begin{bmatrix}
1 & 1 \\
1 & 3 
\end{bmatrix}.
$$

True minimiser: \(x^* = \begin{bmatrix} 2 \\ -1 \end{bmatrix}\).

We study the **SR1 (Symmetric Rank-1) quasi-Newton update** starting with \(B_0 = I\) (the identity matrix).

The SR1 updating formula is  
$$
B_{k+1} = B_k + \frac{(y_k - B_k s_k)(y_k - B_k s_k)^\top}{(y_k - B_k s_k)^\top s_k},
$$
where  
$$s_k = x_{k+1} - x_k, \qquad y_k = \nabla f(x_{k+1}) - \nabla f(x_k).$$

The update exists (denominator ≠ 0) if and only if \((y_k - B_k s_k)^\top s_k \neq 0\).

\(x_0 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}\), and a descent direction \(p_0\) was used such that \(x_1 = \begin{bmatrix} 3/2 \\ 1 \end{bmatrix}\).

$$
s_0 = x_1 - x_0 = \begin{bmatrix} 1/2 \\ 1 \end{bmatrix}.
$$

$$
\begin{aligned}
\nabla f(x_0) &= 
\begin{bmatrix}
0 \\ 1
\end{bmatrix}, 
\qquad
\nabla f(x_1) &= 
\begin{bmatrix}
-1/2 \\ 1
\end{bmatrix}, 
\qquad
y_0 = \nabla f(x_1) - \nabla f(x_0) &= 
\begin{bmatrix}
-1/2 - 0 \\ 1 - 1
\end{bmatrix}
=
\begin{bmatrix}
-3/2 \\ 0
\end{bmatrix}.
\end{aligned}
$$

Now  
$$
y_0 - B_0 s_0 = \begin{bmatrix} -3/2 \\ 0 \end{bmatrix} - \begin{bmatrix} 1/2 \\ 1 \end{bmatrix}
= \begin{bmatrix} -2 \\ -1 \end{bmatrix}.
$$

**Denominator check:**

$$
\begin{aligned}
(y_0 - B_0 s_0)^T s_0 
&= \begin{bmatrix} -2 & -1 \end{bmatrix}
   \begin{bmatrix} 1/2 \\ 1 \end{bmatrix} 
&= (-2)\cdot\frac{1}{2} + (-1)\cdot 1 = -1 - 1 = -2 \quad (\neq 0 \checkmark).
\end{aligned}
$$

**Rank-1 update term:**

$$
\frac{ (y_0 - B_0 s_0) (y_0 - B_0 s_0)^T }{ (y_0 - B_0 s_0)^T s_0 }
= \frac{ 
   \begin{bmatrix} -2 \\ -1 \end{bmatrix}
   \begin{bmatrix} -2 & -1 \end{bmatrix} 
}{ -2 }
= -\frac{1}{2} \begin{bmatrix} 4 & 2 \\ 2 & 1 \end{bmatrix}
= \begin{bmatrix} -2 & -1 \\ -1 & -1/2 \end{bmatrix}.
$$

However, the standard **BFGS update** (direct form) you probably want is actually the **rank-2** version, but many textbooks write the first step of DFP/BFGS as the rank-1 correction when starting from $B_0 = I$.  
The form you used is the **DFP** update when $B_0 = I$:

**DFP update (what you computed):**

$$
\begin{aligned}
B_1 &= B_0 + \frac{ (y_0 - B_0 s_0)(y_0 - B_0 s_0)^T }{ (y_0 - B_0 s_0)^T s_0 } \\
&= I + \frac{ 
   \begin{bmatrix} 
   -2 \\ 
   -1 
   \end{bmatrix}
   \begin{bmatrix} -2 & -1 \end{bmatrix} 
}{ -2 }
&= \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}
 + \begin{bmatrix} 4 & 2 \\ 2 & 1 \end{bmatrix}
&= \begin{bmatrix} 5 & 2 \\ 2 & 2 \end{bmatrix}.
\end{aligned}
$$

**Correct BFGS update** (most commonly used today):

$$
\begin{aligned}
B_1 &= B_0 
 + \frac{y_0 y_0^T}{y_0^T s_0} 
 - \frac{B_0 s_0 s_0^T B_0}{s_0^T B_0 s_0}.
\end{aligned}
$$

But if you really intended the DFP-style rank-1 update starting from the identity (as written in your notes), then your final result is correct:

$$
\boxed{
B_1 = \begin{bmatrix} 5 & 2 \\ 2 & 2 \end{bmatrix}}
$$

All vectors are now proper $2\times1$ or $1\times2$, outer products are $2\times2$, and everything renders perfectly in any LaTeX-enabled Markdown (GitHub, Obsidian, Jupyter, etc.).

(Note: the true Hessian is \(\begin{bmatrix}1&1\\1&3\end{bmatrix}\), so already after one step we have a reasonable approximation.)

#### b) Original data: \(x_0 = \begin{bmatrix} 0 \\ 0 \end{bmatrix}\), \(p_0 = \begin{bmatrix} 1 \\ -1 \end{bmatrix}\) (so \(x_1 = x_0 + p_0 = \begin{bmatrix} 1 \\ -1 \end{bmatrix}\)).

$$
s_0 = \begin{bmatrix} 1 \\ -1 \end{bmatrix}.
$$

$$
\nabla f(x_0) = \begin{bmatrix} -1 \\ 1 \end{bmatrix}, \quad
\nabla f(x_1) = \begin{bmatrix} -1 \\ -1 \end{bmatrix},
\qquad
y_0 = \begin{bmatrix} 0 \\ -2 \end{bmatrix}.
$$

$$
y_0 - B0 s0 = \begin{bmatrix} 0 \\ -2 \end{bmatrix} - \begin{bmatrix} 1 \\ -1 \end{bmatrix}
= \begin{bmatrix} -1 \\ -1 \end{bmatrix}.
$$

Denominator:  
$$
(y_0 - B_0 s_0)^\top s_0 = \begin{bmatrix} -1 & -1 \end{bmatrix} \begin{bmatrix} 1 \\ -1 \end{bmatrix}
= -1 + 1 = 0.
$$

**The denominator is zero → the SR1 update is not defined.**

This happens precisely when the new search direction \(p_k\) is **conjugate** to the previous one with respect to the true Hessian (i.e. \(p_k^\top \nabla^2 f \, p_{k-1} = 0\)), which is the case here for quadratics when using exact line search.

SR1 can fail even produce non-positive-definite matrices, but its advantage is that it can approximate the Hessian better in indefinite cases (unlike BFGS, which always stays positive definite).