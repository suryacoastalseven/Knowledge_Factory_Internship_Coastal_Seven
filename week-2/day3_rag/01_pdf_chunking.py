# 01_pdf_chunking.py
import PyPDF2

def extract_and_chunk_pdf(pdf_path: str, chunk_size: int = 1000):
    print(f"--- 1. Extracting text from {pdf_path} ---")
    
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() + " "
                
        print(f"✅ Total characters extracted: {len(text)}")
        
        # Chunking Process (Splitting text into smaller pieces)
        chunks = []
        for i in range(0, len(text), chunk_size):
            chunk = text[i : i + chunk_size]
            chunks.append(chunk)
            
        print(f"✅ Text split into {len(chunks)} chunks (Size: {chunk_size} chars each).")
        return chunks

    except FileNotFoundError:
        print("❌ Error: 'sample.pdf' not found. Please place a PDF file in this folder.")
        return []

if __name__ == "__main__":
    # Ensure you have a sample.pdf in the folder
    my_chunks = extract_and_chunk_pdf("sample.pdf")
    
    if my_chunks:
        print("\nPreview of Chunk 1:")
        print("-" * 40)
        print(my_chunks[0][:200] + "...") # Printing first 200 chars
        print("-" * 40)