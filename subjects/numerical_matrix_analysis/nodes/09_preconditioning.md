# Matrix Computations

**Marko Huhtanen**

## 9 Preconditioning

Typically different iterative methods for solving (52) behave quite similarly. Put in other words, if an iterative method converges slowly, it is unlikely that another iterative method would drastically differ in speed. (Bear also in mind what happened in Problem 32.) In situations like this one needs to **precondition** the linear system. This happens in most cases. What complicates things is the fact that there are many alternatives which speed up the convergence very differently. Therefore generating a preconditioner is not an easy task — it usually requires deep understanding of where the matrix A comes from.

Preconditioning means constructing an invertible matrix $M \in \mathbb{C}^{n \times n}$ which multiplies the original linear system (52) from the left

$$
M A x = M b = c \tag{75}
$$

(this is **left preconditioning**). One can also precondition from the right: solve $A M y = b$ and set $x = M y$.

The goal is to obtain a linear system (with the same solution) whose coefficient matrix $M A$ (or $A M$) has much more favourable spectral properties for an iterative method than the original $A$.

Ideally we would take $M = A^{-1}$, but computing and applying the exact inverse is far too expensive. Therefore $M$ must be a cheap approximation to $A^{-1}$: we want

- solving $M z = r$ to be very cheap (typically $O(n)$ or $O(n \log n)$ operations),
- $M \approx A^{-1}$ “in the directions that matter”.

In practice $M$ often does not appear explicitly — we only implement a routine that solves linear systems with $M$.

### 9.1 Classical iterative methods = explicit preconditioners

The oldest preconditioners come from **splitting** the matrix

$$
A = M_1 + M_2, \quad M = M_1^{-1}.
$$

The resulting iteration

$$
x_{k+1} = M^{-1} (b - M_2 x_k) = x_k + M^{-1} r_k
$$

converges if the spectral radius of the iteration matrix

$$
B = -M_1^{-1} M_2
$$

is smaller than 1:

$$
\rho(B) = \lim_{k \to \infty} \|B^k\|^{1/k} < 1.
$$

**Example 19 (Jacobi / damped Jacobi)**  
Take $M_1 = \operatorname{diag}(A) + \omega I$ with suitable $\omega \in \mathbb{C}$ (often $\omega = 0$). Then solving with $M_1$ costs $O(n)$ and the method is fully parallelisable. Convergence is very slow for most discretised PDEs.

**Example 20 (Gauss–Seidel / SOR / SSOR)**  
Order the unknowns and eliminate variable $x_i$ using only the already updated variables $x_1,\dots,x_{i-1}$. This corresponds to taking $M_1$ = lower triangular part of $A$ (including diagonal), possibly with a relaxation parameter $\omega$. Still $O(n)$ work per iteration, but sequential by nature.

These classical methods are rarely competitive today for large 3D problems, but they are simple, fully explicit, and useful as building blocks (smoothers) in multigrid.

### 9.2 Incomplete factorizations (ILU, IC, ...)

The most popular general-purpose preconditioners are **incomplete LU factorizations**. The idea is extremely simple:

1. Perform Gaussian elimination as usual,
2. but whenever a fill element appears outside a prescribed sparsity pattern, drop it.

Typical choices of allowed pattern:

- ILU(0): same sparsity pattern as $A$,
- ILU(p): allow p levels of fill,
- ILUT(τ, p): drop fill elements smaller than τ times the norm of the row and keep at most p largest.

The resulting approximate factors $\hat{L}$, $\hat{U}$ satisfy

$$
A = \hat{L} \hat{U} - E, \quad \|E\| \text{ hopefully small}.
$$

Then $M = \hat{L} \hat{U}$ is used as a preconditioner (never formed explicitly — only forward/back substitution with $\hat{L}$ and $\hat{U}$).

Advantages:
- Often very effective,
- Only two sparse triangular solves per iteration.

Disadvantages:
- No guaranteed existence or stability (pivoting restricted or forbidden),
- Fill-in can still be large,
- Difficult to parallelise.

For symmetric positive definite matrices one uses incomplete Cholesky (IC) instead of ILU.

### 9.3 Sparse approximate inverses (SPAI, FSAI, ...)

Instead of approximating a factorization of $A$, one directly minimises

$$
\|I - M A\|_F \quad \text{or} \quad \|I - A M\|_F
$$

subject to $M$ having a prescribed sparsity pattern (often just a few nonzeros per row). This yields independent small dense least-squares problems (one per row/column of $M$), which are easy to solve and fully parallel.

Advantages:
- Excellent parallelism,
- Application of $M$ is just a sparse matrix-vector product.

Disadvantages:
- Often less powerful than ILU,
- Memory can be an issue if too many nonzeros are allowed.

### 9.4 Algebraic multigrid (AMG)

For problems coming from discretised elliptic PDEs, geometric multigrid is extremely efficient, but requires the grid hierarchy. **Algebraic multigrid** builds a hierarchy purely from the matrix entries (using ideas from classical AMG: strong/weak connections, interpolation operators, etc.).

Very robust and efficient for many diffusion-type problems, but setup can be expensive and tuning is an art.

### 9.5 Domain-decomposition / Schwarz methods

Split the domain into overlapping or non-overlapping subdomains, solve local problems on subdomains, and glue the solutions together iteratively. Can be used as preconditioners for the Schur complement or as standalone iterative methods.

### 9.6 How to choose a preconditioner?

There is no universal answer. The best choice depends heavily on:

- Where does $A$ come from?
- Is it symmetric positive definite? Hermitian? Structured?
- Available parallelism?
- Acceptable setup time?

In practice one often starts with ILU(0) or damped Jacobi and moves to more sophisticated preconditioners (AMG, domain decomposition, approximate inverse, etc.) if needed.

**Problem 26** Implement the Jacobi iteration for a small 2D Poisson matrix (5-point stencil) and experiment with the optimal $\omega$.

**Problem 27** For the same matrix, implement Gauss–Seidel and SOR. Find (numerically) the optimal relaxation parameter for SOR.

### References (continued)

[1] M. Byckling and M. Huhtanen, Preconditioning with direct approximate factorization, SIAM J. Sci. Comput., 36(1), pp. A80–A104, 2014.

[4] A. Greenbaum, Iterative Methods for Solving Linear Systems, SIAM, Philadelphia, 1997.

[9] Y. Saad, Iterative Methods for Sparse Linear Systems, 2nd edition, SIAM, 2003 (freely available online).

[10] H. A. van der Vorst, Iterative Krylov Methods for Large Linear Systems, Cambridge University Press, 2003.

---
*This chapter continues the discussion of large-scale linear systems and focuses on practical preconditioning techniques used in modern iterative solvers.*