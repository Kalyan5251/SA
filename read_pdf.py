import PyPDF2

try:
    with open("SA_Chatbot_Flow_Documentation (1).pdf", "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = []
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text.append(t)
        
    with open("extracted_text.txt", "w", encoding="utf-8") as out:
        out.write("\n=== PAGE BREAK ===\n".join(text))
        
    print("Extraction successful.")
except Exception as e:
    print(f"Error: {e}")
