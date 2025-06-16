MATCH_ONE = "MATCH-ONE"
MATCH_ZERO_OR_MORE = "MATCH-ZERO-OR-MORE"

class Regex:
    def __init__(self, pattern):
        self.matchers = []
        self.parse(pattern)

    def match(self, s):
        return self.next(s, 0, 0)

    def next(self, s, s_idx, m_idx):
        if m_idx == len(self.matchers) and s_idx == len(s):
            return True
        if m_idx >= len(self.matchers):
            return False
        if s_idx >= len(s):
            m_type, _ = self.matchers[m_idx]
            if m_type == MATCH_ZERO_OR_MORE:
                return self.next(s, s_idx, m_idx + 1)
            return False
        m_type, _ = self.matchers[m_idx]
        if m_type == MATCH_ONE:
            return self.match_one(s, s_idx, m_idx)
        if m_type == MATCH_ZERO_OR_MORE:
            if self.match_zero_or_more(s, s_idx, m_idx):
                return True
        return False
    
    def match_one(self, s, s_idx, m_idx):
        # match a single character in the string at index s_idx + 1
        _, m_char = self.matchers[m_idx]
        if m_char == '.' or m_char == s[s_idx]:
            return self.next(s, s_idx + 1, m_idx + 1)
        return False

    def match_zero_or_more(self, s, s_idx, m_idx):
        # repeated match one
        _, m_char = self.matchers[m_idx]
        i = 0
        while s_idx + i < len(s) and (s[s_idx + i] == m_char or m_char == '.'):
            i += 1
            if self.next(s, s_idx + i, m_idx + 1):
                return True
        return self.next(s, s_idx, m_idx + 1)
        
    def parse(self, pattern) -> None:
        i = 0
        while i < len(pattern):
            char = pattern[i]
            if 'a' <= char <= 'z':
                self.matchers.append((MATCH_ONE, char))
            elif char == '.':
                self.matchers.append((MATCH_ONE, char))
            elif char == '*':
                self.matchers.pop()
                if self.matchers:
                    m_type, m_char = self.matchers[-1]
                    if m_type == MATCH_ZERO_OR_MORE and pattern[i-1] == m_char:
                        continue
                self.matchers.append((MATCH_ZERO_OR_MORE, pattern[i-1]))
            i += 1

class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        regex = Regex(p)
        return regex.match(s)
    

s = Solution()
result = s.isMatch("aaaaaaaaaaaaaaaaaaab", "a*a*a*a*a*a*a*a*a*a*")
print(result)