import sys
import os
import streamlit as st

# Ensure Python recognizes "src" as a module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Attempt to import backend function safely
try:
    from src.backend import query_ionos
except ModuleNotFoundError as e:
    st.error(f"❌ Module Import Error: {e}")
    st.stop()

# Sidebar Information about Ashley
st.sidebar.title("🤖 Meet Ashley")
st.sidebar.write("""
Your personal AI assistant, designed to assist with cloud consulting, technical questions, and general inquiries.""") 

st.sidebar.write("""Whether you need insights on IONOS Cloud, industry trends, or just a casual chat, Ashley is here to help.
""")

# Add AI avatar for branding (optional)
st.sidebar.markdown("---")  # Divider
st.sidebar.subheader("👤 About")
st.sidebar.write("**Ashley** is customized by **Isayah Young Burke**, IONOS Cloud Consultant.")
st.sidebar.write("Built to enhance workflow, provide technical insights, and assist with AI-related tasks.")

st.sidebar.markdown("---")  # Divider
st.sidebar.subheader("🌐 Resources & Connections")

st.sidebar.markdown("[🔗 Let's Connect on LinkedIn](https://www.linkedin.com/in/young-burke/)")  
st.sidebar.markdown("[☁️ Check out IONOS Cloud](https://cloud.ionos.com/compute/cloud-cubes)")  

st.sidebar.markdown("---")  # Divider
st.sidebar.subheader("📌 Future Enhancements")
st.sidebar.write("More AI integrations and improvements coming soon!")

# 📩 Contact & Inquiry Form
st.sidebar.markdown("---")  # Divider
st.sidebar.subheader("📨 Submit an Inquiry")

with st.sidebar.form(key="contact_form"):
    user_name = st.text_input("Your Name")
    user_email = st.text_input("Your Email")
    user_message = st.text_area("Your Message")
    
    submit_button = st.form_submit_button(label="Send Inquiry")

    if submit_button:
        if user_name and user_email and user_message:
            # Store the inquiry (you can later modify this to send it via email or store it in a database)
            inquiry = {
                "name": user_name,
                "email": user_email,
                "message": user_message
            }

            # Save inquiries to a local file (or you can integrate with a database)
            inquiry_file = "inquiries.json"
            if os.path.exists(inquiry_file):
                with open(inquiry_file, "r") as f:
                    inquiries = json.load(f)
            else:
                inquiries = []

            inquiries.append(inquiry)

            with open(inquiry_file, "w") as f:
                json.dump(inquiries, f, indent=4)

            st.sidebar.success("✅ Inquiry submitted successfully!")
        else:
            st.sidebar.warning("⚠️ Please fill in all fields before submitting.")

# Streamlit UI Setup
st.title("🚀 Ashley - Your AI Cloud Assistant")

# Initialize chat history in session state
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
