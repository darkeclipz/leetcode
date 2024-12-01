/*
 * Problem:
 * 
 * Given a string s, find the length of the longest substring without repeating characters.
 */

namespace LeetCode.Problems;

public class Problem3 
{
    public int LengthOfLongestSubstring(string s)
    {
        if (s.Length <= 1) return s.Length;

        // We create a window of unique characters, indicated by [left, right].
        var left = 0;
        var right = 0;
        var maxLength = 0;
        var visited = new HashSet<char>();

        while (right < s.Length)
        {
            // Check if the new character is unique...
            if (!visited.Add(s[right]))
            {
                // The character is not unique, so we move the left side of the window over
                while (visited.Contains(s[right]))
                {
                    visited.Remove(s[left]);
                    left++;
                }

                visited.Add(s[right]);
            }

            // Keep track of the maximum amount of unique characters we encounter.
            maxLength = Math.Max(maxLength, visited.Count);
            
            // Expand the window on the right side.
            right++;
        }
        
        return maxLength;
    }
}