
from spacy.language import Language
from spacy.tokens import Token

extensions = [
    ('is_infinitive', False),
    ('is_reflexive', False),
    ('is_auxiliary', False),
    ('original_form', ''),
    ('is_noun', False),
    ('is_adjective', False),
    ('is_adverb', False),
    ('is_preposition', False),
    ('exclude', False)
]

for ext_name, default in extensions:
    Token.set_extension(ext_name, default=default, force=True)
    
@Language.component("italian_pos_refiner")
def italian_pos_refiner(doc):
    pos_mapping = {
        "PROPN": [("exclude", True, None)],
        "VERB": [("is_infinitive", True, lambda token: token.tag_ == "VER:inf"), 
                 ("original_form", lambda token: token.lemma_, None)],
        "AUX": [("is_auxiliary", True, None), 
                ("original_form", lambda token: token.lemma_, None)],
        "NOUN": [("is_noun", True, lambda token: not token.ent_type_)],
        "ADJ": [("is_adjective", True, None)],
        "ADP": [("is_preposition", True, None)]
    }

    for token in doc:
        attrs = pos_mapping.get(token.pos_, [])
        for attr, value, condition in attrs:
            if condition is None or condition(token):
                setattr(token._, attr, value(token) if callable(value) else value)

    return doc