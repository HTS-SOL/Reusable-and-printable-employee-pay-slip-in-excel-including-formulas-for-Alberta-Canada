import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def generate_payslip(employee_info, pay_details, deductions, employer_info, bank_details, filename="payslip.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    
    elements.append(Table([["Employee Pay Slip"]], colWidths=[500], style=[
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 16),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12)
    ]))
    
    def create_section(title, data):
        rows = [[title.title()]] + [[k.title(), v] for k, v in data.items()]
        table = Table(rows, colWidths=[200, 300])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        return table
    
    elements.append(create_section("Employer Information", employer_info))
    elements.append(create_section("Employee Information", employee_info))
    elements.append(create_section("Pay Details", pay_details))
    elements.append(create_section("Deductions", deductions))
    elements.append(create_section("Bank Details", bank_details))
    
    doc.build(elements)

def main():
    st.title("Payslip Generator")
    
    with st.form("Payslip Form"):
        st.subheader("Employer Information")
        employer_info = {
            "Company Name": st.text_input("Company Name"),
            "Business Number": st.text_input("Business Number"),
            "Company Address": st.text_input("Company Address"),
            "Company Contact": st.text_input("Company Contact")
        }
        
        st.subheader("Employee Information")
        employee_info = {
            "Full Name": st.text_input("Full Name"),
            "Employee Id": st.text_input("Employee Id"),
            "Sin": st.text_input("Sin"),
            "Job Title": st.text_input("Job Title"),
            "Department": st.text_input("Department"),
            "Pay Rate": st.number_input("Pay Rate", min_value=0.0)
        }
        
        st.subheader("Pay Details")
        pay_details = {
            "Pay Period": st.text_input("Pay Period"),
            "Pay Date": st.date_input("Pay Date"),
            "Regular Hours Worked": st.number_input("Regular Hours Worked", min_value=0.0),
            "Overtime Hours": st.number_input("Overtime Hours", min_value=0.0),
            "Vacation Hours Used": st.number_input("Vacation Hours Used", min_value=0.0),
            "Sick Leave Taken": st.number_input("Sick Leave Taken", min_value=0.0),
            "Statutory Holidays": st.number_input("Statutory Holidays", min_value=0.0)
        }
        
        st.subheader("Deductions")
        deductions = {
            "Federal Income Tax": st.number_input("Federal Income Tax", min_value=0.0),
            "Provincial Income Tax": st.number_input("Provincial Income Tax", min_value=0.0),
            "Cpp": st.number_input("Cpp", min_value=0.0),
            "Ei": st.number_input("Ei", min_value=0.0),
            "Net Monthly Income": st.number_input("Net Monthly Income", min_value=0.0)
        }
        
        st.subheader("Bank Details")
        bank_details = {
            "Account Number": st.text_input("Account Number"),
            "Payment Method": st.selectbox("Payment Method", ["Direct Deposit", "Cheque"])
        }
        
        submit = st.form_submit_button("Generate Payslip")
    
    if submit:
        generate_payslip(employee_info, pay_details, deductions, employer_info, bank_details)
        st.session_state["payslip_generated"] = True
        st.success("Payslip generated successfully!")
    
    if st.session_state.get("payslip_generated", False):
        with open("payslip.pdf", "rb") as file:
            st.download_button("Download Payslip", file, file_name="payslip.pdf", mime="application/pdf")

if __name__ == "__main__":
    main()
