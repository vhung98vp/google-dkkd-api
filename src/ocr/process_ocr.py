import pymupdf
import easyocr
import time

# Initialize EasyOCR reader
reader = easyocr.Reader(['vi'])  # Add other languages as needed


def pdf_to_images(pdf_path, get_first_only=True, crop=True):
    """
    Convert each page of a PDF to an image.
    Keep first page full, others page get only last 1/4 past to get doc ids of shareholders
    """
    pdf_document = pymupdf.open(pdf_path)
    images = []
    if get_first_only:
        page = pdf_document[0]
        pix = page.get_pixmap(dpi=300, colorspace=pymupdf.csGRAY) 
        images.append(pix.tobytes("png"))
    else:
        for page in pdf_document[1:]:
            if crop:
                crop_box = pymupdf.Rect(446.457, 0, 595.276, 841.890)
                page.set_cropbox(crop_box)
            pix = page.get_pixmap(dpi=300, colorspace=pymupdf.csGRAY) 
            images.append(pix.tobytes("png"))

    # for page_number in range(len(pdf_document)):
    #     page = pdf_document[page_number] 
    #     if skip_first and page_number == 0:  # If not get first page
    #         continue
    #     if crop and page_number > 0: # Crop others page 
    #         # print(pdf_document[page_number].rect)
    #         crop_box = pymupdf.Rect(446.457, 0, 595.276, 841.890)
    #         page.set_cropbox(crop_box)
    #     pix = page.get_pixmap(dpi=300, colorspace=pymupdf.csGRAY) 
    #     images.append(pix.tobytes("png"))
    pdf_document.close()
    return images


def extract_text_from_pdf(pdf_path, get_first_only=False):
    """
    Extract text from a PDF. Return array of text in each page
    """
    start = time.time()

    images = pdf_to_images(pdf_path, get_first_only)
    extracted_text = []
    for img in images:
        text = reader.readtext(img, detail=0)  # `detail=0` gives plain text
        extracted_text.append("\n".join(text))  # Combine text from the page

    print(f"Elapsed OCR time: {time.time()-start:.6f} seconds")
    return extracted_text

def read_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def write_text_to_txt(extracted_text, path):
    with open(path, 'w', encoding='utf-8') as text_file:
        for page_num, page_text in enumerate(extracted_text, 1):            
            # Write the page text to the file
            text_file.write(f"--- Page {page_num} ---\n")
            text_file.write(page_text + "\n")
            text_file.write("\n" + "-" * 50 + "\n")