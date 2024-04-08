import spacy
from spacy.tokens import Token
from lingua_craft.pos_refiner import italian_pos_refiner, correct_verb_forms

nlp = spacy.load("it_core_news_lg")
if "italian_pos_refiner" not in nlp.pipe_names:
    nlp.add_pipe("italian_pos_refiner", after="tagger")
if "correct_verb_forms" not in nlp.pipe_names:
    nlp.add_pipe("correct_verb_forms", last=True)

print(f"Pipeline components: {nlp.pipe_names}")

def extract_pos_elements(text):
    doc = nlp(text)
    pos_elements = {"verbs": [], "nouns": [], "adjectives": [], "prepositions": []}

    for token in doc:
        print(f"Token: {token.text}, Lemma: {token.lemma_}, POS: {token.pos_}")
        # Adjusting logic to capture corrected lemmas
        if token.pos_ == "VERB" or (token.pos_ == "AUX" and token.lemma_ == "venire"):
            pos_elements["verbs"].append(token.lemma_)
        elif token._.is_noun:
            pos_elements["nouns"].append(token.text)
        elif token._.is_adjective:
            pos_elements["adjectives"].append(token.text)
        elif token._.is_preposition:
            pos_elements["prepositions"].append(token.text)

    for key in pos_elements.keys():
        pos_elements[key] = sorted(list(set(pos_elements[key])))

    print(f"Extracted POS elements: {pos_elements}")
    return pos_elements


def identify_nouns(text):
    doc = nlp(text)
    nouns = [token.text for token in doc if token.pos_ == "NOUN"]
    return nouns

def identify_and_lemmatize_verbs(text):
    doc = nlp(text)
    verbs = [token.lemma_.lower() for token in doc if token.pos_ == "VERB"]
    unique_verbs = sorted(list(set(verbs)), reverse=False)
    return unique_verbs
