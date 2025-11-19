# Introduction to Optimization: Convexity of Sublevel Sets (H1r.pdf, Page 3)

### 4. Assume \( g : \mathbb{R}^n \to \mathbb{R} \) is convex and let \( c \in \mathbb{R} \). Show that the sublevel set
$$
S_c(g) = \{ x \in \mathbb{R}^n \mid g(x) \leq c \}
$$
is a convex set.

**Proof**

Let \( x, y \in S_c(g) \) be arbitrary and let \( \lambda \in [0,1] \).

By definition of the sublevel set we have \( g(x) \leq c \) and \( g(y) \leq c \).

We need to show that the convex combination also belongs to the sublevel set, i.e.,
$$
g(\lambda x + (1-\lambda)y) \leq c.
$$

Since \( g \) is convex,
$$
g(\lambda x + (1-\lambda)y) \leq \lambda g(x) + (1-\lambda)g(y) \leq \lambda c + (1-\lambda)c = c.
$$

Thus \( \lambda x + (1-\lambda)y \in S_c(g) \) for all \( \lambda \in [0,1] \), so \( S_c(g) \) is convex.  
□

### Reference (Numerical Optimization, page 8)

- A set \( S \subset \mathbb{R}^n \) is **convex** if for any \( x,y \in S \) and any \( \lambda \in [0,1] \),
  $$
  \lambda x + (1-\lambda)y \in S.
  $$

- A function \( f : S \to \mathbb{R} \) with convex domain \( S \) is **convex** if for any \( x,y \in S \) and any \( \lambda \in [0,1] \),
  $$
  f(\lambda x + (1-\lambda)y) \leq \lambda f(x) + (1-\lambda)f(y).
  $$

### Visual Summary (from sketches)
- Non-convex functions → sublevel sets are typically non-convex.
- Convex functions → sublevel sets are convex (the region “below” the graph is convex).
- Strictly convex functions → sublevel sets are strictly convex (or at least convex with no flat parts in certain directions).

This is the standard proof that **sublevel sets of convex functions are convex sets** — one of the most important facts in convex optimization.

# Gradients and Hessians of Quadratic Forms (H1r.pdf, Page 4)

### 5. Let \( a \in \mathbb{R}^n \) and let \( A \in \mathbb{R}^{n \times n} \) be a symmetric matrix.  
Compute the gradient and the Hessian of the functions  
\( f_1(x) = a^\top x \) and \( f_2(x) = x^\top A x \).

#### \( f_1(x) = a^\top x = a_1 x_1 + a_2 x_2 + \dots + a_n x_n \)

$$
\frac{\partial f_1}{\partial x_i} = a_i \quad \Longrightarrow \quad
\nabla f_1(x) = a, \qquad
\nabla^2 f_1(x) = O \quad \text{(the zero matrix)}.
$$

#### \( f_2(x) = x^\top A x \)

(We use symmetry of \( A \), i.e. \, a_{ij} = a_{ji} \). Example for \( n=2 \):)

$$
\begin{aligned}
f_2(x) &= \begin{bmatrix} x_1 & x_2 \end{bmatrix}
\begin{bmatrix} a_{11} & a_{12} \\ a_{12} & a_{22} \end{bmatrix}
\begin{bmatrix} x_1 \\ x_2 \end{bmatrix} \\
&= a_{11} x_1^2 + 2 a_{12} x_1 x_2 + a_{22} x_2^2.
\end{aligned}
$$

Partial derivatives:

$$
\frac{\partial f_2}{\partial x_1} = 2 a_{11} x_1 + 2 a_{12} x_2, \quad
\frac{\partial f_2}{\partial x_2} = 2 a_{12} x_1 + 2 a_{22} x_2.
$$

Thus

$$
\nabla f_2(x) = \begin{bmatrix}
2 a_{11} x_1 + 2 a_{12} x_2 \\
2 a_{12} x_1 + 2 a_{22} x_2
\end{bmatrix}
= 2 \begin{bmatrix} a_{11} & a_{12} \\ a_{12} & a_{22} \end{bmatrix}
\begin{bmatrix} x_1 \\ x_2 \end{bmatrix}
= 2 A x.
$$

Hessian:

$$
\nabla^2 f_2(x) = 2 A.
$$

**General rule (symmetric \( A \))**:

$$
\boxed{
\begin{aligned}
f(x) &= x^\top A x && \Longrightarrow &\quad \nabla f(x) = 2 A x \\
&& \Longrightarrow &\quad \nabla^2 f(x) = 2 A
\end{aligned}
}

\quad \text{(scalar case: } f(x)=a x^2 \;\; \nabla f = 2ax, \;\; \nabla^2 f = 2a \text{)}
$$

#### Standard quadratic objective (most common form in the course)

$$
f(x) = \frac{1}{2} x^\top A x - b^\top x
\qquad \Longrightarrow \qquad
\nabla f(x) = A x - b, \quad \nabla^2 f(x) = A.
$$




# Descent Directions & Exact Line Search Example (H1r.pdf, Page 5)**

### 6. Consider the function  
$$f(x_1,x_2) = (x_1 + x_2^2)^2.$$  
At the point $\bar{x} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$ we consider the search direction $p = \begin{bmatrix} -1 \\ 1 \end{bmatrix}$.  
Show that $p$ is a **descent direction** and find all minimisers of the line-search problem  
$$\min_{\alpha \in \mathbb{R}} f(\bar{x} + \alpha p).$$

#### Step 1: Gradient of $f$

$$
\nabla f(x) = 2(x_1 + x_2^2) \begin{bmatrix} 1 \\ 2x_2 \end{bmatrix}.
$$

At $\bar{x} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$:

$$
\nabla f(\bar{x}) = 2(1 + 0) \begin{bmatrix} 1 \\ 0 \end{bmatrix} = \begin{bmatrix} 2 \\ 0 \end{bmatrix}.
$$

Directional derivative:

$$
\nabla f(\bar{x})^\top p = \begin{bmatrix} 2 & 0 \end{bmatrix} \begin{bmatrix} -1 \\ 1 \end{bmatrix} = -2 < 0 \quad \Longrightarrow \quad p \text{ is a descent direction}.
$$

(Taylor expansion confirms: $f(\bar{x} + \alpha p) = f(\bar{x}) + \alpha \nabla f(\bar{x})^\top p + O(\alpha^2) < f(\bar{x})$ for small $\alpha > 0$.)

#### Step 2: Exact line search along the direction $p$

Parametrise the line:

$$
\bar{x} + \alpha p = \begin{bmatrix} 1 \\ 0 \end{bmatrix} + \alpha \begin{bmatrix} -1 \\ 1 \end{bmatrix} = \begin{bmatrix} 1 - \alpha \\ \alpha \end{bmatrix}.
$$

Substitute into $f$:

$$
\begin{align}
f(\bar{x} + \alpha p) &= ( (1 - \alpha) + \alpha^2 )^2 = (1 - \alpha + \alpha^2)^2 =: g(\alpha).
\end{align}
$$

Minimize $g(\alpha) = ( \alpha^2 - \alpha + 1 )^2$.

Derivative:

$$
g'(\alpha) = 2(\alpha^2 - \alpha + 1)(2\alpha - 1).
$$

Set $g'(\alpha) = 0$:

- $2\alpha - 1 = 0 \quad \Longrightarrow \quad \alpha = \frac{1}{2}$,
- or $\alpha^2 - \alpha + 1 = 0 \quad \Longrightarrow \quad \Delta = 1 - 4 = -3 < 0 \quad (\text{no real root})$.

Only critical point: $\alpha = \frac{1}{2}$.

Second derivative test or note $g(\alpha) > 0$ for all $\alpha$, so $g(\alpha)$ is convex → unique global minimum at $\alpha = \frac{1}{2}$.

Thus the **only minimiser** of the line-search problem is

$$
\alpha^* = \frac{1}{2}, \qquad \bar{x} + \alpha^* p = \begin{bmatrix} 1 - \frac{1}{2} \\ \frac{1}{2} \end{bmatrix} = \begin{bmatrix} \frac{1}{2} \\ \frac{1}{2} \end{bmatrix},
$$

with optimal value

$$
f\left( \frac{1}{2} + \left(\frac{1}{2}\right)^2 \right)^2 = \left( \frac{3}{4} \right)^2 = \frac{9}{16}.
$$

(Note: the global minimisers of $f$ are all points on the parabola $x_1 = -x_2^2$, where $f = 0$, but the line search only asks for the best point along this specific ray.)