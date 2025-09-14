import os, pytest
from lexsense.processing import NLPProcessor
os.environ['TESTING'] = '1'

@pytest.fixture(scope="module")
def proc():
    return NLPProcessor()

def test_classification(proc):
    assert proc.classify_text("This contract includes a clause and both parties agree.") == "Contract"
    assert proc.classify_text("John filed a lawsuit against XYZ Corp. The court case is ongoing.") == "Lawsuit"
    assert proc.classify_text("Company released a new AI model with significant improvements.") == "AI Release"
    assert proc.classify_text("The Government passed a new Act to regulate AI.") == "Regulation"
    assert proc.classify_text("Generic text.") == "Other"

def test_entity_extraction_regex(proc):
    text = "The European Commission and OpenAI collaborated on AI Ethics Guidelines. AlphaCorpInc and Beta LLC, along with the USA, participated."
    ents = set(proc.extract_entities(text))
    expected = {"European Commission", "AI Ethics Guidelines", "AlphaCorpInc", "Beta LLC", "USA"}
    assert expected.issubset(ents)
