import os
import pickle
import time
from flask import session
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import pipeline
from PyPDF2 import PdfReader
from pathlib import Path
from model import *

# Load API Keys
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Initialize Models
text_generator = pipeline("text2text-generation", model="t5-small")
vector_model = HuggingFaceEmbeddings(model_name="sentence-transformers/multi-qa-MiniLM-L6-cos-v1")

# Paths for Index & Cache
INDEX_ONE = "genAI/handbook_index.pkl"
INDEX_TWO = "genAI/db_index.pkl"
CACHE_DIR = "genAI/cache"
Path(CACHE_DIR).mkdir(parents=True, exist_ok=True)

# Rate Limit Config
RATE_LIMIT = 10  # Max requests per user per 5 minutes
RATE_LIMIT_WINDOW = 300  # 5 minutes
CONTEXT_WINDOW_SIZE = 10  # Stores last 20 interactions

LAST_ACADEMIC_REFRESH = None

# ====== Utility Functions ====== #

def get_cache_path(user_id):
    """Returns the cache file path for a user."""
    return os.path.join(CACHE_DIR, f"user_{user_id}.pkl")

def load_cache(user_id):
    """Loads the user-specific cache."""
    path = get_cache_path(user_id)
    if Path(path).exists():
        with open(path, "rb") as f:
            return pickle.load(f)
    return {}

def save_cache(user_id, cache):
    """Saves the user-specific cache."""
    path = get_cache_path(user_id)
    with open(path, "wb") as f:
        pickle.dump(cache, f)

def extract_pdf_content(file_path):
    """Extracts text from a PDF and splits it into chunks."""
    reader = PdfReader(file_path)
    content = "\n".join([pg.extract_text() for pg in reader.pages if pg.extract_text()])
    processor = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    return processor.split_text(content)

def setup_index(chunks, file):
    """Creates and stores an FAISS index if not already present."""
    if Path(file).exists():
        with open(file, "rb") as f:
            return pickle.load(f)
    if not chunks:
        return None

    index = FAISS.from_texts(chunks, vector_model)
    with open(file, "wb") as f:
        pickle.dump(index, f)

    return index

def get_alternatives(query):
    """Generates query paraphrases for better retrieval."""
    prompt = f"Paraphrase this question in 3 different ways: {query}"
    results = text_generator(prompt, max_length=50, do_sample=True, num_return_sequences=3)
    return [query] + [res["generated_text"] for res in results]

def fetch_results(query, index):
    """Finds the most relevant information from the FAISS index."""
    if index is None:
        return []

    queries = get_alternatives(query)
    docs = []

    for q in queries:
        relevant = index.similarity_search(q, k=3)
        docs.extend(relevant)

    return list(set(doc.page_content for doc in docs))

# ====== Query Processing & AI Response ====== #

def prepare_message(query, handbook_data, academic_data, user_id):
    """Generates the final AI prompt based on conversation history and retrieved data."""
    conversation_history = session.get("conversation_history", [])
    conversation_text = "\n".join(conversation_history[-CONTEXT_WINDOW_SIZE:])
    extracted_db_data = extract_some_records()

    return f"""
        You are seek.AI, an AI assistant for IIT Madras B.S. in Data Science students. You only provide responses from academic sources.

        ## Academic Levels:
        level 1. Foundational
        level 2. Diploma (Programming/Data Science)
        level 3. BSc Degree
        level 4. BS Degree
        
        Track the user's level across conversations. If unclear, ask and remember. If a course list is requested but level is unknown, ask for clarification.

        ## Assignments & Deadlines:
         for assignment and deadline realted query **only** relies on {extract_db_records}
        - If subject found in the extract_db_records only then give answer for that if not found deny to answer
        - If an assignment is found in the database, provide details including deadlines.
        - If missing, respond: "No assignment deadlines found for this course."
        - If a course is not found, state: "This course may not be offered this term."
        - If irrelevant to Data Science or Programming, respond: "This course is not part of our program."

        ##some Q/A examples
        - what is my level - then return his level not more thing
        - if student ask for couses list down course - just listing not any mush things
        - try to understand all previous massages in Conversation History if any current query looks ambigous and if not under-standable then ask for more details and respond i could not get you intention
        
        ## Response Logic:
        - if query has 2-3 words and not having proper student intention then tell Im not able to under stand what you want to ask can you please elaborate more.
        - Ensure correctness. No speculative answers.
        - If no data is found, respond: "I couldn’t find relevant information."

        ## Sources:
        - Conversation history: {conversation_text}
        - Current query: "{query}"
        - Extracted database records: {extracted_db_data}
        - Handbook data: {handbook_data}
        - Academic data: {academic_data}
        
        Answer **only** what is explicitly asked in the query. Do not provide extra details or additional context.
        don't ever reveal any database 
    """

def process_query(query, handbook_idx, academic_idx, user_id):
    """Processes the query with caching, rate limiting, and retrieval."""
    cache = load_cache(user_id)

    if query in cache:
        return f"Cached result: {cache[query]}"

    # Rate Limiting
    current_time = time.time()
    user_requests = session.get("request_log", [])
    user_requests = [t for t in user_requests if current_time - t < RATE_LIMIT_WINDOW]

    if len(user_requests) >= RATE_LIMIT:
        return "Rate limit exceeded. Please wait before making more requests."

    user_requests.append(current_time)
    session["request_log"] = user_requests

    # Fetch Relevant Data
    handbook_info = fetch_results(query, handbook_idx)
    academic_info = fetch_results(query, academic_idx)

    handbook_data = "\n".join(handbook_info) if handbook_info else "No relevant handbook information found."
    academic_data = "\n".join(academic_info) if academic_info else "No relevant academic data found."

    # Generate Response
    prompt = prepare_message(query, handbook_data, academic_data, user_id)
    ai_model = genai.GenerativeModel(model_name="gemini-2.0-flash")
    result = ai_model.generate_content(prompt)
    response_text = result.text

    # Store Response in Cache
    cache[query] = response_text
    save_cache(user_id, cache)

    # Update Conversation History
    conversation_history = session.get("conversation_history", [])
    conversation_history.append(f"User: {query}")
    conversation_history.append(f"AI: {response_text}")
    session["conversation_history"] = conversation_history[-(2 * CONTEXT_WINDOW_SIZE):]

    return response_text

# ====== Data Retrieval ====== #

def extract_some_records():
    data = []
    try:
        for course in Course.query.all():
            data.append((f"Course: {course.name} (Code: {course.course_code}). {course.desc}", {"type": "course", "course_id": course.course_id}))

        for assignment in Assignment.query.all():
            data.append((f"Assignment {assignment.assignment_id} for {assignment.course_id} due {assignment.due_date}", {"type": "assignment", "assignment_id": assignment.assignment_id, "course_id": assignment.course_id}))

    except Exception as e:
        print(f"Error fetching data: {e}")
    print(data)
    return data

def extract_db_records():
    data = []
    try:
        for course in Course.query.all():
            data.append(f"Course: {course.name} (Code: {course.course_code}). {course.desc}")

        for assignment in Assignment.query.all():
            data.append(f"Assignment {assignment.assignment_id} for {assignment.course_id} due {assignment.due_date}")

        for student in Student.query.all():
            data.append(f"Student: {student.first_name} {student.last_name} (ID: {student.student_id})")

        for instructor in Instructor.query.all():
            data.append(f"Instructor: {instructor.name} (ID: {instructor.instructor_id})")

        for week in Week.query.all():
            data.append(f"Week {week.week_no} for Course {week.course_id}")

        for video in Video.query.all():
            data.append(f"Video {video.video_id} (Week {video.week_id}): {video.title} - {video.video_url}")

    except Exception as e:
        print(f"Error fetching data: {e}")
    # print(data)
    return data 

def retrieve_handbook_index():
    """Retrieves or rebuilds the handbook index."""
    return setup_index(extract_pdf_content("genAI/handbook.pdf"), INDEX_ONE)

def retrieve_academic_index():
    """Retrieves or rebuilds the academic index."""
    global LAST_ACADEMIC_REFRESH
    if LAST_ACADEMIC_REFRESH is None or not Path(INDEX_TWO).exists() or (time.time() - LAST_ACADEMIC_REFRESH > 3600):
        LAST_ACADEMIC_REFRESH = time.time()
        return setup_index(extract_db_records(), INDEX_TWO)
    return setup_index(None, INDEX_TWO)

# ====== Chat Execution ====== #

def chat(query, user_id):
    """Handles a chat query from a user."""
    handbook_faiss = retrieve_handbook_index()
    db_faiss = retrieve_academic_index()

    if db_faiss is None:
        return "No academic data available at the moment."

    return process_query(query, handbook_faiss, db_faiss, user_id)
