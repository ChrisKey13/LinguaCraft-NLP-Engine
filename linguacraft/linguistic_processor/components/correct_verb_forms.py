from spacy.language import Language

@Language.component("correct_verb_forms")
def correct_verb_forms(doc):
    for token in doc:
        if token.text.lower() == "viene" and token.lemma_ != "venire":
            token.lemma_ = "venire"
    return doc
