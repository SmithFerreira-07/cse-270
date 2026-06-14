import pytest
import json
import build_sentences
from build_sentences import (get_seven_letter_word, parse_json_from_file, choose_sentence_structure,
                              get_pronoun, get_article, get_word, fix_agreement, build_sentence, structures)

def test_get_seven_letter_word(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'SEVENLE')
    assert get_seven_letter_word() == 'SEVENLE'
    
    monkeypatch.setattr('builtins.input', lambda _: 'sixlet')
    with pytest.raises(ValueError):
        get_seven_letter_word()

def test_parse_json_from_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "test.json"
    p.write_text('{"key": "value"}')
    assert parse_json_from_file(str(p)) == {"key": "value"}

    with pytest.raises(FileNotFoundError):
        parse_json_from_file("nonexistent_file.json")

    p2 = d / "bad_test.json"
    p2.write_text('{"key": "value", }') # Invalid JSON
    with pytest.raises(json.JSONDecodeError):
        parse_json_from_file(str(p2))

def test_choose_sentence_structure():
    structure = choose_sentence_structure()
    assert structure in structures

def test_get_pronoun():
    pronoun = get_pronoun()
    assert pronoun in build_sentences.pronouns

def test_get_article():
    article = get_article()
    assert article in build_sentences.articles

def test_get_word():
    words = ["apple", "banana", "cherry"]
    assert get_word('A', words) == "apple"
    assert get_word('C', words) == "cherry"

def test_fix_agreement():
    # Rule 1
    s1 = ["he", "really", "like", "it"]
    fix_agreement(s1)
    assert s1 == ["he", "really", "likes", "it"]

    s2 = ["she", "never", "care", "about", "it"]
    fix_agreement(s2)
    assert s2 == ["she", "never", "cares", "about", "it"]

    # Rule 2
    s3 = ["a", "big", "apple"]
    fix_agreement(s3)
    assert s3 == ["an", "big", "apple"]
    
    s4 = ["a", "small", "pear"]
    fix_agreement(s4)
    assert s4 == ["a", "small", "pear"]

    # Rule 3
    s5 = ["the", "very", "small", "boy", "run"]
    fix_agreement(s5)
    assert s5 == ["the", "very", "small", "boy", "runs"]

    s6 = ["I", "see", "the", "very", "small", "boy", "run"]
    fix_agreement(s6)
    assert s6 == ["I", "see", "the", "very", "small", "boy", "run"]


def test_build_sentence(monkeypatch):
    data = {
        "adjectives": ["adjA", "adjB", "adjC", "adjD", "adjE", "adjF", "adjG", "adjH"],
        "nouns": ["nounA", "nounB", "nounC", "nounD", "nounE", "nounF", "nounG", "nounH"],
        "verbs": ["verbA", "verbB", "verbC", "verbD", "verbE", "verbF", "verbG", "verbH"],
        "adverbs": ["advA", "advB", "advC", "advD", "advE", "advF", "advG", "advH"],
        "prepositions": ["prepA", "prepB", "prepC", "prepD", "prepE", "prepF", "prepG", "prepH"]
    }
    
    monkeypatch.setattr(build_sentences, 'get_article', lambda: 'a')
    monkeypatch.setattr(build_sentences, 'get_pronoun', lambda: 'she')
    
    structure = ["PRO","ADV","VERB","ART","ADJ","NOUN","PREP","ART","ADJ","NOUN"]
    result = build_sentence("AAAAAAAA", structure, data)
    assert result == "She adva verbas a adja nouna prepa a adja nouna"
    
    monkeypatch.setattr(build_sentences, 'get_article', lambda: 'the')
    structure2 = ["ART","ADJ","NOUN","ADV","VERB","PREP","ART","ADJ","NOUN"]
    result2 = build_sentence("AAAAAAAA", structure2, data)
    assert result2 == "The adja nouna adva verbas prepa the adja nouna"

    monkeypatch.setattr(build_sentences, 'get_article', lambda: 'a')
    data["nouns"][0] = "apple"
    result3 = build_sentence("AAAAAAAA", structure2, data)
    assert result3 == "An adja apple adva verba prepa an adja apple"