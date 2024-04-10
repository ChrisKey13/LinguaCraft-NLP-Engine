from spacy.language import Language

@Language.component("correct_verb_forms")
def correct_verb_forms(doc):
    for token in doc:
        if token.text.lower() == "viene" and token.lemma_ != "venire":
            print(f"Before correction: {token.text} - {token.lemma_}")
            token.lemma_ = "venire"
            print(f"After correction: {token.text} - {token.lemma_}")
    return doc
