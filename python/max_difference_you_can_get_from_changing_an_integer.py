class Solution:
    def maxDiff(self, num: int) -> int:
        digits = [int(x) for x in str(num)]
        largest_digit = self.findLargestDigit(digits)
        smallest_digit = self.findSmallestDigit(digits)
        replace_largest_digit_with = 9
        replace_smallest_digit_with = 1 if digits[0] == smallest_digit else 0
        x = int(str(num).replace(str(largest_digit), str(replace_largest_digit_with)))
        y = int(str(num).replace(str(smallest_digit), str(replace_smallest_digit_with)))
        return x - y
    def findLargestDigit(self, digits):
        for digit in digits:
            if digit != 9:
                return digit
        return 9
    def findSmallestDigit(self, digits):
        for digit in digits:
            if digit not in [0, 1]:
                return digit
        return 1