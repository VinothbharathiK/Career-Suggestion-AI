# career_suggestions/views.py
from django.shortcuts import render
from django import forms
from career_suggestions.career_data import CAREER_KEYWORDS, CAREER_DATA
import PyPDF2
import docx
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

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
        print("DEBUG: Extracted PDF text (first 100 chars):", text[:100]) # Debugging
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def extract_text_from_docx(docx_file):
    text = ""
    try:
        doc = docx.Document(docx_file)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        print("DEBUG: Extracted DOCX text (first 100 chars):", text[:100]) # Debugging
    except Exception as e:
        print(f"Error reading DOCX: {e}")
    return text


def generate_suggestions_from_interests(interests_text):
    lower_interests = interests_text.lower()
    career_scores = {}

    print("DEBUG: Inside generate_suggestions_from_interests") # Debugging

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
    tokens = word_tokenize(lower_text)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [w for w in tokens if not w in stop_words]

    career_scores = {}

    print("DEBUG: Inside generate_suggestions_from_text") # Debugging
    print("DEBUG: CAREER_KEYWORDS type:", type(CAREER_KEYWORDS)) # Debugging

    for career, data in CAREER_KEYWORDS.items():
        print(f"DEBUG: Type of data for {career}:", type(data)) # Debugging
        if isinstance(data, list):
            print(f"DEBUG: Unexpected list for career: {career}, value: {data}") # Debugging
            continue # Skip this iteration to avoid the error
        try:
            for keyword in data["keywords"]:
                if keyword in filtered_tokens:
                    score = data.get("weight", 1) # Use .get() with a default
                    career_scores[career] = career_scores.get(career, 0) + score
        except KeyError as e:
            print(f"DEBUG: KeyError for career: {career}, error: {e}, data: {data}") # Debugging
            continue

    # Consider combinations (example - adjust based on filtered tokens)
    # ... (rest of your function)

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

            print(f"DEBUG: Interests entered: '{interests}'")   # Debugging
            print(f"DEBUG: Resume file uploaded: {resume_file}") # Debugging

            if resume_file:
                if resume_file.name.endswith('.pdf'):
                    resume_text = extract_text_from_pdf(resume_file)
                elif resume_file.name.endswith(('.doc', '.docx')):
                    resume_text = extract_text_from_docx(resume_file)
                else:
                    suggestions_with_details.append({'title': "Invalid resume format. Please upload a PDF or Word document.", 'description': "", 'resources': []})

                if resume_text:
                    print("DEBUG: Calling generate_suggestions_from_text") # Debugging
                    suggested_careers = generate_suggestions_from_text(resume_text)
                    print("DEBUG: Suggestions from resume:", suggested_careers) # Debugging
            elif interests:
                print("DEBUG: Calling generate_suggestions_from_interests") # Debugging
                suggested_careers = generate_suggestions_from_interests(interests)
                print("DEBUG: Suggestions from interests:", suggested_careers) # Debugging
            else:
                suggested_careers = []
                suggestions_with_details.append({'title': "Please enter your interests or upload your resume to get suggestions.", 'description': "", 'resources': []})

            for career in suggested_careers:
                details = CAREER_DATA.get(career, {"description": "Description not available.", "resources": []})
                suggestions_with_details.append({'title': career, 'description': details['description'], 'resources': details['resources']})

    else:
        form = InterestForm()

    return render(request, 'career_suggestions/index.html', {'form': form, 'suggestions': suggestions_with_details})