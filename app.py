import streamlit as st
from document_loader import read_file
from vector_store import create_chunks
from rag_pipeline import generate_answer


st.set_page_config(
    page_title="Domain RAG Chatbot",
    layout="wide"
)
st.title("Domain-Specific RAG Chatbot")
st.write(
    "Upload PDF documents and ask questions "
    "based on their content."
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');

.stApp {
    background-color: #F4F6F9;
    font-family: 'Montserrat', sans-serif;
}
 
h1 {
    color: #1E3A8A;
    font-family: 'Montserrat', sans-serif;
    text-align: center;
    font-weight: 700;
    font-size: 2.2rem;
    margin-bottom: 0.5rem;
}

.stButton > button {
    background-color: #2563EB;
    color: white;
    font-family: 'Montserrat', sans-serif;
    font-size: 15px;
    font-weight: 600;
    border-radius: 8px;
    border: none;
    height: 45px;
    width: 100%;
    transition: all 0.2s ease-in-out;
}

.stButton > button:hover {
    background-color: #1D4ED8;
    transform: translateY(-1px);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}
</style>
""", unsafe_allow_html=True)
st.sidebar.title("About Project")

st.sidebar.write("""
This application is  a chatbot that answers questions from uploaded PDFs such as course notes, 
company policies, manuals, legal documents
""")
if "documents" not in st.session_state:
    st.session_state.documents = [] 
if "chunks" not in st.session_state:
    st.session_state.chunks = [] 
if "messages" not in st.session_state:
    st.session_state.messages = []
with st.sidebar:
     st.header("Upload Documents")
     uploaded_files = st.file_uploader( 
          "Upload  files", 
          type=["pdf", "docx", "txt"],
            accept_multiple_files=True
              ) 
     process_button = st.button( 
          " Process Documents", 
          use_container_width=True ) 
     st.divider()
clear_button = st.button( 
      "Clear Chat",
       use_container_width=True )

if process_button:


    if not uploaded_files:
         st.warning("please upload atleast one file")
    else:        
         all_documents=[]
         with st.spinner("reading and processing files..."):
              for upfile in uploaded_files:
                   document=read_file(upfile)
                   all_documents.extend(document)
              if not all_documents:
                   st.error("No readable text was found in uploaded file")     
              else:
                   all_chunks=[]
                   for document in all_documents:
                        chunks=create_chunks(document["text"],chunk_size=100)
                        for chunk in chunks:
                             all_chunks.append({
                                 "text": chunk, 
                                 "source": document["source"], 
                                 "page": document["page"] 
                             })
                   st.session_state.documents = ( all_documents )
                   st.session_state.chunks = ( all_chunks )          
                   st.success( f"Successfully processed " 
                              f"{len(uploaded_files)} FILE(s)." 
                              ) 
                   st.info( f"Created {len(all_chunks)} "
                            f"document chunks."
                              )      
if clear_button:

    st.session_state.messages = []
    st.rerun()                              
              
# Display existing chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if message["role"] == "assistant" and "sources" in message and message["sources"]:
            with st.expander("View Sources", expanded=False):
                for i, source in enumerate(message["sources"], start=1):
                    st.markdown(f"**Source {i}:** {source['source']} (Page {source['page']}) | *Score: {source['score']:.2f}*")
                    st.info(source["chunk"])

question = st.chat_input( 
     "Ask a question about your documents..." 
     )
if question:

    if not st.session_state.chunks:

        st.warning("please upload atleast one file")
    else:
        # Display user message in chat message container
        with st.chat_message("user"):
            st.write(question)
        
        # Append user message to chat history
        st.session_state.messages.append({"role": "user", "content": question})

        with st.chat_message("assistant"):
            with st.spinner("Searching from the document..."):
                 answer, sources = generate_answer(
                    question,
                    st.session_state.chunks,
                    top_k=3
                )
            st.write(answer)    
            if sources:
                with st.expander("View Sources", expanded=False):
                    for i, source in enumerate(sources, start=1):
                        st.markdown(f"**Source {i}:** {source['source']} (Page {source['page']}) | *Score: {source['score']:.2f}*")
                        st.info(source["chunk"])
            
            # Append assistant message to chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources
            })

                  