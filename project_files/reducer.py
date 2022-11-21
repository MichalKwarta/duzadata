#!/usr/bin/env python3

from sys import stdin


def print_key_value(key:str, value:int):
    tabulated_key ='\t'.join(key.split('_'))
    print(f"{tabulated_key}\t{value}")

last_key,key = None,None
sum_value = 0
for line in stdin:
    key,value = line.strip().split('\t')
    

    value_int = int(value)
    
    if last_key == key:
        sum_value += value_int
    else:
        if last_key:
            print_key_value(last_key, sum_value)
        sum_value = value_int
        last_key = key

if last_key == key and last_key is not None:
    print_key_value(last_key, sum_value)
