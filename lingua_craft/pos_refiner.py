import spacy
from spacy.language import Language
from spacy.tokens import Token
import logging

Token.set_extension('lemma', default=None, force=True)

nlp = spacy.load("it_core_news_lg")

Token.set_extension('is_infinitive', default=False, force=True)
Token.set_extension('is_reflexive', default=False, force=True)
Token.set_extension('is_auxiliary', default=False, force=True)
Token.set_extension('original_form', default='', force=True)
Token.set_extension('is_noun', default=False, force=True)
Token.set_extension('is_adjective', default=False, force=True)
Token.set_extension('is_adverb', default=False, force=True)
Token.set_extension('is_preposition', default=False, force=True)
Token.set_extension('exclude', default=False, force=True)



@Language.component("italian_pos_refiner")
def italian_pos_refiner(doc):
    logging.debug("Running italian_pos_refiner on document.")
    pos_mapping = {
        "PROPN": {"attr": "exclude", "value": True, "condition": lambda token: True},
        "VERB": {"attr": ["is_infinitive", "original_form"], "value": [True, lambda token: token.lemma_], "condition": lambda token: token.tag_ == "VER:inf"},
        "AUX": {"attr": ["is_auxiliary", "original_form"], "value": [True, lambda token: token.lemma_], "condition": lambda token: True},
        "NOUN": {"attr": "is_noun", "value": True, "condition": lambda token: not token.ent_type_},
        "ADJ": {"attr": "is_adjective", "value": True, "condition": lambda token: True},
        "ADV": {"attr": "is_adverb", "value": True, "condition": lambda token: True},
        "ADP": {"attr": "is_preposition", "value": True, "condition": lambda token: True},
    }
    
    for token in doc:
        if token.pos_ in pos_mapping:
            pos_info = pos_mapping[token.pos_]
            condition_met = pos_info["condition"](token)
            
            if condition_met:
                if isinstance(pos_info["attr"], list):
                    for i, attr in enumerate(pos_info["attr"]):
                        value = pos_info["value"][i](token) if callable(pos_info["value"][i]) else pos_info["value"][i]
                        setattr(token._, attr, value)
                else:
                    value = pos_info["value"](token) if callable(pos_info["value"]) else pos_info["value"]
                    setattr(token._, pos_info["attr"], value)

    return doc

@Language.component("correct_verb_forms")
def correct_verb_forms(doc):
    for token in doc:
        if token.text.lower() == "viene" and token.lemma_ != "venire":
            # Before correction for debugging
            print(f"Before correction: {token.text} - {token.lemma_}")
            token.lemma_ = "venire"
            # Confirming correction
            print(f"After correction: {token.text} - {token.lemma_}")
    return doc

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

nlp = spacy.load("it_core_news_lg")
if "italian_pos_refiner" not in nlp.pipe_names:
    nlp.add_pipe("italian_pos_refiner", after="tagger")
if "lemmatizer" in nlp.pipe_names:
    nlp.add_pipe("correct_verb_forms", after="lemmatizer")
else:
    nlp.add_pipe("correct_verb_forms", last=True) 
print(f"Pipeline components: {nlp.pipe_names}")

