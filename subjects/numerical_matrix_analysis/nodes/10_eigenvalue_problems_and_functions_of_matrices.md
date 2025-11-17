# Matrix Computations

**Marko Huhtanen**

## 10 Eigenvalue problems and functions of matrices

### Preconditioning for linear systems and eigenvalue problems

In the LU factorization, A ≈ LU, then M = U^{-1} L^{-1}.

For the preconditioned system, the (0) case, (0) LL^*.

L^{-1} A L^{-*} ˆx = L^{-1} b.

The matrix L^{-1} A L^{-*}

For A, ˆx j , x j = L^{-*} ˆx j

For A, A.

The eigenvalue problem Ax = λ x

with A ∈ C^{n×n}, λ ∈ C, x ∈ C^n.

### Gershgorin circle theorem

The spectrum ⇤(A)

for A ∈ C^{n×n}

j = 1, ..., n

R j = sum_{l≠j} |a jl|.

D j = {z ∈ C : |a jj - z| ≤ R j}.

For A ∈ C^{n×n}

⇤(A) ⊂ union_{j=1}^n D j,

The D j are the Gershgorin disks for A.

n n

### The power method

The field of values F(A) = {x^* A x : ||x|| = 1}.

For A, A, F(A)

(A x, x) = x^* A x

x ∈ C^n , ||x|| = 1

For A

The power method:

q(0)

for k = 1, 2, ...

z = A q(k-1)

q(k) = z / ||z||

λ(k) = (A q(k), q(k))

end

### Convergence of power method

A = X Λ X^{-1}

X = [x1 x2 · · · xn]

|λ1| > |λ2| ≥ |λ3| ≥ · · · ≥ |λn|.

a1 ≠ 0

q(0) = a1 x1 + · · · + an x n.

q(0)

k

A k q(0) = a1 λ1^k (x1 + sum_{j=2}^n (λ j / λ1)^k a j / a1 x j ).

q(k) = A k q(0) / || A k q(0) || converges to x1 if |λ j / λ1| < 1.

The error O( ( |λ j| / |λ1| ) ^k )

For A, A

### Householder reflections

The norm ||A||

O(n^2)

For A

The Householder matrix H = I - 2 v^* v / v^* v

v ∈ C^n , H

v

x ∈ C^n

v

H x

e1

v = x + α e1 , α = (x,e1) / |(x,e1)| * ||x|| if (x, e1) = 0, α = ||x||

H x = - α e1

### Reducing to Hessenberg form

To make A Hessenberg, n -1 Householder.

The matrix A, A

The reduced form is n -1

Q0 = H_{n-1} H_{n-2} · · · H1

Q0 A Q0^* = H

Where H is upper Hessenberg, h j k = 0 for j ≥ k + 2

### QR iteration for Hessenberg

A ∈ C^{n×n}

H

O(n3)

For the QR iteration on Hessenberg

Q(0) = I

for k = 1, 2, ...

Z = H Q(k-1)

Z = Q(k) R(k)

end

Then H k = Q^* (k) H Q(k)

Then for the implicit QR, H_{k-1} = Q^* (k-1) H Q(k-1) = (Q^* (k-1) Q(k)) R(k)

H k = R(k) (Q^* (k-1) Q(k))

Then the loop for k = 0,1,2,... H k = ˆ Q (k) ˆ R (k) , H k+1 = ˆ R (k) ˆ Q (k)

With H0 = H

Then the converged H k is the Schur form.

The full A = ( ˆ Q (0) · · · ˆ Q (k-1) ˆ Q (k) ) H k+1 ( ˆ Q (k) ˆ Q (k-1) · · · ˆ Q (0) ) ^*

Q , T

A in C^{n x n}

The spectrum of A

λ j in ⇤(A)

A

T

H

P

(1, n)

✏

✏

### Generalized eigenvalue problem

A, B ∈ C^{n×n}

The generalized eigenvalue problem Ax = λ B x

Q, Z ∈ C^{n×n}

T, S ∈ C^{n×n}

A = Q T Z^*

B = Q S Z^*

The polynomial p(λ) = det(A - λ B)

p

λ

z1 ∈ C^n

A z1 = λ B z1

Z1 ∈ C^{n×n} , z1

Q1 ∈ C^{n×n}

q1 = B z1 / ||B z1|| if B z1 = 0, q1 = A z1 / ||A z1||

A = Q1 T1 Z1^*

T1

B = Q1 S1 Z1^*

S1

(n -1) (n -1)

T1 , S1

A = Q1 Q2 T2 Z2^* Z1^*

T2 T1 T2

B = Q1 Q2 S2 Z2^* Z1^*

S2 S1 S2

Ax - λ B x = 0

Q (T - λ S) Z^* x = 0

Q^* y = Z^* x

(T - λ S) y = 0

t jj - λ s jj = 0 for j = 1,...,n

If s jj ≠ 0 , λ = t jj / s jj

If s jj = 0, infinite

Then y , x = Z y.

For B

M y = λ y

### Condition of eigenvalue

B = A + E , then δ(⇤(A + E), ⇤(A)) ≤ κ(X) ||E||

For μ in ⇤(A + E)

If μ in ⇤(A), δ = 0

Else, 1 ≤ ||(μ I - Λ(A))^{-1} || || X^{-1} || ||E|| ||X||

||(μ I - Λ(A))^{-1}|| = 1 / min |μ - λ j (A)|

κ(X)

The condition number κ(B) = ||B|| ||B^{-1}||

For perturbations in eigenvalue.

Then for approximated ˆ λ j , ˆ x j , the residual || A ˆx j - ˆλ j ˆx j ||

Then || ˆλ j - λ j || , || ˆx j - x j || bound.

### Trace and determinant

For A ∈ C^{n×n}, tr(A) = sum j a jj

The characteristic polynomial p(λ) = det(A - λ I) = (-1)^n λ^n + (-1)^{n-1} tr(A) λ^{n-1} + · · · + det(A).

### Cayley-Hamilton

p(A) = 0

### Functions of matrices

p(A) = sum a j A j , for p(z) = sum a j z j

For f(A), if f is analytic, f(A) = 1/(2 π i) int_Γ f(λ) (λ I - A)^{-1} dλ , where Γ encloses the spectrum.

If A = X Λ X^{-1}, then f(A) = X f(Λ) X^{-1}, where f(Λ) = diag(f(λ1), ..., f(λn))

The spectrum ⇤(f(A)) = f(⇤(A))

For x j eigenvector of A with λ j , then f(A) x j = f(λ j) x j

For A skew-Hermitian A^* = - A

Then the Cayley transform (I - A) (I + A)^{-1}

With f(z) = (1 - z)/(1 + z)

The Cayley transform maps skew-Hermitian to unitary.

### Matrix exponential

For A ∈ C^{n×n}

The matrix exponential e ^ A = sum_{j=0}^∞ A^j / j!

e^{A t} for t > 0

e^{A t} b

### References

The references are listed in the last page.

[1] M. Byckling and M. Huhtanen...

and others.

So, this is the structure.

Now, to write the .md.<|control12|>```markdown
# Matrix Computations

**Marko Huhtanen**

## 10 Eigenvalue problems and functions of matrices

### Preconditioning for eigenvalue problems

In the LU factorization, A ≈ LU, then M = U^{-1} L^{-1}.

For the preconditioned system, the (0) case, (0) LL^*.

L^{-1} A L^{-*} ˆx = L^{-1} b.

The matrix L^{-1} A L^{-*} 

For A, ˆx j , x j = L^{-*} ˆx j

For A, A.

The eigenvalue problem Ax = λ x

with A ∈ C^{n×n}, λ ∈ C, x ∈ C^n.

### Gershgorin circle theorem

The spectrum Λ(A)

for A ∈ C^{n×n}

j = 1, . . . n

R j = ∑_{l≠j} |a jl|.

D j = {z ∈ C : |a jj −z| ≤ R j}.

For A ∈ C^{n×n}

Λ(A) ⊂ ⋃_{j=1}^n D j,

D j

A

n

n

### Field of values

A

A

A ∈ C^{n×n}

F(A) = {x^* Ax : ||x|| = 1}.

A

A

F(A)

(Ax, x) = x^* Ax

x ∈ C^n

||x|| = 1

A

### Power method

q(0)

for k = 1, 2, . . .

z = A q^{ (k-1) }

q^{(k)} = z / ||z||

λ^{(k)} = (A q^{(k)}, q^{(k)})

end

### Convergence of power method

A

A = X Λ X^{-1}

X = [x1 x2 · · · xn]

|λ1| > |λ2| ≥|λ3| ≥· · · ≥|λn|.

a1 ≠ 0

q(0) = a1 x1 + · · · + an xn.

q(0)

k

A^k q(0) = X Λ^k X^{-1} q(0)

2

64

a1

an

3

75 = a1 λ1^k (x1 + ∑_{j=2}^n (λj / λ1)^k a j / a1 xj).

q^{(k)}

x1, . . . , xn

q(0)

x1

O( ( |λj| / |λ1| )^k )

A

A

A

O(n^2)

A

### Householder reflections

Λ(A) 

H = I −2 v^* v / v^* v

v ∈ C^n

H

v

x ∈ C^n

v

H x

e1

v = x + α e1

α = (x, e1) / |(x, e1)| ||x||

(x, e1) = 0

α = ||x||

H x = − α e1

n -1

Q0 = H_{n-1} H_{n-2} · · · H1

Q0 A Q0^*

0

H 2 C^{n×n}

h j k = 0

j ≥ k + 2

H1

x = [0 a21 a31 · · · an1]^T

e1

e2

H1

H1 A H1^* = ˜ A

x = [0 0 ˜ a32 ˜ a32 · · · ˜ an2]^T

e1

e3

H2

H2 H1 A H1^* H2^* = ˜ ˜ A

Q0 A Q0^* = H

The Hessenberg form.

### QR iteration

A 2 C^{n×n}

The Hessenberg form H

O(n3)

The QR iteration

Q(0) = I

for k = 1, 2, . . .

Z^{(k)} = H Q^{(k-1)}

Z^{(k)} = Q^{(k)} R^{(k)}

end

The Z^{(k)}

H_{k-1} = Q^* (k-1) H Q(k-1) = Q^* (k-1) ( H Q(k-1) ) = (Q^* (k-1) Q(k)) R(k)

H k = R(k) (Q^* (k-1) Q(k))

for k = 0, 1, 2, . . .

H k = ˆ Q^{(k)} ˆ R^{(k)}

H k+1 = ˆ R^{(k)} ˆ Q^{(k)}

end

H0 = H

H k

ˆ Q (0) · · · ˆ Q (k-1) ˆ Q (k) H k+1 ˆ Q^* (k) ˆ Q^* (k-1) · · · ˆ Q^* (0) = H

The converged form is the Schur form.

Q , T

### Gershgorin for Hessenberg

A 2 C^{n×n}

Λ(A)

λ j 2 Λ(A)

A

T

H

P

(1, n)

ε

ε

### Generalized eigenvalue problem

A, B 2 C^{n×n}

Q, Z 2 C^{n×n}

T, S 2 C^{n×n}

A = Q T Z^*

B = Q S Z^*

p(λ) = det(A −λ B)

p

λ

z1 2 C^n

A z1 = λ B z1

Z1 2 C^{n×n}

z1

Q1 2 C^{n×n}

q1 = B z1 / || B z1 ||

x, y 2 C^n

B z1 = 0

q1 = A z1 / || A z1 ||

A = Q1 T1 Z1^*

T1

B = Q1 S1 Z1^*

S1

(n −1)

(n −1)

T1

S1

A = Q1 Q2 T2 Z2^*

Q, Z

T2

T1

T2

B = Q1 Q2 S2 Z2^*

S2

S1

S2

Ax = λ B x = 0

Q ( T - λ S ) Z^* x = 0

Q^* y = Z^* x

(T - λ S) y = 0

t jj - λ s jj = 0

j = 1, . . . , n

s jj ≠ 0

λ = t jj / s jj

s jj = 0

1

y

λ

x = Z y.

B

M y = λ y

### Sensitivity of eigenvalues

A, B 2 C^{n×n}

M = X A Y

N = X B Y

X, Y 2 C^{n×n}

M x = λ N x

A, B 2 C^{n×n}

Q, Z

Q^* A Z

Q^* B Z

x

Y

δ(x, Y ) = inf_{y in Y} ||x - y||.

X

Y

δ(X, Y ) = sup_{x in X} δ(x, Y ).

X

Y

d(X, Y ) = max{δ(X, Y ), δ(Y, X)}

A 2 C^{n×n}

A = X Λ X^{-1}

δ(Λ(A + E), Λ(A)) ≤ κ(X) ||E||.

μ 2 Λ(A + E)

μ 2 Λ(A)

δ(μ, Λ(A)) = 0

κ(X) ||E||.

μ ∉ Λ(A)

(μ I − Λ(A))^{-1} X^{-1} (μ I − A - E) X = I - (μ I - Λ(A))^{-1} X^{-1} E X

1 ≤ || (μ I − Λ(A))^{-1} X^{-1} E X || ≤ ||(μ I − Λ(A))^{-1}|| ||X^{-1}|| ||E|| ||X||.

The inverse (I - M)^{-1} if ||M|| < 1

(I − M)^{-1} = sum_{k=0}^∞ M^k

M

### Perturbation for eigenvalue approximation

|| A ˆx j - ˆλ j ˆx j ||

ˆλ j

ˆx j

λ j

x j

|| ˆλ j - λ j ||

|| ˆx j - x j ||

λ j

x j

### Functions of matrices

A 2 C^{n×n}

tr(A) = sum_{j=1}^n a jj

p(λ) = det(A - λ I) = (-1)^n λ^n + (-1)^{n-1} tr(A) λ^{n-1} + · · · + det(A).

p(A) = 0

p(A) = sum_{j=0}^k a j A^j

p(z) = sum_{j=0}^k a j z^j

For the matrix exponential e^A = sum_{j=0}^∞ A^j / j!

e^A

⇤(f(A)) = f(⇤(A))

xj

A

λ j

xj

f(A)

f(λ j).

A 2 C^{n×n}

A^* = -A

(I −A)(I + A)^{-1}

A

f(z) = 1−z / 1+z

A 2 C^{n×n}

e^{A t}

t > 0

e^{A t} b

### Using the structure in computations: Cholesky factorization

The Cholesky factorization replaces the LU if the matrix is positive definite.

Definition 10 A matrix A ∈ C^{n×n} is positive definite if (Ax, x) > 0 for x ≠ 0.

For f(x) = x^* A x + b^* x + c, the minimum at A x = -b/2.

Block form A = [ a11 a^* ; a B ]

a11 > 0

A = [ α 0 ; a/α I ] [ 1 0 ; 0 B - a a^* / a11 ] [ α a^* / α ; 0 I ] = R1 A1 R1^*

α = sqrt(a11)

A1 = B - a a^* / a11

Then A1 positive definite.

Problem 18 Show that the submatrix B−aa^* / a11 is positive definite.

Then A = R1 R2 · · · Rn I R n^* · · · R2^* R1^* = R R^* , R = R1 · · · Rn

The Cholesky, R upper triangular.

Storage n^2 / 2, complexity ≈1/3 n^3

Proposition Assume A positive definite. Then the Cholesky factorization exists.

Proof By induction, since A1 positive definite.

For Hermitian A, from SVD of R = U Σ V^* , A = U Σ^2 U^*

### Sylvester equation

A, B, C ∈ C^{n×n}, solve A X - X B = C for X.

The map X 7→ A X - X B

From C^{n×n} to C^{n×n}

Dimension n^2 , invertible if spectra of A and B disjoint.

Complexity O(n3)

### FFT

The fast Fourier transform.

For circulant matrices.

The Fourier matrix F_n with entries f j k = ω^{ (j-1) (k-1) } / sqrt(n), ω = e^{-2 π i / n}

Then Q = 1/sqrt(n) F_n

C circulant, then Q^* C Q = diag(p(1), p(ω), ... ), where p is the polynomial from the first row.

Complexity O(n log n) for matrix-vector.

For Toeplitz, embed in circulant.

### Iterative methods for linear systems

To solve A x = b for large n.

### Preconditioning

For iterative methods, to speed up convergence.

M A x = M b

M ≈ A^{-1}

Splitting A = M1 + M2 , M = M1^{-1}

The iteration x k+1 = M^{-1} (b - M2 x k)

Converges if ρ ( - M1^{-1} M2 ) < 1

### References

[1] M. Byckling and M. Huhtanen, Preconditioning with direct approximate factorization, SIAM J. Sci. Comput., 36(1), pp. A80–A104, 2014.

[2] Bai, Z., Demmel, J., Dongarra, J., Ruhe, A., van der Vorst, H. (eds.): Templates for the Solution of Algebraic Eigenvalue Problems: A Practical Guide, SIAM, Philadelphia (2000)

[3] G.H. Golub and C.F. Van Loan, Matrix Computations, The Johns Hopkins University Press, the 3rd ed., 1996.

[4] A. Greenbaum, Iterative Methods for Solving Linear Systems, SIAM, Philadelphia, 1997.

[5] B. Parlett, The Symmetric Eigenvalue Problem, Classics in Applied Mathematics 20, SIAM, Philadelphia, 1997.

[6] SPAL, http://www.computational.uni-bsch.ch/software/spai/

[7] Y. Saad, Numerical Methods for Large Eigenvalue Problems, 2nd edition, SIAM Philadelphia 2011.

[8] L.N. Trefethen and D. Bau, III, Numerical Linear Algebra, SIAM Philadelphia, 1997.