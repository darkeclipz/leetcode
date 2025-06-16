class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        counter = {}
        max_count = 0
        max_num = 0
        for k in nums:
            if k not in counter:
                counter[k] = 0
            counter[k] += 1
            if counter[k] > max_count:
                max_count = counter[k]
                max_num = k
        return max_num