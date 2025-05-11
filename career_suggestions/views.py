# career_suggestions/views.py
from django.shortcuts import render
from django import forms

class InterestForm(forms.Form):
    interests = forms.CharField(widget=forms.Textarea, label='Tell us about your skills and interests in AI:')

# More advanced rule-based suggestion logic
def generate_suggestions_from_interests(interests_text):
    suggestions = set()
    lower_interests = interests_text.lower()

    # Machine Learning
    if 'machine learning' in lower_interests or 'deep learning' in lower_interests or 'statistical modeling' in lower_interests:
        if 'algorithms' in lower_interests or 'model development' in lower_interests:
            suggestions.add("Machine Learning Engineer")
        if 'research' in lower_interests or 'theory' in lower_interests or 'innovation' in lower_interests:
            suggestions.add("AI Researcher")
        if 'neural networks' in lower_interests or 'tensorflow' in lower_interests or 'pytorch' in lower_interests or 'keras' in lower_interests:
            suggestions.add("Deep Learning Engineer")
        if 'data analysis' in lower_interests or 'feature engineering' in lower_interests:
            suggestions.add("Machine Learning Scientist")

    # Data Science
    if 'data science' in lower_interests or 'data analysis' in lower_interests or 'big data' in lower_interests:
        if 'statistics' in lower_interests or 'hypothesis testing' in lower_interests or 'predictive modeling' in lower_interests:
            suggestions.add("Data Scientist")
        if 'sql' in lower_interests or 'databases' in lower_interests or 'etl' in lower_interests or 'data warehousing' in lower_interests:
            suggestions.add("Data Analyst")
        if 'business intelligence' in lower_interests or 'reporting' in lower_interests or 'dashboards' in lower_interests or 'insights' in lower_interests:
            suggestions.add("Business Intelligence Analyst")

    # Natural Language Processing
    if 'natural language processing' in lower_interests or 'nlp' in lower_interests or 'text analysis' in lower_interests:
        if 'language models' in lower_interests or 'transformers' in lower_interests or 'sentiment analysis' in lower_interests:
            suggestions.add("NLP Engineer")
        if 'linguistics' in lower_interests or 'language understanding' in lower_interests or 'text generation' in lower_interests:
            suggestions.add("Computational Linguist")
        if 'chatbots' in lower_interests or 'conversational ai' in lower_interests:
            suggestions.add("Chatbot Developer")

    # Computer Vision
    if 'computer vision' in lower_interests or 'image processing' in lower_interests or 'video analysis' in lower_interests:
        if 'image recognition' in lower_interests or 'object detection' in lower_interests or 'cv' in lower_interests:
            suggestions.add("Computer Vision Engineer")
        if 'deep learning' in lower_interests and ('images' in lower_interests or 'video' in lower_interests):
            suggestions.add("Deep Learning Vision Engineer")

    # Robotics and Automation
    if 'robotics' in lower_interests or 'automation' in lower_interests or 'ai in robotics' in lower_interests:
        if 'control systems' in lower_interests or 'sensors' in lower_interests or 'embedded systems' in lower_interests:
            suggestions.add("Robotics Engineer")
        if 'path planning' in lower_interests or 'motion control' in lower_interests or 'perception' in lower_interests:
            suggestions.add("AI in Robotics Specialist")

    # AI Ethics and Governance
    if 'ai ethics' in lower_interests or 'responsible ai' in lower_interests or 'ai governance' in lower_interests:
        suggestions.add("AI Ethics Consultant")
        suggestions.add("Policy Advisor (AI)")

    # General AI/ML Enthusiast
    if not suggestions and ('ai' in lower_interests or 'artificial intelligence' in lower_interests or 'machine learning' in lower_interests):
        suggestions.add("Consider exploring various roles within AI based on your further interests.")

    return list(suggestions)

def index(request):
    suggestions = []
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            interests = form.cleaned_data['interests']
            suggestions = generate_suggestions_from_interests(interests)
            if not suggestions:
                suggestions.append("No specific AI career suggestions based on your input.")
    else:
        form = InterestForm()

    return render(request, 'career_suggestions/index.html', {'form': form, 'suggestions': suggestions})
