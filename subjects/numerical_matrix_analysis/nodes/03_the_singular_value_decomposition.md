# Matrix Computations
**Marko Huhtanen**

## 3 The singular value decomposition (continued)

Solving (5) clearly does not look easy. It can be done with the help of the **singular value decomposition**. Before defining the SVD, recall that a matrix $Q \in \mathbb{C}^{n \times n}$ is **unitary** if its columns are orthonormal, i.e.,

$$
Q^* Q = I \quad \Leftrightarrow \quad \|Qx\| = \|x\| \quad \text{for all } x \in \mathbb{C}^n. \tag{7-8}
$$

**Example 5** There are a lot of unitary matrices. Unitary matrices can be generated easily once you invoke the Gram-Schmidt process. That is, take any linearly independent $b_1, \dots, b_n \in \mathbb{C}^n$ and orthonormalize them to have $q_1, \dots, q_n$. Then put $Q_n = [q_1 \cdots q_n]$.

**Definition 3** The **singular value decomposition** of $A \in \mathbb{C}^{n \times n}$ is a factorization

$$
A = U \Sigma V^* \quad \text{with} \quad U, V \in \mathbb{C}^{n \times n} \text{ unitary and } \Sigma = \operatorname{diag}(\sigma_1, \dots, \sigma_n) \in \mathbb{C}^{n \times n}
$$

with the **singular values** satisfying

$$
\sigma_1 \geq \sigma_2 \geq \cdots \geq \sigma_n \geq 0.
$$

Linear algebraically this means that there exist orthonormal bases such that associated linear map $A: \mathbb{C}^n \to \mathbb{C}^n$ can be represented with a diagonal matrix in these bases.

**Problem 3** Assume $A \in \mathbb{C}^{n \times n}$ is nonsingular. Show that orthonormalizing its columns with the Gram-Schmidt process starting from the leftmost column is equivalent to computing a representation $A = QR$ with $Q$ unitary and $R$ upper triangular with positive diagonal entries. (This is called the **QR factorization** of $A$.)

Recall that unitary matrices appear also in connection with the Hermitian eigenvalue problem. (Here we assume you have taken an undergraduate linear algebra course.)

**Problem 4** Assume $A \in \mathbb{C}^{n \times n}$ is Hermitian, i.e., $A^* = A$. Show that $A$ can be unitarily diagonalized, i.e.,

$$
A = U \Lambda U^* \quad \text{with unitary } U \in \mathbb{C}^{n \times n} \text{ and diagonal } \Lambda \in \mathbb{C}^{n \times n}. \tag{9}
$$

(Hint: show first that eigenvectors related to differing eigenvalues are orthogonal.)

That there exists a singular value decomposition is based on inspecting the eigenvalue problem for $A^*A$. Since $A^*A$ is Hermitian, it can be unitarily diagonalized as

$$
A^* A = V \Lambda V^*.
$$

Take this to be our $V$. Assume now that the eigenvalues are ordered non-increasingly. (Note that $A^*A$ is positive semidefinite, i.e., its eigenvalues are nonnegative.) Take any eigenvectors $v_j$ and $v_l$ of $A^*A$. Then $Av_j$ and $Av_l$ are orthogonal by the fact that

$$
(Av_j, Av_l) = (v_j, A^* A v_l) = (v_j, \lambda_l v_l) = 0 \quad \text{if } \lambda_j \neq \lambda_l.
$$

Consequently, take the columns of $U$ to be

$$
u_j = \frac{A v_j}{\sqrt{\lambda_j}} = \frac{A v_j}{\sigma_j} \quad \text{for nonzero eigenvalues } \lambda_j \text{ of } A^*A.
$$

For zero eigenvalues $\lambda_j$ of $A^*A$, just take any remaining eigenvectors in the null space of $A$ by (10). Corresponding to these, take any set of orthonormal vectors in the orthogonal complement of the vectors. For them, the corresponding singular values are zeros.

Because of (8) we have

$$
\|A\| = \|U \Sigma V^*\| = \|\Sigma\| \quad \Rightarrow \quad \|A\| = \sigma_1. \tag{12}
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

Let us outline that $\sigma_{k+1}$ is actually the minimum. Consider $V_1 V_2 \in F_k$ realizing (5). Let $w_1^*, \dots, w_k^*$ be the nonzero rows of $V_2$. Then choose a unit vector $v$ which is a linear combination of $v_1, \dots, v_{k+1}$ which is in the orthogonal complement of $w_1, \dots, w_k$. (For this, find a nonzero solution to a $k$-by-$(k+1)$ homogeneous linear system involving the matrix $[w_j^* v_l]_{j=1,\dots,k,\,l=1,\dots,k+1}$.) Then $(A - V_1 V_2)v = Av$ and its norm is at least $\sigma_{k+1}$. This means that span of $w_1^*, \dots, w_k^*$ equals the span of $v_1^*, \dots, v_k^*$. Arguing similarly with $A^*$ we may conclude that the span of columns of $V_1$ equals the span of $u_1, \dots, u_k$. From this it follows that the best choice is (13). End of proof. ∎

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

The trace is computed by summing the diagonal entries of the matrix. This simply means that $\mathbb{C}^{n \times n}$ is treated as $\mathbb{C}^n$ using the standard inner product.

**Theorem** 

$$
\|A\|_F = \sqrt{\sum_{j=1}^n \sum_{k=1}^n |a_{jk}|^2}.
$$

This is clearly an easy computation whereas computing $\|A\|$ is much more involved requiring the largest singular value of $A$.

**Example 6** There are situations where the SVD is used in analyzing data. This may also take place for the data is manipulated. (By “data” we mean the matrix $A$ you have somehow generated in your application.) This can be
