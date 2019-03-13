#animation compiler

numb = int(input("number of frames:"))
file = input("output file:")

frames = []
for i in range(numb):
    with open("frame_" +str(i) +".txt", "r") as sub_f:
        frames.append(sub_f.read())

with open(file, "w") as f: f.write("\n::seperator::\n".join(frames))