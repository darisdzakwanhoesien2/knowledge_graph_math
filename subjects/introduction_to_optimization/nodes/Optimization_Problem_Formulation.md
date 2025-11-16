# Optimization Problem Formulation

**Type:** Concept  
**Domain:** Optimization Foundations  
**Prerequisites:** Calculus, Linear Algebra  
**Related Nodes:** Feasible_Region, Objective_Function, Local_vs_Global_Optimum, Convex_Sets

---

## 1. Definition

An **optimization problem** is defined as:

\[
\min_{x \in \mathcal{X}} f(x)
\]

where:

- \( f : \mathbb{R}^n \to \mathbb{R} \) is the **objective function**
- \( \mathcal{X} \subseteq \mathbb{R}^n \) is the **feasible set**

---

## 2. General Form

\[
\begin{aligned}
\min_x \; f(x) \\
\text{s.t.} \\
g_i(x) \le 0,\quad i=1,\ldots,m \\
h_j(x) = 0,\quad j=1,\ldots,p
\end{aligned}
\]

---

## 3. Types of Optimization Problems

- **Unconstrained**
- **Constrained**
- **Convex**
- **Nonconvex**
- **Smooth / Nonsmooth**

---

## 4. Examples

- Linear programming  
- Quadratic programming  
- Regularized machine learning objectives  

---

## 5. Cross-Links

- *Feasible_Region* defines domain restrictions  
- *Convex_Sets* ensures tractability  
- *KKT_Conditions* generalize optimality conditions  
