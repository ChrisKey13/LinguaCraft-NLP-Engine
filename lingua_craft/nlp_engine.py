import spacy

nlp = spacy.load("it_core_news_lg") 

def identify_nouns(text):
    doc = nlp(text)
    nouns = [token.text for token in doc if token.pos_ == "NOUN"]
    print(nouns)
    return nouns
