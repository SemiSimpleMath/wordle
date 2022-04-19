with open("results.txt") as file:
    data = file.read()

words = data.split("\n")


tuple_words = []

for word in words:
    w = word.split("    ")
    tuple_words.append((w[1], w[0]))

tuple_words = sorted(tuple_words, key = lambda x: float(x[0]))

print(tuple_words)