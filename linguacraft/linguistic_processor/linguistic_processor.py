import spacy
import re
from linguacraft.linguistic_processor.components.italian_pos_refiner import italian_pos_refiner
from .components.correct_verb_forms import correct_verb_forms


class LinguisticProcessor:
    def __init__(self, model="it_core_news_lg"):
        self.nlp = spacy.load(model)
        self.setup_pipeline()
    
    def setup_pipeline(self):
        if "italian_pos_refiner" not in self.nlp.pipe_names:
            self.nlp.add_pipe("italian_pos_refiner", after="tagger")
        if "correct_verb_forms" not in self.nlp.pipe_names:
            self.nlp.add_pipe("correct_verb_forms", last=True)
        
    def validate_text(self, text):
        if not isinstance(text, str):
            raise ValueError("Input must be a string")
        if not text.strip():
            raise ValueError("Input cannot be empty or whitespace")
        if not re.match(r'^[\w\s,.!?]+$', text):
            raise ValueError("Input contains invalid characters.")
        
    def process_text(self, text):
        self.validate_text(text)
        doc = self.nlp(text)
        pos_elements = {"verbs": [], "nouns": [], "adjectives": [], "prepositions": []}
        
        for token in doc:
            if token.pos_ == "VERB" or (token.pos_ == "AUX" and token.lemma_ == "venire"):
                pos_elements["verbs"].append(token.lemma_.lower())
            elif token._.is_noun:
                pos_elements["nouns"].append(token.text.lower())
            elif token._.is_adjective:
                pos_elements["adjectives"].append(token.text.lower())
            elif token._.is_preposition:
                pos_elements["prepositions"].append(token.text.lower())

        for key in pos_elements.keys():
            pos_elements[key] = sorted(list(set(pos_elements[key])), reverse=False)
        
        return pos_elements