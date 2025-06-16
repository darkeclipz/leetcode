namespace LeetCode.Problems;

public class Problem3396 
{
    public int MinimumOperations(int[] nums)
    {
        var current = nums.AsSpan();
        var result = 0;

        while (!IsDistinct(current))
        {
            current = current.Length <= 3 ? [] : current[3..];
            result++;
        }
        
        return result;
    }

    private bool IsDistinct(Span<int> nums)
    {
        HashSet<int> set = [];

        foreach (var num in nums)
        {
            if (!set.Add(num))
            {
                return false;
            }
        }

        return true;
    }
}