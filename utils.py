
import prune
from collections import defaultdict

def load_words():
    with open("wordle_words.txt") as file:
        data = file.read()

    words = data.split("\n")


    final = []
    for word in words:
        if len(word) == 5:
            final.append(word)

    return final


def create_contains_dicts(words):
    contains_dicts = [set() for i in range(0,26)]

    for i, word in enumerate(words):
        for j, letter in enumerate(word):
            n = ord(letter) - ord('a')
            contains_dicts[n].add(word)

    return contains_dicts

def create_doesnt_contain_dicts(final):

    d = [set() for i in range(0, 26)]

    for i, word in enumerate(final):
        for j in range(0, 26):
            n = j + ord('a')

            if chr(n) not in word:
                d[j].add(word)

    return d


def convert_to_tuple_list(s):

    s_list = s.split(";")
    result = []
    for i, val in enumerate(s_list):
        val_list = val.split(",")
        if len(val_list) < 2:
            return result
        pos, let = val_list[0], val_list[1]
        result.append((pos, let))
    return result


def find_next_word(contains_dicts, doesnt_contain_dicts, possible_words, correct_letters_wrong_place, correct_letters_exact_place, incorrect_letters):

    if len(incorrect_letters) == 5:
        possible_words = prune.nothing_correct(doesnt_contain_dicts, incorrect_letters)
    else:
        if len(correct_letters_wrong_place) > 0 or len(correct_letters_exact_place) > 0:
            possible_words = prune.initial_prune(contains_dicts, correct_letters_wrong_place, correct_letters_exact_place)

    possible_words = prune.exact_position_shrink(possible_words, correct_letters_exact_place)
    possible_words = prune.position_shrink(possible_words, correct_letters_wrong_place)



    d_exact_count_known = prune.excess_letter_count(correct_letters_wrong_place, correct_letters_exact_place, incorrect_letters)

    if len(d_exact_count_known) > 0:
        possible_words = prune.count_shrink(possible_words, d_exact_count_known)

    bad_letters = set(incorrect_letters)
    remove_set = set()
    for l in bad_letters:

        if l in d_exact_count_known:
            remove_set.add(l)
    for item in remove_set:
        bad_letters.remove(item)
    if len(bad_letters) < 5:
        possible_words = prune.bad_letters_shrink(possible_words, bad_letters)

        if len(d_exact_count_known) > 0:
            possible_words = prune.count_shrink(possible_words, d_exact_count_known)

        must_contain_dict = defaultdict(int)

        for item in correct_letters_wrong_place:
            pos, let = item
            must_contain_dict[let] += 1

        for item in correct_letters_exact_place:
            pos, let = item
            must_contain_dict[let] += 1

        possible_words = prune.must_contain_shrink(possible_words, must_contain_dict)


    return possible_words



def compute_data(w, t):
    wd = {}
    td = {}
    for i, l in enumerate(w):
        if l not in wd:
            wd[l] = [i]
        else:
            wd[l].append(i)
    for i, l in enumerate(t):
        if l not in td:
            td[l] = [i]
        else:
            td[l].append(i)
    incorrect_letters = []
    wrong_place_match = set()
    exact_place_match = set()

    for k, val in wd.items():

        if k in td:
            max_count = min(len(val), len(td[k]))

            count = 0
            for pos in val:
                if pos in td[k]:
                    if count < max_count:
                        exact_place_match.add((pos, k))
                        count += 1
                    else:
                        incorrect_letters.append(k)
            for pos in val:
                if pos not in td[k]:
                    if count < max_count:
                        wrong_place_match.add((pos, k))
                        count += 1
                    else:
                        incorrect_letters.append(k)
        else:
            incorrect_letters.append(k)

    return incorrect_letters, wrong_place_match, exact_place_match



def compute_index(final, contains_dicts, doesnt_contain_dicts):

    index_dict = {}
    for word in final:
        index = 0
        for target in final:

            incorrect_letters, correct_letters_wrong_place, correct_letters_exact_place = compute_data(word, target)
            possible_words = final.copy()

            index += len(find_next_word(contains_dicts, doesnt_contain_dicts, possible_words, correct_letters_wrong_place, correct_letters_exact_place, incorrect_letters))
        index_dict[word] = index/len(final)
    return index_dict