var sln = new Solution();
Console.WriteLine(sln.MaximumSwap(2736));
Console.WriteLine(sln.MaximumSwap(9973));
Console.WriteLine(sln.MaximumSwap(98368));
Console.WriteLine(sln.MaximumSwap(19931105));

public class Solution {
    public int MaximumSwap(int num) {
        int best = int.MinValue;
        char[] digits = num.ToString().ToCharArray();

        for(int i = 0; i < digits.Length; i++)
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
