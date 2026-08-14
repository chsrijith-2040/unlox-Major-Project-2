# Domain-Specific RAG Chatbot

A simple and efficient Retrieval-Augmented Generation (RAG) Chatbot built with Python and Streamlit. This application allows users to upload documents (PDF, DOCX, TXT) and ask questions based strictly on the content of those documents. The answering engine is powered by the Google Gemini API using the `google-genai` SDK, while the retrieval mechanism uses a lightweight TF-IDF and Cosine Similarity approach.

---

## 🚀 Features

- **Multi-Format Document Support**: Upload and process `.pdf`, `.docx`, and `.txt` files.
- **Local Text Processing & Chunking**: Automatic document parsing, extraction, and sliding-window chunking (default chunk size of 100 words with a 20-word overlap) to preserve context.
- **In-Memory TF-IDF Vector Retrieval**: Uses scikit-learn's `TfidfVectorizer` and cosine similarity to find the top $k$ most relevant document chunks relative to the user's question, bypassing the need for an external vector database.
- **LLM-Powered Answering**: Utilizes the `gemini-3.5-flash` model for generating concise, context-constrained answers.
- **Source Citation & Verification**: Displays sources, page numbers, and cosine similarity scores for transparency.
- **Clean Streamlit UI**: User-friendly chat interface with session persistence and a button to clear chat history.

---

## 🛠️ Project Structure

- **[`app.py`](file:///c:/Users/hp/Desktop/unloxs%20major%20project-2/app.py)**: The entry point of the Streamlit application. Manages UI layout, file uploads, chat history session states, and coordinates document processing.
- **[`document_loader.py`](file:///c:/Users/hp/Desktop/unloxs%20major%20project-2/document_loader.py)**: Standardizes extraction of text from PDF, DOCX, and TXT files, associating text with metadata like filename and page numbers.
- **[`vector_store.py`](file:///c:/Users/hp/Desktop/unloxs%20major%20project-2/vector_store.py)**: Implements text chunking with context overlap and retrieves top relevant chunks using TF-IDF and Cosine Similarity.
- **[`rag_pipeline.py`](file:///c:/Users/hp/Desktop/unloxs%20major%20project-2/rag_pipeline.py)**: Manages communication with the Gemini API using the Google GenAI SDK. Coordinates the retrieval step, builds the prompt, and gets the model's response.
- **[`prompt.py`](file:///c:/Users/hp/Desktop/unloxs%20major%20project-2/prompt.py)**: Stores the prompt engineering template, enforcing strict constraints (e.g. answer *only* using context; do not hallucinate; answer concisely).
- **[`requirements.txt`](file:///c:/Users/hp/Desktop/unloxs%20major%20project-2/requirements.txt)**: Python package dependencies.
- **[`.env`](file:///c:/Users/hp/Desktop/unloxs%20major%20project-2/.env)**: Holds the local configuration variables (API keys).

---

## 📋 Prerequisites

Make sure you have Python 3.9+ installed on your system.

---

## 🔧 Installation & Setup

1. **Clone or Navigate to the Directory**:
   ```bash
   cd "c:\Users\hp\Desktop\unloxs major project-2"
   ```

2. **Create and Activate a Virtual Environment**:
   - **On Windows**:
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
   - **On macOS/Linux**:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the root directory (or update the existing one) with your Gemini API key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

---

## 🖥️ Running the Application

Launch the Streamlit dashboard by running:
```bash
streamlit run app.py
```
This will start the local server, typically opening a browser window at `http://localhost:8501`.

---

## 💡 How It Works (RAG Flow)

1. **Upload & Extract**: Users upload files via the Streamlit sidebar. Text is extracted from each file and indexed page-by-page.
2. **Chunking**: The extracted text is divided into chunks of 100 words. A 20-word overlap is prepended to each chunk (except the first) to maintain local semantic context across chunks.
3. **Retrieval**: When a query is entered, the user's question and all chunk texts are vectorised using a TF-IDF vectorizer (with unigrams and bigrams). Cosine similarity is calculated to find the top $k$ chunks (default: 3).
4. **Prompting & LLM Call**: The top chunks are packed into a prompt template, which explicitly tells the Gemini model to behave as a document question-answering assistant and stick *strictly* to the context.
5. **Display & Citation**: The generated answer is presented in the chat along with an expandable "View Sources" dropdown, showing original chunk snippets, source file names, page numbers, and search scores.
