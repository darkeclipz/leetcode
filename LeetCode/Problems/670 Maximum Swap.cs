namespace LeetCode.Problems;

public class Problem670
{
    public int MaximumSwap(int num)
    {
        int best = int.MinValue;
        char[] digits = num.ToString().ToCharArray();

        for (int i = 0; i < digits.Length; i++)
        {
            for (int j = i + 1; j < digits.Length; j++)
            {
                (digits[i], digits[j]) = (digits[j], digits[i]);
                int candidate = int.Parse(new string(digits));
                best = Math.Max(best, candidate);
                (digits[i], digits[j]) = (digits[j], digits[i]);
            }
        }

        return best;
    }
}