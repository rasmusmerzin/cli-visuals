#text-based effects

import os

anims = {}

for i in os.listdir("effects"):
    if i[-4:] == ".txt":
        with open("effects/" +i) as f:
            anims[i[:-4]] = f.read().split("\n::seperator::\n")

def get_animation(name):
    if name in anims: return anims[name]

def get_all():
    return anims
