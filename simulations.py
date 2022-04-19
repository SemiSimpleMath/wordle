
"""
This is a wordl solver


"""

import prune
from collections import defaultdict

import utils









def save_result(d):
    f = open("results.txt", "w")
    for key, val in d.items():
        s = key + "    " + str(val) + "\n"
        f.write(s)
    f.close()



all_words = utils.load_words()

print("Total words: ", len(all_words))
contains_dicts = [set() for i in range(0,26)]


contains_dicts = utils.create_contains_dicts(all_words)

#global
total_number_words = len(all_words)


doesnt_contain_dicts = utils.create_doesnt_contain_dicts(all_words)


answer = compute_index(all_words)

save_result(answer)

