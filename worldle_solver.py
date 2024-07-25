import itertools
import re
import time

letters = "abcdefghijklmnopqrstuvwxyz"
global total
total = 0

with open("words.txt", "r+") as f:
    words = f.read().splitlines()
    
def sequences(words, count=4):
    values = {}
    combinations = []
    for x in range(1, count):
        for combination in itertools.product(letters, repeat=x):
            combination = "".join(combination)
            for word in words:
                if combination in word:
                    for c in re.finditer(combination, word):
                        combinations.append((combination, c.span()))
                        global total
                        total += 1
    for combination in set(combinations):
        values[combination] = combinations.count(combination)
        
    return values # key=(combination, (start, end)) value=count



def sequence_values(words):
    values = {}
    sequence_values = sequences(words)
    total = sum(sequence_values[k] for k in sequence_values)
    for k in sorted(sequence_values, key=sequence_values.get, reverse=True):
        values[k] = sequence_values[k]/total

    return values # key=(combination, (start, end)) value=score


def word_values(words):
    word_values = {}
    sequences = sequence_values(words)
    for word in words:
        word_values[word] = 0
        for sequence, span in sequences:
            if sequence in word:
                for c in re.finditer(sequence, word):
                    global total
                    total += 1
                    if word[c.start():c.end()] == sequence:
                        word_values[word] = word_values[word] + sequences[(sequence, span)]
        word_values[word] = word_values[word] + len(set(word))
    values = {}
    for k in sorted(word_values, key=word_values.get, reverse=False):
        values[k] = word_values[k]

    return values

def best_word(words):
    all_words = word_values(words)
    return max(all_words, key=all_words.get)

def remove_words_by_letter(words, incorrect_letters):
    bad_words = []
    for word in words:
        for position, letter in enumerate(word):
            if (letter, position) in incorrect_letters:
                bad_words.append(word)
                
    for bad_word in set(bad_words):
        words.remove(bad_word)
                
    return words

def remove_words_by_confirmed(words, confirmed_letters):
    bad_words = []
    for word in words:
        for letter in confirmed_letters:
            if word[letter[1]] == letter[0] or letter[0] not in word:
                bad_words.append(word)
            
    for bad_word in set(bad_words):
        words.remove(bad_word)
    return words

def remove_words_by_correct(words, correct_letters):
    bad_words = []
    for word in words:
        for letter in correct_letters:
            if word[letter[1]] != letter[0]:
                bad_words.append(word)
            
    for bad_word in set(bad_words):
        words.remove(bad_word)

    return words

def parse_word(word, keys, incorrect_letters, confirmed_letters, correct_letters):
    # y=confirm n=incorrect m=correct
    if keys == "yyyyy":
        return None, None, None, True
    for position, key in enumerate(keys):
        key = key.lower()
        if key == "y":
            correct_letters.append((word[position], position))
        elif key == "m":
            confirmed_letters.append((word[position], position))
        else:
            for x in range(5):
                if (word[position], x) in correct_letters:
                    continue
                incorrect_letters.append((word[position], x))
    return incorrect_letters, confirmed_letters, correct_letters, False

incorrect_letters = []             
confirmed_letters = []
correct_letters = []
while True:
    s = time.time()
    best = best_word(words)
    print(f"Total Comparisons: {total}")
    print(f"Elapsed time: {time.time() - s}s")
    print(f"Best Word: {best}")
    keys = input(f"Enter keys for [{best}]: ")
    incorrect_letters, confirmed_letters, correct_letters, complete = parse_word(best, keys, incorrect_letters, confirmed_letters, correct_letters)
    if complete:
        print("Done")
        break
    
    words = remove_words_by_letter(words, incorrect_letters)
    words = remove_words_by_confirmed(words, confirmed_letters)
    words = remove_words_by_correct(words, correct_letters)










