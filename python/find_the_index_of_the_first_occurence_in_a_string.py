class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        ptr = 0
        i = 0
        while i < len(haystack):
            if haystack[i] == needle[ptr]:
                ptr += 1
                if ptr == len(needle):
                    return i - len(needle) + 1
            else:
                i -= ptr
                ptr = 0
            i += 1
        return -1

print(Solution().strStr("mississippi", "issip"))