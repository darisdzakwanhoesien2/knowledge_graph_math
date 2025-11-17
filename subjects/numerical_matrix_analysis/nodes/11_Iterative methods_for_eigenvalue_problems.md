# Matrix Computations

**Marko Huhtanen**

## 11 Iterative methods for eigenvalue problems

When the dimensions are large, the eigenvalue problem is more varied than that of solving a linear system. There are therefore many methods for computing eigenvalues. In what follows we shortly describe how one should approach a very large eigenvalue problem.

### The power method

The power method is an iterative method for locating the largest eigenvalue μ, i.e., filter = A, of a matrix A.

To find an eigenvalue close to a shift μ ∈ C, use the inverse iteration with the filter = (A - μ I)^{-1}.

The largest eigenvalue of the filter is 1 / (λ - μ) where λ is the eigenvalue of A closest to μ.

The inverse iteration is

for k = 1, 2, . . .

z^{(k)} = (A - μ I)^{-1} q^{(k-1)}

q^{(k)} = z^{(k)} / ||z^{(k)||

λ^{(k)} = (A q^{(k)}, q^{(k)})

end

To choose μ dynamically, use the Rayleigh quotient iteration

for k = 1, 2, . . .

μ = (q^{(k-1)}, A q^{(k-1)})

z^{(k)} = (A - μ I)^{-1} q^{(k-1)}

q^{(k)} = z^{(k)} / ||z^{(k)||}

λ^{(k)} = (A q^{(k)}, q^{(k)})

end

This converges cubically for Hermitian A.

For non-Hermitian A, the convergence can be quadratic.

The problem is solving the linear system at each step.

For large n, use iterative methods to approximate the solve.

### Arnoldi method

The Arnoldi method approximates eigenvalues by projecting onto Krylov subspaces.

The Krylov subspace K_j(A; b) = span{b, Ab, ..., A^{j-1} b}

Then orthonormalize to get Q_j with Q_j^* Q_j = I, A Q_j = Q_{j+1} \hat H_j where \hat H_j is (j+1) x j upper Hessenberg.

H_j = Q_j^* A Q_j is j x j upper Hessenberg.

The eigenvalues \hat λ_k of H_j are Ritz values, approximating eigenvalues of A.

The Ritz vectors \hat x_k = Q_j v_k where H_j v_k = \hat λ_k v_k

The residual ||A \hat x_k - \hat λ_k \hat x_k|| = |h_{j+1, j}| |e_j^* v_k|

If small, good approximation.

For j << n, the cost is O(n j^2) for dense A, but for sparse A, O(n j) per step.

To compute several eigenvalues, use restart with the best Ritz vector or block Arnoldi.

For Hermitian A, it's Lanczos method, tridiagonal H_j.

### Proposition 2

Suppose a nonsingular matrix subspace V is equivalent to a matrix subspace which is closed.

### Problem 11

Let A ∈ C^{n×n}. For iterative methods the matrix subspaces

K_j(A; I) = span{I, A, ..., A^{j-1}}

are very important. Assume A is diagonalizable. Show that there exists a unique Hermitian positive definite X such that A = X Λ X^{-1} with Λ diagonal and X^* X = I. (Show that if A = X Λ X^{-1}, then A = (X (X^* X)^{-1/2}) Λ ((X^* X)^{-1/2})^{-1} X^* (X^* X)^{1/2}, and this is the required form.)

### 5 Factoring algorithmically

Assume given two nonsingular matrix subspaces V1 and V2, of which one is invertible. Let us suppose V2 is invertible with the inverse W. Suppose A ∈ C^{n×n} is nonsingular and the task is to recover whether A ∈ V1 V2. Clearly, A = V1 V2 holds if and only if

A W = V1

for some nonsingular W ∈ W. This latter problem is linear and thereby completely solvable. (If a problem is linear, it can be solved in a finite number of flops.) Once done, we obtain the factorization A = V1 W^{-1}.

To accomplish this task, we will use projections. Recall that a linear operator P on a vector space is a projection if P^2 = P. A projector moves points onto its range and acts like the identity operator on the range. (The range means the subspace R(P) = {y : y = P x for some x}.) Such operators are of importance in numerical computations and approximation.

It is preferable to use orthogonal projectors since they take the shortest path while moving points to the range. This requires that the vector space is equipped with an inner product (and thus has the notion of orthogonality). We say that P is an orthogonal projector if

R(P) ⊥ R(I - P),

i.e., the range of P is orthogonal to the range of I - P. Orthogonality requires using an inner product. Since we are interested in matrix subspaces, on C^{n×n} we use the trace inner product.

After all this theory, fortunately there is an easy way of constructing an orthogonal projector onto a given subspace. Take an orthonormal basis q1, ..., qk of the subspace. Then set

P x = sum_{j=1}^k q_j (x, q_j).

It is rare that an orthonormal basis is available, i.e., having an orthonormal basis requires taking a basis of the subspace and orthonormalizing it. Typically the Gram-Schmidt process is needed here.

The orthogonal projector on C^{n×n} onto the set of Hermitian matrices is P A = 1/2 (A + A^*).

Similarly for complex symmetric.

A matrix subspace V is standard if it has a basis of standard matrices (one 1, rest 0).

Then P A zeros out entries outside the sparsity pattern of V.

Observe that any matrix M = P M + (I - P) M.

To factor A = V1 V2, construct orthogonal projector P1 onto V1.

Solve min_W || (I - P1) A W ||

Then V1 = P1 A W, A ≈ V1 W^{-1}

Similarly from the right.

For LU, V1 lower triangular, V2 upper.

The equations become small triangular solves.

### Example

A = [1 2; 1 1]

P1 = P2 = projector onto span{I}

Then solve (I - P) A S = 0 for S diagonal.

Get A = S1 S2 with S1, S2 scalar multiples of I.

### Conditioning

The error ||A - V1 W^{-1}|| ≤ κ(W) || (I - P1) A W ||

κ(W) = ||W|| ||W^{-1}|| = σ1 / σn from SVD.

### Example ill-conditioned

A = [ε 1; 1 1]

As ε → 0, factorization with large entries.

### LU with partial pivoting

The LU with partial pivoting is a special case.

### Proposition

Assume there are nonsingular elements in V. Then the set of nonsingular elements is open and dense.

Proof: The singular set is closed (det = 0), and cannot have interior, since det as polynomial has finite zeros in one variable.

### Invertible matrix subspaces

A matrix subspace V is invertible if the set of inverses (of nonsingular elements) is a matrix subspace (up to closure).

For lower triangular, the inverse is lower triangular.

For the product V1 V2, if V2 invertible with inverse W, then A in V1 V2 iff A W in V1.

### Problem 12

If P projection, orthogonal if ||P|| = 1 and ||x||^2 = ||P x||^2 + || (I - P) x||^2.

### Definition 8

Sparsity structure of V is locations nonzero in some V in V.

### 6 Computing the LU factorization with partial pivoting

In practice, compute P A = L U, P permutation for stability.

P unitary, P^{-1} = P^T.

Problem 13 Complexity of Gaussian elimination ≈ 2/3 n^3 flops.

Example with 4x4 matrix, standard GE gives L with large entries.

With partial pivoting, choose largest in column for pivot, swap rows.

Then apply Gauss transform L j = I + l j e j ^*

l j zeros first j entries.

L j^{-1} = I - l j e j ^*

The product L = inverse of product of L j '

After permuting to make L j ' lower triangular.

If A nonsingular, partial pivoting always succeeds.

Problem 15 ||L||_∞ ≤ n

### Growth factor

In practice growth small, but theoretically can be 2^{n-1}

Example with nearly singular matrix.

With complete pivoting P A Q = L U, better growth but more expensive.

### Floating point

In double precision ε_machine = 2^{-53} ≈ 1.11e-16

Computed ˆ L ˆ U = A + δ A, ||δ A|| O(ε ||L|| ||U||)

With partial pivoting, backward stable ||δ A|| O(ρ ε) ||A|| , ρ growth factor, usually small.

### 7 Using the structure in computations: Cholesky factorization, Sylvester equation and FFT

Cholesky for positive definite A = R^* R, R upper triangular.

A positive definite if Hermitian and (A x, x) > 0 for x ≠ 0.

Block form, induct.

Complexity 1/3 n^3

Sylvester A X - X B = C, solve with O(n^3) if spectra disjoint.

FFT for circulant matrices, diagonalized by Fourier matrix.

O(n log n) matvec.

For Toeplitz, embed in circulant.

### 8 Iterative methods for linear systems

To solve A x = b large n.

Iterative, no factoring.

Info from matvec A v.

Cost per step O(n) or O(n log n)

Approximations x j , residual r j = b - A x j

### Least squares

To solve M y = c , min ||M y - c|| , M k x j

M = [m1 ... mj], columns orthonormal.

Then y = M^* c, approx M y

### Krylov subspace

K j (A ; b) = span {b, Ab, ..., A^{j-1} b}

y 2 C^j

min || b - A Q j y ||

Q j orthonormal basis of K j

A Q j = Q_{j+1} ˆ H j

Then min || ||b|| e1 - ˆ H j y ||

Solve small least squares.

x j = Q j y

GMRES

Stateful.

For Hermitian A, Lanczos, tridiagonal.

Convergence depends on spectrum.

If clustered, fast.

For positive definite Hermitian, CG in A-norm.

CG algorithm stateful short recurrence.

For non-Hermitian, GMRES full orthogonalization.

BiCGSTAB for non-Hermitian, short recurrence but can break down.

See [4]

### 9 Preconditioning

To speed up iterative methods, precondition M A x = M b

M ≈ A^{-1}

Splitting A = M1 + M2, M = M1^{-1}

Iteration x k+1 = x k + M r k

Converges if ρ(I - M A) < 1

Jacobi M1 = diag(A)

Gauss-Seidel M1 lower triangular.

Incomplete LU, drop fill in GE.

SPAI approximate inverse min || I - M A ||_F sparse M.

AMG for PDE.

DD for parallel.

See [4,9,10]

### 10 Eigenvalue problems and functions of matrices

Gershgorin disks D j center a jj radius sum |a jl|

Λ(A) in union D j

Field of values F(A) = { x^* A x : ||x|| = 1 }

Power method converges to dominant eigenvalue.

Householder for QR.

Hessenberg reduction O(n^3)

QR iteration with shifts for Schur.

Generalized A x = λ B x, QZ.

Sensitivity κ(X) ||E|| for perturbation.

Functions f(A) = X f(Λ) X^{-1}

Square root iteration.

Cayley for unitary from skew-Hermitian.

Exp by scaling and squaring or Pade.

### References

As before.

Now, to rewrite the document into .md format.<|control12|>```markdown
# Matrix Computations

**Marko Huhtanen**

## 11 Iterative methods for eigenvalue problems

When the dimensions are large, the eigenvalue problem is more varied than that of solving a linear system. There are therefore many methods for computing eigenvalues. In what follows we shortly describe how one should approach a very large eigenvalue problem.

The power method is an iterative method for locating the largest eigenvalue μ, i.e., filter = A, of a matrix A.

To find an eigenvalue close to a shift μ ∈ C, use the inverse iteration with the filter = (A - μ I)^{-1}.

The largest eigenvalue of the filter is 1 / (λ - μ) where λ is the eigenvalue of A closest to μ.

The inverse iteration is

for k = 1, 2, . . .

z^{(k)} = (A - μ I)^{-1} q^{(k-1)}

q^{(k)} = z^{(k)} / ||z^{(k)||}

λ^{(k)} = (A q^{(k)}, q^{(k)})

end

To choose μ dynamically, use the Rayleigh quotient iteration

for k = 1, 2, . . .

μ = (q^{(k-1)}, A q^{(k-1)})

z^{(k)} = (A - μ I)^{-1} q^{(k-1)}

q^{(k)} = z^{(k)} / ||z^{(k)||}

λ^{(k)} = (A q^{(k)}, q^{(k)})

end

This converges cubically for Hermitian A.

For non-Hermitian, it may not converge.

The problem with inverse iteration is solving the linear system at each step, which is expensive for large n.

To avoid this, one can use approximate solves, but that's advanced.

### Arnoldi method

The Arnoldi method approximates eigenvalues by projecting onto Krylov subspaces.

The Krylov subspace K_j(A; b) = span{b, Ab, ..., A^{j-1} b}

Then orthonormalize to get Q_j with Q_j^* Q_j = I, A Q_j = Q_{j+1} \hat H_j where \hat H_j is (j+1) x j upper Hessenberg.

H_j = Q_j^* A Q_j is j x j upper Hessenberg.

The eigenvalues \hat λ_k of H_j are Ritz values, approximating eigenvalues of A.

The Ritz vectors \hat x_k = Q_j v_k where H_j v_k = \hat λ_k v_k

The residual ||A \hat x_k - \hat λ_k \hat x_k|| = |h_{j+1, j}| |e_j^* v_k|

If small, good approximation.

For j << n, cheap.

To restart, take the best Ritz vector as new q(0)

For multiple eigenvalues, use block methods or deflated.

### Proposition 2

Suppose a nonsingular matrix subspace V is equivalent to a matrix subspace which is closed.

### Problem 11

Let A ∈ C^{n×n}. For iterative methods the matrix subspaces

K_j(A; I) = span{I, A, ..., A^{j-1}}

are very important. Assume A is diagonalizable. Show that there exists a unique Hermitian positive definite X such that A = X Λ X^{-1} with Λ diagonal and X^* X = I. (Show that if A = X Λ X^{-1}, then A = (X (X^* X)^{-1/2}) Λ ((X^* X)^{-1/2})^{-1} X^* (X^* X)^{1/2}, and this is the required form.)

### 5 Factoring algorithmically

Assume given two nonsingular matrix subspaces V1 and V2, of which one is invertible. Let us suppose V2 is invertible with the inverse W. Suppose A ∈ C^{n×n} is nonsingular and the task is to recover whether A ∈ V1 V2. Clearly, A = V1 V2 holds if and only if

A W = V1

for some nonsingular W ∈ W. This latter problem is linear and thereby completely solvable. (If a problem is linear, it can be solved in a finite number of flops.) Once done, we obtain the factorization A = V1 W^{-1}.

To accomplish this task, we will use projections. Recall that a linear operator P on a vector space is a projection if P^2 = P. A projector moves points onto its range and acts like the identity operator on the range. (The range means the subspace R(P) = {y : y = P x for some x}.) Such operators are of importance in numerical computations and approximation.

It is preferable to use orthogonal projectors since they take the shortest path while moving points to the range. This requires that the vector space is equipped with an inner product (and thus has the notion of orthogonality). We say that P is an orthogonal projector if

R(P) ⊥ R(I - P),

i.e., the range of P is orthogonal to the range of I - P. Orthogonality requires using an inner product. Since we are interested in matrix subspaces, on C^{n×n} we use the trace inner product.

After all this theory, fortunately there is an easy way of constructing an orthogonal projector onto a given subspace. Take an orthonormal basis q1, ..., qk of the subspace. Then set

P x = sum_{j=1}^k q_j (x, q_j).

It is rare that an orthonormal basis is available, i.e., having an orthonormal basis requires taking a basis of the subspace and orthonormalizing it. Typically the Gram-Schmidt process is needed here.

The orthogonal projector on C^{n×n} onto the set of Hermitian matrices is P A = 1/2 (A + A^*).

Similarly for complex symmetric.

A matrix subspace V is standard if it has a basis of standard matrices (one 1, rest 0).

Then P A zeros out entries outside the sparsity pattern of V.

Observe that any matrix M = P M + (I - P) M.

To factor A = V1 V2, construct orthogonal projector P1 onto V1.

Solve min_W || (I - P1) A W ||

Then V1 = P1 A W, A ≈ V1 W^{-1}

Similarly from the right.

For LU, V1 lower triangular, V2 upper.

The equations become small triangular solves.

### Example

A = [1 2; 1 1]

P1 = P2 = projector onto span{I}

Then solve (I - P) A S = 0 for S diagonal.

Get A = S1 S2 with S1, S2 scalar multiples of I.

### Conditioning

The error ||A - V1 W^{-1}|| ≤ κ(W) || (I - P1) A W ||

κ(W) = ||W|| ||W^{-1}|| = σ1 / σn from SVD.

### Example ill-conditioned

A = [ε 1; 1 1]

As ε → 0, factorization with large entries.

### LU with partial pivoting

The LU with partial pivoting is a special case.

### Proposition

Assume there are nonsingular elements in V. Then the set of nonsingular elements is open and dense.

Proof: The singular set is closed (det = 0), and cannot have interior, since det as polynomial has finite zeros in one variable.

### Invertible matrix subspaces

A matrix subspace V is invertible if the set of inverses (of nonsingular elements) is a matrix subspace (up to closure).

For lower triangular, the inverse is lower triangular.

For the product V1 V2, if V2 invertible with inverse W, then A in V1 V2 iff A W in V1.

### Problem 12

If P projection, orthogonal if ||P|| = 1 and ||x||^2 = ||P x||^2 + || (I - P) x||^2.

### Definition 8

Sparsity structure of V is locations nonzero in some V in V.

### 6 Computing the LU factorization with partial pivoting

In practice, compute P A = L U, P permutation for stability.

P unitary, P^{-1} = P^T.

Problem 13 Complexity of Gaussian elimination ≈ 2/3 n^3 flops.

Example with 4x4 matrix, standard GE gives L with large entries.

With partial pivoting, choose largest in column for pivot, swap rows.

Then apply Gauss transform L j = I + l j e j ^*

l j zeros first j entries.

L j^{-1} = I - l j e j ^*

The product L = inverse of product of L j '

After permuting to make L j ' lower triangular.

If A nonsingular, partial pivoting always succeeds.

Problem 15 ||L||_∞ ≤ n

### Growth factor

In practice growth small, but theoretically can be 2^{n-1}

Example with nearly singular matrix.

With complete pivoting P A Q = L U, better growth but more expensive.

### Floating point

In double precision ε_machine = 2^{-53} ≈ 1.11e-16

Computed ˆ L ˆ U = A + δ A, ||δ A|| O(ε ||L|| ||U||)

With partial pivoting, backward stable ||δ A|| O(ρ ε) ||A|| , ρ growth factor, usually small.

### 7 Using the structure in computations: Cholesky factorization, Sylvester equation and FFT

Cholesky for positive definite A = R^* R, R upper triangular.

A positive definite if Hermitian and (A x, x) > 0 for x ≠ 0.

Block form, induct.

Complexity 1/3 n^3

Sylvester A X - X B = C, solve with O(n^3) if spectra disjoint.

FFT for circulant matrices, diagonalized by Fourier matrix.

O(n log n) matvec.

For Toeplitz, embed in circulant.

### 8 Iterative methods for linear systems

To solve A x = b large n.

Iterative, no factoring.

Info from matvec A v.

Cost per step O(n) or O(n log n)

Approximations x j , residual r j = b - A x j

### Least squares

To solve M y = c , min ||M y - c|| , M k x j

M = [m1 ... mj], columns orthonormal.

Then y = M^* c, approx M y

### Krylov subspace

K j (A ; b) = span {b, Ab, ..., A^{j-1} b}

y 2 C^j

min || b - A Q j y ||

Q j orthonormal basis of K j

A Q j = Q_{j+1} ˆ H j

Then min || ||b|| e1 - ˆ H j y ||

Solve small least squares.

x j = Q j y

GMRES

Stateful.

For Hermitian A, Lanczos, tridiagonal.

Convergence depends on spectrum.

If clustered, fast.

For positive definite Hermitian, CG in A-norm.

CG algorithm stateful short recurrence.

For non-Hermitian, GMRES full orthogonalization.

BiCGSTAB for non-Hermitian, short recurrence but can break down.

See [4]

### 9 Preconditioning

To speed up iterative methods, precondition M A x = M b

M ≈ A^{-1}

Splitting A = M1 + M2, M = M1^{-1}

Iteration x k+1 = x k + M r k

Converges if ρ(I - M A) < 1

Jacobi M1 = diag(A)

Gauss-Seidel M1 lower triangular.

Incomplete LU, drop fill in GE.

SPAI approximate inverse min || I - M A ||_F sparse M.

AMG for PDE.

DD for parallel.

See [4,9,10]

### 10 Eigenvalue problems and functions of matrices

Gershgorin disks D j center a jj radius sum |a jl|

Λ(A) in union D j

Field of values F(A) = { x^* A x : ||x|| = 1 }

Power method converges to dominant eigenvalue.

Householder for QR.

Hessenberg reduction O(n^3)

QR iteration with shifts for Schur.

Generalized A x = λ B x, QZ.

Sensitivity κ(X) ||E|| for perturbation.

Functions f(A) = X f(Λ) X^{-1}

Square root iteration.

Cayley for unitary from skew-Hermitian.

Exp by scaling and squaring or Pade.

### References

[1] M. Byckling and M. Huhtanen, Preconditioning with direct approximate factorization, SIAM J. Sci. Comput., 36(1), pp. A80–A104, 2014.

[2] Bai, Z., Demmel, J., Dongarra, J., Ruhe, A., van der Vorst, H. (eds.): Templates for the Solution of Algebraic Eigenvalue Problems: A Practical Guide, SIAM, Philadelphia (2000)

[3] G.H. Golub and C.F. Van Loan, Matrix Computations, The Johns Hopkins University Press, the 3rd ed., 1996.

[4] A. Greenbaum, Iterative Methods for Solving Linear Systems, SIAM, Philadelphia, 1997.

[5] B. Parlett, The Symmetric Eigenvalue Problem, Classics in Applied Mathematics 20, SIAM, Philadelphia, 1997.

[6] SPAL, http://www.computational.uni-bsch.ch/software/spai/

[7] Y. Saad, Numerical Methods for Large Eigenvalue Problems, 2nd edition, SIAM Philadelphia 2011.

[8] L.N. Trefethen and D. Bau, III, Numerical Linear Algebra, SIAM Philadelphia, 1997.

[9] Y. Saad, Iterative Methods for Sparse Linear Systems, 2nd edition, SIAM, 2003.

[10] H. A. van der Vorst, Iterative Krylov Methods for Large Linear Systems, Cambridge University Press, 2003.