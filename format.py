a = "abcdefghijklmnopqrstuvwxyz"
with open("words.txt", "r+") as f:
    words = [x for x in f.read().splitlines() if len(x) == 6]
    f.truncate(0)
open("words.txt", "w").close()
with open("words.txt", "r+") as f:
    for word in sorted(words):
        cancel = False
        for letter in word:
            if letter not in a:
                cancel = True
        if cancel:
            continue
        f.write(word.lower()+"\n")
