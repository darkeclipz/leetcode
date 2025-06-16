class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        result = sorted(list(set(nums)))
        nums.clear()
        nums.extend(result)
        return len(nums)