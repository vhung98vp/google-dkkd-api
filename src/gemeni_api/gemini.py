import os
import re
import json
from dotenv import load_dotenv
import google.generativeai as genai
import base64



def read_pdf_file(file_path):
    try:
        with open(file_path, "rb") as doc_file:
            return base64.standard_b64encode(doc_file.read()).decode("utf-8")
    except FileNotFoundError:
        print(f"File not found: {file_path}") # Print the file name if not found
        return None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def read_pdf_files(file_paths):
    pdf_bytes = []
    for file_path in file_paths:
        pdf_bytes.append({'mime_type': 'application/pdf', 'data': read_pdf_file(file_path)})
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


    # Read and encode the local file
    docs_data = read_pdf_files(pdfs_path)

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([prompt, *docs_data])

    return clean_json_response(response.text)
