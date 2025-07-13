import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config("🧠 Knowledge Bot", layout="centered")
st.title("📄 Knowledge Bot - Ask Questions from Documents")

# Upload PDFs & Images
st.subheader("📤 Upload Files")
files = st.file_uploader(
    "Upload PDF or Image files", 
    type=["pdf", "png", "jpg", "jpeg"], 
    accept_multiple_files=True
)

if st.button("Upload Documents") and files:
    with st.spinner("Uploading and indexing..."):
        file_data = [("files", (f.name, f, f.type)) for f in files]
        res = requests.post(f"{API_URL}/upload/", files=file_data)
        if res.ok:
            st.success("✅ Documents indexed!")
        else:
            st.error(f"❌ Upload failed: {res.text}")

st.markdown("---")

# Ask Questions
st.subheader("💬 Ask a Question")
query = st.text_input("Your question based on uploaded documents:")

if st.button("Ask") and query.strip():
    with st.spinner("🤖 Thinking..."):
        res = requests.post(f"{API_URL}/ask", json={"question": query})
        if res.ok:
            st.success(res.json()["answer"])
        else:
            st.error("❌ Error getting response.")
