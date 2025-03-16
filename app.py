import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# ---------- SQLite Helper Functions ----------

def init_db():
    conn = sqlite3.connect("app.db", check_same_thread=False)
    c = conn.cursor()
    # Create CRM table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS crm (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           name TEXT,
           contact TEXT,
           email TEXT,
           company TEXT,
           address TEXT,
           requirement TEXT,
           lead_stage TEXT
        )
    ''')
    # Create To‑Do table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS todo (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           task TEXT,
           date_open TEXT,
           date_close TEXT,
           reminder TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_crm_entry(entry):
    conn = sqlite3.connect("app.db", check_same_thread=False)
    c = conn.cursor()
    c.execute(
        "INSERT INTO crm (name, contact, email, company, address, requirement, lead_stage) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (entry["name"], entry["contact"], entry["email"], entry["company"], entry["address"], entry["requirement"], entry["lead_stage"])
    )
    conn.commit()
    conn.close()

def add_todo_entry(entry):
    conn = sqlite3.connect("app.db", check_same_thread=False)
    c = conn.cursor()
    c.execute(
        "INSERT INTO todo (task, date_open, date_close, reminder) VALUES (?, ?, ?, ?)",
        (entry["task"], entry["date_open"], entry["date_close"], entry["reminder"])
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

# ---------- Initialize Database ----------
init_db()

# ---------- Streamlit App UI ----------
st.title("CRM & To‑Do Application with Delete Option")

# Create two columns for side-by-side sections
col1, col2 = st.columns(2)

# ----- CRM Section -----
with col1:
    st.header("CRM Application")
    
    # Form to add a new CRM entry
    with st.form("crm_form", clear_on_submit=True):
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
    
    st.subheader("CRM Entries")
    df_crm = load_crm_entries()
    if not df_crm.empty:
        st.dataframe(df_crm)
        # Provide a dropdown to choose a CRM ID for deletion
        delete_crm_id = st.selectbox("Select CRM ID to delete", options=df_crm["id"].tolist(), key="crm_delete")
        if st.button("Delete Selected CRM Entry"):
            delete_crm_entry(delete_crm_id)
            st.success(f"Deleted CRM Entry with ID {delete_crm_id}")
            # Refresh table after deletion
            df_crm = load_crm_entries()
            st.dataframe(df_crm)
    else:
        st.info("No CRM entries yet.")

# ----- To‑Do Section -----
with col2:
    st.header("To‑Do List")
    
    # Form to add a new To‑Do entry
    with st.form("todo_form", clear_on_submit=True):
        task = st.text_input("Task")
        date_open = st.date_input("Date of Opening", value=date.today())
        date_close = st.date_input("Closing Date", value=date.today())
        reminder = st.text_input("Reminder", help="e.g., Follow up soon")
        submitted_todo = st.form_submit_button("Add Task")
        if submitted_todo:
            entry = {
                "task": task,
                "date_open": date_open.strftime("%Y-%m-%d"),
                "date_close": date_close.strftime("%Y-%m-%d"),
                "reminder": reminder
            }
            add_todo_entry(entry)
            st.success("To‑Do Entry added!")
    
    st.subheader("To‑Do Entries")
    df_todo = load_todo_entries()
    if not df_todo.empty:
        st.dataframe(df_todo)
        # Provide a dropdown to choose a To‑Do ID for deletion
        delete_todo_id = st.selectbox("Select To‑Do ID to delete", options=df_todo["id"].tolist(), key="todo_delete")
        if st.button("Delete Selected To‑Do Entry"):
            delete_todo_entry(delete_todo_id)
            st.success(f"Deleted To‑Do Entry with ID {delete_todo_id}")
            # Refresh table after deletion
            df_todo = load_todo_entries()
            st.dataframe(df_todo)
    else:
        st.info("No To‑Do entries yet.")
