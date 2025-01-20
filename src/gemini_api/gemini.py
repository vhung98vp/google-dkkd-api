import os
import re
import json
from dotenv import load_dotenv
import google_search.generativeai as genai
import base64
from ..logger_config import get_logger

logger = get_logger(__name__)


def read_pdf_file(file_path):
    try:
        with open(file_path, "rb") as doc_file:
            return base64.standard_b64encode(doc_file.read()).decode("utf-8")
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}") # Print the file name if not found
        return None
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return None

def read_pdf_files(file_paths):
    pdf_bytes = []
    for file_path in file_paths:
        pdf_byte = read_pdf_file(file_path)
        if pdf_byte:
            pdf_bytes.append({'mime_type': 'application/pdf', 'data': pdf_byte})
    return pdf_bytes

def clean_json_response(text):
    json_pattern = r'```json([\s\S]+?)```'
    json_data = re.sub(json_pattern, r'\1', text)
    return json.loads(json_data)


def extract_data_from_pdfs(pdfs_path):
    # Get env file
    load_dotenv()
    api_key = os.getenv('API_KEY')
    prompt = os.getenv('PROMPT')
    genai.configure(api_key=api_key)

    # Read and encode local files
    docs_data = read_pdf_files(pdfs_path)

    # Call gemini model and return result
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([prompt, *docs_data])

    return clean_json_response(response.text)
