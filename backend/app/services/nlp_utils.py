import spacy 

nlp = spacy.load("ru_core_news_sm")

ALLOWED_KEYWORDS = [
    "работа", "резюме", "интервью", "вакансия",
    "жұмыс", "түйіндеме",
    "job", "resume", "interview", "cv"
]

def is_relevant_to_business(text: str) -> bool:
    doc = nlp(text.lower())
    lemmas = [token.lemma_ for token in doc]
    print("🔍 Леммы:", lemmas)
    for lemma in lemmas:
        if lemma in ALLOWED_KEYWORDS:
            return True
    return False
