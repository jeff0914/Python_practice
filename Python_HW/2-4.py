import sys

lines = sys.stdin.read().splitlines()

for i, line in enumerate(lines):
    
    print(f"{line}{i+1}")