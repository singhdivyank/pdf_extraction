FILE_EXTENSIONS = ["pdf", "jpg", "jpeg", "png"]

# GPT prompts
RESUME_PROMPT = """
Want to extract fields: "Name", "Address", "Github_Url", "Linkedin_Url", "Organization_Names", "Designations_Held", "Years_of_Experience", "University_Name", "Academic_Qualification", "Specialization", "Skills" and "Certifications"
Return results in JSON format without any explanation. The content is as follows:
"""
INVOICE_PROMPT = "Extract entities and their values as a key-value pair from the provided OCR text in JSON format."

# for tkinter
TKINTER_CONSTS = {
    "title": "Extraction results",
    "text_height": '960',
    "text_width": '1080',
    "ui_geometry": '960x1080'
}

# AWS constants
DYNAMODB_TABLES = {
    "resume": "",
    "invoice": "",
    "kyc": ""
}
DYNAMODB_THROUGHPUT = {
    'ReadCapacityUnits': 10,
    'WriteCapacityUnits': 10
}

# openai models
OPENAI_MODELS = {
    "extraction_model": "text-davinci-003",
    "chat_model": "gpt-3.5-turbo"
}
