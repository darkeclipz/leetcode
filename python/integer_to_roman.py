class Solution:
    def intToRoman(self, num: int) -> str:
        c_tbl = {
            'I': 1,
            'V': 5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000
        }
        keys = list(c_tbl.keys())
        remainder = num
        result = ""
        while remainder > 0:
            max_idx = len(c_tbl) - 1
            while max_idx > 0 and c_tbl[keys[max_idx]] <= remainder:
                max_idx -= 1
            result += keys[max_idx]
            remainder -= c_tbl[keys[max_idx]]
        return result

