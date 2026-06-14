import json
import random

pronouns = ["he","she","they","I","we"]
articles = ["a","the"]

# These are sentence structures
structures = [
    ["ART","ADJ","NOUN","ADV","VERB","PREP","ART","ADJ","NOUN"],    
    ["PRO","ADV","VERB","ART","ADJ","NOUN","PREP","ART","ADJ","NOUN"],
    ["PRO","ADV","VERB","PREP","ART","ADJ","NOUN","PREP","ART","ADJ","NOUN"],
    ["PRO","ADV","VERB","ART","ADJ","NOUN","PREP","ART","ADJ","NOUN"]
]

def get_seven_letter_word():
    """ 
        Expects a minimum 7-letter word from the user at the console.
        Raises a ValueError if it doesn't get one
    """
    result = input("Please enter a word with at least 7 letters: ")
    if len(result) < 7:
        raise ValueError
    return result.upper()

def parse_json_from_file(file_path):
    """
    Opens the file at file_path for reading and parses the JSON data from the file
    May raise FileNotFoundError, json.JSONDecodeError
    """
    with open(file_path, 'r') as file:
        json_data = json.load(file)
        return json_data

def choose_sentence_structure():
    """ Selects a sentence structure at random from the list. """
    return random.choice(structures)

def get_pronoun():
    """ Gets a random pronoun from the list. """
    return random.choice(pronouns)

def get_article():
    """ Gets a random article from the list. """
    return random.choice(articles)

def get_word(letter, speech_part):    
    """ Gets a part of speech from the word list and letter passed in. 
        The ordinal value of the letter passed in is subtracted from 65 (the ordinal value for 'A' in ASCII)
        This means A=0, B=1, C=2, etc. and this determines the index of the list to use.
    """
    return speech_part[ord(letter) - 65]

def fix_agreement(sentence):
    """ Corrects the verbs to match the pronoun as needed
        Corrects the article a to an when needed
        This mutates the sentence list as appropriate and returns nothing
        This method makes use of the known sentence structures.
    """    
    for index in range(len(sentence)):
        word = sentence[index]
        # Rule 1: If the word he or she is found, add an s to the verb two words ahead in the sentence
        if word in ["he","she"]:
            sentence[index+2] = sentence[index+2] + "s"
        # Rule 2: If the indefinite article 'a' is found, 
        # check the starting letter of the noun two words ahead and replace with 'an' if the word starts with a vowel       
        if word == "a":
            first_letter = sentence[index + 2][0]
            if first_letter in "aeiou":
                sentence[index] = 'an'
        # Rule 3: 'The' at the beginning of the sentence needs a verb update 4 words later to add an 's'
        if word == "the" and index == 0:            
            sentence[index + 4] = sentence[index + 4] + "s"

def build_sentence(seed_word, structure, data):
    """ Builds a sentence using the seed_word to select words using the structure and data given. """
    sentence = []
    index = 0
    for part in structure:
        if part == 'ART':
            sentence.append(get_article())
        elif part == 'ADJ':
            sentence.append(get_word(seed_word[index], data["adjectives"]))
            index+=1
        elif part == 'NOUN':
            sentence.append(get_word(seed_word[index], data["nouns"]))
            index+=1
        elif part == 'VERB':
            sentence.append(get_word(seed_word[index], data["verbs"]))
            index+=1
        elif part == 'ADV':
            sentence.append(get_word(seed_word[index], data["adverbs"]))
            index+=1
        elif part == 'PREP':
            sentence.append(get_word(seed_word[index], data["prepositions"]))
            index+=1
        elif part == 'PRO':
            sentence.append(get_pronoun())
    
    fix_agreement(sentence)
    
    # Constructs a sentence by joining all of the items in the sentence list with a space.
    result = " ".join(sentence).capitalize()
    return result

def main():
    user_input = get_seven_letter_word()
    structure = choose_sentence_structure()
    data = parse_json_from_file("word_lists.json")
    sentence = build_sentence(user_input, structure, data)
    print(sentence)
    
if __name__ == '__main__':
    main()