import pytest
from linguacraft.linguistic_processor.linguistic_processor import LinguisticProcessor

@pytest.fixture
def setup_nlp_engine():
    return LinguisticProcessor()

def test_process_text_common_scenario(setup_nlp_engine):
    processor = setup_nlp_engine
    text = "Il rapido volpe marrone salta sopra il cane pigro."
    pos_elements = processor.process_text(text)
    expected_nouns = ["volpe", "cane"]
    assert set(pos_elements['nouns']) == set(expected_nouns)

@pytest.mark.parametrize("text,expected_output", [
    ("La volpe salta alto.",
     {"verbs": ["saltare"], "nouns": ["volpe"], "adjectives": ["alto"], "prepositions": []}),
    ("I gatti dormivano sul divano.",
     {"verbs": ["dormire"], "nouns": ["divano", "gatti"], "adjectives": [], "prepositions": ["sul"]}),
    ("123", {"verbs": [], "nouns": [], "adjectives": [], "prepositions": []}),
    ("""
     In un piccolo paese italiano, la vita scorreva tranquilla e prevedibile. Giovanni, un giovane insegnante di storia, 
     era solito passeggiare lungo i vecchi sentieri della città ogni mattina prima di recarsi al lavoro.
     """,
     {"verbs": ["passeggiare", "recare si", "scorrere"],
      "nouns": ["città", "insegnante", "lavoro", "mattina", "paese", "sentieri", "storia", "vita"],
      "adjectives": ["giovane", "italiano", "piccolo", "prevedibile", "solito", "tranquilla", "vecchi"],
      "prepositions": ["al", "della", "di", "in", "lungo"]}),
])
def test_extract_pos_elements_varied_input(text, expected_output, setup_nlp_engine):
    processor = setup_nlp_engine
    pos_elements = processor.process_text(text)
    assert pos_elements == expected_output
    
@pytest.mark.parametrize("text, exception_message", [
    ("", "Input cannot be empty or whitespace"),
    ("   ", "Input cannot be empty or whitespace"),
    ("@#$%^&*", "Input contains invalid characters"),
    ("√§√∏√ß√±√£√≠", "Input contains invalid characters")
])

def test_invalid_input(setup_nlp_engine, text, exception_message):
    processor = setup_nlp_engine
    with pytest.raises(ValueError) as excinfo:
        processor.process_text(text)
    assert exception_message in str(excinfo.value)