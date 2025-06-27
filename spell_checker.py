import sys
import re
import difflib

def load_words(filename):
    """Loads a set of valid words from a file."""
    try:
        with open(filename, 'r') as file:
            words = {line.strip().lower() for line in file if line.strip()}
        return words
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return set()
    except Exception as e:
        print(f"An error occurred: {e}")
        return set()

def calculate_distance(word1, word2):
    """Calculates the Levenshtein distance between two words."""
    m = len(word1)
    n = len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if word1[i - 1] == word2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,      # deletion
                dp[i][j - 1] + 1,      # insertion
                dp[i - 1][j - 1] + cost  # substitution
            )
    return dp[m][n]

def get_similar_words(word, valid_words, num_suggestions=3):
    """Finds similar words using difflib for better real-world suggestions."""
    return difflib.get_close_matches(word.lower(), valid_words, n=num_suggestions, cutoff=0.65)

def get_user_correction(word, suggestions):
    """Prompts the user to choose a correction from a list of suggestions."""
    if not suggestions:
        print(f"No suggestions found for '{word}'.")
        return word

    print(f"Did you mean '{word}'?")
    for i, suggestion in enumerate(suggestions):
        print(f"{i + 1}. {suggestion}")
    print("0. Keep original word")

    while True:
        try:
            choice = int(input(f"Enter your choice (0-{len(suggestions)}): "))
            if 0 <= choice <= len(suggestions):
                return word if choice == 0 else suggestions[choice - 1]
            else:
                print("Invalid choice. Please enter a number within the valid range.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def read_input_text(filename):
    """Reads and tokenizes the input text into words and non-word characters."""
    try:
        with open(filename, 'r') as f:
            text = f.read()
        tokens = re.findall(r'\w+|\W+', text)
        return tokens
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []

def write_corrected_text(filename, corrected_text):
    """Writes the corrected text to a file."""
    try:
        with open(filename, 'w') as f:
            f.write(corrected_text)
        print(f"Corrected text written to '{filename}' successfully.")
    except IOError as e:
        print(f"Error writing to file: {e}")

def is_misspelled_word(token, valid_words):
    """Checks if a token is a misspelled word."""
    return token.isalpha() and token.lower() not in valid_words

def produce_corrected_text(tokens, valid_words):
    """Spell-checks and corrects a list of tokens."""
    correct_tokens = []

    for token in tokens:
        if is_misspelled_word(token, valid_words):
            suggestions = get_similar_words(token, valid_words)
            correct_token = get_user_correction(token, suggestions)
            correct_tokens.append(correct_token)
        else:
            correct_tokens.append(token)

    return "".join(correct_tokens)

# Main program
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python spell_checker.py <valid_words_file> <text_file> <output_file>")
        sys.exit(1)

    valid_words_file = sys.argv[1]
    text_file = sys.argv[2]
    output_file = sys.argv[3]

    valid_words = load_words(valid_words_file)
    tokens = read_input_text(text_file)
    corrected_text = produce_corrected_text(tokens, valid_words)
    write_corrected_text(output_file, corrected_text)
    print(f"\nCorrected text written to {output_file}")
