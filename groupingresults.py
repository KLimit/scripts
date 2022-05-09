"""Useful tools for grouping test results.

From an ipython log I made.
"""

from itertools import groupby
import re
import itertools
import os
import sys


def groupranges(nums, differ=1):
    grouped = []
    currlist = []
    for i, num in enumerate(nums):
        try:
            diff = num - nums[i+1]
        except IndexError:
            currlist.append(num)
            grouped.append(currlist)
            return grouped
        if diff == -differ:
            currlist.append(num)
        else:
            currlist.append(num)
            grouped.append(currlist)
            currlist = []
    return grouped
    

def stringranges(nums, differ=1):
    if len(nums) == 1:
        return f'{nums[0]}'
    strranges = []
    for group in groupranges(nums):
        if len(group) == 1:
            strranges.append(f'{group[0]}')
        else:
            strranges.append(f'{group[0]}-{group[-1]}')
    return strranges
    

def grouplist(fails, numpttn=r'(?<!^)(?<=_)(\d+)$'):
    def delnumpttn(st):
        return re.sub(numpttn, '', st)
    for key, group in groupby(sorted(fails), delnumpttn):
        nums = sorted([
            int(re.search(numpttn, item).groups()[0]) for item in group
        ])
        for rn in stringranges(nums):
            print(f'* {key}_{rn}')
