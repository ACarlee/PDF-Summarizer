import PyPDF2
from openai import OpenAI

client = OpenAI() # Initialize the OpenAI client

def extract_text_from_pdf(pdf_path):

    with open(pdf_path, 'rb') as file: # rb opens the file to read in binary mod
        pdf_reader = PyPDF2.PdfReader(file) # Creates a PDF reader object
        read_text = ""
        
        for page_num in range(len(pdf_reader.pages)): # Loop through each page in the PDF
            page = pdf_reader.pages[page_num]
            read_text += page.extract_text() # Extract text from the current page
            
    return read_text


def summarize_text(text):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful teacher that wants to answer the user's question completely."},
            {"role": "user", "content": f"Please summarize the following text:\n\n{text}"}
        ]
    )
    
    return completion.choices[0].message
   
def extract_summary(text):
    try:
        content_onwards = text.split("content=", 1)[1] #Extract text after "content="
        summary = content_onwards.split(", refusal=None", 1)[0] #Extract text before ", refusal=None"
        
        return summary.strip()  # Then remove any leading or trailing whitespace
    except IndexError:
        return ""  # Return an empty string if not found

given_pdf_path = input("Please enter the path to the PDF file: ").strip('"')  # Remove any surrounding quotes so that PyPDF2 can read the file

try:
    pdf_text = extract_text_from_pdf(given_pdf_path)

    generated_summary = summarize_text(pdf_text) 
    summary_str = str(generated_summary) #Casting to string so that we can use .strip() in extract_summary(text)
    final_summary = extract_summary(summary_str)
    print("Summary:\n", final_summary) 

except FileNotFoundError:
    print("Error: The file was not found")
except Exception as e:
    print(f"An error occurred: {e}")