import streamlit as st
import sqlite3
import pandas as pd
from datetime import date, datetime

# ---------- SQLite Helper Functions ----------

def init_db():
    conn = sqlite3.connect("app.db", check_same_thread=False)
    c = conn.cursor()
    # Create CRM table (with an entry_date field)
    c.execute('''
        CREATE TABLE IF NOT EXISTS crm (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           entry_date TEXT,
           name TEXT,
           contact TEXT,
           email TEXT,
           company TEXT,
           address TEXT,
           requirement TEXT,
           lead_stage TEXT
        )
    ''')
    # Create To‑Do table with an additional 'status' column for task state
    c.execute('''
        CREATE TABLE IF NOT EXISTS todo (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           task TEXT,
           date_open TEXT,
           date_close TEXT,
           reminder TEXT,
           status TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_crm_entry(entry):
    conn = sqlite3.connect("app.db", check_same_thread=False)
    c = conn.cursor()
    c.execute(
        "INSERT INTO crm (entry_date, name, contact, email, company, address, requirement, lead_stage) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (entry["entry_date"], entry["name"], entry["contact"], entry["email"], entry["company"], entry["address"], entry["requirement"], entry["lead_stage"])
    )
    conn.commit()
    conn.close()

def add_todo_entry(entry):
    conn = sqlite3.connect("app.db", check_same_thread=False)
    c = conn.cursor()
    c.execute(
        "INSERT INTO todo (task, date_open, date_close, reminder, status) VALUES (?, ?, ?, ?, ?)",
        (entry["task"], entry["date_open"], entry["date_close"], entry["reminder"], entry["status"])
    )
    conn.commit()
    conn.close()

def load_crm_entries():
    conn = sqlite3.connect("app.db", check_same_thread=False)
    df = pd.read_sql_query("SELECT * FROM crm", conn)
    conn.close()
    return df

def load_todo_entries():
    conn = sqlite3.connect("app.db", check_same_thread=False)
    df = pd.read_sql_query("SELECT * FROM todo", conn)
    conn.close()
    return df

def delete_crm_entry(entry_id):
    conn = sqlite3.connect("app.db", check_same_thread=False)
    c = conn.cursor()
    c.execute("DELETE FROM crm WHERE id=?", (entry_id,))
    conn.commit()
    conn.close()

def delete_todo_entry(entry_id):
    conn = sqlite3.connect("app.db", check_same_thread=False)
    c = conn.cursor()
    c.execute("DELETE FROM todo WHERE id=?", (entry_id,))
    conn.commit()
    conn.close()

def update_todo_status(task_id, new_status):
    """Update the status for a given todo task."""
    conn = sqlite3.connect("app.db", check_same_thread=False)
    c = conn.cursor()
    c.execute("UPDATE todo SET status = ? WHERE id = ?", (new_status, task_id))
    conn.commit()
    conn.close()

# ---------- Initialize Database ----------
init_db()

# ---------- Streamlit App UI ----------

# Inject custom CSS for a polished look
st.markdown(
    """
    <style>
    .header {
        text-align: center;
        color: #007bff;
        font-size: 2.5em;
        font-weight: 600;
        margin-bottom: 20px;
    }
    .subheader {
        text-align: center;
        font-size: 1.5em;
        font-weight: 500;
        margin: 20px 0 10px 0;
        border-bottom: 2px solid #007bff;
        padding-bottom: 5px;
    }
    .section {
        background-color: #fff;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown('<div class="header">Enhanced CRM & To‑Do App</div>', unsafe_allow_html=True)

# Create two columns for side-by-side layout
col1, col2 = st.columns(2)

# ----- CRM Section -----
with col1:
    st.markdown('<div class="subheader">CRM Application</div>', unsafe_allow_html=True)
    with st.form("crm_form", clear_on_submit=True):
        entry_date = st.date_input("Entry Date", value=date.today())
        crm_name = st.text_input("Name")
        crm_contact = st.text_input("Contact")
        crm_email = st.text_input("Email")
        crm_company = st.text_input("Company")
        crm_address = st.text_input("Address")
        crm_requirement = st.text_area("Requirement")
        lead_stage = st.selectbox("Stage of Lead", ["New", "In Progress", "Qualified", "Closed"])
        submitted_crm = st.form_submit_button("Add CRM Entry")
        if submitted_crm:
            entry = {
                "entry_date": entry_date.strftime("%Y-%m-%d"),
                "name": crm_name,
                "contact": crm_contact,
                "email": crm_email,
                "company": crm_company,
                "address": crm_address,
                "requirement": crm_requirement,
                "lead_stage": lead_stage
            }
            add_crm_entry(entry)
            st.success("CRM Entry added!")
    
    st.markdown('<div class="subheader">CRM Entries</div>', unsafe_allow_html=True)
    df_crm = load_crm_entries()
    if not df_crm.empty:
        st.dataframe(df_crm, use_container_width=True)
        delete_crm_id = st.selectbox("Select CRM ID to delete", options=df_crm["id"].tolist(), key="crm_delete")
        if st.button("Delete Selected CRM Entry"):
            delete_crm_entry(delete_crm_id)
            st.success(f"Deleted CRM Entry with ID {delete_crm_id}")
            df_crm = load_crm_entries()
            st.dataframe(df_crm, use_container_width=True)
    else:
        st.info("No CRM entries yet.")

# ----- To‑Do Section -----
with col2:
    st.markdown('<div class="subheader">To‑Do List</div>', unsafe_allow_html=True)
    with st.form("todo_form", clear_on_submit=True):
        task = st.text_input("Task")
        date_open = st.date_input("Date of Opening", value=date.today())
        date_close = st.date_input("Closing Date", value=date.today())
        # Radio button for task status (default is Pending)
        status = st.radio("Task Status", options=["Pending", "Completed"], index=0)
        # Checkbox to optionally set a reminder date
        set_reminder = st.checkbox("Set Reminder?")
        reminder_date = None
        if set_reminder:
            reminder_date = st.date_input("Reminder Date", value=date.today())
        submitted_todo = st.form_submit_button("Add Task")
        if submitted_todo:
            entry = {
                "task": task,
                "date_open": date_open.strftime("%Y-%m-%d"),
                "date_close": date_close.strftime("%Y-%m-%d"),
                "reminder": reminder_date.strftime("%Y-%m-%d") if reminder_date else "",
                "status": status
            }
            add_todo_entry(entry)
            st.success("To‑Do Entry added!")
    
    st.markdown('<div class="subheader">To‑Do Entries</div>', unsafe_allow_html=True)
    df_todo = load_todo_entries()
    if not df_todo.empty:
        # Create header row using columns
        header_cols = st.columns([1, 4, 2, 2, 2])
        header_cols[0].write("ID")
        header_cols[1].write("Task")
        header_cols[2].write("Status")
        header_cols[3].write("Opened")
        header_cols[4].write("Reminder")

        # Loop through each todo task and display details with an embedded radio button.
        for _, row in df_todo.iterrows():
            row_cols = st.columns([1, 4, 2, 2, 2])
            row_cols[0].write(row["id"])

            # Apply conditional styling:
            # - Strikethrough for completed tasks
            # - Red text for pending tasks older than 2 days
            task_text = row["task"]
            d_open = date.fromisoformat(row["date_open"])
            if row["status"] == "Completed":
                task_text = f"<s>{task_text}</s>"
            elif row["status"] == "Pending" and (date.today() - d_open).days > 2:
                task_text = f'<span style="color:red;">{task_text}</span>'
            row_cols[1].markdown(task_text, unsafe_allow_html=True)

            # Embed the radio button inside the row for status change
            new_status = row_cols[2].radio(
                "",
                options=["Pending", "Completed"],
                index=0 if row["status"] == "Pending" else 1,
                key=f"row_radio_{row['id']}"
            )

            row_cols[3].write(row["date_open"])
            row_cols[4].write(row["reminder"])

            # Update the task status if the radio selection changed
            if new_status != row["status"]:
                update_todo_status(row["id"], new_status)
                st.experimental_rerun()

        delete_todo_id = st.selectbox("Select To‑Do ID to delete", options=df_todo["id"].tolist(), key="todo_delete")
        if st.button("Delete Selected To‑Do Entry"):
            delete_todo_entry(delete_todo_id)
            st.success(f"Deleted To‑Do Entry with ID {delete_todo_id}")
    else:
        st.info("No To‑Do entries yet.")
