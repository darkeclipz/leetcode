namespace LeetCode.Problems;

public class Problem4 
{
    public double FindMedianSortedArrays(int[] nums1, int[] nums2)
    {
        var left = nums1.AsSpan();
        var right = nums2.AsSpan();
        var leftMedian = left.Median();
        var rightMedian = right.Median();
        
        if (leftMedian > rightMedian)
        {
            var temp = left;
            left = right;
            right = temp;
            (leftMedian, rightMedian) = (rightMedian, leftMedian);
        }

        Console.WriteLine($"({left.Median()}, {right.Median()})");
        
        left = left.DropLeftHalf();
        right = right.DropRightHalf();
        
        Console.WriteLine($"({left.Median()}, {right.Median()})");
        
        return 0.0;
    }
}

public static class Extensions
{
    public static double Median(this Span<int> slice)
    {
        int size = slice.Length;

        if (size % 2 == 0)
        {
            return (slice[size / 2 - 1] + slice[size / 2]) / 2.0;
        }
        
        return slice[size / 2];
    }

    public static Span<int> DropLeftHalf(this Span<int> slice)
    {
        if (slice.Length <= 1) return slice;
        
        if (slice.Length % 2 == 0)
        {
            return slice[(slice.Length / 2)..];    
        }

        return slice[(slice.Length / 2 - 1)..];
    }

    public static Span<int> DropRightHalf(this Span<int> slice)
    {
        if (slice.Length <= 1) return slice;
        
        if (slice.Length % 2 == 0)
        {
            return slice[..(slice.Length / 2)];    
        }

        return slice[..(slice.Length / 2 + 1)];
    }
}