import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

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
    # Create To‑Do table
    c.execute('''
        CREATE TABLE IF NOT EXISTS todo (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           task TEXT,
           date_open TEXT,
           date_close TEXT,
           reminder TEXT
        )
    ''')
    # Create Meeting table with additional columns for purpose and remark
    c.execute('''
        CREATE TABLE IF NOT EXISTS meeting (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           meeting_date TEXT,
           name TEXT,
           email TEXT,
           contact TEXT,
           address TEXT,
           department TEXT,
           purpose TEXT,
           remark TEXT
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
        "INSERT INTO todo (task, date_open, date_close, reminder) VALUES (?, ?, ?, ?)",
        (entry["task"], entry["date_open"], entry["date_close"], entry["reminder"])
    )
    conn.commit()
    conn.close()

def add_meeting_entry(entry):
    conn = sqlite3.connect("app.db", check_same_thread=False)
    c = conn.cursor()
    c.execute(
        "INSERT INTO meeting (meeting_date, name, email, contact, address, department, purpose, remark) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (entry["meeting_date"], entry["name"], entry["email"], entry["contact"], entry["address"], entry["department"], entry["purpose"], entry["remark"])
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

def load_meeting_entries():
    conn = sqlite3.connect("app.db", check_same_thread=False)
    df = pd.read_sql_query("SELECT * FROM meeting", conn)
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

def delete_meeting_entry(entry_id):
    conn = sqlite3.connect("app.db", check_same_thread=False)
    c = conn.cursor()
    c.execute("DELETE FROM meeting WHERE id=?", (entry_id,))
    conn.commit()
    conn.close()

def update_meeting_entry(entry):
    conn = sqlite3.connect("app.db", check_same_thread=False)
    c = conn.cursor()
    c.execute(
        "UPDATE meeting SET meeting_date=?, name=?, email=?, contact=?, address=?, department=?, purpose=?, remark=? WHERE id=?",
        (entry["meeting_date"], entry["name"], entry["email"], entry["contact"], entry["address"], entry["department"], entry["purpose"], entry["remark"], entry["id"])
    )
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

st.markdown('<div class="header">Enhanced CRM, To‑Do & Meeting App</div>', unsafe_allow_html=True)

# Create three tabs for CRM, To‑Do, and Meeting applications
tabs = st.tabs(["CRM Application", "To‑Do List", "Meeting List"])

# ----- CRM Tab -----
with tabs[0]:
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

# ----- To‑Do Tab -----
with tabs[1]:
    st.markdown('<div class="subheader">To‑Do List</div>', unsafe_allow_html=True)
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
    
    st.markdown('<div class="subheader">To‑Do Entries</div>', unsafe_allow_html=True)
    df_todo = load_todo_entries()
    if not df_todo.empty:
        st.dataframe(df_todo, use_container_width=True)
        delete_todo_id = st.selectbox("Select To‑Do ID to delete", options=df_todo["id"].tolist(), key="todo_delete")
        if st.button("Delete Selected To‑Do Entry"):
            delete_todo_entry(delete_todo_id)
            st.success(f"Deleted To‑Do Entry with ID {delete_todo_id}")
            df_todo = load_todo_entries()
            st.dataframe(df_todo, use_container_width=True)
    else:
        st.info("No To‑Do entries yet.")

# ----- Meeting Tab -----
with tabs[2]:
    st.markdown('<div class="subheader">Meeting List</div>', unsafe_allow_html=True)
    # Meeting Entry Form with additional fields Purpose and Remark
    with st.form("meeting_form", clear_on_submit=True):
        meeting_date = st.date_input("Meeting Date", value=date.today())
        meeting_name = st.text_input("Name")
        meeting_email = st.text_input("Email")
        meeting_contact = st.text_input("Contact")
        meeting_address = st.text_input("Address")
        meeting_department = st.text_input("Department")
        purpose = st.text_input("Purpose")
        remark = st.text_area("Remark")
        submitted_meeting = st.form_submit_button("Add Meeting Entry")
        if submitted_meeting:
            entry = {
                "meeting_date": meeting_date.strftime("%Y-%m-%d"),
                "name": meeting_name,
                "email": meeting_email,
                "contact": meeting_contact,
                "address": meeting_address,
                "department": meeting_department,
                "purpose": purpose,
                "remark": remark
            }
            add_meeting_entry(entry)
            st.success("Meeting Entry added!")
    
    st.markdown('<div class="subheader">Meeting Entries</div>', unsafe_allow_html=True)
    df_meeting = load_meeting_entries()
    if not df_meeting.empty:
        st.dataframe(df_meeting, use_container_width=True)
        col1, col2 = st.columns(2)
        with col1:
            delete_meeting_id = st.selectbox("Select Meeting ID to delete", options=df_meeting["id"].tolist(), key="meeting_delete")
            if st.button("Delete Selected Meeting Entry"):
                delete_meeting_entry(delete_meeting_id)
                st.success(f"Deleted Meeting Entry with ID {delete_meeting_id}")
                df_meeting = load_meeting_entries()
                st.dataframe(df_meeting, use_container_width=True)
        with col2:
            edit_meeting_id = st.selectbox("Select Meeting ID to edit", options=df_meeting["id"].tolist(), key="meeting_edit")
            if st.button("Edit Selected Meeting Entry"):
                # Retrieve the selected meeting entry
                entry_to_edit = df_meeting[df_meeting["id"] == edit_meeting_id].iloc[0]
                with st.form("edit_meeting_form", clear_on_submit=True):
                    meeting_date_edit = st.date_input("Meeting Date", value=pd.to_datetime(entry_to_edit["meeting_date"]))
                    meeting_name_edit = st.text_input("Name", value=entry_to_edit["name"])
                    meeting_email_edit = st.text_input("Email", value=entry_to_edit["email"])
                    meeting_contact_edit = st.text_input("Contact", value=entry_to_edit["contact"])
                    meeting_address_edit = st.text_input("Address", value=entry_to_edit["address"])
                    meeting_department_edit = st.text_input("Department", value=entry_to_edit["department"])
                    purpose_edit = st.text_input("Purpose", value=entry_to_edit["purpose"] if "purpose" in entry_to_edit else "")
                    remark_edit = st.text_area("Remark", value=entry_to_edit["remark"] if "remark" in entry_to_edit else "")
                    submitted_edit = st.form_submit_button("Update Meeting Entry")
                    if submitted_edit:
                        updated_entry = {
                            "id": edit_meeting_id,
                            "meeting_date": meeting_date_edit.strftime("%Y-%m-%d"),
                            "name": meeting_name_edit,
                            "email": meeting_email_edit,
                            "contact": meeting_contact_edit,
                            "address": meeting_address_edit,
                            "department": meeting_department_edit,
                            "purpose": purpose_edit,
                            "remark": remark_edit,
                        }
                        update_meeting_entry(updated_entry)
                        st.success(f"Meeting Entry with ID {edit_meeting_id} updated!")
                        df_meeting = load_meeting_entries()
                        st.dataframe(df_meeting, use_container_width=True)
    else:
        st.info("No Meeting entries yet.")
