import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Simplex Step-by-Step Explorer", layout="wide")

st.title("Simplex / Tableau Step-by-Step Explorer")
st.markdown("""
This app loads an initial simplex tableau (based on the screenshot you provided) and lets you
walk through pivot steps interactively. Features:
- Show current tableau
- Auto-select entering variable (most negative objective coefficient) and leaving row (min positive ratio)
- Manually pick pivot column/row
- Apply pivot and record step history
- Undo / redo steps

How to use: run `streamlit run streamlit_simplex_app.py`.
""")

# -------------------------
# Utility functions
# -------------------------

def make_initial_tableau():
    # The tableau is arranged as columns: x1, x2, s1, s2, s3, s4, RHS
    # We'll set it to the numbers visible in the image's first tableau row block
    cols = ['x1','x2','s1','s2','s3','s4','RHS']
    data = [
        [6, 4, 1, 0, 0, 0, 24],  # s1
        [1, 2, 0, 1, 0, 0, 6],   # s2
        [-1,1, 0, 0, 1, 0, 1],   # s3
        [0,1, 0, 0, 0, 1, 2],    # s4
        [-5,-4,0,0,0,0,0]        # objective row (min row)
    ]
    df = pd.DataFrame(data, columns=cols, index=['s1','s2','s3','s4','obj'])
    return df


def pivot(tableau, pivot_row, pivot_col):
    # pivot_row: integer index, pivot_col: column name
    T = tableau.copy().astype(float)
    pivot_val = T.iloc[pivot_row][pivot_col]
    if pivot_val == 0:
        raise ValueError('Pivot value is zero')
    # divide pivot row
    T.iloc[pivot_row] = T.iloc[pivot_row] / pivot_val
    # eliminate other rows
    for r in range(T.shape[0]):
        if r == pivot_row:
            continue
        factor = T.iloc[r][pivot_col]
        T.iloc[r] = T.iloc[r] - factor * T.iloc[pivot_row]
    return T


def find_entering_column(tableau):
    # For minimization with last row as objective, choose most negative coefficient in objective row (excluding RHS)
    obj = tableau.iloc[-1].copy()
    obj = obj.drop('RHS')
    most_negative = obj.min()
    if most_negative >= 0:
        return None
    return obj.idxmin()


def find_leaving_row(tableau, entering_col):
    # ratio test: RHS / column value for positive column entries
    ratios = []
    for i, idx in enumerate(tableau.index[:-1]):  # exclude objective row
        col_val = tableau.iloc[i][entering_col]
        rhs = tableau.iloc[i]['RHS']
        if col_val > 0:
            ratios.append((i, rhs / col_val))
    if not ratios:
        return None
    # pick row with smallest ratio
    ratios.sort(key=lambda x: x[1])
    return ratios[0][0]

# -------------------------
# Session state initialization
# -------------------------

if 'history' not in st.session_state:
    st.session_state.history = []
if 'current' not in st.session_state:
    st.session_state.current = make_initial_tableau()
    st.session_state.history.append(st.session_state.current.copy())
if 'step_notes' not in st.session_state:
    st.session_state.step_notes = []

# -------------------------
# Sidebar controls
# -------------------------

with st.sidebar:
    st.header('Controls')
    auto_pivot = st.checkbox('Auto-select pivot (entering & leaving)', value=True)
    manual_enter = st.checkbox('Allow manual pivot selection', value=False)
    if st.button('Reset to initial'):
        st.session_state.current = make_initial_tableau()
        st.session_state.history = [st.session_state.current.copy()]
        st.session_state.step_notes = []

    st.markdown('---')
    st.write('History')
    if st.button('Undo last step'):
        if len(st.session_state.history) > 1:
            st.session_state.history.pop()
            st.session_state.current = st.session_state.history[-1].copy()
            if st.session_state.step_notes:
                st.session_state.step_notes.pop()
    if st.button('Clear history'):
        st.session_state.history = [st.session_state.current.copy()]
        st.session_state.step_notes = []

# -------------------------
# Main display: current tableau
# -------------------------

st.subheader('Current tableau')
st.dataframe(st.session_state.current.style.format(precision=6))

# show basic info: entering column and leaving row if auto
enter_col = None
leave_row = None
if auto_pivot:
    enter_col = find_entering_column(st.session_state.current)
    if enter_col is not None:
        leave_row = find_leaving_row(st.session_state.current, enter_col)

col1, col2 = st.columns([2,1])
with col1:
    st.markdown('**Auto selection**')
    st.write('Entering column:', enter_col)
    st.write('Leaving row index:', leave_row)

with col2:
    st.markdown('**Manual pivot**')
    cols = list(st.session_state.current.columns)
    # Exclude RHS from pivot columns
    pivot_columns = [c for c in cols if c != 'RHS']
    manual_col = st.selectbox('Pivot column', options=pivot_columns, index=0)
    manual_row_label = st.selectbox('Pivot row (constraint rows)', options=list(st.session_state.current.index[:-1]))
    manual_row = list(st.session_state.current.index).index(manual_row_label)
    apply_manual = st.button('Apply manual pivot')

# Apply auto pivot button
if auto_pivot and enter_col is not None:
    if st.button('Apply auto pivot'):
        if leave_row is None:
            st.error('No leaving row found -- unbounded?')
        else:
            newT = pivot(st.session_state.current, leave_row, enter_col)
            st.session_state.current = newT
            st.session_state.history.append(newT.copy())
            st.session_state.step_notes.append(f'Pivot on col {enter_col}, row {st.session_state.current.index[leave_row]}')

# Apply manual pivot
if manual_enter and apply_manual:
    try:
        newT = pivot(st.session_state.current, manual_row, manual_col)
        st.session_state.current = newT
        st.session_state.history.append(newT.copy())
        st.session_state.step_notes.append(f'Manual pivot on col {manual_col}, row {manual_row_label}')
    except Exception as e:
        st.error(str(e))

# Show step notes and history
st.markdown('---')
st.subheader('Step history')
for i, tbl in enumerate(st.session_state.history):
    with st.expander(f'Step {i}'):
        st.write('Note:', st.session_state.step_notes[i-1] if i>0 and i-1 < len(st.session_state.step_notes) else 'initial')
        st.dataframe(tbl.style.format(precision=6))

# Export current tableau
st.markdown('---')
if st.button('Export current tableau to CSV'):
    csv = st.session_state.current.to_csv(index=True)
    st.download_button('Download CSV', data=csv, file_name='tableau_current.csv')

# Minimal explanation block
st.markdown('''
### Notes
- The objective row is assumed to be the last row and the problem is set as minimization (as in your screenshot). If you have a different orientation (maximization), sign flips are needed.
- Pivot operations divide the pivot row by the pivot element, then eliminate the pivot column in other rows.

If you want I can extend this app to:
- Parse arbitrary tableaux pasted as CSV
- Visualize basic variable assignments after each step
- Animate the row operations step-by-step (show intermediate arithmetic)
''')
