#!/usr/bin/env python3


from sys import stdin

last_key,key = None,None
sum_value = 0
for line in stdin:
    key,value = line.strip().split('\t')

    value_int = int(value)
    
    if last_key == key:
        sum_value += value_int
    else:
        if last_key:
            print(f"{last_key}\t{sum_value}")
        sum_value = value_int
        last_key = key

if last_key == key:
    print(f"{last_key}\t{sum_value}")
