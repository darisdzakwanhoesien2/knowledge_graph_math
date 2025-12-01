import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Simplex Guided Example", layout="wide")

st.title("Simplex — Guided Walkthrough (Example from Notes)")


# ------------------------------------------------------------
# Problem from your screenshot
# ------------------------------------------------------------
# min -12 x1 - 9 x2
# x1 <= 1000
# x2 <= 1500
# x1 + x2 <= 1750
# 4x1 + 2x2 <= 4800

A = np.array([
    [1, 0],
    [0, 1],
    [1, 1],
    [4, 2]
], dtype=float)

b = np.array([1000., 1500., 1750., 4800.], dtype=float)
c = np.array([-12., -9.], dtype=float)

m, n = A.shape
I = np.eye(m)
A_std = np.hstack([A, I])  # [x1 x2 | s1 s2 s3 s4]


# ------------------------------------------------------------
# Build initial tableau
# ------------------------------------------------------------
cols = [f"x{i+1}" for i in range(n)] + [f"s{i+1}" for i in range(m)] + ["RHS"]
idx = [f"s{i+1}" for i in range(m)] + ["obj"]

T = np.zeros((m + 1, n + m + 1))
T[:m, :n+m] = A_std
T[:m, -1] = b
T[-1, :n] = c  # objective row: (-12, -9, 0,0,0,0 | 0)


def arr_to_df(arr):
    return pd.DataFrame(arr, columns=cols, index=idx)


# ------------------------------------------------------------
# Session State
# ------------------------------------------------------------
if "tbl" not in st.session_state:
    st.session_state.tbl = T.copy()

if "basis" not in st.session_state:
    st.session_state.basis = [f"s{i+1}" for i in range(m)]  # initial slack basis

if "step" not in st.session_state:
    st.session_state.step = 0

if "notes" not in st.session_state:
    st.session_state.notes = ["initial"]


# ------------------------------------------------------------
# Display tableau
# ------------------------------------------------------------
st.subheader("Current Tableau")
st.dataframe(arr_to_df(st.session_state.tbl).style.format(precision=4))


# ------------------------------------------------------------
# Controls
# ------------------------------------------------------------
st.markdown("---")
colA, colB, colC = st.columns([1,1,2])

with colA:
    if st.button("Reset"):
        st.session_state.tbl = T.copy()
        st.session_state.basis = [f"s{i+1}" for i in range(m)]
        st.session_state.step = 0
        st.session_state.notes = ["initial"]

with colB:
    if st.button("Prev Step") and st.session_state.step > 0:
        st.session_state.step -= 1

with colC:
    if st.button("Next Step"):
        st.session_state.step += 1

step = st.session_state.step


# ------------------------------------------------------------
# Step 0 — Show B⁻¹b
# ------------------------------------------------------------
if step == 0:
    st.subheader("Step 0 — Initial Basic Feasible Solution")
    st.write("Initial basis:", st.session_state.basis)

    rhs = st.session_state.tbl[:m, -1]
    st.write("Since B = I initially, B⁻¹b = b:")

    df = pd.DataFrame({"basic var": st.session_state.basis, "value": rhs})
    st.table(df)

    st.write("Objective row:")
    st.write(arr_to_df(st.session_state.tbl).iloc[-1, :])

    st.stop()


# ------------------------------------------------------------
# Step 1 — Choose entering variable
# ------------------------------------------------------------
if step == 1:
    st.subheader("Step 1 — Choose entering variable")

    obj = st.session_state.tbl[-1, :n]  # only x1, x2
    entering_idx = int(np.argmin(obj))
    entering_var = cols[entering_idx]

    st.write("Objective coefficients:", obj)
    st.write("Most negative -> entering:", entering_var)

    st.session_state.entering_idx = entering_idx

    st.stop()


# ------------------------------------------------------------
# Step 2 — Compute u = B⁻¹ a_j and ratio test
# ------------------------------------------------------------
if step == 2:
    st.subheader("Step 2 — Compute u = B⁻¹ a_j and ratio test")

    entering_idx = st.session_state.entering_idx
    entering_var = cols[entering_idx]

    st.write("Entering variable:", entering_var)

    # Build B from basis columns
    basis_cols = [cols.index(v) for v in st.session_state.basis]
    B = st.session_state.tbl[:m, basis_cols]

    try:
        B_inv = np.linalg.inv(B)
    except:
        B_inv = np.eye(m)

    a_j = st.session_state.tbl[:m, entering_idx]
    u = B_inv @ a_j

    st.write("Column a_j:", a_j)
    st.write("B⁻¹:")
    st.write(B_inv)
    st.write("u = B⁻¹ a_j:", u)

    ratios = []
    for i in range(m):
        if u[i] > 1e-12:
            ratios.append((i, st.session_state.tbl[i, -1] / u[i]))

    if not ratios:
        st.error("Unbounded: no positive u_i.")
        st.stop()

    ratios.sort(key=lambda x: x[1])
    leaving_row = ratios[0][0]
    leaving_var = st.session_state.basis[leaving_row]

    st.write("Ratios (row, RHS/u):", ratios)
    st.write(f"Leaving variable: {leaving_var}")

    st.session_state.leaving_row = leaving_row
    st.session_state.u = u

    st.stop()


# ------------------------------------------------------------
# Step 3 — Pivot
# ------------------------------------------------------------
if step == 3:
    st.subheader("Step 3 — Pivot and update tableau")

    entering_idx = st.session_state.entering_idx
    leaving_row = st.session_state.leaving_row
    entering_var = cols[entering_idx]

    A_tbl = st.session_state.tbl.copy()
    pivot = A_tbl[leaving_row, entering_idx]

    if abs(pivot) < 1e-12:
        st.error("Pivot is zero.")
        st.stop()

    # Normalize pivot row
    A_tbl[leaving_row, :] /= pivot

    # Eliminate others
    for r in range(A_tbl.shape[0]):
        if r != leaving_row:
            factor = A_tbl[r, entering_idx]
            A_tbl[r, :] -= factor * A_tbl[leaving_row, :]

    # Update basis
    old_basis = st.session_state.basis.copy()
    st.session_state.basis[leaving_row] = entering_var
    st.session_state.tbl = A_tbl

    st.write("Updated basis:", st.session_state.basis)
    st.write("Updated tableau:")
    st.dataframe(arr_to_df(st.session_state.tbl).style.format(precision=4))

    # Compute B⁻¹b
    basis_cols = [cols.index(v) for v in st.session_state.basis]
    B = st.session_state.tbl[:m, basis_cols]

    try:
        B_inv = np.linalg.inv(B)
        B_inv_b = B_inv @ st.session_state.tbl[:m, -1]
        st.write("B⁻¹b after pivot:", B_inv_b)
    except:
        st.warning("B became singular → degeneracy")

    st.stop()


# ------------------------------------------------------------
# Step >= 4 — Continue simplex
# ------------------------------------------------------------
if step >= 4:
    st.subheader(f"Step {step} — Continue simplex iterations")
    st.write("Basis:", st.session_state.basis)
    st.dataframe(arr_to_df(st.session_state.tbl).style.format(precision=4))

    st.write("Press **Next Step** to choose next entering variable.")



# import streamlit as st
# import pandas as pd
# import numpy as np

# st.set_page_config(page_title="Simplex Suite — Guided Example", layout="wide")
# st.title("Simplex Suite — Guided Walkthrough: Example from Notes")
# st.markdown(
#     """
#     We will walk through the specific LP shown in your screenshot (minimize -12 x1 -9 x2 with 4 inequalities).
#     This guided mode follows the steps in the notes: build standard-form tableau, identify entering variable,
#     compute the pivot column effect u = B^{-1} a_j, perform ratio test, pivot, and show updated basis values B^{-1} b.

#     Use the step controls to advance through the worked example.
#     """
# )

# # -------------------------
# # Problem definition (from screenshot)
# # -------------------------
# # min -12 x1 -9 x2
# # s.t.
# # x1 <= 1000
# # x2 <= 1500
# # x1 + x2 <= 1750
# # 4 x1 + 2 x2 <= 4800
# # x >= 0

# A = np.array([[1, 0],
#               [0, 1],
#               [1, 1],
#               [4, 2]], dtype=float)

# b = np.array([1000., 1500., 1750., 4800.], dtype=float)

# # objective coefficients for minimization in original x-space
# c = np.array([-12., -9.], dtype=float)  # note: minimization; tableau will store these as cost row

# # Build standard-form tableau with slack variables s1..s4. We'll order variables as [x1, x2, s1, s2, s3, s4, RHS]
# m, n = A.shape
# I = np.eye(m)
# A_std = np.hstack([A, I])
# cols = [f'x{i+1}' for i in range(n)] + [f's{i+1}' for i in range(m)] + ['RHS']
# idx = [f's{i+1}' for i in range(m)] + ['obj']

# # Initial tableau array
# T = np.zeros((m+1, n+m+1), dtype=float)
# T[:m, :n+m] = A_std
# T[:m, -1] = b
# # objective row: c^T for x (minimization). For tableau we put cost row as c (not negated) and RHS 0
# # Many tableau conventions differ; we'll follow the screenshot: objective row is (-12, -9, 0,0,0,0 | 0)
# T[-1, :n] = c  # place -12, -9 in last row

# # helper conversions
# def arr_to_df(arr):
#     return pd.DataFrame(arr, columns=cols, index=idx)

# # session state for step-by-step
# if 'tbl' not in st.session_state:
#     st.session_state.tbl = T.copy()
# if 'step' not in st.session_state:
#     st.session_state.step = 0
# if 'basis' not in st.session_state:
#     # initial basic variables are the slacks s1..s4 (their columns form identity)
#     st.session_state.basis = [f's{i+1}' for i in range(m)]
# if 'notes' not in st.session_state:
#     st.session_state.notes = ['initial']

# # -------------------------
# # Display current tableau
# # -------------------------
# st.subheader('Initial tableau (standard form)')
# st.write('Variable ordering: ', cols)
# st.dataframe(arr_to_df(st.session_state.tbl).style.format(precision=6))

# # Step controls
# st.markdown('---')
# st.subheader('Guided steps')
# col1, col2, col3 = st.columns([1,1,2])
# with col1:
#     if st.button('Reset example'):
#         st.session_state.tbl = T.copy()
#         st.session_state.step = 0
#         st.session_state.basis = [f's{i+1}' for i in range(m)]
#         st.session_state.notes = ['initial']
# with col2:
#     if st.button('Previous step'):
#         if st.session_state.step > 0:
#             st.session_state.step -= 1
# with col3:
#     if st.button('Next step'):
#         st.session_state.step += 1

# step = st.session_state.step

# # -------------------------
# # Step 0: Show initial basic feasible solution (B = I)
# # -------------------------
# if step == 0:
#     st.markdown('### Step 0 — initial basic feasible solution')
#     st.write('Basic variables (initial):', st.session_state.basis)
#     B_inv_b = st.session_state.tbl[:m, -1]  # since B = I, B^{-1} b = b
#     df = pd.DataFrame({'basic_var': st.session_state.basis, 'value': B_inv_b})
#     st.table(df)
#     st.write('Objective row (c for original x):')
#     st.write(arr_to_df(st.session_state.tbl).loc['obj', :n+2])
#     st.write('Note from notes: since c_B = 0, compute reduced costs s = c_N - c_B B^{-1} N = c_N. Most negative is -12 -> entering x1.')

# # -------------------------
# # Step 1: Choose entering variable (most negative cost coefficient)
# # -------------------------
# elif step == 1:
#     st.markdown('### Step 1 — choose entering variable')
#     obj_row = st.session_state.tbl[-1, :n]  # cost coefficients for x variables
#     st.write('Objective coefficients (for x):', {f'x{i+1}': obj_row[i] for i in range(n)})
#     entering_idx = int(np.argmin(obj_row))
#     entering_var = cols[entering_idx]
#     st.write(f'Entering variable (most negative): {entering_var} with coefficient {obj_row[entering_idx]}')
#     st.session_state.notes.append(f'enter {entering_var}')
#     st.session_state.entering_idx = entering_idx

# # -------------------------
# # Step 2: Compute u = B^{-1} * a_j and ratio test
# # -------------------------
# elif step == 2:
#     st.markdown('### Step 2 — compute u = B^{-1} a_j and perform ratio test')
#     entering_idx = st.session_state.get('entering_idx', 0)
#     entering_var = cols[entering_idx]
#     # B is the identity initially; its columns correspond to slack columns indexes n..n+m-1
#     B_cols = list(range(n, n+m))
#     B = st.session_state.tbl[:m, B_cols]
#     # a_j column (full column in constraints)
#     a_j = st.session_state.tbl[:m, entering_idx]
#     # compute u = B^{-1} * a_j. Since B=I, u = a_j
#     try:
#         B_inv = np.linalg.inv(B)
#     except Exception:
#         B_inv = np.eye(m)
#     u = B_inv.dot(a_j)
#     st.write('Entering var:', entering_var)
#     st.write('Column a_j:', a_j)
#     st.write('B^(-1) (current):')
#     st.write(B_inv)
#     st.write('u = B^{-1} a_j =')
#     st.write(u)
#     # ratio test: RHS / u for u>0
#     ratios = []
#     for i in range(m):
#         if u[i] > 1e-12:
#             ratios.append((i, st.session_state.tbl[i, -1] / u[i]))
#     if not ratios:
#         st.warning('No positive entries in u — problem unbounded in this direction')
#     else:
#         ratios.sort(key=lambda x: x[1])
#         leaving_row = ratios[0][0]
#         leaving_var = st.session_state.basis[leaving_row]
#         st.write('Ratios (row, RHS/u):', ratios)
#         st.write(f'Leaving row chosen: {leaving_row} variable {leaving_var}')
#         st.session_state.leaving_row = leaving_row
#         st.session_state.u = u

# # -------------------------
# # Step 3: Perform pivot (make entering basic, leaving nonbasic)
# # -------------------------
# elif step == 3:
#     st.markdown('### Step 3 — pivot to update basis and tableau')
#     entering_idx = st.session_state.get('entering_idx', 0)
#     entering_var = cols[entering_idx]
#     leaving_row = st.session_state.get('leaving_row', 0)

#     # perform tableau pivot on (leaving_row, entering_idx)
#     A_tbl = st.session_state.tbl.copy()
#     pivot_val = A_tbl[leaving_row, entering_idx]
#     if abs(pivot_val) < 1e-12:
#         st.error('Pivot element is zero — cannot pivot')
#     else:
#         # divide pivot row
#         A_tbl[leaving_row, :] = A_tbl[leaving_row, :] / pivot_val
#         # eliminate other rows
#         for r in range(A_tbl.shape[0]):
#             if r == leaving_row: continue
#             factor = A_tbl[r, entering_idx]
#             A_tbl[r, :] = A_tbl[r, :] - factor * A_tbl[leaving_row, :]

#         # update session state
#         old_basis = st.session_state.basis.copy()
#         st.session_state.basis[leaving_row] = entering_var
#         st.session_state.tbl = A_tbl
#         st.session_state.notes.append(f'Pivot: {entering_var} in, {old_basis[leaving_row]} out')

#         st.write('Updated basis:', st.session_state.basis)
#         st.write('Updated tableau:')
#         st.dataframe(arr_to_df(st.session_state.tbl).style.format(precision=6))
#         # show B^{-1} b: recompute from B columns
#         B_cols = [cols.index(v) for v in st.session_state.basis]
#         # convert to indices in tableau (they are among 0..n+m-1)
#         # find actual column indices of basis variables
#         basis_col_indices = []
#         for v in st.session_state.basis:
#             basis_col_indices.append(cols.index(v))
#         # build basis matrix and compute inverse
#         B = st.session_state.tbl[:m, basis_col_indices]
#         try:
#             B_inv = np.linalg.inv(B)
#             B_inv_b = B_inv.dot(st.session_state.tbl[:m, -1])
#             st.write('B^{-1} b =')
#             st.write(B_inv_b)
#         except Exception:
#             st.warning('B matrix inversion failed (singular) — degeneracy possible')

# # -------------------------
# # Step 4+: show that the new tableau restarts Step 1
# # -------------------------
# else:
#     st.markdown(f'### Step {step} — Continue simplex iterations')
#     st.write('Current basis:', st.session_state.basis)
#     st.dataframe(arr_to_df(st.session_state.tbl).style.format(precision=6))
#     st.write('You can continue by pressing Next to compute entering variable again (most negative coefficient in obj row).')

# # -------------------------
# # Footer & export
# # -------------------------
# st.markdown('---')
# if st.button('Export current tableau CSV'):
#     df = arr_to_df(st.session_state.tbl)
#     csv = df.to_csv(index=True)
#     st.download_button('Download CSV', data=csv, file_name='example_tableau.csv')

# st.markdown('''
# ### Notes
# - The example follows the exact steps in the screenshot: initial basic feasible solution with slack variables as basis, choose x1 (most negative -12) as entering variable, compute u = B^{-1} a_j, perform ratio test, pivot and update B^{-1} b and basis.
# - This guided mode currently implements the first pivot and lets you continue iterating with the Next button. I can extend it to automatically complete Phase I/Phase II, implement two-phase switching for more complex problems, or show intermediate arithmetic operations row-by-row.
# ''')
