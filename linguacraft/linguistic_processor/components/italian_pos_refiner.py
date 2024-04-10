
from spacy.language import Language
from spacy.tokens import Token

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
