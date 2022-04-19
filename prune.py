#shrink functions
from collections import defaultdict

def nothing_correct(doesnt_contain_dicts, let):

    f = ord(let[0])-ord('a')

    d = doesnt_contain_dicts[f]

    for i in range(1, len(let)):
        l = ord(let[i]) - ord('a')
        d = d.intersection(doesnt_contain_dicts[l])
    return d


def excess_letter_count(correct_letters_wrong_place, correct_letters_exact_place, incorrect_letters):
    d_correct = defaultdict(int)
    d_incorrect = defaultdict(int)
    d_exact_number_known= {}
    for val in correct_letters_wrong_place:
        pos, l = val
        d_correct[l] += 1

    for val in correct_letters_exact_place:
        pos, l = val
        d_correct[l] += 1

    for val in incorrect_letters:
        d_incorrect[val] += 1

    for key, val in d_incorrect.items():
        if key in d_correct:
            d_exact_number_known[key] = d_correct[key]


    return d_exact_number_known


def initial_prune(contains_dicts, correct_letters_wrong_place, correct_letters_exact_place):
    letters = []


    for i, val in enumerate(correct_letters_wrong_place):
        let = val[1]
        letters.append(let)

    for i, val in enumerate(correct_letters_exact_place):
        let = val[1]
        letters.append(let)

    d = contains_shrink(contains_dicts, letters)

    return d

def contains_shrink(contains_dicts, let):

    f = ord(let[0])-ord('a')

    d = contains_dicts[f].copy()

    for i in range (1, len(let)):
        l = ord(let[i]) - ord('a')
        d=d.intersection(contains_dicts[l])
    return d

def bad_letters_shrink(d, letters):
    remove_list = set()
    for word in d:
        for letter in letters:
            if letter in word:
                remove_list.add(word)
                break

    for word in remove_list:
        d.remove(word)
    return d



def position_shrink(d, letters):
    remove_list = set()
    for word in d:
        for letter in letters:
            pos, let = letter
            if word[int(pos)] == let:
                remove_list.add(word)

    for word in remove_list:
        d.remove(word)
    return d


def exact_position_shrink(d, letters):
    remove_list = set()
    for word in d:
        for letter in letters:
            pos, let = letter
            if word[int(pos)] != let:
                remove_list.add(word)

    for word in remove_list:
        d.remove(word)
    return d

def count_shrink(d, d_exact_count_known):
    remove_list = set()
    for key, val in d_exact_count_known.items():

        for word in d:
            count = 0
            for i, l in enumerate(word):
                if l == key:
                    count += 1
                if count > val:
                    remove_list.add(word)

    for word in remove_list:
        d.remove(word)
    return d

def must_contain_shrink(d, must_contain_dict):
    remove_list = set()
    for word in d:
        for k, val in must_contain_dict.items():
            count = 0
            for i in range(0, len(word)):
                if word[i] == k:
                    count += 1
            if count < val:
                remove_list.add(word)
    for word in remove_list:
        d.remove(word)
    return d