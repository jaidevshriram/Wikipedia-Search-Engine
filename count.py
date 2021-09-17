import os
from tqdm import tqdm
import subprocess

tempFiles = os.listdir("index/")
files = []

for file in tempFiles:
    base = file.split('.')[0]
    if base.isnumeric():
        files.append(file)

count = 0
for file in tqdm(files):
    f = open(os.path.join("index", file), "r")
    for line in f.readlines():
        count += 1

print(subprocess.check_output(['du', '-sh', 'index']))
print(len(files))
print(count)