class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        result = filter(lambda x: x != val, nums)
        result = list(result)
        nums.clear()
        nums.extend(result)
        return len(nums)