import sys
file = sys.argv[1]
lines = map(str.strip, open(file))
outline = []
for line in lines:
    if not line.startswith('> '):
        outline.append(line)
    elif outline[-1].startswith('> '):
        outline[-1] += '\n' + line
    else:
        outline.append(line)

print('-'*80)
for line in outline:
    print(line)
    input()
