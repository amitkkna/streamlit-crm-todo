import streamlit as st
import pandas as pd
from io import BytesIO
from fpdf import FPDF

# Inject custom CSS for improved styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f4f6f9;
    }
    .header-title {
        font-size: 2.5em;
        font-weight: 600;
        text-align: center;
        color: #007bff;
        margin-bottom: 20px;
    }
    .section-header {
        font-size: 1.5em;
        font-weight: 500;
        color: #333;
        margin-bottom: 10px;
        border-bottom: 2px solid #007bff;
        padding-bottom: 5px;
        text-align: center;
    }
    .card {
        background: #fff;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .download-button {
        margin: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App Title
st.markdown('<div class="header-title">CRM & To‑Do Application</div>', unsafe_allow_html=True)

# Initialize session state for persistent storage
if 'crm_entries' not in st.session_state:
    st.session_state.crm_entries = []
if 'todo_entries' not in st.session_state:
    st.session_state.todo_entries = []

# Create two columns for the two sections
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-header">CRM Application</div>', unsafe_allow_html=True)
    
    with st.form("crm_form", clear_on_submit=True):
        crm_name = st.text_input("Name")
        crm_contact = st.text_input("Contact")
        crm_email = st.text_input("Email")
        crm_company = st.text_input("Company")
        crm_address = st.text_input("Address")
        crm_requirement = st.text_area("Requirement")
        lead_stage = st.selectbox("Stage of Lead", ["New", "In Progress", "Qualified", "Closed"])
        submit_crm = st.form_submit_button("Add CRM Entry")
        if submit_crm:
            st.session_state.crm_entries.append({
                "name": crm_name,
                "contact": crm_contact,
                "email": crm_email,
                "company": crm_company,
                "address": crm_address,
                "requirement": crm_requirement,
                "lead_stage": lead_stage
            })
            st.success("CRM Entry added!")
    
    st.markdown('<div class="section-header">CRM Entries</div>', unsafe_allow_html=True)
    if st.session_state.crm_entries:
        df_crm = pd.DataFrame(st.session_state.crm_entries)
        st.dataframe(df_crm, use_container_width=True)
        
        # Prepare CRM Excel download
        crm_excel = BytesIO()
        with pd.ExcelWriter(crm_excel, engine="xlsxwriter") as writer:
            df_crm.to_excel(writer, index=False, sheet_name="CRM Data")
        crm_excel.seek(0)
        st.download_button(
            "Download CRM Excel", 
            crm_excel, 
            file_name="crm_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="crm_excel",
            help="Download CRM data as Excel"
        )
        
        # Prepare CRM PDF download
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="CRM Data", ln=True, align='C')
        pdf.ln(10)
        for entry in st.session_state.crm_entries:
            line = (f"Name: {entry.get('name', '')}, Contact: {entry.get('contact', '')}, "
                    f"Email: {entry.get('email', '')}, Company: {entry.get('company', '')}, "
                    f"Address: {entry.get('address', '')}, Requirement: {entry.get('requirement', '')}, "
                    f"Stage: {entry.get('lead_stage', '')}")
            pdf.multi_cell(0, 10, line)
        pdf_output = pdf.output(dest='S').encode('latin1')
        crm_pdf = BytesIO(pdf_output)
        st.download_button(
            "Download CRM PDF",
            crm_pdf,
            file_name="crm_data.pdf",
            mime="application/pdf",
            key="crm_pdf",
            help="Download CRM data as PDF"
        )
    else:
        st.info("No CRM entries yet.")

with col2:
    st.markdown('<div class="section-header">To‑Do List</div>', unsafe_allow_html=True)
    
    with st.form("todo_form", clear_on_submit=True):
        task = st.text_input("Task")
        date_open = st.date_input("Date of Opening")
        date_close = st.date_input("Closing Date")
        reminder = st.text_input("Reminder", help="e.g., Follow up soon")
        submit_todo = st.form_submit_button("Add Task")
        if submit_todo:
            st.session_state.todo_entries.append({
                "task": task,
                "date_open": date_open.strftime("%Y-%m-%d"),
                "date_close": date_close.strftime("%Y-%m-%d"),
                "reminder": reminder
            })
            st.success("To‑Do Entry added!")
    
    st.markdown('<div class="section-header">To‑Do Entries</div>', unsafe_allow_html=True)
    if st.session_state.todo_entries:
        df_todo = pd.DataFrame(st.session_state.todo_entries)
        st.dataframe(df_todo, use_container_width=True)
        
        # Prepare To‑Do Excel download
        todo_excel = BytesIO()
        with pd.ExcelWriter(todo_excel, engine="xlsxwriter") as writer:
            df_todo.to_excel(writer, index=False, sheet_name="ToDo Data")
        todo_excel.seek(0)
        st.download_button(
            "Download To‑Do Excel", 
            todo_excel, 
            file_name="todo_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="todo_excel",
            help="Download To‑Do data as Excel"
        )
        
        # Prepare To‑Do PDF download
        pdf_todo = FPDF()
        pdf_todo.add_page()
        pdf_todo.set_font("Arial", size=12)
        pdf_todo.cell(200, 10, txt="To‑Do Data", ln=True, align='C')
        pdf_todo.ln(10)
        for item in st.session_state.todo_entries:
            line = (f"Task: {item.get('task', '')}, Date Open: {item.get('date_open', '')}, "
                    f"Date Close: {item.get('date_close', '')}, Reminder: {item.get('reminder', '')}")
            pdf_todo.multi_cell(0, 10, line)
        pdf_todo_output = pdf_todo.output(dest='S').encode('latin1')
        todo_pdf = BytesIO(pdf_todo_output)
        st.download_button(
            "Download To‑Do PDF",
            todo_pdf,
            file_name="todo_data.pdf",
            mime="application/pdf",
            key="todo_pdf",
            help="Download To‑Do data as PDF"
        )
    else:
        st.info("No To‑Do entries yet.")
