import re
import jellyfish
from string import ascii_letters, ascii_lowercase

jaro_threshold = 0.8  # jaro distance threshold value

""" Get similar number given a string

Returns:
    string -- Correction result
"""


def get_similar_number(text):
    if len(text) == 0:
        return ""

    text = text.lower()

    text_split = list(text)

    for index, character in enumerate(text_split):
        if not character.isdigit():
            if character == "b":
                text_split[index] = "6"
            elif character == "o":
                text_split[index] = "0"
            elif character == "l":
                text_split[index] = "1"
            elif character == "i":
                text_split[index] = "1"
            elif character == "(":
                text_split = "1"
            elif character == "?":
                text_split[index] = "7"
            else:
                text_split[index] = ""

    return "".join(text_split)


""" Find a word similar to a target word from a text

Returns:
    integer -- The index where a similar word is found
"""


def similar_in_sentence(text, target_word, threshold=0.8):
    text = text.lower()

    split = text.split(" ")  # tokenization

    target_word = target_word.lower()
    index = -1  # default value

    for word in split:
        similarity_distance = jellyfish.jaro_distance(target_word, word)
        if similarity_distance >= threshold:  # threshold
            index = text.find(word)  # replace the index if the word is found
            break

    return index


""" Remove words that are similar found in the text

Returns:
    string -- The resulted text after the similar word has been removed
"""


def remove_similar_word(text, target_word):
    text_split = text.split(" ")

    text_split = [word.lower() for word in text_split]
    target_word = target_word.lower()

    for index, text_word in enumerate(text_split):
        if jellyfish.jaro_distance(target_word, text_word) >= jaro_threshold:
            del text_split[index]

    text_split = [word.upper() for word in text_split]

    return " ".join(text_split)


""" Remove words that are similar found in the text, given more than one words

Returns:
    string -- The resulted text after the similar words has been removed
"""


def remove_similar_sentence(text, target_sentence):
    target_sentence_split = target_sentence.split(" ")

    result = text

    for target_word in target_sentence_split:
        result = remove_similar_word(result, target_word)

    return result


""" Get words given a text
    When mode = clean is used, remove all special characters

Returns:
    array -- List of words
"""


def get_words(text, mode='clean'):
    words = text.split()

    if mode == 'clean':
        words = [word.lower() for word in words]  # convert into lowercase

    pattern = re.compile(r'^[\W_]+$')  # Is not standalone special character

    for index, word in enumerate(words):
        if pattern.match(word):
            del words[index]
        else:
            if mode == 'clean':
                # remove special characters from the word
                words[index] = remove_special_character(words[index])

    return words


""" Remove all whitespaces found in a string

Returns:
    string -- The resulted string
"""


def remove_all_whitespaces(word):
    return re.sub(r'\s+', '', word)


""" Sees if the word is alphabetic

Returns:
    boolean -- Is alphabetic (true) or not (false)
"""


def is_alphabetic(word):
    return re.match('[A-Za-z]', word)


""" Removes all alphabet in a text

Returns:
    string -- The resulted text
"""


def remove_all_alphabet(word):
    return re.sub('[A-Za-z]+', '', word)


""" Corrects a text containing an address

Returns:
    string -- The resulted text
"""


def remove_special_character_except_slash_dash_comma_dot(word):
    return re.sub('[&\\#+()$~%\'"*?!|<>{};]“', '', word)


""" Removes all special characters (except slash and dash) in a text

Returns:
    string -- The resulted text
"""


def remove_special_character_except_slash_dash(word):
    return re.sub('[&\\#,+()$~%.\'":*?!|<>{};]', '', word)


""" Removes all special characters (except slash) in a text

Returns:
    string -- The resulted text
"""


def remove_special_character_except_slash(word):
    return re.sub('[&\\#,+()$~%.\'":*?!|<>{};-]', '', word)


""" Removes all special characters (except dash) in a text

Returns:
    string -- The resulted text
"""


def remove_special_character_except_dash(word):
    return re.sub('[&\\#,+()$~%.\'":*?!|<>{};/]', '', word)


""" Removes all special characters in a text

Returns:
    string -- The resulted text
"""


def remove_special_character(word):
    return re.sub('[^A-Za-z0-9 ]+', '', word)


def remove_except_whole_uppercase(word):
    words = word.split(" ")

    filtered = []

    for current_word in words:
        if len(remove_except_alphabet_uppercase(current_word)) == len(current_word):
            filtered.append(current_word)

    return " ".join(filtered)


""" Removes everything except uppercase alphabetical characters

Returns:
    string -- The resulted text
"""


def remove_except_alphabet_uppercase(word):
    return re.sub('[^A-Z ]+', '', word)


""" Removes everything except alphabetical characters

Returns:
    string -- The resulted text
"""


def remove_except_alphabet(word):
    return re.sub('[^A-Za-z ]+', '', word)


""" Remove everything except digits

Returns:
    string -- The resulted text
"""


def remove_except_digits(word):
    return re.sub('[^0-9 ]+', '', word)


""" Removes everything except alphabets and digits

Returns:
    string -- The resulted text
"""


def remove_except_alphabet_and_digits(word):
    return re.sub('[^A-Za-z0-9 ]+', '', word)


""" Removes multiple whitespace

Returns:
    string -- The resulted text
"""


def remove_multiple_space(word):
    return ' '.join(word.split())


""" Checks if the string contains number

Returns:
    boolean -- Contains number (true) or not (false)
"""


def has_numbers(text):
    return any(char.isdigit() for char in text)


""" Checks if there are n occurences of digits (default = 5) given a text

Returns:
    boolean -- The string contains n digits (true) or not (false)
"""


def has_n_numbers(text, n=5):
    detected_digits = 0

    for char in text:
        if(char.isdigit()):
            detected_digits += 1

    # print("Checking " + text + " " + str(detected_digits >= n))

    return (detected_digits >= n)


""" Removes alien unicode characters

Returns:
    boolean -- The string contains n digits (true) or not (false)
"""


def clean_unicode(text):
    return (text.encode('ascii', 'ignore')).decode("utf-8")


""" Removes all uppercase characters

Returns:
    string -- The cleaned string
"""


def remove_all_uppercase(text):
    lowercase = set('ABCDEFGHIJLKMNOPQRSTUVWXYZ')
    return ''.join(x for x in text if x not in lowercase)


""" Removes all uppercase characters

Returns:
    string -- The cleaned string
"""


def remove_all_lowercase(text):
    lowercase = set('abcdefghijklmnopqrstuvwxyz')
    return ''.join(x for x in text if x not in lowercase)


""" Checks if the string has n uppercase characters (default=3)

Returns:
    boolean -- Has >= n uppercase characters (True) or not (False)
"""


def has_n_uppercase_characters(text, n=3):
    text = remove_except_alphabet(text)
    text = remove_all_whitespaces(text)
    text = remove_all_lowercase(text)

    return (len(text) >= n)


""" Checks if the string has n uppercase characters (default=3)

Returns:
    boolean -- Has >= n uppercase characters (True) or not (False)
"""


def has_n_lowercase_characters(text, n=3):
    text = remove_except_alphabet(text)
    text = remove_all_whitespaces(text)
    text = remove_all_uppercase(text)

    return (len(text) >= n)


""" Removes words with the length of n (default=2)

Returns:
    string -- The cleaned string
"""


def remove_word_n_characters(text, n=2):
    words = text.split(" ")

    filtered = []

    for word in words:
        if not len(word) == n:
            filtered.append(word)

    return " ".join(filtered)


""" Checks if the string has >= n uppercase words

Returns:
    string -- The cleaned string
"""


def has_n_uppercase_words(text, n=2):
    words = text.split(" ")

    lowercase = set('abcdefghijklmnopqrstuvwxyz')

    filtered_words = []

    for word in words:
        valid = True

        for char in word:
            if char in lowercase:
                valid = False

                break

        if not valid:
            continue

        filtered_words.append(word)

    return len(filtered_words) >= n


""" Removes all single characters

Returns:
    string -- The cleaned string
"""


def remove_single_characters(text):
    words = text.split(" ")

    filtered_words = []

    for word in words:
        if len(word) > 1:
            filtered_words.append(word)

    return " ".join(filtered_words).strip()


""" Ensures that the resulted string begins with words with the length > 1

Returns:
    string -- The cleaned string
"""


def remove_leading_single_character(text):
    words = text.split(" ")

    result = []

    for word in words:
        if len(word) == 1 and len(result) == 0:
            continue

        result.append(word)

    return " ".join(result)


""" Ensures that the resulted string begins with an alphabet

Returns:
    string -- The cleaned string
"""


def ensure_alphabet_is_leading(text):
    text = text.strip()

    words = text.split(" ")

    alphabet = set('abcdefghijklmnopqrstuvwxyz')

    filtered_words = []

    index_alphabet = -1

    for index, word in enumerate(words):
        if is_alphabetic(word):
            index_alphabet = index
            break

    if index_alphabet == -1:
        return text

    for index, word in enumerate(words):
        if index >= index_alphabet:
            filtered_words.append(word)

    return " ".join(filtered_words).strip()


""" Removes all pipe signs

Returns:
    string -- The cleaned string
"""


def remove_pipe_sign(text):
    return text.replace('|', '')


""" Removes standalone numbers

Returns:
    string -- The cleaned string
"""


def remove_single_numbers(text):
    numbers = set('0123456789')

    words = text.split(" ")

    filtered_words = []

    for word in words:
        if len(word) == 1 and word in numbers:
            continue

        filtered_words.append(word)

    return " ".join(filtered_words)


""" Extracts date from a string with malformed date

Returns:
    string -- The extracted date
"""


def extract_date(text):
    date_regex = re.compile(
        r'(0[1-9]|[12][0-9]|3[01])[-](0[1-9]|1[012])[-]\d{4}')

    words = text.split(" ")

    date_matches = list(filter(date_regex.match, words))

    date = ''

    if len(date_matches) > 0:
        date = date_matches[0]

        date_split = date.split("-")

        if not (int(date_split[0]) <= 31 and int(date_split[1]) <= 12 and int(date_split[2]) >= 1900):
            date = ""

    else:
        date_line = remove_all_whitespaces(text)
        date_line = remove_except_digits(date_line)

        if has_n_numbers(date_line, n=7):
            day = date_line[-8:-6]
            month = date_line[-6:-4]
            year = date_line[-4:]

            if int(day) <= 31 and int(month) <= 12 and int(year) >= 1900:
                date = day + '-' + month + '-' + year

    return date


def remove_all_enter(word):
    return re.sub(r'\n+', '', word)
