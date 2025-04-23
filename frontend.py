# import nltk
# import streamlit as st
# import time
# import requests
# import os
# import re
# import PyPDF2
# from nltk.tokenize import word_tokenize
# from nltk.stem import WordNetLemmatizer
# from nltk.stem.porter import PorterStemmer
# from nltk.corpus import stopwords


# # Helper function to make the API call
# def make_api_call(data):
#     # Replace the URL with your API endpoint
#     url = "http://localhost:8000/in"
#     response = requests.post(url, json=data)
#     return response.json()

# # Helper function to extract text from PDF
# def pdf_to_text(pdf_file):

#   pdf_reader = PyPDF2.PdfFileReader(pdf_file)

#   text = ''
#   for page_num in range(pdf_reader.numPages):
#       page = pdf_reader.getPage(page_num)
#       text += page.extractText()

#   # print(text)
#   return text

# def tokenize(text):
#     """Tokenize the text

#     Parameters
#     ----------
#     text: String
#         The message to be tokenized

#     Returns
#     -------
#     List
#         List with the clean tokens
#     """
#     text = text.lower()
#     text = re.sub("[^a-zA-Z0-9]", " ", text)
#     tokens = word_tokenize(text)
#     tokens = [w for w in tokens if w not in stopwords.words("english")]

#     lemmatizer = WordNetLemmatizer()
#     stemmer = PorterStemmer()

#     clean_tokens_list = []
#     for tok in tokens:
#         lemmatizer_tok = lemmatizer.lemmatize(tok).strip()
#         clean_tok = stemmer.stem(lemmatizer_tok)
#         clean_tokens_list.append(clean_tok)

#     return clean_tokens_list

# # Streamlit app
# def main():
#     st.title('Document similarity')

#     uploaded_files = st.file_uploader("Choose a PDF file", accept_multiple_files=True)
#     if uploaded_files:
#         if len(uploaded_files) == 2:
#             file_1 = uploaded_files[0]
#             file_2 = uploaded_files[1]

#             st.write("PDFs successfully uploaded.")

#             if st.button("Submit"):
#                 start = time.time()
#                 print("Conversion started")
#                 text1 = pdf_to_text(file_1)
#                 tokenized_text1 = " ".join(tokenize(text1))

#                 text2 = pdf_to_text(file_2)
#                 tokenized_text2 = " ".join(tokenize(text2))
#                 et = time.time()
#                 print(et - start)
#                 print("Conversion ended")
#                 my_obj = {
#                     "t1": text1,
#                     "t2": text2
#                 }
#                 print("Request Sent")
#                 start = time.time()
#                 res = make_api_call(my_obj)
#                 et = time.time()
#                 print(et - start)
#                 print("Response recieved")
#                 st.write(res)
#                 # data = {
#                 #     "file_1_text": extract_text_from_pdf(file_1),
#                 #     "file_2_text": extract_text_from_pdf(file_2)
#                 # }
#                 # response = make_api_call(data)
#                 # st.write("API Response:")
#                 # st.write(response)
#         else:
#             st.error("Please upload exactly 2 PDF files.")

# if __name__ == '__main__':
#     main()

import nltk
import streamlit as st
import time
import requests
import os
import re
import PyPDF2
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

# Set page configuration for a cleaner look
st.set_page_config(
    page_title="Document Similarity",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 4px;
        transition: all 0.3s;
    }
    
    .stButton button:hover {
        background-color: #45a049;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    
    .file-uploader {
        border: 2px dashed #ddd;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    .highlight-value {
        color: #FF0000;
        font-weight: bold;
        font-size: 1.1em;
    }
    
    .result-card {
        background-color: #f9f9f9;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .comparison-history {
        position: fixed;
        right: 0;
        top: 0;
        height: 100vh;
        width: 0;
        background-color: white;
        box-shadow: -2px 0 5px rgba(0,0,0,0.1);
        transition: width 0.3s;
        overflow-y: auto;
        z-index: 1000;
        padding: 20px 0;
    }
    
    .comparison-history.expanded {
        width: 350px;
    }
    
    .history-toggle {
        position: fixed;
        right: 20px;
        bottom: 20px;
        z-index: 1001;
    }
    
    h1 {
        color: #2c3e50;
        margin-bottom: 30px;
    }
    
    .header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
    }
    
    .loader {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Helper function to make the API call
def make_api_call(data):
    # Replace the URL with your API endpoint
    url = "http://localhost:8000/in"
    response = requests.post(url, json=data)
    return response.json()

# Helper function to extract text from PDF
def pdf_to_text(pdf_file):
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    
    text = ''
    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        text += page.extractText()
    
    return text

def tokenize(text):
    """Tokenize the text

    Parameters
    ----------
    text: String
        The message to be tokenized

    Returns
    -------
    List
        List with the clean tokens
    """
    text = text.lower()
    text = re.sub("[^a-zA-Z0-9]", " ", text)
    tokens = word_tokenize(text)
    tokens = [w for w in tokens if w not in stopwords.words("english")]

    lemmatizer = WordNetLemmatizer()
    stemmer = PorterStemmer()

    clean_tokens_list = []
    for tok in tokens:
        lemmatizer_tok = lemmatizer.lemmatize(tok).strip()
        clean_tok = stemmer.stem(lemmatizer_tok)
        clean_tokens_list.append(clean_tok)

    return clean_tokens_list

# Initialize session state for comparison history
if 'history' not in st.session_state:
    st.session_state.history = []

if 'show_history' not in st.session_state:
    st.session_state.show_history = False

# Streamlit app
def main():
    # Header section
    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown("<h1>Document Similarity Analyzer</h1>", unsafe_allow_html=True)
    
    # Main content
    st.markdown("<div class='file-uploader'>", unsafe_allow_html=True)
    uploaded_files = st.file_uploader("Upload PDF files for comparison", 
                                     accept_multiple_files=True,
                                     type="pdf")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if uploaded_files:
        if len(uploaded_files) == 2:
            file_1 = uploaded_files[0]
            file_2 = uploaded_files[1]

            st.success(f"Files uploaded: '{file_1.name}' and '{file_2.name}'")

            submit_col1, submit_col2 = st.columns([1, 5])
            with submit_col1:
                submit_button = st.button("Compare Documents")
            
            if submit_button:
                with st.spinner("Processing documents..."):
                    start = time.time()
                    text1 = pdf_to_text(file_1)
                    tokenized_text1 = " ".join(tokenize(text1))

                    text2 = pdf_to_text(file_2)
                    tokenized_text2 = " ".join(tokenize(text2))
                    conversion_time = time.time() - start
                    
                    my_obj = {
                        "t1": text1,
                        "t2": text2
                    }
                    
                    start = time.time()
                    res = make_api_call(my_obj)
                    api_time = time.time() - start
                
                st.markdown("<div class='result-card'>", unsafe_allow_html=True)
                st.markdown("### Similarity Results")
                
                # Assuming the API returns a dictionary with BERT and TF-IDF scores
                if isinstance(res, dict) and 'bert_similarity' in res and 'tfidf_similarity' in res:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**BERT Similarity:** <span class='highlight-value'>{res['bert_similarity']:.4f}</span>", 
                                  unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"**TF-IDF Similarity:** <span class='highlight-value'>{res['tfidf_similarity']:.4f}</span>", 
                                  unsafe_allow_html=True)
                    
                    # Add to history
                    history_entry = {
                        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                        'file1': file_1.name,
                        'file2': file_2.name,
                        'bert': res['bert_similarity'],
                        'tfidf': res['tfidf_similarity']
                    }
                    st.session_state.history.append(history_entry)
                else:
                    st.error("Invalid response format from API")
                    st.json(res)
                
                st.markdown(f"<small>Processing time: {conversion_time:.2f}s (document processing) + {api_time:.2f}s (similarity computation)</small>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
        else:
            st.warning("Please upload exactly 2 PDF files for comparison.")
    
    # Toggle button for history panel
    st.markdown(
        f"""
        <div class="history-toggle">
            <button onclick="document.querySelector('.comparison-history').classList.toggle('expanded');">
                {("Hide" if st.session_state.show_history else "Show")} History
            </button>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Comparison History Panel (Collapsible from right side)
    history_class = "comparison-history expanded" if st.session_state.show_history else "comparison-history"
    st.markdown(f"<div class='{history_class}'>", unsafe_allow_html=True)
    st.markdown("<h3>Comparison History</h3>", unsafe_allow_html=True)
    
    if not st.session_state.history:
        st.markdown("<p>No comparison history yet.</p>", unsafe_allow_html=True)
    else:
        for i, entry in enumerate(reversed(st.session_state.history)):
            st.markdown(
                f"""
                <div class='result-card'>
                    <small>{entry['timestamp']}</small>
                    <p><strong>{entry['file1']}</strong> vs <strong>{entry['file2']}</strong></p>
                    <p>BERT: <span class='highlight-value'>{entry['bert']:.4f}</span></p>
                    <p>TF-IDF: <span class='highlight-value'>{entry['tfidf']:.4f}</span></p>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()