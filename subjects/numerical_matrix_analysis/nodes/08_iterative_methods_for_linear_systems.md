# Matrix Computations

**Marko Huhtanen**

## 8 Iterative methods for linear systems

Next we consider ways to solve the linear system

$$
Ax = b \tag{52}
$$

for an invertible $A \in \mathbb{C}^{n \times n}$ and $b \in \mathbb{C}^n$ given when $n$ is large. By large is meant that direct methods such as the LU factorization of $O(n^3)$ and $O(n^2)$ storage are not acceptable. This $n$ is of order $O(10^4)$ or larger. (Floating point operations have been performed. In iterative methods one uses information based on matrix-vector products and the norm of (52). A rule of thumb is that a single iteration step should not cost more than $O(n)$ or $O(n \log n)$ floating point operations. The approximations (hopefully) improve step by step until sufficient.

Practically all the problems considered so far in these lecture notes appear for $n$ large. The large scale eigenvalue problem is encountered often. So is the task of computing the SVD. (Or, rather, some singular values and possibly related singular vectors.) Also the problem of applying the exponential of a very large matrix to a vector arises in practice.

**Example 18** One way of ranking pages of each web-page by executing Google's PageRank algorithm. This requires finding one eigenvector associated with the eigenvalue 1 of a so-called stochastic matrix. (Google matrix wikipedia" for more details.) The size of this matrix is enormous. That it is hopeless to solve this eigenvalue problem with classical techniques. Iterative methods is the only option. Large problems like this arise in information retrieval and data analysis when there is a lot of data. And that is often the case!

Instead of direct methods, in large scale problems one executes iterative methods. Iterative methods require a different mindset compared with when direct methods are used. By iterative methods we mean algorithms which are not based on factoring the coefficient matrix $A$, obtained after a finite number of floating point operations have been performed. In iterative methods one uses information based on matrix-vector products and the norm of (52). A rule of thumb is that a single iteration step should not cost more than $O(n)$ or $O(n \log n)$ floating point operations. The approximations (hopefully) improve step by step until sufficient.

The jth approximation $x_j$ satisfies $\|x - x_j\|$ decreasing as $j$ increases, and $\|A x_j - b\|$ decreasing.

Each iteration costs $O(n)$ or $O(n \log n)$.

If $A$ is sparse, then matrix-vector product is $O(n)$.

To solve $My = c$ with $M \in \mathbb{C}^{k \times j}$, $c \in \mathbb{C}^k$, $k \geq j$, this is a least squares problem $\min_{y \in \mathbb{C}^j} \|My - c\|_2$.

If $A$ is Hermitian, then use $A^*$.

$M = \{My : y \in \mathbb{C}^j\} \subset \mathbb{C}^n$

The method is based on Krylov subspaces.

$K_j(A; b) = \operatorname{span}\{b, Ab, A^2 b, \dots, A^{j-1} b\}$

$A K_j(A; b) \subset K_{j+1}(A; b)$

The GMRES method minimizes the residual over the Krylov subspace.

Use Arnoldi method to orthonormalize the basis.

The Arnoldi process:

$q_1 = b / \|b\|$

Then for $k=2,3,\dots$

$h_{k, k-1} q_k = A q_{k-1} - \sum_{l=1}^{k-1} h_{l, k-1} q_l$

where $h_{l, k-1} = (A q_{k-1}, q_l)$

Note that $h_{l, k-1} = (q_{k-1}, A q_l)$ if $A$ Hermitian.

This gives $A Q_j = Q_{j+1} \hat{H}_j$

where $Q_j = [q_1 \dots q_j] \in \mathbb{C}^{n \times j}$, $\hat{H}_j = \{h_{st}\} \in \mathbb{C}^{(j+1) \times j}$

Then the minimization $\min_{deg(p) \leq j-1} \|A p_{j-1}(A) b - b\| = \min_{y_j \in \mathbb{C}^j} \|\hat{H}_j y_j - \alpha e_1\|$, $\alpha = \|b\|$.

Then $x_j = Q_j y_j$

The process stops when $j = \dim K_j(A; b) = \dim K_{j+1}(A; b)$.

$r_j = b - A x_j$

If $j$ small, then solve the small least squares.

For convergence, if $A = I - B$ with $\|B\| < 1$, then residual bounded by $\|B\|^j / (1 - \|B\|)$

The Arnoldi process computes $\hat{H}_j$

$h_{k, k-1} = \|A q_{k-1} - \sum_{l=1}^{k-1} h_{l, k-1} q_l\|$

If $A Q_j = Q_j H_j$ with $H_j \in \mathbb{C}^{j \times j}$ upper Hessenberg.

If $j=n$, then $H_n$ is the Hessenberg form of $A$.

For convergence analysis, if $A = X \Lambda X^{-1}$, then bound with $\kappa(X)$ and min max |λ p(λ) - 1|

If normal, $\kappa=1$.

If $A = P D P^T$ with $P$ permutation, then consider min max |p(λ) - 1| over eigenvalues.

To shift, if $B = \lambda I + \mu A$, then $K_j(A; b) = K_j(B; b)$

For Hermitian positive definite $A$, the error in A-norm $\|x - x_j\|_A = (x - x_j, A (x - x_j))^{1/2}$

min $\|p_{j-1}(A) b - A^{-1} b\|_2^A = \|A p_{j-1}(A) b - b\|_{A^{-1}}$

The conjugate gradient method uses the A-inner product.

$q_1 = A b / \|A b\|_{A^{-1}} = A b / (A b, b)^{1/2}$

$\tilde{q}_1 = A^{-1} q_1 = b / (A b, b)^{1/2}$

The directions are A-conjugate.

The CG algorithm:

x_0 arbitrary, r_0 = b - A x_0, p_0 = r_0

for k=1,2,...

\alpha_k = (r_{k-1}, r_{k-1}) / (p_{k-1}, A p_{k-1})

x_k = x_{k-1} + \alpha_k p_{k-1}

r_k = r_{k-1} - \alpha_k A p_{k-1}

\beta_k = (r_k, r_k) / (r_{k-1}, r_{k-1})

p_k = r_k + \beta_k p_{k-1}

For normal A, similar.

If not Hermitian, use GMRES.

The problem with this is that the CG and MINRES methods can be expensive, since need to store all previous directions if restart.

The problem is to converge very slowly for the normal equations in realistic problems. (And, of course, we must be able to perform matrix-vector products with $A^*$ inexpensively.) Therefore, as a rule, using the normal equations are being avoided, at least when differential equations are being discretized.

Iterative methods applied to (52) when A has no special properties cannot be realized in short term recurrence. Methods such as BICGSTAB rely on a short term recurrence corresponding residuals. Methods such as BICGSTAB try to avoid the cost of storing the whole basis by using another method (like the Lanczos) but this can lead to breakdown.

For more details on iterative methods, see [4].

## 9 Preconditioning

Typically different iterative methods for solving (52) behave quite similarly. Put in other words, if an iterative method converges slowly, typically that another iterative method would drastically differ in speed. (Bear also in mind what happened in Problem 32.) In situations like this one needs to precondition the linear system. This happens in most cases. What complicates things is the fact that there are many alternatives which speed up the convergence very differently. Therefore generating a preconditioner is not an easy task as it requires computing a linear system.

Preconditioning means a construction of an invertible matrix $M \in \mathbb{C}^{n \times n}$ which multiplies the original linear system (52) from the left so as to have

$$
M A x = M b = c. \tag{75}
$$

This is called left preconditioning. There is an analogous way to precondition from the right: Solve $A M y = b$ and then set $x = M y$.

The purpose of preconditioning is to obtain a linear system (with the same solution as the original one) for which iterative methods converge substantially faster than for the original one.

To construct $M$ there is a balance. The goal is certainly clear. $M$ should approximate the inverse of $A$. However, the cost and storage required to have $M = A^{-1}$ is overwhelming and therefore completely out of the question. One should thus somehow compute an inexpensive approximation to the inverse of $A$.

In practice, $M$ may not appear explicitly. The reason for this is that one only needs to be able to perform matrix-vector products with it. (Recall that

The problem with this is that the CG and MINRES methods can be expensive.

Iterative methods applied to (52) when $A$ has no special properties cannot be realized in short term recurrence.

For more details on iterative methods, see [4].

### References

[1] M. Byckling and M. Huhtanen, Preconditioning with direct approximate factorization, SIAM J. Sci. Comput., 36(1), pp. A80-A104, 2014.

[2] Bai, Z., Demmel, J., Dongarra, J., Ruhe, A., van der Vorst, H. (eds.): Templates for the Solution of Algebraic Eigenvalue Problems: A Practical Guide, SIAM, Philadelphia (2000)

[3] G.H. Golub and C.F. Van Loan, Matrix Computations, The Johns Hopkins University Press, the 3rd ed., 1996.

[4] A. Greenbaum, Iterative Methods for Solving Linear Systems, SIAM, Philadelphia, 1997.

[5] B. Parlett, The Symmetric Eigenvalue Problem, Classics in Applied Mathematics 20, SIAM, Philadelphia, 1997.

[6] SPAL, http://www.computational.uni-bsch.ch/software/spai/

[7] Y. Saad, Numerical Methods for Large Eigenvalue Problems, 2nd edition, SIAM Philadelphia 2011.

[8] L.N. Trefethen and D. Bau, III, Numerical Linear Algebra, SIAM Philadelphia, 1997.

---

*Page 1 of original notes contains big-O complexity and problem statement for large linear systems.*

*Page 2 contains least squares formulation and Krylov subspace introduction.*

*Page 3 contains QR decomposition in Arnoldi process and example data points.*

*Page 4 contains polynomial approximation and convergence bounds.*

*Page 5 contains continuation of Arnoldi algorithm.*

*Page 6 contains LU factorization discussion (from previous section).*

*Page 7 contains convergence analysis.*

*Page 8 contains more on Arnoldi and minimization.*

*Page 9 contains dual basis for CG.*

*Page 10 contains CG formulation and preconditioning intro.*

*Page 11 contains preconditioning and references.*