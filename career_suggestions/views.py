# career_suggestions/views.py
from django.shortcuts import render
from django import forms
from .career_data import CAREER_DATA, CAREER_KEYWORDS
import PyPDF2
import docx
import nltk
from nltk.tokenize import word_tokenize

class InterestForm(forms.Form):
    interests = forms.CharField(widget=forms.Textarea, label='Tell us about your skills and interests in AI:', required=False)
    resume = forms.FileField(required=False)

def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def extract_text_from_docx(docx_file):
    text = ""
    try:
        doc = docx.Document(docx_file)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX: {e}")
    return text


def generate_suggestions_from_interests(interests_text):
    lower_interests = interests_text.lower()
    career_scores = {}

    for career, data in CAREER_KEYWORDS.items():
        score = 0
        for keyword in data["keywords"]:
            if keyword in lower_interests:
                score += data["weight"]
        if score > 0:
            career_scores[career] = score

    # Consider combinations (example)
    if "machine learning" in lower_interests and "computer vision" in lower_interests:
        if "robotics" in lower_interests:
            career_scores["AI in Robotics Specialist"] = career_scores.get("AI in Robotics Specialist", 0) + 5
        else:
            career_scores["Computer Vision Engineer"] = career_scores.get("Computer Vision Engineer", 0) + 2
            career_scores["Machine Learning Engineer"] = career_scores.get("Machine Learning Engineer", 0) + 2

    # Sort careers by score in descending order
    sorted_careers = sorted(career_scores.items(), key=lambda item: item[1], reverse=True)
    return [career for career, score in sorted_careers]

def generate_suggestions_from_text(text):
    lower_text = text.lower()
    career_scores = {}

    for career, data in CAREER_KEYWORDS.items():
        score = 0
        for keyword in data["keywords"]:
            if keyword in lower_text:
                score += data["weight"]
        if score > 0:
            career_scores[career] = score

    # Consider combinations (example - adjust based on resume analysis)
    if "machine learning" in lower_text and "computer vision" in lower_text:
        if "robotics" in lower_text:
            career_scores["AI in Robotics Specialist"] = career_scores.get("AI in Robotics Specialist", 0) + 5
        else:
            career_scores["Computer Vision Engineer"] = career_scores.get("Computer Vision Engineer", 0) + 2
            career_scores["Machine Learning Engineer"] = career_scores.get("Machine Learning Engineer", 0) + 2

    sorted_careers = sorted(career_scores.items(), key=lambda item: item[1], reverse=True)
    return [career for career, score in sorted_careers]

def index(request):
    suggestions_with_details = []
    if request.method == 'POST':
        form = InterestForm(request.POST, request.FILES)
        if form.is_valid():
            interests = form.cleaned_data['interests']
            resume_file = form.cleaned_data['resume']
            resume_text = ""

            print(f"Interests entered: '{interests}'")  # Debugging
            print(f"Resume file uploaded: {resume_file}") # Debugging

            if resume_file:
                if resume_file.name.endswith('.pdf'):
                    resume_text = extract_text_from_pdf(resume_file)
                elif resume_file.name.endswith(('.doc', '.docx')):
                    resume_text = extract_text_from_docx(resume_file)
                else:
                    suggestions_with_details.append({'title': "Invalid resume format. Please upload a PDF or Word document.", 'description': "", 'resources': []})

            if resume_text:
                suggested_careers = generate_suggestions_from_text(resume_text)
                # print("Suggestions from resume:", suggested_careers) # Debugging
            elif interests:
                print("Calling generate_suggestions_from_interests") # Debugging
                suggested_careers = generate_suggestions_from_interests(interests)
                # print("Suggestions from interests:", suggested_careers) # Debugging
            else:
                suggested_careers = []
                suggestions_with_details.append({'title': "Please enter your interests or upload your resume to get suggestions.", 'description': "", 'resources': []})

            for career in suggested_careers:
                details = CAREER_DATA.get(career, {"description": "Description not available.", "resources": []})
                suggestions_with_details.append({'title': career, 'description': details['description'], 'resources': details['resources']})

    else:
        form = InterestForm()

    return render(request, 'career_suggestions/index.html', {'form': form, 'suggestions': suggestions_with_details})