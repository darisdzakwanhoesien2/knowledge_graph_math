# Matrix Computations

**Marko Huhtanen**

## 1 Introduction

Matrix computations is at the center of numerical analysis (or scientific computing or computational science or data science, or whatever discipline requires concretely solving problems) requiring knowledge of several mathematical techniques and at least a rudimentary understanding of programming. In the early era during the 50s and 60s, the field could be described as being composed of certain fundamental matrix factorizations and how to compute them reliably. Then computer architectures were sequential whereas parallel computing has become the dominant paradigm since. These include the LU factorization and SVD decomposition, as well as algorithms for solving the eigenvalue problem. The complexity of these algorithms is $O(n^3)$ while the storage requirement is $O(n^2)$.

Having these algorithms in an acceptable (early) form did not mean that the numerical linear algebra problems were wiped away. First, there are a lot of applications requiring far more intricate factorizations which an active area of research nowadays. Second, typically applications involve partial differential equations (PDE), already from the very early era of computing of the 40s. Problems with PDE can be solved approximately only. Once discretized, the matrices approximating the corresponding linear operators are sparse. Roughly, this means that only $O(n)$ of the entries are nonzeros. (The reason: differentiation operates locally on functions at a point.) Stored by taking this into account, i.e., zeros are not stored, the storage requirement is just $O(n)$ as opposed to $O(n^2)$. Consequently, very large matrices could be generated to approximate the original problem. In fact, so large that the existing matrix computational techniques could not be used at all to solve the corresponding linear algebra problems. This was (and still is) certainly irritating: everything has been carefully set up and it just remains to do the matrix computations. Except that it is not going to happen. The solution turns out to be out of reach because of its severe computational complexity. Something that was considered originally a trivial linear algebra problem has turned into an exact opposite, i.e., actually an exceptionally tough problem. So either you scale down your ambitions and accept coarser approximations (something you do not want to do), or try to solve the linear algebra problems somehow (but

---
*Page 1 of original notes contains only big-O complexity illustrations:*

O(n³)  
O(n²)  

O(n)  
O(n)  
O(n²)  

---

not at any cost since you cannot afford it). This is a typical situation. This type of “very large scale problems” appear everywhere and they must be solved in one way or the other and as fast as possible.

From the 70s iterative methods started seriously gaining ground to solve very large linear algebra problems without $O(n^3)$ complexity and $O(n^2)$ storage requirement. Analogous developments are still going on in every area of numerical analysis. As a rule, in exciting iterative methods, the matrix (or matrices) related with the problem cannot be manipulated freely. For example, it may be that matrix-vector products with the matrix is the only information available, although you certainly want to avoid such an extreme. However, mathematically this means that the underlying assumptions are getting closer to those usually made in, let us say, operator theory. To get an idea what this could imply as opposed to studying classical matrix analysis, assuming having the Hermitian transpose may be unrealistic.

A reason for writing these lecture notes is the hope of being able to combine classical matrix analytic techniques with those mathematical ideas that are useful in solving practical problems and developing new algorithms. Occasionally this means that the viewpoint is slightly abstract. The abstractness is, however, not an aim. After all, computations are at center of this course and that means that at some point one must come up with an algorithm to solve the problem. A purpose of this course is that the student can, with self confidence, enter and deal with applications where matrices appear.

It is assumed that the students have learnt undergraduate linear algebra and know things such as the Gram-Schmidt orthogonalization process, the Gaussian elimination and know basics of the eigenvalues and eigenvectors, like how to solve tiny (2-by-2 or 3-by-3) eigenvalue problems by hand. One should also be familiar with the standard Euclidean geometry of $\mathbb{C}^n$ originating from the inner product

$$
(x,y) = y^*x = \sum_{j=1}^n x_j \overline{y_j}
\qquad x,y \in \mathbb{C}^n .
$$

(This is, of course, needed in the Gram-Schmidt orthogonalization.)

## 2 Product of matrix subspaces in factoring matrices

Matrices arise in applications such as discretizing PDE, optimization, representing graphs, digitalizing images, storing data etc. Once the matrix is stored on a computer¹ (or on several computers), the underlying problem remains

---

*Page 2 of original notes contains only the following mathematical notation:*

O(n³)  
O(n²)  

$$
\begin{aligned}
\mathbb{C}^n \\
(x,y) &= y^*x = \sum_{j=1}^n x_j \overline{y_j} \\
x,y &\in \mathbb{C}^n
\end{aligned}
$$

---

¹ Computer matters have any device that performs arithmetic operations.