# Matrix Computations
**Marko Huhtanen**

## 5 Factoring algorithmically

Assume given two nonsingular matrix subspaces V₁ and V₂ of which one is invertible. Let us first suppose V₂ is invertible with the inverse W. Suppose A ∈ ℂⁿˣⁿ is nonsingular and the task is to recover whether A ∈ V₁V₂. Clearly, A = V₁V₂ holds if and only if

$$
A W = V₁ \tag{20}
$$

for some nonsingular W ∈ W. This latter problem is linear and thereby completely solvable. (If a problem is linear, it can be solved in a finite number of flops.) Once done, we obtain the factorization A = V₁W⁻¹.

To accomplish this task, we will use projections. Recall that a linear operator P on a vector space is a projection if P² = P. A projector maps points onto its range and acts like the identity operator on the range. (The range means the subspace R(P) = {y : y = Px for some x}.) Such operators are of importance in numerical computations and approximation.

In the so-called dimension reduction approximation, the task is to find in some sense a good projector which is used to replace the original problem with a problem of much smaller dimension. Observe that if P is a projector, then so is I − P.

It is preferable to use orthogonal projectors since they take the shortest path while moving points to the range. This requires that the vector space is equipped with an inner product (and thus has the notion of orthogonality). We say that P is an orthogonal projector if

$$
R(P) \perp R(I-P).
$$

i.e., the range of P is orthogonal to the range of I−P. Orthogonality requires using an inner product. Since we are interested in matrix subspaces, on ℂⁿˣⁿ we use (14).

After all this theory, fortunately there is an easy way of constructing an orthogonal projector onto a given subspace. Take an orthonormal basis q₁, …, qₖ of the subspace. Then set

$$
P x = \sum_{j=1}^{k} q_j (x, q_j). \tag{25}
$$

It is rare that an orthonormal basis is available, i.e., having an orthonormal basis requires taking a basis of the subspace and orthonormalizing it. Typically the Gram–Schmidt process is needed here.

Let us now focus on matrix subspaces and orthogonal projectors onto them. Occasionally orthogonal projectors onto familiar matrix subspaces are readily available without invoking the Gram–Schmidt process to have (25). The orthogonal projector on ℂⁿˣⁿ onto the set of Hermitian matrices is given by

$$
P A = \frac{1}{2} (A + A^*). \tag{26}
$$

(Because the set of Hermitian matrices is a subspace over ℝ, use (15).) This is the so-called Hermitian part of a matrix A. Similarly, onto the set of complex symmetric matrices the orthogonal projector acts according to

$$
P A = \frac{1}{2} (A + A^T). \tag{27}
$$

These are very simple to apply.

**Problem 12** Suppose P is a projection. Then show that P is an orthogonal projection if the operator norm ||P|| = 1 if for every x holds ||x|| = ||(I−P)x|| + ||Px||.

A matrix is called standard if there is exactly one entry which equals 1 while other entries equal zero. A matrix subspace V is called standard if it has a basis consisting of standard matrices. This simply means that there are n² interdependencies between the entries of V ∈ V. In this case the orthogonal projector P onto V acts such that P A simply replaces with zeros those entries of A which are outside the sparsity structure of V. (You can also see this by using (25).) Other entries of A are kept intact. For example, if the matrix subspace is the set of diagonal matrices, P A equals the diagonal matrix whose diagonal is that of A.

**Definition 8** The sparsity structure of a matrix subspace V means the location of those entries which are nonzero for some V ∈ V.

Observe that any matrix M decomposes as

$$
M = P M + (I−P) M.
$$

### 5.1 How to factor with matrix subspaces

Let V₁ and V₂ be given matrix subspaces. To factor A = V₁V₂, the idea is the following.

1. Construct an orthogonal projector P₁ onto V₁.
2. Solve the linear least squares problem

   $$
   \min_{W} \|(I - P_1) A W\|
   $$

   to have (I−P₁) A W ≈ 0. This yields W such that A W ≈ V₁.
3. Set V₁ = P₁ A W.
4. Then A ≈ V₁ W⁻¹.

Similarly, one can start from the right by constructing an orthogonal projector P₂ onto V₂ and solving

$$
\min_{W} \|(I - P_2) W A\|
$$

to have W A ≈ V₂.

**Example** Take

$$
A = \begin{bmatrix} 1 & 2 \\ 1 & 1 \end{bmatrix}.
$$

Let P₁ = P₂ = P be the orthogonal projector onto span{I}. Then

$$
(I-P)A = \begin{bmatrix} s_1 & s_2 \\ s_2 & s_3 \end{bmatrix}
= (I-P) \begin{bmatrix} s_1 + 2s_2 \\ s_2 + 2s_3 \\ s_1 + s_2 \\ s_2 + s_3 \end{bmatrix}
= \begin{bmatrix} 0 & -s_1/2 + s_3 \\ s_1/2 - s_3 & 0 \end{bmatrix}.
$$

Setting s₁ = 2s₃ we have a solution. Then with s₂ arbitrary we obtain

$$
A S = S_1, \quad S = \begin{bmatrix} 2 & 0 \\ 0 & 1 \end{bmatrix}, \;
S_1 = A S = \begin{bmatrix} 2 & 2 \\ 2 & 1 \end{bmatrix}, \;
S_2 = S^{-1} = \begin{bmatrix} 1/2 & 0 \\ 0 & 1 \end{bmatrix}.
$$

Thus A = S₁ S₂ with S₁, S₂ ∈ span{I}.

### 5.2 Conditioning and accuracy

The approximation error satisfies

$$
\|A - V_1 W^{-1}\| \leq \|W^{-1}\| \cdot \|A W - V_1\| \leq \kappa(W) \cdot \|(I-P_1) A W\|
$$

where the condition number

$$
\kappa(W) = \|W\| \|W^{-1}\|
$$

appears. From the SVD of W one obtains κ(W) = σ₁/σₙ.

**Example (ill-conditioned factorization)** Take

$$
A = \begin{bmatrix} \varepsilon & 1 \\ 1 & 1 \end{bmatrix}.
$$

When ε → 0 we have a nearby singular matrix. One possible factorization is

$$
A = \begin{bmatrix} 1 & 0 \\ 1/\varepsilon & 1 \end{bmatrix}
\begin{bmatrix} \varepsilon & 1 \\ 0 & 1 - 1/\varepsilon \end{bmatrix}.
$$

The factor on the right becomes huge when ε → 0.

In practice, one tries to avoid badly conditioned intermediate results.

### 5.3 Connection to the LU factorization

The LU factorization with partial pivoting can also be derived from this framework (although historically it was discovered much earlier).

The lower triangular matrices form a matrix subspace V₁, upper triangular form V₂. The algorithm proceeds by alternately applying orthogonal projectors (corresponding to choosing the largest pivot in the column) and solving small linear systems — which is exactly what Gaussian elimination with partial pivoting does.

This unified view shows that the classical LU factorization is just a very special case of the general problem of factoring with matrix subspaces.