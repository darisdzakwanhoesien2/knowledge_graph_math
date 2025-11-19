# Tekniikan matematiikka / Engineering mathematics  
**Optimoinnin perusteet (031025A) / Introduction to Optimization**  
**Loppukoe / Exam, 19.12.2019**

### 1. Tarkastellaan rajoittamatonta optimointiongelmaa / Let us consider the unconstrained optimization problem

$$
\min_{x \in \mathbb{R}^3} f(x) = x_1^2 + x_2^2 + x_3^2 - x_1 x_2 - 2x_1 + 4x_2
$$

Onko kohdefunktio $f(x)$ konveksi? Anna perustelu.  
Is the objective function $f(x)$ convex? Justify your answer.

Ratkaise ongelma konjugaattigradienttimenetelmällä lähtien alkuarvauksesta  
Solve the problem using the conjugate gradient method starting from the initial guess

$$
x^{(0)} = \begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix}.
$$

### 2. Tarkastellaan optimointiongelmaa / Consider the optimization problem

$$
\min \; -x_1 - x_2
$$

rajoitteineen / subject to

$$
\begin{align*}
x_2 &\leq 3, \\
x_1^2 + x_2 &\leq 1.
\end{align*}
$$

Käytä KKT-ehtoja ongelman optimaalisen ratkaisun löytämiseen.  
Use the KKT conditions to locate the optimal solution of the problem.

### 3. Tarkastellaan rajoitettua optimointiongelmaa / Let us consider the constrained optimization problem

$$
\min \; x_1^2 + x_2^2 + x_3^2 - x_1 x_2 - 2x_1 + 4x_2
$$

rajoitteineen / subject to

$$
\begin{align*}
-x_1 - x_2 &\leq 0, \\
1 - x_2 &\leq 0.
\end{align*}
$$

a) Määritä ongelman dualifunktio ja vastaava dualiongelma.  
   Find the dual function and the corresponding dual problem.

b) Ratkaise dualiongelman optimaalinen ratkaisu.  
   Find the optimal solution of the dual problem.

### 4. Tarkastellaan optimointiongelmaa / Consider the (constrained) optimization problem

$$
\min_{x \in \mathbb{R}^2} \frac{1}{2} \|Ax - b\|^2,
$$

missä / where

$$
A = \begin{bmatrix}
2 & -1 \\
-1 & 2 \\
1 & 1
\end{bmatrix}, \quad
b = \begin{bmatrix}
2 \\
1 \\
4
\end{bmatrix}.
$$

Osoita, että piste / Show that the point

$$
\tilde{x} = \begin{bmatrix}
\frac{4}{3} \\
\frac{8}{3}
\end{bmatrix}
$$

on tehtävän optimaalinen ratkaisu.  
is the optimal solution.