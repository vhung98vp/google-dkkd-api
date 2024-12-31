import re
import json
from process_ocr import extract_text_from_pdf, write_text_to_txt

# Patterns for each piece of information
COMPANY_PATTERNS = {
    "full_name": r"Tên công ty viết bằng tiếng Việt:\s*(.*?)Tên",
    "int_name": r"Tên công ty viết bằng tiếng nước ngoài:\s*(.*?)Tên",
    "short_name": r"Tên công ty viết tắt:\s*(.*?)\n2(.+)Mã số doanh nghiệp",
    "comapny_tax_id": r"Mã số doanh nghiệp:\s*(\d+)\n",
    "address": r"Địa chỉ trụ sở chính:\s*(.*?)\n5(.+)Người đại diện theo pháp luật",
    "tel": r"Điện thoại:\s*(.*?)\n",
    #"email": r"Email:\s*(.*?{50}$)\nWebsite",
    "bank_account": r"Số tài khoản:\s*(.*?)\n",
    "capital": r"Vốn điều lệ:\s*([0-9.\s\n]+)\nđồng",
    "representative": {
        "full_name": r"Người đại diện theo pháp luật\nHọ và tên:\s*(.*?)\n",
        "dob": r"Sinh ngày:\s*(\d{2}/\d{2}/\d{4})\n",
        "document_type": r"Loại giấy tờ pháp lý của cá nhân:\s*(.*?)\n",
        "document_number": r"Số giấy tờ pháp lý của cá nhân:\s*(\d+)\n",
        "address": r"Địa chỉ thường trú:\s*(.*?)\nĐịa chỉ liên lạc"
    }
}

#DOC_IDS_PATTERN = re.compile(r'[\s\n]([A-Z]\d{7,8}|\d{12}|\d{9})[\s\n]', re.DOTALL)
DOC_IDS_PATTERN = re.compile(r'([A-Z]\d{7,8}|\d{12}|\d{9})[\s\n]', re.DOTALL)
MAX_NUM_PATTERN = re.compile(r'\d{1,3}(?:\.\d{3})+')


# Exact doc ids
def find_doc_ids(text, pattern=DOC_IDS_PATTERN):
    matches = list(set(pattern.findall(text)))
    return matches

def find_max_capital(text, current, pattern=MAX_NUM_PATTERN):
    def to_number(num_string):
        return int(num_string.replace('.', ''))
    
    matches = pattern.findall(text)
    if current != 'N/A':
        matches.append(current.replace(' ', ''))
    return max(matches, key=to_number)


# Extract information
def extract_company_info(text, data_patterns=COMPANY_PATTERNS):
    # Define a function to extract information using regex
    def extract_info(pattern, text, group=1, default="N/A"):
        match = re.search(pattern, text, re.DOTALL)
        return match.group(group).strip().replace('\n', ' ') if match else default
    
    result = {}
    for key, pattern in data_patterns.items():
        if isinstance(pattern, dict):  # Nested fields for "Người đại diện"
            result[key] = {
                sub_key: extract_info(sub_pattern, text)
                for sub_key, sub_pattern in pattern.items()
            }
        else:
            result[key] = extract_info(pattern, text)
    # result["shareholders"] = find_doc_ids(docs_text)
    
    return result


def extract_data_from_pdfs(pdfs_path, quick_search=True, output_file=None):
    """Extract company info from pdfs"""

    # Get text from first page, first PDF
    full_text = extract_text_from_pdf(pdfs_path[0], True)

    # If search all, get others page from all PDFs
    if not quick_search:
        for pdf_path in pdfs_path:
            text = extract_text_from_pdf(pdf_path, False)
            full_text.extend(text)
    
    write_text_to_txt(full_text, f"{pdfs_path[0]}.txt")
    company_info = extract_company_info(full_text[0])
    company_info["shareholders"] = find_doc_ids('\n'.join(full_text[1:]))
    company_info["capital"] = find_max_capital('\n'.join(full_text[1:]), company_info["capital"])

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(company_info, f, ensure_ascii=False, indent=4)
    return company_info