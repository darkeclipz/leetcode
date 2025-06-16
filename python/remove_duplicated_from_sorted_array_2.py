class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        memo = {}
        i = 0
        while i < len(nums):
            if nums[i] in memo:
                memo[nums[i]] += 1
                if memo[nums[i]] > 2:
                    nums.pop(i)
                    continue
            else:
                memo[nums[i]] = 1
            i += 1
        return len(nums)