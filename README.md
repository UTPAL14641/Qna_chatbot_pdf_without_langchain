# AI-powered PDF Question Answering App

This project is a full-stack application designed to answer your questions about the content of a uploaded PDF document. It leverages the power of Artificial Intelligence (AI) to process the PDF, extract key information, and provide relevant answers to your queries.

## Key Features

- **PDF Uploading:** Upload a PDF document for processing.
- **Text Extraction and Vectorization:** The application efficiently extracts text from the PDF and converts it into a vector representation suitable for similarity search.
- **Similarity Search:** It utilizes Chromadb, a vector database, to perform similarity searches based on the extracted text vectors.
- **Context-Aware Question Answering:** When you ask a question, the application considers the relevant context from the PDF to formulate a comprehensive response. This context includes the surrounding text on the page where the answer might be found.
- **Mistral LLM Integration:** The retrieved context is combined with your query and passed to a Mistral LLM (Large Language Model) to generate a well-structured answer.
- **Implementing things from scratch** and thus avoiding usage of heavy frameworks like Langchain and LlamaIndex. It potentially lower costs for high-volume processing. You might also gain more control over how the system analyzes the text.
## Technologies

- Backend: FastAPI (web framework), Chromadb (vector database), PyPDF2 (PDF processing), uvicorn (ASGI server)
- Frontend: Streamlit (web framework)
- Additional Dependencies: python-dotenv (environment variables)

## Requirements

- Python 3.11.5 (or compatible version)
- Docker (for containerization)

## Installation

1. **Clone the repository:**

   ```bash
   git clone [https://github.com/your-username/pdf-question-answering-app.git](https://github.com/your-username/pdf-question-answering-app.git)

2. **Create a virtual environment (recommended):**
   ```Bash
   conda create --name pdf-qa-env python=3.11.5 -y
   source activate pdf-qa-env
3. **Install dependencies:**
   ```Bash
   pip install -r requirements.txt
   pip install -r Frontend/requirements.txt

## Running the application locally
1. Run the Backend:
   ```Bash
   uvicorn fastapi_app:app --reload
2. Run the Frontend(run the backend first):
   ```Bash
   streamlit run frontend/streamlit_app.py
3. ## Accessing the frontend:
   ```Bash
   http://localhost:8501
4. ## Using Docker Images:**Build the frontend and backend images by running**
   ```Bash
   docker-compose up -d
5. Viewing the logs (optional):To view the logs generated by your running containers, use the following command:
   ```Bash
   docker-compose logs
This will display the combined logs from all running services defined in your docker-compose.yml file
6. **You can also specify the name of a particular service to view its individual logs:**
  ```Bash
docker-compose logs <service_name>

  
