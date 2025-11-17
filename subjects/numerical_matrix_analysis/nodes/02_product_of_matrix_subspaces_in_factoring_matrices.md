# Matrix Computations

**Marko Huhtanen**

## 2 Product of matrix subspaces in factoring matrices

Factoring matrices is the way to solve small linear algebra problems. (Small is relative. It typically means that you can use a PC or some device you can easily access to finish the computations sufficiently fast.) Factoring provides a way to decompose the original problem into a sequence of simpler problems which can be solved fast each. The most well-known (and most important) case is that of solving a linear system

$$
Ax = b \tag{1}
$$

with a nonsingular matrix $A \in \mathbb{C}^{n \times n}$ and a vector $b \in \mathbb{C}^n$. The task is to find the vector $x$. As you probably remember, the solution can be obtained by the Gaussian elimination. This means, once you realize what you are doing, computing the LU factorization of $A$, i.e., $A$ is represented as (actually replaced with) the product

$$
A = LU, \tag{2}
$$

where $L$ is a lower triangular and $U$ an upper triangular matrix.² For the computational complexity, it requires $O(n^3)$ floating point operations to compute the LU factorization. With the help of the LU factorization, solving (1) is easy: Let $y = Ux$ be the new unknown vector. Then solve $Ly = b$ by forward substitution. (Easy!) Thereafter solve $Ux = y$ by back substitution. (Easy!)

In view of large scale problems and various applications, it is beneficial to approach factoring matrices more generally. A reason for this is that a large family of factoring problems can be formulated in a unified way, thereafter only the algorithm to solve your particular factoring problem remains to be chosen. Moreover, because of storage requirements and computational complexity, approximate factoring may be more realistic than factoring exactly. (In (2) approximate factoring could mean $A \approx \hat{L}\hat{U}$ for some computed upper and lower triangular matrices $\hat{L}$ and $\hat{U}$.) Then it is useful to have a general and sufficiently flexible formulation to solve this approximate factoring problem.

The notion of **matrix subspace** is a reasonably flexible structure to be used in factoring. That is, $V \subset \mathbb{C}^{n \times n}$ is a matrix subspace of $\mathbb{C}^{n \times n}$ over $\mathbb{C}$ (or $\mathbb{R}$) if

$$
\alpha V_1 + \beta V_2 \in V
\quad \text{whenever } \alpha,\beta \in \mathbb{C} \text{ (or } \mathbb{R}\text{)} \text{ and } V_1,V_2 \in V.
$$

Any subalgebra of $\mathbb{C}^{n \times n}$ is clearly also a subspace of $\mathbb{C}^{n \times n}$. (If $V$ is a subalgebra, you can sum and multiply matrices without leaving $V$.) Lower and upper triangular matrices are subalgebras of $\mathbb{C}^{n \times n}$. They provide an example of how fixing a sparsity pattern of matrices corresponds to a matrix subspace.

² Later on, we will see that partial pivoting is needed to compute $PA = LU$.

### Examples of matrix subspaces

**Example 1**  
The set of complex symmetric matrices consists of matrices $M \in \mathbb{C}^{n \times n}$ satisfying $M^T = M$. It is a matrix subspace of $\mathbb{C}^{n \times n}$ of dimension  
$n + (n-1) + \cdots + 1 = \frac{n(n+1)}{2}$.

In physics and chemistry problems you often have matrices of the following type.

**Example 2**  
The set of Hermitian matrices consists of matrices $M \in \mathbb{C}^{n \times n}$ satisfying $M^* = M$. It is a matrix subspace of $\mathbb{C}^{n \times n}$ over $\mathbb{R}$ of dimension  
$n + 2(n-1 + \cdots + 1) = n^2$.

**Example 3**  
The set of Toeplitz matrices consists of matrices $M \in \mathbb{C}^{n \times n}$ having constant diagonals. It is a matrix subspace of $\mathbb{C}^{n \times n}$ of dimension $2n-1$.

The structure you have in the LU factorization is the following.

**Definition 1**  
Assume $V_1$ and $V_2$ are matrix subspaces of $\mathbb{C}^{n \times n}$ over $\mathbb{C}$ (or $\mathbb{R}$). Their **set of products** is defined as

$$
V_1 V_2 = \{ V_1 V_2 : V_1 \in V_1 \text{ and } V_2 \in V_2 \}.
$$

A matrix subspace is a simple structure. The product of matrix subspaces is much richer, flexible and, in particular, far more useful.

With two matrix subspaces $V_1$ and $V_2$, basic questions arising in practice are the following. For a given $A \in \mathbb{C}^{n \times n}$, does

$$
A \in V_1 V_2 \;\;? \quad \text{If so, how to compute such a factorization of } A\,?
$$

Are the many ways? What is the computational complexity, i.e., how to compute the factorization fast? If we do not care about an exact factorization, how to approximate $A$ with an element of the set of products to have $A \approx V_1 V_2$? (All these questions arise with the LU factorization. Then $V_1$ consists of lower triangular matrices and $V_2$ of upper triangular matrices.)

**Problem 1**  
Show that a nonsingular $A \in \mathbb{C}^{n \times n}$ has an LU factorization if and only if it is **strongly nonsingular**³.

³ A matrix is strongly nonsingular if its principal minors are nonzero.

**Problem 2**  
Show that either $A \in \mathbb{C}^{n \times n}$ has an LU factorization or there is a matrix arbitrarily close to $A$ which has. (In other words, the closure of the set of products of lower and upper triangular matrices is whole $\mathbb{C}^{n \times n}$.)

Let us first focus on the singular value decomposition (SVD) which is used nowadays “everywhere” in applications. The reason for its popularity is not just its mathematical richness. Rather, it is the fact that algorithms exist, dating from the 60s, for efficiently computing it. The singular value decomposition is related with the problem of approximating a given matrix $A \in \mathbb{C}^{n \times n}$ with matrices of rank $k$ at most. (Such an abstract formulation sounds so unappealing that it is hard to believe that the SVD is of any use at all!) Such matrices can be expressed as the product of appropriate matrix subspaces defined in terms of their sparsity patterns.

**Definition 2**  
Matrices of rank $k$ at most in $\mathbb{C}^{n \times n}$ is the set of products $V_1 V_2$ where $V_1$ (resp. $V_2$) is the subspace of $\mathbb{C}^{n \times n}$ consisting of matrices having the last $n-k$ columns (resp. rows) zeros.

Matrices of rank $k$ at most in $\mathbb{C}^{n \times n}$ are denoted $F_k$. Of course, for $k < n$ such matrices are singular. (Remember: $A$ is nonsingular if and only if its nullspace $\{x : Ax = 0\}$ consists only of the zero vector.)

Matrix subspaces are “flat” and thereby very simple objects. Since $F_k$ is not a subspace, it is somewhat “curved”. It is not easy to geometrically try to visualize it. Algebraically, one can try to decompose $F_k$.

Namely, often one uses the **outer product** expression

$$
V_1 V_2 = [u_1 \; u_2 \; \cdots \; u_k \; 0 \; \cdots \; 0] 
\begin{bmatrix} v_1^* \\ v_2^* \\ \vdots \\ v_k^* \\ 0 \\ \vdots \\ 0 \end{bmatrix}
= \sum_{j=1}^k u_j v_j^* \tag{3}
$$

with $u_j, v_j \in \mathbb{C}^n$ for $j=1,\dots,k$, to represent matrices from $F_k$. Observe that an element of $F_k$ requires storing only $2nk$ complex numbers. This is extremely important whenever $k \ll n$, providing an example of a family of matrices that can be well compressed. (Compressing means that you need less storage than you expect from the outset.) This means that the rank-one matrices in the sum are not expressed as matrices explicitly unless necessary. Certain operations, such as computing matrix-vector products, are still possible (and less expensive) by using the expansion (3).

**Example 4**  
Matrices of the form $I + V_1 V_2$ are important as well, where $I \in \mathbb{C}^{n \times n}$ denotes the identity matrix and $V_1 V_2 \in F_k$. Historically they are related with integral equations. More importantly, they can be inverted quickly (whenever invertible) since their structure is preserved in inversion.

In the rank-one case, try this out by finding the scalar $\alpha \in \mathbb{C}$ that solves the equation

$$
(I + u_1 v_1^*)(I + \alpha u_1 v_1^*) = I.
$$

The cost is about one inner product. This is an example of a matrix which is very “easy” to invert, i.e., never use standard methods such as the Gaussian elimination with matrices of this form.

### 3 The singular value decomposition

The singular value decomposition solves the problem of approximating a matrix $A$ with matrices from $F_k$. To do such approximations, we need to measure the distance between two matrices. There are many ways of doing this. The (operator) norm of a matrix $A \in \mathbb{C}^{n \times n}$ is defined as

$$
\|A\| = \max_{\|x\|=1} \|Ax\|. \tag{4}
$$

It expresses how large at most can $A$ make unit vectors.⁴ Then the distance between two matrices $A, B \in \mathbb{C}^{n \times n}$ is simply $\|A - B\|$.

The singular value decomposition SVD has many applications. (The approach is completely analogous if $A$ is rectangular but not square.) Let us describe one application from the view point of data compression. When $A$ is stored on a computer, $n^2$ complex numbers must be kept in memory. Often this is supposed to be sent to another computer. When $n$ is very large, both of these tasks can cause serious problems. There are ways to try to approximate matrices somehow with fewer parameters, i.e., to compress $A$. In this process some information is lost. But if the loss is small, one can accept it.

The singular value decomposition is related with compression through the approximation problem

$$
\min_{F_k \in F_k} \|A - F_k\|, \tag{5}
$$

where the norm of a matrix was defined in (4).⁵ Bear in mind that an element of $F_k$ requires storing just $2nk$ complex numbers. Consequently, if for a small $k$ the value of (5) is small, then $A$ can be well compressed by using a matrix $F_k$. (There are many other techniques to compress matrices. In image processing such techniques are very important.)

Observe that in case of a compression when we do not have zero in (5), we are satisfied with an approximate factorization

$$
A \approx V_1 V_2 \tag{6}
$$

⁴ Unit vector is a vector of length one.  
⁵ This approximation problem can be formulated in Banach spaces, to measure compactness. It is just, in the Euclidean setting of $\mathbb{C}^n$ where the SVD happens to solve the problem.