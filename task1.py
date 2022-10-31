#!/usr/bin/env python3

#vi +':wq ++ff=unix' filename.py line endings have CR characters
import operator
import sys

with open(sys.argv[1], 'rb') as in_file:
    data = in_file.read()       # data is of type "bytes"
    hexdata = data.hex()              # hexdata is a string of hex digits
    bindata = bytes.fromhex(hexdata)  # bindata should be the same as data

n = 32
chunks = [hexdata[i:i+n] for i in range(0, len(hexdata), n)]
occ_map = {}
for chunk in chunks:
    if chunk in occ_map:
        occ_map[chunk] += 1
    else:
        occ_map[chunk] = 1

sorted_occ = sorted(occ_map.items(), key=operator.itemgetter(1), reverse=True)
sorted_iter = iter(sorted_occ)

# Decrypt map
de_map = {}
first = next(sorted_iter)
second = next(sorted_iter)

# 2 acc per TRANSAC and per INVOICE, 1 per BALANCE, therefore accs must be most frequent
de_map[first[0]] = "account1" # Cannot determine what acc
de_map[second[0]] = "account2" # Cannot determine what acc
de_map[chunks[0]] = "Command" # First line must be some command

adj_acc_map = []
more_freq = {}
for index, line in enumerate(chunks):
    if line in de_map:
        if chunks[index-1] not in de_map:
            if chunks[index-1] in more_freq:
                more_freq[chunks[index-1]] += 1
            else:
                more_freq[chunks[index-1]] = 1
            adj_acc_map.append(chunks[index-1])
        adj_acc_map.append(de_map[line])

#print(*adj_acc_map, sep='\n')

more_freq = sorted(more_freq.items(), key=operator.itemgetter(1), reverse=True)

acc_count = 0

# Check if first command was a BALANCE
if chunks[-1] in de_map: # True, last command ended with call to some acc, therefore was BALANCE
    de_map[chunks[-2]] = "BALANCE"
else :
    if chunks[-2] in de_map and chunks[-3] in de_map:
        de_map[chunks[-4]] = "INVOICE" 
    else: 
        de_map[chunks[-5]] = "TRANSFER"

adj_acc_map = []

for index, line in enumerate(chunks):
    if line in de_map:
        if chunks[index-1] not in de_map:
            adj_acc_map.append(chunks[index-1])
        adj_acc_map.append(de_map[line])

#print(*adj_acc_map, sep='\n')

# Using an list of lines adjacent to known command, determine other commands
curr_acc = None
last_unk = None
for index, line in enumerate(adj_acc_map):
    # Assume first command is BALANCE, detect other
    # !!What if first command is not BALANCE?
    if line == "account1" or line == "account2":
        # INVOICES will always have two accounts adjacent, mark and continue
        if adj_acc_map[index - 1] == "account1" or adj_acc_map[index - 1] == "account2":
            de_map[last_unk] = "INVOICE"
            curr_acc = None
            continue
        if curr_acc == line: # Found same acc twice in a row
            if "BALANCE" in de_map.values():
                de_map[last_unk] = "TRANSFER"
            else: 
                de_map[last_unk] = "BALANCE"
            curr_acc = None
        else:
            curr_acc = line
    elif line == "BALANCE" or line == "TRANSFER" or line == "INVOICE":
        curr_acc = None # Reset curr acc
    else:
        last_unk = line

adj_acc_map = []

# Reval adjacents for final print
for index, line in enumerate(chunks):
    if line in de_map:
        if chunks[index-1] not in de_map:
            adj_acc_map.append(chunks[index-1])
        adj_acc_map.append(de_map[line])

# Final output, only of commands
for line in adj_acc_map:
    if line == "BALANCE" or line == "TRANSFER" or line == "INVOICE":
        print(line)
