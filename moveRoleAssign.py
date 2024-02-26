import re

from move import Move
from move_translations_data import ignore_patterns, description_translations

def MoveRoleFind(move):
    description = move.effectDesc

    sentences = description.replace('\n', ' ').split('. ')
    output_file = open('missingtranslations.txt', 'a')

    for sentence in sentences:
        # Remove leading and trailing whitespaces, and trailing period
        cleaned_sentence = sentence.strip().rstrip('.')

        role_found = description_translations.get(cleaned_sentence)
        
         # Check if the sentence should be ignored
        if cleaned_sentence in ignore_patterns:
            continue

        if role_found is not None:
            move.role.append(role_found)
        else:
            # Handle case where translation is not found
            output_file.write(f"No translation set for: '{cleaned_sentence}'\n")
            pass

