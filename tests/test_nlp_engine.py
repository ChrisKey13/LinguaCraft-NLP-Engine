from lingua_craft.nlp_engine import identify_nouns, identify_and_lemmatize_verbs

def test_identify_nouns():
    text = "Il rapido volpe marrone salta sopra il cane pigro."
    expected_nouns = ["volpe", "cane"]
    assert identify_nouns(text) == expected_nouns
    
    
def test_identify_and_lemmatize_verbs():
    text = "La volpe salta alto."
    expected_verbs = ["saltare"]
    assert identify_and_lemmatize_verbs(text) == expected_verbs
    
    text = "I gatti dormivano sul divan"
    expected_verbs = ["dormire"]
    assert identify_and_lemmatize_verbs(text) == expected_verbs