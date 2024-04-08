import pytest
from lingua_craft.nlp_engine import identify_nouns, extract_pos_elements

def test_identify_nouns():
    text = "Il rapido volpe marrone salta sopra il cane pigro."
    expected_nouns = ["volpe", "cane"]
    assert identify_nouns(text) == expected_nouns
    
@pytest.mark.parametrize("text, expected_output", [
    ("La volpe salta alto.",
        {
            "verbs": [
                "saltare"
            ],
            "nouns": [
                "volpe"
            ],
            "adjectives": [
                "alto"
            ],
            "prepositions": []
        }
     ),
    ("I gatti dormivano sul divano.",
        {
            "verbs": [
                "dormire"
            ],
            "nouns": [
                "divano", "gatti"
            ],
            "adjectives": [],
            "prepositions": ["sul"]
        }
     ),
    (
        """
        Giovanni Drogo, protagonista del romanzo, dopo l’accademia militare e con il grado di tenente viene assegnato alla Fortezza Bastiani: una caserma fortificata nel mezzo del deserto dei Tartari.
        """, 
        {
            "verbs": [
                "assegnare", "fortificare", "venire"
            ],
            "nouns": [
                'accademia', 'caserma', 'deserto', 'grado', 'mezzo', 'protagonista', 'romanzo', 'tenente'
            ],
            "adjectives": [
                "militare"
            ],
            "prepositions": [
                'alla', 'con', 'dei', 'del', 'di', 'dopo', 'nel'
            ]
        }
    )
])

def test_extract_pos_elements(text, expected_output):
    assert extract_pos_elements(text) == expected_output