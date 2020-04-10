import json
from difflib import get_close_matches

data = json.load(open("data.json"))


def confirm(question):
    res = input(f"{question} [Y/n]: ").lower()
    return not res or res == "y"


def translate(w, confidence=0.8):
    w = w.lower()
    if w in data:
        return data[w]
    elif ww := get_close_matches(w, data.keys(), n=1, cutoff=confidence):
        ww = ww[0]
        if confirm(f"Did you mean '{ww}' instead?"):
            return data[ww]

    return f"The word '{w}' doesn't exist, please double check it'"


while True:
    word = input("Please enter the word: ")
    output = translate(word)

    if isinstance(output, list):
        for idx, out in enumerate(output, 1):
            print(f"{idx}. {out}")
    else:
        print(output)

    if not confirm("Continue?"):
        print("Bye!")
        break
