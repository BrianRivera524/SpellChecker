# SpellChecker

This is a program to check spelling. It will find typos and give you suggestions to try and fix them, 
the user must choose which suggestion to keep, or to keep the original word. To correctly use the 
program, you must do so in this manner: python spell_checker.py <valid_words_file> <text_file> <output_file>
In this case:

<valid_words_file> = valid_words.txt   ||    contains all valid words in the English dictionary

<text_file> = input.txt     ||    you may alter this input as you'd like

<output_file> = corrected_text.txt      ||    you may alter this name to be any, followed by ".txt" to generate a new text file with the corrected words from the input