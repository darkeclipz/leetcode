class Solution:
    def myAtoi(self, s: str) -> int:
        sign = 1
        s = s.lstrip()
        if not s:
            return 0
        if s[0] == '-':
            sign = -1
            s = s[1:]
        elif s[0] == '+':
            s = s[1:]
        buffer = []
        for char in s:
            if '0' <= char <= '9':
                buffer.append(char)
            else:
                break
        if not buffer:
            return 0
        num = sign * int("".join(buffer))
        return Solution.clamp(num, -2**31, 2**31-1)
    def clamp(x, a, b):
        if x < a: return a
        if x > b: return b
        return x