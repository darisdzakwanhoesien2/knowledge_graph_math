# Matrix Computations
**Marko Huhtanen**

## 6 Computing the LU factorization with partial pivoting

Here appears (after minor manipulations) the so-called condition number

$$
\kappa(W) = \|W\| \|W^{-1}\|
$$

of W which scales the accuracy of the approximations. This is no accident. The condition number appears often in assessing accuracy of numerical linear algebra computations. From the SVD of W one obtains $\kappa(W) = \sigma_1 / \sigma_n$.

### 6.1 Partial pivoting

In factoring in practice, one typically computes a single element of the null-space (28) or (30). This should be done as fast as possible without sacrificing the accuracy of the numerical results. We also want to avoid what happened in Example 15. This means that one tries to benefit from the properties of the factorization problem as much as possible. For the LU factorization this means computing the standard LU factorization not for A but for a matrix which has the rows of A reordered, i.e.,

$$
PA = LU, \tag{34}
$$

where P is a permutation matrix to make the computations numerically more stable. This permutation is not known in advance. Finding P is part of the algorithm called the LU factorization with partial pivoting. (A simple way to define a permutation on each row and column of P there is exactly one 1 while the other entries are zeros.) Since P is unitary and we have $\|Px\| = \|x\|$. Thus, P is unitary and we have $P^{-1} = P^* = P^T$.

**Problem 13** Show that the complexity of the standard Gaussian elimination for $A \in \mathbb{C}^{n \times n}$ (when all the pivots are nonzero) is $\approx \frac{2}{3}n^3$ flops.⁹

We work out a low dimensional example to see what is going on.¹⁰ For the matrix A below, the standard Gaussian row operations give

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
\end{bmatrix} = LU.
$$

In the L factor we get a hint of the catastrophic behaviour of Example 15, i.e., away from the diagonal appear large entries. To avoid this, one must “partial pivot” inbetween the row operations. The resulting LU factorization with partial pivoting has replaced the standard LU factorization since the 1960s. (To such an extent that by an LU factorization of A is typically meant the LU factorization (34).)

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
\frac{1}{2} & 1 & 0 & 0 \\
\frac{1}{4} & 0 & 1 & 0 \\
\frac{3}{4} & 0 & 0 & 1
\end{bmatrix}
\begin{bmatrix}
8 & 7 & 9 & 5 \\
4 & 3 & 3 & 1 \\
2 & 1 & 1 & 0 \\
6 & 7 & 9 & 8
\end{bmatrix}
= \begin{bmatrix}
8 & 7 & 9 & 5 \\
0 & -\frac{1}{2} & -\frac{3}{2} & -\frac{3}{2} \\
0 & -\frac{3}{4} & -\frac{5}{4} & -\frac{5}{4} \\
0 & \frac{7}{4} & \frac{9}{4} & \frac{17}{4}
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
0 & -\frac{1}{2} & -\frac{3}{2} & -\frac{3}{2} \\
0 & -\frac{3}{4} & -\frac{5}{4} & -\frac{5}{4} \\
0 & \frac{7}{4} & \frac{9}{4} & \frac{17}{4}
\end{bmatrix}
= \begin{bmatrix}
8 & 7 & 9 & 5 \\
0 & \frac{7}{4} & \frac{9}{4} & \frac{17}{4} \\
0 & -\frac{3}{4} & -\frac{5}{4} & -\frac{5}{4} \\
0 & -\frac{1}{2} & -\frac{3}{2} & -\frac{3}{2}
\end{bmatrix}
$$

and

$$
L_2 P_2 L_1 P_1 A = \begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & \frac{3}{7} & 1 & 0 \\
0 & \frac{2}{7} & 0 & 1
\end{bmatrix}
\begin{bmatrix}
8 & 7 & 9 & 5 \\
0 & \frac{7}{4} & \frac{9}{4} & \frac{17}{4} \\
0 & -\frac{3}{4} & -\frac{5}{4} & -\frac{5}{4} \\
0 & -\frac{1}{2} & -\frac{3}{2} & -\frac{3}{2}
\end{bmatrix}
= \begin{bmatrix}
8 & 7 & 9 & 5 \\
0 & \frac{7}{4} & \frac{9}{4} & \frac{17}{4} \\
0 & 0 & -\frac{2}{7} & \frac{4}{7} \\
0 & 0 & -\frac{6}{7} & -\frac{2}{7}
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
0 & 0 & -\frac{1}{3} & 1
\end{bmatrix}
$$

we complete the process to have

$$
L_3 P_3 L_2 P_2 L_1 P_1 A = U = \begin{bmatrix}
8 & 7 & 9 & 5 \\
0 & \frac{7}{4} & \frac{9}{4} & \frac{17}{4} \\
0 & 0 & -\frac{6}{7} & -\frac{2}{7} \\
0 & 0 & 0 & 2
\end{bmatrix}.
$$

The matrices used in the elimination have a special structure as the following problem illustrates.

**Problem 14** The Gaussian row operation matrices (also called the Gauss transforms) can be expressed as

$$
L_j = I + l_j e_j^*, \quad l_j \in \mathbb{C}^n
$$

with $l_j \in \mathbb{C}^n$ having the first $j$ entries zeros. Show that $L_j^{-1} = I - l_j e_j^*$. (Here $e_j$ denotes the $j$th standard basis vector.) Using this, show that the inverse of $L_{n-1} \cdots L_1$ is $I - \sum_{j=1}^{n-1} l_j e_j^*$. This makes finding $L$ very easy!

This looks certainly complicated. However, we have (hidden) here the searched factorization $PA = LU$. To see this, we need a trick. There holds

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

Observe that when $P_l$ is applied to a vector, it does not permute the $l-1$ first entries. Therefore $e_j^* P_{j+1} \cdots P_{n-1} = (P_{n-1} \cdots P_{j+1} e_j)^* = e_j^*$. Moreover, the first $j$ entries of $l_j = P_{j+1} \cdots P_{n-1} l_j$ are zeros while the remaining entries are just those of $l_j$ permuted. This means that each $L_j'$ is a Gauss transform. Hence the product $L_3' L_2' L_1'$ has an inverse which is easily found (see Problem 14). This is how we get the factors $P$, $L$ and $U$ of the partially pivoted LU factorization $PA = LU$ of $A$.

If $A \in \mathbb{C}^{n \times n}$ is nonsingular, then the Gaussian elimination with partial pivoting always yields a factorization (34). The reason is that the permutations and Gauss transforms are invertible, so that the transformed matrix remains invertible. (And if there were just zeros in a column such that no $P_l$ can bring a nonzero to the $l$th diagonal position, then the first $l$ columns would be necessarily linearly dependent.) The practical importance is that it helps to control the growth of the L factor.

**Problem 15** In assessing accuracy of finite precision computations, often the norm used on $\mathbb{C}^n$ is

$$
\|x\|_{\infty} = \max_{1\leq j\leq n} |x_j|.
$$

This is the so-called max norm. Then the corresponding norm of a matrix $A \in \mathbb{C}^{n \times n}$ is defined as

$$
\|A\|_{\infty} = \max_{\|x\|_{\infty}=1} \|Ax\|_{\infty}.
$$

Show that in (34) produced with the partially pivoted Gaussian elimination we have $\|L\|_{\infty} \leq n$.

In the 1-norm

$$
\|x\|_1 = \max_{1\leq j\leq n} |x_j|
$$

one can show that $\|L\|_1 \leq n$. In practice one often has $\|L\|_1 \ll n$.

### 6.2 Growth factor and numerical stability

Although partial pivoting controls the growth of the L factor very well in practice, theoretically the growth can be exponential. This is illustrated by the following example.

**Example 16** Take $A = \{a_{ij}\}$ with

$$
a_{ij} = \begin{cases}
1, & i=j \\
-1, & i>j \\
0, & \text{otherwise}.
\end{cases}
$$

Then with very small $\varepsilon>0$ one has

$$
P_1 = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}, \quad
P_1 A = \begin{bmatrix} 1 & 1 \\ \varepsilon & 1 \end{bmatrix}
\begin{bmatrix} 1 & 1 \\ 0 & 1-\varepsilon \end{bmatrix}.
$$

With $\varepsilon = 10^{-18}$ one has $1-\varepsilon \approx 1$ and the second pivot is tiny. This forces large multipliers in L and huge entries in U. In the $n\times n$ case the largest entry in U grows like $2^{n-1}$.

In practice such matrices never appear. The worst observed growth in real applications is very modest (around 10–100). Nevertheless, theoretically one can have

$$
\max_{i,j} |u_{ij}| \approx 2^{n-1} \max_{i,j} |a_{ij}|.
$$

This means that the complexity of finding the LU factorization with partial pivoting is still $O(n^3)$, but the storage requirement can be up to $O(n^2)$ in the worst case (instead of $O(n)$).

One can try to remedy the situation by also allowing column pivoting, i.e., computing

$$
PAQ = LU
$$

with permutation matrices $P$ and $Q$. This is called complete pivoting. It is more expensive ($O(n^3)$ still, but larger constant) and in practice the growth is only marginally better.

### 6.3 Floating point arithmetic and backward stability

In IEEE 754 double precision (the standard today), the unit roundoff is

$$
\varepsilon_{\text{machine}} = 2^{-53} \approx 1.11 \times 10^{-16}.
$$

The floating-point numbers are of the form $x(1+\varepsilon)$ with $|\varepsilon| \leq \varepsilon_{\text{machine}}$.

In finite precision, the computed factors $\hat{L}$ and $\hat{U}$ satisfy

$$
\hat{L} \hat{U} = A + \delta A, \quad \|\delta A\| = O(\varepsilon_{\text{machine}} \|L\| \|U\|).
$$

With partial pivoting one has the famous backward stability result:

$$
\hat{L} \hat{U} = PA + \delta A, \quad \|\delta A\| \leq O(\rho \varepsilon_{\text{machine}}) \|A\|
$$

where the growth factor

$$
\rho = \frac{\max_{i,j} |u_{ij}|}{\max_{i,j} |a_{ij}|}
$$

is typically very close to 1 (rarely exceeds 100). This means that the computed LU factorization is as accurate as if we had solved the nearby problem $(A + \delta A)x = b$ exactly, with a tiny relative perturbation $\delta A$.

⁹ By a flop is meant a floating point operation: sum, difference, product or a fraction of two complex numbers.  
¹⁰ This example is from [8].