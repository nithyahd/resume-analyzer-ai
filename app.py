from flask_cors import CORS
from flask import Flask, request, jsonify
import pdfplumber
import spacy
import re

app = Flask(__name__)
CORS(app)

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file.stream) as pdf:  # Use .stream for file upload
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_email(text):
    return re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)

def extract_phone(text):
    return re.findall(r'\+?\d[\d -]{8,12}\d', text)

def extract_skills(text):
    skills_keywords = ['python', 'java', 'c++', 'machine learning', 'html', 'css', 'sql', 'javascript', 'react', 'node.js', 'git']
    text = text.lower()
    return [skill for skill in skills_keywords if skill in text]

def extract_name(text):
    lines = text.split('\n')
    top_lines = lines[:5]  # Take the top 5 lines only
    doc = nlp(" ".join(top_lines))  # Process only the top lines

    for ent in doc.ents:
        if ent.label_ == "PERSON" and len(ent.text.split()) <= 4:
            return ent.text.strip()

    return "Name Not Found"


@app.route("/analyze", methods=["POST"])
def analyze_resume():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    text = extract_text_from_pdf(file)

    result = {
        "Name": extract_name(text),
        "Email": extract_email(text),
        "Phone": extract_phone(text),
        "Skills": extract_skills(text)
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)