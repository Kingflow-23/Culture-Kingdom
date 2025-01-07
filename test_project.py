from project import get_num_players, get_num_questions, get_difficulty, clean_text
from pytest import raises

def test_get_num_players():
    assert get_num_players(1) == 1
    assert get_num_players(20) == 20
    assert get_num_players(30) == 30
    
    
def test_get_num_questions():
    assert get_num_questions(1) == 1
    assert get_num_questions(20) == 20
    assert get_num_questions(30) == 30
    

def test_get_difficulty():
    assert get_difficulty("1") == "easy"
    assert get_difficulty("2") == "medium"
    assert get_difficulty("3") == "hard"
    

def test_clean_text():
    text_to_clean = "Hello &amp; welcome to the world of coding! &lt;Python&gt; is awesome &amp; versatile."
    text_cleaned = "Hello & welcome to the world of coding! <Python> is awesome & versatile."
    assert clean_text(text_to_clean) == text_cleaned
    
def test_get_num_players_str():
    with raises(ValueError):
        assert get_num_players("abc")
        
def test_get_num_questions_str():
    with raises(ValueError):
        assert get_num_questions("abc")
        
def test_get_difficulty_str():
    with raises(ValueError):
        assert get_difficulty("abc")