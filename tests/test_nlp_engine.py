from lingua_craft.nlp_engine import identify_nouns

def test_identify_nouns():
    text = "Il rapido volpe marrone salta sopra il cane pigro."
    expected_nouns = ["volpe", "cane"]
    assert identify_nouns(text) == expected_nouns