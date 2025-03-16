import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# ---------- SQLite Helper Functions ----------

def init_db():
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    # Create CRM table if not exists
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
    # Create ToDo table if not exists
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
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    c.execute("INSERT INTO crm (name, contact, email, company, address, requirement, lead_stage) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (entry["name"], entry["contact"], entry["email"], entry["company"], entry["address"], entry["requirement"], entry["lead_stage"]))
    conn.commit()
    conn.close()

def add_todo_entry(entry):
    conn = sqlite3.connect("app.db")
    c = conn.cursor()
    c.execute("INSERT INTO todo (task, date_open, date_close, reminder) VALUES (?, ?, ?, ?)",
              (entry["task"], entry["date_open"], entry["date_close"], entry["reminder"]))
    conn.commit()
    conn.close()

def load_crm_entries():
    conn = sqlite3.connect("app.db")
    df = pd.read_sql_query("SELECT * FROM crm", conn)
    conn.close()
    return df

def load_todo_entries():
    conn = sqlite3.connect("app.db")
    df = pd.read_sql_query("SELECT * FROM todo", conn)
    conn.close()
    return df

# ---------- Initialize Database ----------
init_db()

# ---------- Streamlit App UI ----------
st.title("CRM & To‑Do Application with Filtering")

st.markdown("### CRM Application")
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

# ------------------ CRM Filter Options ------------------
st.markdown("#### Filter CRM Entries")
filter_name = st.text_input("Filter by Name", key="filter_name")
filter_stage = st.selectbox("Filter by Stage of Lead", options=["All", "New", "In Progress", "Qualified", "Closed"], key="filter_stage")

df_crm = load_crm_entries()
if not df_crm.empty:
    if filter_name:
        df_crm = df_crm[df_crm['name'].str.contains(filter_name, case=False, na=False)]
    if filter_stage != "All":
        df_crm = df_crm[df_crm['lead_stage'] == filter_stage]
    st.dataframe(df_crm)
else:
    st.info("No CRM entries yet.")

st.markdown("---")
st.markdown("### To‑Do List")
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

# ------------------ To‑Do Filter Options ------------------
st.markdown("#### Filter To‑Do Entries")
filter_task = st.text_input("Filter by Task", key="filter_task")
df_todo = load_todo_entries()
if not df_todo.empty:
    if filter_task:
        df_todo = df_todo[df_todo['task'].str.contains(filter_task, case=False, na=False)]
    st.dataframe(df_todo)
else:
    st.info("No To‑Do entries yet.")
