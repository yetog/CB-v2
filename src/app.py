import sys
import os
import json
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables (for security)
load_dotenv()

# Ensure Python recognizes "src" as a module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import backend function safely
try:
    from src.backend import query_ionos
except ModuleNotFoundError as e:
    st.error(f"❌ Module Import Error: {e}")
    st.stop()

# 📌 Sidebar - Meet Ashley
st.sidebar.title("🤖 Meet Ashley")
st.sidebar.write("""
Your personal AI assistant, designed to assist with cloud consulting, technical questions, and general inquiries.
""")

st.sidebar.markdown("---")
st.sidebar.subheader("👤 About")
st.sidebar.write("**Ashley** is built and customized by **Isayah Young Burke**, IONOS Cloud Consultant.")
st.sidebar.write("Ashley enhances workflow, provides technical insights, and assists with AI-related tasks.")

st.sidebar.markdown("---")
st.sidebar.subheader("🌐 Resources & Connections")
st.sidebar.markdown("[🔗 Let's Connect on LinkedIn](https://www.linkedin.com/in/young-burke/)")
st.sidebar.markdown("[☁️ Check out IONOS Cloud](https://cloud.ionos.com/compute/cloud-cubes)")

st.sidebar.markdown("---")
st.sidebar.subheader("📌 Future Enhancements")
st.sidebar.write("More AI integrations and improvements coming soon!")

# 📩 Contact & Inquiry Form
st.sidebar.markdown("---")
st.sidebar.subheader("📨 Coming Soon")

with st.sidebar.form(key="contact_form"):
    user_name = st.text_input("Your Name")
    user_email = st.text_input("Your Email")
    user_message = st.text_area("Your Message")

    submit_button = st.form_submit_button(label="Send Inquiry")

    if submit_button:
        if user_name and user_email and user_message:
            # Save Inquiry
            inquiry = {
                "name": user_name,
                "email": user_email,
                "message": user_message,
            }

            # Save inquiries to a JSON file
            inquiry_file = "inquiries.json"
            if os.path.exists(inquiry_file):
                with open(inquiry_file, "r") as f:
                    inquiries = json.load(f)
            else:
                inquiries = []

            inquiries.append(inquiry)

            with open(inquiry_file, "w") as f:
                json.dump(inquiries, f, indent=4)

            # Send Email Notification
            sender_email = os.getenv("SENDER_EMAIL", "your_email@gmail.com")  # Your email
            sender_password = os.getenv("EMAIL_PASSWORD", "your-email-password")  # App Password (Secure)
            receiver_email = "isayahy@gmail.com"  # Your email for receiving inquiries

            subject = f"New Inquiry from {user_name}"
            body = f"Name: {user_name}\nEmail: {user_email}\nMessage: {user_message}"

            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = sender_email
            msg["To"] = receiver_email

            try:
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, receiver_email, msg.as_string())
                st.sidebar.success("✅ Inquiry submitted successfully! We'll get back to you soon.")
            except Exception as e:
                st.sidebar.error(f"🚨 Failed to send email: {e}")

        else:
            st.sidebar.warning("⚠️ Please fill in all fields before submitting.")

# 🟢 Streamlit UI Setup
st.title("🚀 Ashley - Your AI Cloud Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if user_input := st.chat_input("Ask Ashley anything..."):
    # Save user input to chat history
    st.session_state["messages"].append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            # Call backend function for response
            response = query_ionos(user_input)
            st.markdown(response)

            # Save assistant response to chat history
            st.session_state["messages"].append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"❌ Error querying IONOS API: {e}")
