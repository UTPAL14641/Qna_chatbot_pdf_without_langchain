import streamlit as st
import requests, json
import os

def handle_file_upload():
  uploaded_file = st.file_uploader("Upload PDF", type="pdf")
  if uploaded_file is not None:
    # Validate PDF (consider using libraries like PyPDF2 or MuPDF)
    try:
      with open(uploaded_file.name, "rb") as f:
        f.read(1024)  # Read a small chunk to check for valid PDF
    except Exception as e:
      st.error(f"Invalid PDF: {str(e)}")
      return None

    # Create the "artifacts/uploaded" directory if it doesn't exist
    os.makedirs("artifacts/uploaded", exist_ok=True)

    # Save the uploaded PDF to the "artifacts/uploaded" folder
    uploaded_pdf_path = os.path.join("artifacts", "uploaded", uploaded_file.name)
    with open(uploaded_pdf_path, "wb") as f:
      f.write(uploaded_file.getbuffer())
      
    return uploaded_pdf_path
def handle_query_submission(pdf_path):
  if not pdf_path:
    return None

  query = st.text_input("Enter your question about the uploaded PDF:")
  if not query:
    return None

  # Replace with the actual URL of your FastAPI backend, but include a path parameter for pdf_path
  api_url = f"http://127.0.0.1:8000/query/{pdf_path}"  # Include pdf_path in the URL
  headers = {"Content-Type": "application/json"}
  data = {"query": query}

  try:
    response = requests.post(api_url, headers=headers, json=data)
    response.raise_for_status()  # Raise an exception for non-2xx status codes
    return response.json()
  except requests.exceptions.RequestException as e:
    st.error(f"Error communicating with backend: {str(e)}")
    return None
def display_results(answer):
    if answer:
        st.success(f"Answer: {answer}")
    else:
        st.warning("No answer found for your query.")

if __name__ == "__main__":
    st.title("PDF Question Answering App")

    uploaded_pdf_path = handle_file_upload()
    query_answer = handle_query_submission(uploaded_pdf_path)
    display_results(query_answer)
