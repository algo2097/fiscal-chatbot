import spacy
import dateparser
from transformers import pipeline

intents = ["get_total_revenue", "calculate_revenue_change", "get_net_income",
           "get_income_change", "get_total_assets", "get_total_liabilities",
           "cash_flow", "calculate_revenue_to_assets", "calculate_income_to_liabilities",
           "compare_company_revenue"]

classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")


def detect_intent(message):
    result = classifier(message, candidate_labels=intents)
    intent = result['labels'][0]
    print(intent)
    return intent


nlp = spacy.load(r'W:\Chatbot\pythonProject\chatbot_env\Lib\site-packages\en_core_web_sm\en_core_web_sm-3.7.1')


print("Model loaded successfully")


def extract_ent(message):
    doc = nlp(message)
    companies = []
    years = []
    for ent in doc.ents:
        if ent.label_ == "ORG":
            companies.append(ent.text)
        elif ent.label_ == "DATE":
            date = dateparser.parse(ent.text)
            if date:
                years.append(date.year)
    return companies, years


def intent_entities(message):
    companies, years = extract_ent(message)
    intent = detect_intent(message)
    return intent, companies, years
