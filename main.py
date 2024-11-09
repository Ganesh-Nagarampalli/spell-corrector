import re
import sys
import json
from collections import Counter

# Preprocess text data
def process_text(path):
    words = []
    with open(path) as f:
        file_name_data = f.read()
    file_name_data = file_name_data.lower()
    words = re.findall(r'\w+', file_name_data)
    return words

# Load words from the text file and prepare vocabulary
book_words = process_text('alice_in_wonderland.txt')
vocab = set(book_words)

# Create a counter dictionary for word frequency
def get_count(words):
    word_count_dict = Counter(words)
    return word_count_dict

word_count_dict = get_count(book_words)

# Calculate probability of occurrence for each word
def occurr_prob(word_count_dict):
    probs = {}
    m = sum(word_count_dict.values())
    for key in word_count_dict:
        probs[key] = word_count_dict[key] / m
    return probs

prob_of_occurr = occurr_prob(word_count_dict)

# Edit distance functions
def del_letter(word):
    return [word[:i] + word[i+1:] for i in range(len(word))]

def switch_letter(word):
    return [word[:i] + word[i+1] + word[i] + word[i+2:] for i in range(len(word)-1)]

def replace_letter(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    return [word[:i] + l + word[i+1:] for i in range(len(word)) for l in letters]

def insert_letter(word):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    return [word[:i] + l + word[i:] for i in range(len(word)+1) for l in letters]

def edit_one_letter(word):
    return set(del_letter(word) + switch_letter(word) + replace_letter(word) + insert_letter(word))

def edit_two_letter(word):
    return set(e2 for e1 in edit_one_letter(word) for e2 in edit_one_letter(e1))

def get_correlations(word, probs, vocab, n=5):
    suggestions = (word in vocab and [word]) or \
                  edit_one_letter(word).intersection(vocab) or \
                  edit_two_letter(word).intersection(vocab)
    n_best = sorted([(s, probs.get(s, 0)) for s in suggestions], key=lambda x: x[1], reverse=True)[:n]
    return n_best

# Main function
if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_word = sys.argv[1]
        corrections = get_correlations(input_word, prob_of_occurr, vocab)
        print(json.dumps(corrections))  # Print JSON for Node.js to parse
    else:
        print(json.dumps([]))  # Empty list if no input
