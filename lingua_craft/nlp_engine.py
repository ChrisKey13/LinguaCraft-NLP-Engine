import spacy

nlp = spacy.load("it_core_news_lg") 

def identify_nouns(text):
    doc = nlp(text)
    nouns = [token.text for token in doc if token.pos_ == "NOUN"]
    return nouns

def identify_and_lemmatize_verbs(text):
    doc = nlp(text)
    verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
    return verbs
