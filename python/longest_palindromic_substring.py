class Solution:
    def longestPalindrome(self, s: str) -> str:
        if len(s) == 1:
            return s
        max_n = 0
        palindrome = ""
        for start in range(0, len(s)):
            for end in range(start + 1, len(s) + 1):
                substr = s[start:end]
                if substr == substr[::-1]:
                    n = len(substr)
                    if n > max_n:
                        max_n = n
                        palindrome = substr
        return palindrome