# Matrix Computations

**Marko Huhtanen**

## 7 Using the structure in computations: Cholesky factorization, Sylvester equation and FFT

To solve a linear system (1), we know now that it can be done reliably at the cost of $O(n^3)$ floating point operations (flops) requiring storing $n^2$ numbers. This is the "worst scenario" in the sense that it can only be improved. (With a linear system one should always ask, do I really need the LU factorization or is there a much faster way?) An improvement requires that the linear system has some special structure. This is often the case in applications. We illustrate this with three very different examples: the Cholesky factorization, the Sylvester equation and the use of the FFT, the so-called fast Fourier transform. Each of these cases rely on entirely different ideas.

The Cholesky factorization replaces the LU factorization if the matrix is positive definite. It simply means computing the LU factorization by keeping in mind (and using it at every step) that $A$ is positive definite.

**Definition 10** A matrix $A \in \mathbb{C}^{n \times n}$ is **positive definite** if it is Hermitian and satisfies

$$
(Ax, x) > 0
$$

for any nonzero $x \in \mathbb{C}^n$.

Problems related with energy minimization typically involve positive definite matrices. (In physics, there is no lack of such problems!) Unless you know from your application that $A$ must be positive definite, this definition is not very practical.

**Example 17** In optimization you encounter problems involving functions

$$
f: \mathbb{R}^n \to \mathbb{R}, \quad f(x) = x^* A x + b^* x + c,
$$

where $A \in \mathbb{R}^{n \times n}$ is positive definite, $b \in \mathbb{R}^n$ and $c \in \mathbb{R}$. The minimum of $f$ is attained at $x$ solving $A x = -b/2$. (Since $A$ is Hermitian, this is a symmetric matrix.)

**Problem 17** Show that a Hermitian matrix is positive definite if and only if its eigenvalues are strictly positive. Moreover, show that if $A$ is positive definite and $M$ is invertible, then $M A M^*$ is positive definite.

Suppose $A \in \mathbb{C}^{n \times n}$ is positive definite. Write it in block form

$$
A = \begin{bmatrix} a_{11} & a^* \\ a & B \end{bmatrix}
$$

with $a \in \mathbb{C}^{n-1}$. Take $x = e_1$. Then $a_{11} > 0$ since $A$ is positive definite. Set

$$
A = \begin{bmatrix} \alpha & 0 \\ a/\alpha & I \end{bmatrix}
\begin{bmatrix} 1 & 0 \\ 0 & B - a a^*/a_{11} \end{bmatrix}
\begin{bmatrix} \alpha & a^*/\alpha \\ 0 & I \end{bmatrix}
= R_1 A_1 R_1^*
$$

with $\alpha = \sqrt{a_{11}}$. Then $A_1 = B - a a^*/a_{11}$ is positive definite of order $(n-1) \times (n-1)$ (why?).

**Problem 18** Show that the submatrix $B - a a^*/a_{11}$ is positive definite.

Continuing this way we obtain $A = R_1 R_2 \cdots R_n I R_n^* \cdots R_2^* R_1^* = R R^*$, where $R = R_1 \cdots R_n$ is upper triangular. This is called the **Cholesky factorization** of $A$. The matrix $R$ requires storing $n^2/2$ numbers. The complexity is $\approx \frac{1}{3} n^3$ flops.

**Proposition** Assume $A \in \mathbb{C}^{n \times n}$ is positive definite. Then the Cholesky factorization exists.

**Proof.** The Cholesky factorization can be computed recursively. We have shown that if $A$ is positive definite, then $A_1$ is positive definite. The rest follows by induction.

Suppose $A \in \mathbb{C}^{n \times n}$ is Hermitian. Then from the SVD of $R$ we have $R = U \Sigma V^*$, so that $A = U \Sigma^2 U^*$. This is the spectral factorization of $A$. If $A$ is positive definite, then $\Sigma^2 > 0$.

### 7.1 The Sylvester equation

Given $A, B, C \in \mathbb{C}^{n \times n}$, find $X \in \mathbb{C}^{n \times n}$ satisfying

$$
A X - X B = C. \tag{37}
$$

This is called the **Sylvester equation**. The map

$$
X \mapsto A X - X B
$$

is linear from $\mathbb{C}^{n \times n}$ to $\mathbb{C}^{n \times n}$. It has dimension $n^2$ and is invertible if the spectra of $A$ and $B$ are disjoint. The complexity is $O(n^3)$ (but $2$ or $3 n^6$ with naive methods).

The eigenvalue problems (16) and (18) are solved by equivalence transformations defined as follows.

**Definition 5** Matrix subspaces $V$ and $W$ are said to be equivalent if there exist invertible matrices $X, Y$ such that $W = X V Y^{-1}$.

The purpose of equivalence transformation is to produce a "simpler" matrix subspace $W$ for which all the relevant information is readily available. For the eigenvalue problems this means either diagonal or upper triangular matrices. Then the eigenvalues can be found by inspecting the diagonal entries only.

It is of importance that if there are nonsingular elements in $V$, then most of them are. This means that it is very hard then to find a singular matrix in $V$. (We know this from the eigenvalue problem. It is not easy to find the eigenvalues!)

**Proposition 1** Suppose there are nonsingular elements in a matrix subspace $V$. Then the set of nonsingular elements is open and dense.

**Proof.** One can show that $V$ can be identified with $\mathbb{C}^k$ (or $\mathbb{R}^k$), where $k$ is its dimension. Its is clear that $V(p)$ is a closed set in $\mathbb{C}^k$ (or $\mathbb{R}^k$). It cannot have interior points either. Namely, if $\{z_1, \dots, z_k\}$ were an interior point, then fix $z_2, \dots, z_k$ and regard $p$ as a polynomial in the one variable $z_1$. It has a finite number of zeros. Thereby an arbitrary small perturbation yields a nonzero value. End of proof.

Let us now focus on those matrix subspaces which allow fast solving algorithmically. There are two types of nonsingular matrix subspaces. To see this, we start by recalling how the LU factorization is computed. The general case is really not much different.

Suppose $A \in \mathbb{C}^{n \times n}$ is invertible. Let us denote it by $A = V_1 V_2^{-1}$. Assume $V_1$ and $V_2$ are matrix subspaces where one is invertible. Let us first suppose $V_2$ is invertible with the inverse $W$. Suppose $A \in \mathbb{C}^{n \times n}$ is nonsingular and the task is to recover whether $A \in V_1 V_2$. Clearly, $A = V_1 V_2$ holds if and only if

$$
A W = V_1 \tag{21}
$$

for some nonsingular $W \in W$. This latter problem is linear and thereby completely solvable. (If a problem is linear, it can be solved in a finite number of flops.) Once done, we obtain the factorization $A = V_1 W^{-1}$.

To this accomplish this task, we will use projections. Recall that a linear operator $P$ on a vector space is a projection if $P^2 = P$. A projector moves points onto its range and acts like the identity operator on the range. (The range means the subspace $R(P) = \{ y : y = P x \text{ for some } x \}$). Such operators are of importance in numerical computations and approximation.

In the so-called dimension reduction approximation, the task is to find in some sense a good projector which is used to replace the original problem with a problem of much smaller dimension. Observe that if $P$ is a projector, then so is $I - P$.

It is preferable to use orthogonal projectors since they take the shortest path while moving points to the range. This requires that the vector space is equipped with an inner product (and thus has the notion of orthogonality). We say that $P$ is an orthogonal projector if

$$
R(P) \perp R(I - P),
$$

i.e., the range of $P$ is orthogonal to the range of $I - P$. Orthogonality requires using an inner product. Since we are interested in matrix subspaces, on $\mathbb{C}^{n \times n}$ we use (14).

After all this theory, fortunately there is an easy way of constructing an orthogonal projector onto a given subspace. Take an orthonormal basis $q_1, \dots, q_k$ of the subspace. Then set

$$
P x = \sum_{j=1}^k q_j (x, q_j). \tag{25}
$$

It is rare that an orthonormal basis is available, i.e., having an orthonormal basis requires taking a basis of the subspace and orthonormalizing it. Typically the Gram-Schmidt process is needed here.

Let us now focus on matrix subspaces and orthogonal projectors onto them. Occasionally orthogonal projectors onto familiar matrix subspaces are readily available without invoking the Gram-Schmidt process to have (25). The orthogonal projector on $\mathbb{C}^{n \times n}$ onto the set of Hermitian matrices is given by

$$
P A = \frac{1}{2} (A + A^*). \tag{26}
$$

(Because the set of Hermitian matrices is a subspace over $\mathbb{R}$, use (15).) This is the so-called Hermitian part of a matrix $A$. Similarly, onto the set of complex symmetric matrices the orthogonal projector acts according to

$$
P A = \frac{1}{2} (A + A^T). \tag{27}
$$

These are very simple to apply.

**Problem 12** Suppose $P$ is a projection. Then show that $P$ is an orthogonal projection if the operator norm $\|P\| = 1$ if for every $x$ holds $\|x\|^2 = \|(I - P)x\|^2 + \|P x\|^2$.

A matrix is called standard if there is exactly one entry which equals 1 while other entries equal zero. A matrix subspace $V$ is called standard if it has a basis consisting of standard matrices. This simply means that there are $n^2$ interdependencies between the entries of $V \in V$. In this case the orthogonal projector $P$ onto $V$ acts such that $P A$ simply replaces with zeros those entries of $A$ which are outside the sparsity structure of $V$. (You can also see this by using (25).) Other entries of $A$ are kept intact. For example, if the matrix subspace is the set of diagonal matrices, $P A$ equals the diagonal matrix whose diagonal is that of $A$.

**Definition 8** The sparsity structure of a matrix subspace $V$ means the location of those entries which are nonzero for some $V \in V$.

Observe that any matrix $M$ decomposes as

$$
M = P M + (I - P) M.
$$

If $(I - P) M = 0$, then $M \in R(P)$.

To factor $A = V_1 V_2$, the idea is the following. Construct an orthogonal projector $P_1$ onto $V_1$. Solve the linear least squares problem

$$
\min_W \| (I - P_1) A W \|
$$

to have $(I - P_1) A W \approx 0$. This yields $W$ such that $A W \approx V_1$. Set $V_1 = P_1 A W$. Then $A \approx V_1 W^{-1}$.

Similarly, one can start from the right by constructing an orthogonal projector $P_2$ onto $V_2$ and solving

$$
\min_W \| (I - P_2) W A \|
$$

to have $W A \approx V_2$. Then $A = W^{-1} V_2$.

For the LU factorization, $V_1$ is lower triangular, $V_2$ upper triangular. Then the equations become small linear systems.

**Example** Take

$$
A = \begin{bmatrix} \varepsilon & 1 \\ 1 & 1 \end{bmatrix}.
$$

When $\varepsilon \to 0$ we have a nearby singular matrix. One possible factorization is

$$
A = \begin{bmatrix} 1 & 0 \\ 1/\varepsilon & 1 \end{bmatrix} \begin{bmatrix} \varepsilon & 1 \\ 0 & 1 - 1/\varepsilon \end{bmatrix}.
$$

The factor on the right becomes huge when $\varepsilon \to 0$.

The approximation error satisfies

$$
\|A - V_1 W^{-1}\| \leq \|W^{-1}\| \cdot \|A W - V_1\| \leq \kappa(W) \cdot \|(I - P_1) A W\|
$$

where the condition number

$$
\kappa(W) = \|W\| \|W^{-1}\|
$$

of $W$ which scales the accuracy of the approximations. This is no accident. The condition number appears often in assessing accuracy of numerical linear algebra computations. From the SVD of $W$ one obtains $\kappa(W) = \sigma_1 / \sigma_n$.

The eigenvalue problems (16) and (18) are solved by equivalence transformations defined as follows.

A matrix subspace $V$ is said to be equivalent to $W$ if there exist invertible matrices $X, Y$ such that $W = X V Y^{-1}$.

And call it the set of inverses of $V$. It is not easy to characterize this set in general. Like $F_k$, it is somewhat "curved". The structure you have in the lower triangular case is of the following type.

**Definition 6** A matrix subspace $V$ is said to be invertible if there exists a nonsingular matrix $W$ such that

$$
\operatorname{Inv}(V) = \{ W : W \in W, \det W \neq 0 \}.
$$

This means that the set of inverses is a matrix subspace, aside from those matrices which are singular. Or, in other words, the closure of $\operatorname{Inv}(V)$ is a matrix subspace. These matrix subspaces are nice to work with.

It is easy to see that $W$ is unique. Let us denote it by $V^{-1}$ and call all the inverse of $V$.

Returning to the case of LU factorization, the set of lower (upper) triangular matrices of $\mathbb{C}^{n \times n}$ containing invertible elements. (Subalgebras means that we can sum and multiply matrices without leaving the set.) The inverse is the set of lower

$$
L^{-1} = U
$$

is an upper triangular matrix. (Actually, this $L^{-1}$ never explicitly formed.) Then the fact that the inverse of a nonsingular lower triangular matrix is a lower triangular matrix is used to conclude that this actually yields an LU factorization $A = L U$ of $A$.

This approach works more generally once we identify the relevant idea that made the LU factoring possible. First, for a nonsingular subspace $V$, we have

$$
\operatorname{Inv}(V) = \{ V^{-1} : V \in V, \det V \neq 0 \}.
$$

After all this theory, fortunately there is an easy way of constructing an orthogonal projector onto a given subspace. Take an orthonormal basis $q_1, \dots, q_k$ of the subspace. Then set

$$
P x = \sum_{j=1}^k q_j (x, q_j).
$$

**Problem 19** Suppose $T \in \mathbb{C}^{k \times k}$ is upper triangular. Devise a method to perform matrix-vector products with $C \in \mathbb{C}^{n \times n}$ with $n = 2^l \geq k$ containing $T$ as its block. Then products with $T$, i.e., lower dimensional matrix-vector products appropriately with $C$ to have matrix-vector products with $T$.

There are also fast algorithms for solving linear systems involving Toeplitz matrices [3].

### 8 Iterative methods for linear systems

Next we consider ways to solve the linear system

$$
A x = b \tag{52}
$$

for an invertible $A \in \mathbb{C}^{n \times n}$ and $b \in \mathbb{C}^n$ given when $n$ is large. By large is meant that direct methods such as the LU factorization of $O(n^3)$ and $O(n^2)$ storage are not acceptable. This $n$ is of order $O(10^4)$ or larger. (Floating point operations have been performed. In iterative methods one uses information based on matrix-vector products and the norm of (52). A rule of thumb is that a single iteration step should not cost more than $O(n)$ or $O(n \log n)$ floating point operations. The approximations (hopefully) improve step by step until sufficient.

The singular value decomposition solves the problem of approximating a matrix $A$ with matrices of rank $k$ at most can a make unit vector. The distance between two matrices $A, B \in \mathbb{C}^{n \times n}$ is simply $\|A - B\|$.

The singular value decomposition SVD has many applications. (The approach is completely analogous if $A$ is rectangular but not square.) Let us describe one application from the view point of data compression. When $A$ is stored on a computer, $n^2$ complex numbers must be kept in memory. Often this is supposed to be sent to another computer. When $n$ is very large, both of these tasks can cause serious problems. There are ways to try to approximate matrices somehow with fewer parameters, i.e., to compress $A$. In this process some information is lost. But if the loss is small, one can accept it.

The singular value decomposition is related with compression through the approximation problem

$$
\min_{F_k \in F_k} \|A - F_k\|, \tag{5}
$$

where the norm of a matrix was defined in (4). Bear in mind that an element of $F_k$ requires storing just $2 n k$ complex numbers. Consequently, if for a small $k$ the value of (5) is small, then $A$ can be well compressed by using a matrix $F_k$. (There are many other techniques to compress matrices. In image processing such techniques are very important.)

Observe that in case of a compression when we do not have zero in (5), we are satisfied with an approximate factorization

$$
A \approx V_1 V_2 \tag{6}
$$

Unit vector is a vector of length one.

This approximation problem can be formulated in Banach spaces, to measure compactness. It is just, in the Euclidean setting of $\mathbb{C}^n$ where the SVD happens to solve the problem.

Solving (5) clearly does not look easy. It can be done with the help of the **singular value decomposition**. Before defining the SVD, recall that a matrix $Q \in \mathbb{C}^{n \times n}$ is **unitary** if its columns are orthonormal, i.e.,

$$
Q^* Q = I \Leftrightarrow \|Q x\| = \|x\| \quad \text{for all } x \in \mathbb{C}^n. \tag{7-8}
$$

**Example 5** There are a lot of unitary matrices. Unitary matrices can be generated easily once you invoke the Gram-Schmidt process. That is, take any linearly independent $b_1, \dots, b_n \in \mathbb{C}^n$ and orthonormalize them to have $q_1, \dots, q_n$. Then put $Q_n = [q_1 \cdots q_n]$.

**Definition 3** The **singular value decomposition** of $A \in \mathbb{C}^{n \times n}$ is a factorization

$$
A = U \Sigma V^* \quad \text{with unitary } U, V \in \mathbb{C}^{n \times n} \text{ and diagonal } \Sigma \in \mathbb{C}^{n \times n}
$$

with the **singular values** satisfying

$$
\sigma_1 \geq \sigma_2 \geq \cdots \geq \sigma_n \geq 0.
$$

Linear algebraically this means that there exist orthonormal bases such that the associated linear map $A: \mathbb{C}^n \to \mathbb{C}^n$ can be represented with a diagonal matrix in these bases.

**Problem 3** Assume $A \in \mathbb{C}^{n \times n}$ is nonsingular. Show that orthonormalizing its columns with the Gram-Schmidt process starting from the leftmost column is equivalent to computing a representation $A = Q R$ with $Q$ unitary and $R$ upper triangular with positive diagonal entries. (This is called the **QR factorization** of $A$.)

Recall that unitary matrices appear also in connection with the Hermitian eigenvalue problem. (Here we assume you have taken an undergraduate linear algebra course.)

**Problem 4** Assume $A \in \mathbb{C}^{n \times n}$ is Hermitian, i.e., $A^* = A$. Show that $A$ can be unitarily diagonalized, i.e.,

$$
A = U \Lambda U^* \quad \text{with unitary } U \in \mathbb{C}^{n \times n} \text{ and diagonal } \Lambda \in \mathbb{C}^{n \times n}. \tag{9}
$$

(Hint: show first that eigenvectors related to differing eigenvalues are orthogonal.)

That there exists a singular value decomposition is based on inspecting the eigenvalue problem for $A^* A$. Since $A^* A$ is Hermitian, it can be unitarily diagonalized as

$$
A^* A = V \Lambda V^*.
$$

Take this to be our $V$. Assume now that the eigenvalues are ordered non-increasingly. (Note that $A^* A$ is positive semidefinite, i.e., its eigenvalues are nonnegative.) Take any eigenvectors $v_j$ and $v_l$ of $A^* A$. Then $A v_j$ and $A v_l$ are orthogonal by the fact that

$$
(A v_j, A v_l) = (v_j, A^* A v_l) = (v_j, \lambda_l v_l) = 0 \quad \text{if } \lambda_j \neq \lambda_l.
$$

Consequently, take the columns of $U$ to be

$$
u_j = \frac{A v_j}{\sqrt{\lambda_j}} = \frac{A v_j}{\sigma_j} \quad \text{for nonzero eigenvalues } \lambda_j \text{ of } A^* A.
$$

For zero eigenvalues $\lambda_j$ of $A^* A$, just take any remaining eigenvectors in the null space of $A$ by (10). Corresponding to these, take any set of orthonormal vectors in the orthogonal complement of the vectors. For them, the corresponding singular values are zeros.

Because of (8) we have

$$
\|A\| = \|U \Sigma V^*\| = \|\Sigma\| \Rightarrow \|A\| = \sigma_1. \tag{12}
$$

For diagonal matrices the norm is easy to compute and we obtain $\|A\| = \sigma_1$. So the first singular value of $A$ is unique. Equally importantly, it is the singular value decomposition which yields the best way of finding the norm of $A$.

**Problem 5** Show that for a diagonal matrix the norm is the maximal absolute value of its diagonal entries. (Observe that you can restrict the computations to real numbers.)

Repeating these arguments yields the fact that the singular values of a matrix are uniquely determined.

**Problem 6** Show that the singular values of a matrix $A \in \mathbb{C}^{n \times n}$ are unique.

Without resorting to (12) it would be very challenging to compute the norm of $A$. In particular, if you use other than the Euclidean norm in $\mathbb{C}^n$, then you have this challenge. (And numerous other challenges.) So the reason for not using the Euclidean norm should be exceptionally good!

**Theorem 1** Let $A \in \mathbb{C}^{n \times n}$. Then the value of the minimization problem (5) is $\sigma_{k+1}$.

**Proof.** The value of (5) is at most $\sigma_{k+1}$. This is seen by using the singular value decomposition of $A$ and forming $F_k$ by setting $\sigma_{k+1} = \cdots = \sigma_n = 0$. (This corresponds to replacing the $n-k$ last columns of $U$ and rows of $V^*$ with zeros.) Then

$$
F_k = \sum_{j=1}^k \sigma_j u_j v_j^*. \tag{13}
$$

Let us outline that $\sigma_{k+1}$ is actually the minimum. Consider $V_1 V_2 \in F_k$ realizing (5). Let $w_1^*, \dots, w_k^*$ be the nonzero rows of $V_2$. Then choose a unit vector $v$ which is a linear combination of $v_1, \dots, v_{k+1}$ which is in the orthogonal complement of $w_1, \dots, w_k$. (For this, find a nonzero solution to a $k$-by-$(k+1)$ homogeneous linear system involving the matrix $[w_j^* v_l]_{j=1,\dots,k, l=1,\dots,k+1}$.) Then $(A - V_1 V_2) v = A v$ and its norm is at least $\sigma_{k+1}$. This means that span of $w_1^*, \dots, w_k^*$ equals the span of $v_1^*, \dots, v_k^*$. Arguing similarly with $A^*$ we may conclude that the span of columns of $V_1$ equals the span of $u_1, \dots, u_k$. From this it follows that the best choice is (13). End of proof. ∎

The solution (13) constructed from the singular value decomposition solves the minimization problem (5) actually in any unitarily invariant norm. A norm $\|\cdot\|$ on $\mathbb{C}^{n \times n}$ is said to be unitarily invariant if for any $A \in \mathbb{C}^{n \times n}$ holds

$$
\|A\| = \|Q_1 A Q_2\|
$$

for any unitary $Q_1, Q_2 \in \mathbb{C}^{n \times n}$. Aside from the operator norm, the **Frobenius norm** $\|\cdot\|_F$ is often used in practice, due to its computational convenience. The Frobenius norm is induced by the inner product

$$
(A, B) = \operatorname{trace}(B^* A) \tag{14}
$$

on $\mathbb{C}^{n \times n}$. When dealing with matrix subspaces over $\mathbb{R}$, use

$$
(A, B) = \operatorname{Re} \operatorname{trace}(B^* A). \tag{15}
$$

The trace is computed by summing the diagonal entries of the matrix. This simply means that $\mathbb{C}^{n \times n}$ is treated as $\mathbb{C}^{n^2}$ using the standard inner product.

**Theorem** 

$$
\|A\|_F = \sqrt{\sum_{j=1}^n \sum_{k=1}^n |a_{jk}|^2}.
$$

This is clearly an easy computation whereas computing $\|A\|$ is much more involved requiring the largest singular value of $A$.

**Example 6** There are situations where the SVD is used in analyzing data. This may also take place for the data is manipulated. (By “data” we mean the matrix $A$ you have somehow generated in your application.) This can be done in many ways. Principal component analysis is an approach in statistics to analyze data by splitting it into parts as follows. Let $e = (1,1,\dots,1)^T \in \mathbb{C}^n$. The process is simply an SVD approximation after the data has been mean centered, i.e., translated by taking $A - e \alpha^*$ for some $\alpha \in \mathbb{C}^n$ where the $j$th component of $\alpha$ is the average

$$
\alpha_j = \frac{1}{n} \sum_{l=1}^n a_{l j}.
$$

The $j$th column of $A$ is mean corrected. Often one approximates $A \approx e \alpha^* + F_k$ for small $k$ (i.e., a constant column plus a low-rank correction). This is the essence of many data-analysis techniques.

Matrices of the form $I + u v^*$ ($u,v \in \mathbb{C}^n$) are called **rank-one updates** of the identity. They are extremely important in numerical linear algebra (e.g., in Krylov methods, quasi-Newton methods, etc.).

In the rank-one case, try this out by finding the scalar $\alpha \in \mathbb{C}$ that solves the equation

$$
(I + u_1 v_1^*)(I + \alpha u_1 v_1^*) = I.
$$

The cost is about one inner product. This is an example of a matrix which is very “easy” to invert, i.e., never use standard methods such as the Gaussian elimination with matrices of this form.

Another very common situation is to consider shifts of a matrix:

$$
A - \alpha I, \quad \alpha \in \mathbb{C}.
$$

One often approximates $A \approx \alpha I + F_k$ for some low-rank $F_k$.

Matrices arise in applications such as discretizing PDE, optimization, representing graphs, digitalizing images, storing data etc. Once the matrix is stored on a computer¹ (or on several computers), the underlying problem remains

¹ Computer means any device that performs arithmetic operations.

not at any cost since you cannot afford it). This is a typical situation. This type of “very large scale problems” appear everywhere and they must be solved in one way or the other and as fast as possible.

From the 70s iterative methods started seriously gaining ground to solve very large linear algebra problems without $O(n^3)$ complexity and $O(n^2)$ storage requirement. Analogous developments are still going on in every area of numerical analysis. As a rule, in exciting iterative methods, the matrix (or matrices) related with the problem cannot be manipulated freely. For example, it may be that matrix-vector products with the matrix is the only information available, although you certainly want to avoid such an extreme. However, mathematically this means that the underlying assumptions are getting closer to those usually made in, let us say, operator theory. To get an idea what this could imply as opposed to studying classical matrix analysis, assuming having the Hermitian transpose may be unrealistic.

A reason for writing these lecture notes is the hope of being able to combine classical matrix analytic techniques with those mathematical ideas that are useful in solving practical problems and developing new algorithms. Occasionally this means that the viewpoint is slightly abstract. The abstractness is, however, not an aim. After all, computations are at center of this course and that means that at some point one must come up with an algorithm to solve the problem. A purpose of this course is that the student can, with self confidence, enter and deal with applications where matrices appear.

It is assumed that the students have learnt undergraduate linear algebra and know things such as the Gram-Schmidt orthogonalization process, the Gaussian elimination and know basics of the eigenvalues and eigenvectors, like how to solve tiny (2-by-2 or 3-by-3) eigenvalue problems by hand. One should also be familiar with the standard Euclidean geometry of $\mathbb{C}^n$ originating from the inner product

$$
(x,y) = y^* x = \sum_{j=1}^n x_j \bar{y}_j \qquad x,y \in \mathbb{C}^n.
$$

(This is, of course, needed in the Gram-Schmidt orthogonalization.)

## 2 Product of matrix subspaces in factoring matrices

Factoring matrices is the way to solve small linear algebra problems. (Small is relative. It typically means that you can use a PC or some device you can easily access to finish the computations sufficiently fast.) Factoring provides a way to decompose the original problem into a sequence of simpler problems which can be solved fast each. The most well-known (and most important) case is that of solving a linear system

$$
A x = b \tag{1}
$$

with a nonsingular matrix $A \in \mathbb{C}^{n \times n}$ and a vector $b \in \mathbb{C}^n$. The task is to find the vector $x$. As you probably remember, the solution can be obtained by the Gaussian elimination. This means, once you realize what you are doing, computing the LU factorization of $A$, i.e., $A$ is represented as (actually replaced with) the product

$$
A = L U, \tag{2}
$$

where $L$ is a lower triangular and $U$ an upper triangular matrix.² For the computational complexity, it requires $O(n^3)$ floating point operations to compute the LU factorization. With the help of the LU factorization, solving (1) is easy: Let $y = U x$ be the new unknown vector. Then solve $L y = b$ by forward substitution. (Easy!) Thereafter solve $U x = y$ by back substitution. (Easy!)

In view of large scale problems and various applications, it is beneficial to approach factoring matrices more generally. A reason for this is that a large family of factoring problems can be formulated in a unified way, thereafter only the algorithm to solve your particular factoring problem remains to be chosen. Moreover, because of storage requirements and computational complexity, approximate factoring may be more realistic than factoring exactly. (In (2) approximate factoring could mean $A \approx \hat{L} \hat{U}$ for some computed upper and lower triangular matrices $\hat{L}$ and $\hat{U}$.) Then it is useful to have a general and sufficiently flexible formulation to solve this approximate factoring problem.

The notion of **matrix subspace** is a reasonably flexible structure to be used in factoring. That is, $V \subset \mathbb{C}^{n \times n}$ is a matrix subspace of $\mathbb{C}^{n \times n}$ over $\mathbb{C}$ (or $\mathbb{R}$) if

$$
\alpha V_1 + \beta V_2 \in V \quad \text{whenever } \alpha, \beta \in \mathbb{C} \text{ (or } \mathbb{R}\text{) and } V_1, V_2 \in V.
$$

Any subalgebra of $\mathbb{C}^{n \times n}$ is clearly also a subspace of $\mathbb{C}^{n \times n}$. (If $V$ is a subalgebra, you can sum and multiply matrices without leaving $V$.) Lower and upper triangular matrices are subalgebras of $\mathbb{C}^{n \times n}$. They provide an example of how fixing a sparsity pattern of matrices corresponds to a matrix subspace.

² Later on, we will see that partial pivoting is needed to compute $P A = L U$.

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

Matrices of rank $k$ at most in $\mathbb{C}^{n \times n}$ are denoted $F_k$. Of course, for $k < n$ such matrices are singular. (Remember: $A$ is nonsingular if and only if its nullspace $\{x : A x = 0\}$ consists only of the zero vector.)

Matrix subspaces are “flat” and thereby very simple objects. Since $F_k$ is not a subspace, it is somewhat “curved”. It is not easy to geometrically try to visualize it. Algebraically, one can try to decompose $F_k$.

Namely, often one uses the **outer product** expression

$$
V_1 V_2 = [u_1 \ u_2 \ \cdots \ u_k \ 0 \ \cdots \ 0] \begin{bmatrix} v_1^* \\ v_2^* \\ \vdots \\ v_k^* \\ 0 \\ \vdots \\ 0 \end{bmatrix} = \sum_{j=1}^k u_j v_j^* \tag{3}
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
\|A\| = \max_{\|x\|=1} \|A x\|. \tag{4}
$$

It expresses how large at most can $A$ make unit vectors.⁴ Then the distance between two matrices $A, B \in \mathbb{C}^{n \times n}$ is simply $\|A - B\|$.

The singular value decomposition SVD has many applications. (The approach is completely analogous if $A$ is rectangular but not square.) Let us describe one application from the view point of data compression. When $A$ is stored on a computer, $n^2$ complex numbers must be kept in memory. Often this is supposed to be sent to another computer. When $n$ is very large, both of these tasks can cause serious problems. There are ways to try to approximate matrices somehow with fewer parameters, i.e., to compress $A$. In this process some information is lost. But if the loss is small, one can accept it.

The singular value decomposition is related with compression through the approximation problem

$$
\min_{F_k \in F_k} \|A - F_k\|, \tag{5}
$$

where the norm of a matrix was defined in (4).⁵ Bear in mind that an element of $F_k$ requires storing just $2 n k$ complex numbers. Consequently, if for a small $k$ the value of (5) is small, then $A$ can be well compressed by using a matrix $F_k$. (There are many other techniques to compress matrices. In image processing such techniques are very important.)

Observe that in case of a compression when we do not have zero in (5), we are satisfied with an approximate factorization

$$
A \approx V_1 V_2 \tag{6}
$$

⁴ Unit vector is a vector of length one.  
⁵ This approximation problem can be formulated in Banach spaces, to measure compactness. It is just, in the Euclidean setting of $\mathbb{C}^n$ where the SVD happens to solve the problem.

Solving (5) clearly does not look easy. It can be done with the help of the **singular value decomposition**. Before defining the SVD, recall that a matrix $Q \in \mathbb{C}^{n \times n}$ is **unitary** if its columns are orthonormal, i.e.,

$$
Q^* Q = I \Leftrightarrow \|Q x\| = \|x\| \quad \text{for all } x \in \mathbb{C}^n. \tag{7-8}
$$

**Example 5** There are a lot of unitary matrices. Unitary matrices can be generated easily once you invoke the Gram-Schmidt process. That is, take any linearly independent $b_1, \dots, b_n \in \mathbb{C}^n$ and orthonormalize them to have $q_1, \dots, q_n$. Then put $Q_n = [q_1 \cdots q_n]$.

**Definition 3** The **singular value decomposition** of $A \in \mathbb{C}^{n \times n}$ is a factorization

$$
A = U \Sigma V^* \quad \text{with unitary } U, V \in \mathbb{C}^{n \times n} \text{ and diagonal } \Sigma \in \mathbb{C}^{n \times n}
$$

with the **singular values** satisfying

$$
\sigma_1 \geq \sigma_2 \geq \cdots \geq \sigma_n \geq 0.
$$

Linear algebraically this means that there exist orthonormal bases such that the associated linear map $A: \mathbb{C}^n \to \mathbb{C}^n$ can be represented with a diagonal matrix in these bases.

**Problem 3** Assume $A \in \mathbb{C}^{n \times n}$ is nonsingular. Show that orthonormalizing its columns with the Gram-Schmidt process starting from the leftmost column is equivalent to computing a representation $A = Q R$ with $Q$ unitary and $R$ upper triangular with positive diagonal entries. (This is called the **QR factorization** of $A$.)

Recall that unitary matrices appear also in connection with the Hermitian eigenvalue problem. (Here we assume you have taken an undergraduate linear algebra course.)

**Problem 4** Assume $A \in \mathbb{C}^{n \times n}$ is Hermitian, i.e., $A^* = A$. Show that $A$ can be unitarily diagonalized, i.e.,

$$
A = U \Lambda U^* \quad \text{with unitary } U \in \mathbb{C}^{n \times n} \text{ and diagonal } \Lambda \in \mathbb{C}^{n \times n}. \tag{9}
$$

(Hint: show first that eigenvectors related to differing eigenvalues are orthogonal.)

That there exists a singular value decomposition is based on inspecting the eigenvalue problem for $A^* A$. Since $A^* A$ is Hermitian, it can be unitarily diagonalized as

$$
A^* A = V \Lambda V^*.
$$

Take this to be our $V$. Assume now that the eigenvalues are ordered non-increasingly. (Note that $A^* A$ is positive semidefinite, i.e., its eigenvalues are nonnegative.) Take any eigenvectors $v_j$ and $v_l$ of $A^* A$. Then $A v_j$ and $A v_l$ are orthogonal by the fact that

$$
(A v_j, A v_l) = (v_j, A^* A v_l) = (v_j, \lambda_l v_l) = 0 \quad \text{if } \lambda_j \neq \lambda_l.
$$

Consequently, take the columns of $U$ to be

$$
u_j = \frac{A v_j}{\sqrt{\lambda_j}} = \frac{A v_j}{\sigma_j} \quad \text{for nonzero eigenvalues } \lambda_j \text{ of } A^* A.
$$

For zero eigenvalues $\lambda_j$ of $A^* A$, just take any remaining eigenvectors in the null space of $A$ by (10). Corresponding to these, take any set of orthonormal vectors in the orthogonal complement of the vectors. For them, the corresponding singular values are zeros.

Because of (8) we have

$$
\|A\| = \|U \Sigma V^*\| = \|\Sigma\| \Rightarrow \|A\| = \sigma_1. \tag{12}
$$

For diagonal matrices the norm is easy to compute and we obtain $\|A\| = \sigma_1$. So the first singular value of $A$ is unique. Equally importantly, it is the singular value decomposition which yields the best way of finding the norm of $A$.

**Problem 5** Show that for a diagonal matrix the norm is the maximal absolute value of its diagonal entries. (Observe that you can restrict the computations to real numbers.)

Repeating these arguments yields the fact that the singular values of a matrix are uniquely determined.

**Problem 6** Show that the singular values of a matrix $A \in \mathbb{C}^{n \times n}$ are unique.

Without resorting to (12) it would be very challenging to compute the norm of $A$. In particular, if you use other than the Euclidean norm in $\mathbb{C}^n$, then you have this challenge. (And numerous other challenges.) So the reason for not using the Euclidean norm should be exceptionally good!

**Theorem 1** Let $A \in \mathbb{C}^{n \times n}$. Then the value of the minimization problem (5) is $\sigma_{k+1}$.

**Proof.** The value of (5) is at most $\sigma_{k+1}$. This is seen by using the singular value decomposition of $A$ and forming $F_k$ by setting $\sigma_{k+1} = \cdots = \sigma_n = 0$. (This corresponds to replacing the $n-k$ last columns of $U$ and rows of $V^*$ with zeros.) Then

$$
F_k = \sum_{j=1}^k \sigma_j u_j v_j^*. \tag{13}
$$

Let us outline that $\sigma_{k+1}$ is actually the minimum. Consider $V_1 V_2 \in F_k$ realizing (5). Let $w_1^*, \dots, w_k^*$ be the nonzero rows of $V_2$. Then choose a unit vector $v$ which is a linear combination of $v_1, \dots, v_{k+1}$ which is in the orthogonal complement of $w_1, \dots, w_k$. (For this, find a nonzero solution to a $k$-by-$(k+1)$ homogeneous linear system involving the matrix $[w_j^* v_l]_{j=1,\dots,k, l=1,\dots,k+1}$.) Then $(A - V_1 V_2) v = A v$ and its norm is at least $\sigma_{k+1}$. This means that span of $w_1^*, \dots, w_k^*$ equals the span of $v_1^*, \dots, v_k^*$. Arguing similarly with $A^*$ we may conclude that the span of columns of $V_1$ equals the span of $u_1, \dots, u_k$. From this it follows that the best choice is (13). End of proof. ∎

The solution (13) constructed from the singular value decomposition solves the minimization problem (5) actually in any unitarily invariant norm. A norm $\|\cdot\|$ on $\mathbb{C}^{n \times n}$ is said to be unitarily invariant if for any $A \in \mathbb{C}^{n \times n}$ holds

$$
\|A\| = \|Q_1 A Q_2\|
$$

for any unitary $Q_1, Q_2 \in \mathbb{C}^{n \times n}$. Aside from the operator norm, the **Frobenius norm** $\|\cdot\|_F$ is often used in practice, due to its computational convenience. The Frobenius norm is induced by the inner product

$$
(A, B) = \operatorname{trace}(B^* A) \tag{14}
$$

on $\mathbb{C}^{n \times n}$. When dealing with matrix subspaces over $\mathbb{R}$, use

$$
(A, B) = \operatorname{Re} \operatorname{trace}(B^* A). \tag{15}
$$

The trace is computed by summing the diagonal entries of the matrix. This simply means that $\mathbb{C}^{n \times n}$ is treated as $\mathbb{C}^{n^2}$ using the standard inner product.

**Theorem** 

$$
\|A\|_F = \sqrt{\sum_{j=1}^n \sum_{k=1}^n |a_{jk}|^2}.
$$

This is clearly an easy computation whereas computing $\|A\|$ is much more involved requiring the largest singular value of $A$.

**Example 6** There are situations where the SVD is used in analyzing data. This may also take place for the data is manipulated. (By “data” we mean the matrix $A$ you have somehow generated in your application.) This can be done in many ways. Principal component analysis is an approach in statistics to analyze data by splitting it into parts as follows. Let $e = (1,1,\dots,1)^T \in \mathbb{C}^n$. The process is simply an SVD approximation after the data has been mean centered, i.e., translated by taking $A - e \alpha^*$ for some $\alpha \in \mathbb{C}^n$ where the $j$th component of $A$ is the average

The columns of the Fourier matrix are eigenvectors of circulant matrices.

**Problem 23** Let $F_n$ be the Fourier matrix and $P \in \mathbb{C}^{n \times n}$ the permutation matrix (47). Find the diagonal matrix $\Lambda$ satisfying

$$
P F_n = F_n \Lambda,
$$

i.e., determine the eigenvalues of $P$ by hand.

Denote by $Q$ the unitary matrix $Q = \frac{1}{\sqrt{n}} F_n$. Because of (49), $C$ is normal, i.e., unitarily similar with a diagonal matrix. This follows from

$$
Q^* C Q = \sum_{j=0}^{n-1} c_j Q^* P^j Q = \sum_{j=0}^{n-1} c_j (Q^* P Q)^j = \sum_{j=0}^{n-1} c_j \Lambda^j.
$$

Since the eigenvalues of $P$ are known (see Problem 23), this yields a way of finding the eigenvalues of $C$ by evaluating the polynomial $p$ at the eigenvalues of $P$. This can be done in $O(n)$ flops once the eigenvalues of $P$ are known.

Suppose $A \in \mathbb{C}^{n \times n}$ is circulant and $p$ is its polynomial. Then

$$
\Lambda(p(A)) = p(\Lambda(A)),
$$

where $p(\Lambda(A)) = \{ p(\lambda) : \lambda \in \Lambda(A) \}$.

For $n = 2^l$, $C$ can be diagonalized using the FFT as follows. First, the eigenvalues are $p(w^j)$ for $j = 0, \dots, n-1$. These can be computed in $O(n \log_2 n)$ flops using the FFT. Then the eigenvectors are the columns of $F_n$. The inverse is also $F_n$ up to scaling.

To solve $C x = b$, we have $x = F_n^{-1} \Lambda^{-1} F_n b / n$, but adjusted for the scaling.

**Problem 25** Suppose $T \in \mathbb{C}^{k \times k}$ is a Toeplitz matrix. Devise a method to perform matrix-vector products with a circulant matrix $C \in \mathbb{C}^{n \times n}$ with $n = 2^l \geq k$ containing $T$ as its block. Then products with $T$, i.e., lower dimensional matrix-vector products appropriately with $C$ to have matrix-vector products with $T$.

There are also fast algorithms for solving linear systems involving Toeplitz matrices [3].

### 8 Iterative methods for linear systems

Next we consider ways to solve the linear system

$$
A x = b \tag{52}
$$

for an invertible $A \in \mathbb{C}^{n \times n}$ and $b \in \mathbb{C}^n$ given when $n$ is large. By large is meant that direct methods such as the LU factorization of $O(n^3)$ and $O(n^2)$ storage are not acceptable. This $n$ is of order $O(10^4)$ or larger. (Floating point operations have been performed. In iterative methods one uses information based on matrix-vector products and the norm of (52). A rule of thumb is that a single iteration step should not cost more than $O(n)$ or $O(n \log n)$ floating point operations. The approximations (hopefully) improve step by step until sufficient.

Each step (or every now and then) for solving

$$
(A - \lambda^{(k-1)} I) z^{(k)} = q^{(k-1)}
$$

since this linear system varies at each step. Therefore this is more costly than the inverse iteration. If this is affordable, then this beats the shift-and-invert method (104). This is not the best choice, however. On the other hand, once can find publicly available software for the RQI iteration.

Here appears (after minor manipulations) the so-called condition number

$$
\kappa(W) = \|W\| \|W^{-1}\|
$$

of $W$ which scales the accuracy of the approximations. This is no accident. The condition number appears often in assessing accuracy of numerical linear algebra computations. From the SVD of $W$ one obtains $\kappa(W) = \sigma_1 / \sigma_n$.

### 6 Computing the LU factorization with partial pivoting

In factoring in practice, one typically computes

$$
P A = L U, \tag{34}
$$

where $P$ is a permutation matrix to make the computations numerically more stable. This permutation is not known in advance. Finding $P$ is part of the algorithm called the LU factorization with partial pivoting. (A simple way to define a permutation on each row and column of $P$ there is exactly one 1 while the other entries are zeros.) Since $P$ is unitary and we have $\|P x\| = \|x\|$. Thus, $P$ is unitary and we have $P^{-1} = P^* = P^T$.

**Problem 13** Show that the complexity of the standard Gaussian elimination for $A \in \mathbb{C}^{n \times n}$ (when all the pivots are nonzero) is $\approx \frac{2}{3} n^3$ flops.⁹

We work out a low dimensional example to see what is going on.¹⁰ For the matrix $A$ below, the standard Gaussian row operations give

$$
A = \begin{bmatrix}
2 & 1 & 1 & 0 \\
4 & 3 & 3 & 1 \\
8 & 7 & 9 & 5 \\
6 & 7 & 9 & 8
\end{bmatrix}
= \begin{bmatrix}
1 & 0 & 0 & 0 \\
2 & 1 & 0 & 0 \\
4 & 3 & 1 & 0 \\
3 & 4 & 1 & 1
\end{bmatrix}
\begin{bmatrix}
2 & 1 & 1 & 0 \\
0 & 1 & 1 & 1 \\
0 & 0 & 2 & 2 \\
0 & 0 & 0 & 2
\end{bmatrix} = L U.
$$

In the $L$ factor we get a hint of the catastrophic behaviour of Example 15, i.e., away from the diagonal appear large entries. To avoid this, one must “partial pivot” inbetween the row operations. The resulting LU factorization with partial pivoting has replaced the standard LU factorization since the 1960s. (To such an extent that by an LU factorization of $A$ is typically meant the LU factorization (34).)

The rule is simple: the pivot must be the largest entry among those entries being under elimination. This is achieved by permuting rows. We have for the first column

$$
P_1 A = \begin{bmatrix}
0 & 0 & 1 & 0 \\
0 & 1 & 0 & 0 \\
1 & 0 & 0 & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
\begin{bmatrix}
2 & 1 & 1 & 0 \\
4 & 3 & 3 & 1 \\
8 & 7 & 9 & 5 \\
6 & 7 & 9 & 8
\end{bmatrix}
= \begin{bmatrix}
8 & 7 & 9 & 5 \\
4 & 3 & 3 & 1 \\
2 & 1 & 1 & 0 \\
6 & 7 & 9 & 8
\end{bmatrix}.
$$

Then the row operations expressed in terms of a matrix-matrix product for the first column read

$$
L_1 P_1 A = \begin{bmatrix}
1 & 0 & 0 & 0 \\
1/2 & 1 & 0 & 0 \\
1/4 & 0 & 1 & 0 \\
3/4 & 0 & 0 & 1
\end{bmatrix}
\begin{bmatrix}
8 & 7 & 9 & 5 \\
4 & 3 & 3 & 1 \\
2 & 1 & 1 & 0 \\
6 & 7 & 9 & 8
\end{bmatrix}
= \begin{bmatrix}
8 & 7 & 9 & 5 \\
0 & -1/2 & -3/2 & -3/2 \\
0 & -3/4 & -5/4 & -5/4 \\
0 & 7/4 & 9/4 & 17/4
\end{bmatrix}.
$$

Then

$$
P_2 L_1 P_1 A = \begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & 0 & 0 & 1 \\
0 & 0 & 1 & 0 \\
0 & 1 & 0 & 0
\end{bmatrix}
\begin{bmatrix}
8 & 7 & 9 & 5 \\
0 & -1/2 & -3/2 & -3/2 \\
0 & -3/4 & -5/4 & -5/4 \\
0 & 7/4 & 9/4 & 17/4
\end{bmatrix}
= \begin{bmatrix}
8 & 7 & 9 & 5 \\
0 & 7/4 & 9/4 & 17/4 \\
0 & -3/4 & -5/4 & -5/4 \\
0 & -1/2 & -3/2 & -3/2
\end{bmatrix}
$$

and

$$
L_2 P_2 L_1 P_1 A = \begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & 3/7 & 1 & 0 \\
0 & 2/7 & 0 & 1
\end{bmatrix}
\begin{bmatrix}
8 & 7 & 9 & 5 \\
0 & 7/4 & 9/4 & 17/4 \\
0 & -3/4 & -5/4 & -5/4 \\
0 & -1/2 & -3/2 & -3/2
\end{bmatrix}
= \begin{bmatrix}
8 & 7 & 9 & 5 \\
0 & 7/4 & 9/4 & 17/4 \\
0 & 0 & -2/7 & 4/7 \\
0 & 0 & -6/7 & -2/7
\end{bmatrix}.
$$

Then, similarly, with

$$
P_3 = \begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 0 & 1 \\
0 & 0 & 1 & 0
\end{bmatrix}, \quad
L_3 = \begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & -1/3 & 1
\end{bmatrix}
$$

we complete the process to have

$$
L_3 P_3 L_2 P_2 L_1 P_1 A = U = \begin{bmatrix}
8 & 7 & 9 & 5 \\
0 & 7/4 & 9/4 & 17/4 \\
0 & 0 & -6/7 & -2/7 \\
0 & 0 & 0 & 2
\end{bmatrix}.
$$

The matrices used in the elimination have a special structure as the following problem illustrates.

**Problem 14** The Gaussian row operation matrices (also called the Gauss transforms) can be expressed as

$$
L_j = I + l_j e_j^*, \quad l_j \in \mathbb{C}^n
$$

with $l_j \in \mathbb{C}^n$ having the first $j$ entries zeros. Show that $L_j^{-1} = I - l_j e_j^*$. (Here $e_j$ denotes the $j$th standard basis vector.) Using this, show that the inverse of $L_{n-1} \cdots L_1$ is $I - \sum_{j=1}^{n-1} l_j e_j^*$. This makes finding $L$ very easy!

This looks certainly complicated. However, we have (hidden) here the searched factorization $P A = L U$. To see this, we need a trick. There holds

$$
L_3 P_3 L_2 P_2 L_1 P_1 A = L_3' L_2' L_1' P_3 P_2 P_1 A
$$

once we set

$$
L_3' = L_3, \quad L_2' = P_3 L_2 P_3^{-1}, \quad L_1' = P_3 P_2 L_1 P_2^{-1} P_3^{-1}.
$$

We have $P = P_3 P_2 P_1$ and $L^{-1} = L_3' L_2' L_1'$.

Matrices $L_j'$ are easily found. Because of (35),

$$
L_j' = I + P_{n-1} \cdots P_{j+1} l_j e_j^* P_{j+1}^{-1} \cdots P_{n-1}^{-1}.
$$

Observe that when $P_l$ is applied to a vector, it does not permute the $l-1$ first entries. Therefore $e_j^* P_{j+1} \cdots P_{n-1} = (P_{n-1} \cdots P_{j+1} e_j)^* = e_j^*$. Moreover, the first $j$ entries of $l_j = P_{j+1} \cdots P_{n-1} l_j$ are zeros while the remaining entries are just those of $l_j$ permuted. This means that each $L_j'$ is a Gauss transform. Hence the product $L_3' L_2' L_1'$ has an inverse which is easily found (see Problem 14). This is how we get the factors $P$, $L$ and $U$ of the partially pivoted LU factorization $P A = L U$ of $A$.

If $A \in \mathbb{C}^{n \times n}$ is nonsingular, then the Gaussian elimination with partial pivoting always yields a factorization (34). The reason is that the permutations and Gauss transforms are invertible, so that the transformed matrix remains invertible. (And if there were just zeros in a column such that no $P_l$ can bring a nonzero to the $l$th diagonal position, then the first $l$ columns would be necessarily linearly dependent.) The practical importance is that it helps to control the growth of the $L$ factor.

**Problem 15** In assessing accuracy of finite precision computations, often the norm used on $\mathbb{C}^n$ is

$$
\|x\|_\infty = \max_{1 \leq j \leq n} |x_j|.
$$

This is the so-called max norm. Then the corresponding norm of a matrix $A \in \mathbb{C}^{n \times n}$ is defined as

$$
\|A\|_\infty = \max_{\|x\|_\infty = 1} \|A x\|_\infty.
$$

Show that in (34) produced with the partially pivoted Gaussian elimination we have $\|L\|_\infty \leq n$.

In the 1-norm

$$
\|x\|_1 = \sum_{j=1}^n |x_j|
$$

one can show that $\|L\|_1 \leq n$. In practice one often has $\|L\|_1 \ll n$.

### 6.2 Growth factor and numerical stability

Although partial pivoting controls the growth of the $L$ factor very well in practice, theoretically the growth can be exponential. This is illustrated by the following example.

**Example 16** Take $A = \{a_{ij}\}$ with

$$
a_{ij} = \begin{cases}
1, & i=j \\
-1, & i>j \\
0, & \text{otherwise}.
\end{cases}
$$

Then with very small $\varepsilon > 0$ one has

$$
P_1 = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}, \quad
P_1 A = \begin{bmatrix} 1 & 1 \\ \varepsilon & 1 \end{bmatrix}
\begin{bmatrix} 1 & 1 \\ 0 & 1 - \varepsilon \end{bmatrix}.
$$

With $\varepsilon = 10^{-18}$ one has $1 - \varepsilon \approx 1$ and the second pivot is tiny. This forces large multipliers in $L$ and huge entries in $U$. In the $n \times n$ case the largest entry in $U$ grows like $2^{n-1}$.

In practice such matrices never appear. The worst observed growth in real applications is very modest (around 10–100). Nevertheless, theoretically one can have

$$
\max_{i,j} |u_{ij}| \approx 2^{n-1} \max_{i,j} |a_{ij}|.
$$

This means that the complexity of finding the LU factorization with partial pivoting is still $O(n^3)$, but the storage requirement can be up to $O(n^2)$ in the worst case (instead of $O(n)$).

One can try to remedy the situation by also allowing column pivoting, i.e., computing

$$
P A Q = L U
$$

with permutation matrices $P$ and $Q$. This is called complete pivoting. It is more expensive ($O(n^3)$ still, but larger constant) and in practice the growth is only marginally better.

### 6.3 Floating point arithmetic and backward stability

In IEEE 754 double precision (the standard today), the unit roundoff is

$$
\varepsilon_{\text{machine}} = 2^{-53} \approx 1.11 \times 10^{-16}.
$$

The floating-point numbers are of the form $x(1 + \varepsilon)$ with $|\varepsilon| \leq \varepsilon_{\text{machine}}$.

In finite precision, the computed factors $\hat{L}$ and $\hat{U}$ satisfy

$$
\hat{L} \hat{U} = A + \delta A, \quad \|\delta A\| = O(\varepsilon_{\text{machine}} \|L\| \|U\|).
$$

With partial pivoting one has the famous backward stability result:

$$
\hat{L} \hat{U} = P A + \delta A, \quad \|\delta A\| \leq O(\rho \varepsilon_{\text{machine}}) \|A\|
$$

where the growth factor

$$
\rho = \frac{\max_{i,j} |u_{ij}|}{\max_{i,j} |a_{ij}|}
$$

is typically very close to 1 (rarely exceeds 100). This means that the computed LU factorization is as accurate as if we had solved the nearby problem $(A + \delta A) x = b$ exactly, with a tiny relative perturbation $\delta A$.

⁹ By a flop is meant a floating point operation: sum, difference, product or a fraction of two complex numbers.  
¹⁰ This example is from [8].

Here appears (after minor manipulations) the so-called condition number

$$
\kappa(W) = \|W\| \|W^{-1}\|
$$

of $W$ which scales the accuracy of the approximations. This is no accident. The condition number appears often in assessing accuracy of numerical linear algebra computations. From the SVD of $W$ one obtains $\kappa(W) = \sigma_1 / \sigma_n$.

### References

[1] M. Byckling and M. Huhtanen, Preconditioning with direct approximate factorization, SIAM J. Sci. Comput., 36(1), pp. A80–A104, 2014.

[2] Bai, Z., Demmel, J., Dongarra, J., Ruhe, A., van der Vorst, H. (eds.): Templates for the Solution of Algebraic Eigenvalue Problems: A Practical Guide, SIAM, Philadelphia (2000)

[3] G.H. Golub and C.F. Van Loan, Matrix Computations, The Johns Hopkins University Press, the 3rd ed., 1996.

[4] A. Greenbaum, Iterative Methods for Solving Linear Systems, SIAM, Philadelphia, 1997.

[5] B. Parlett, The Symmetric Eigenvalue Problem, Classics in Applied Mathematics 20, SIAM, Philadelphia, 1997.

[6] SPAL, http://www.computational.uni-bsch.ch/software/spai/

[7] Y. Saad, Numerical Methods for Large Eigenvalue Problems, 2nd edition, SIAM Philadelphia 2011.

[8] L.N. Trefethen and D. Bau, III, Numerical Linear Algebra, SIAM Philadelphia, 1997.
