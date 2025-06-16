from typing import List


def all_equal(items):
    if len(items) <= 1:
        return True
    for i in range(1, len(items)):
        if items[i] != items[i-1]:
            return False
    return True

def get_chars(items, index):
    return [str[index] for str in items]

class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        i = 0
        min_length = min(len(str) for str in strs)
        result = ""
        if min_length == 0:
            return ""
        for i in range(min_length):
            chars = get_chars(strs, i)
            if all_equal(chars):
                result = strs[0][0:i+1]
            else:
                break
        return result