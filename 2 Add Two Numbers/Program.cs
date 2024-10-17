/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     public int val;
 *     public ListNode next;
 *     public ListNode(int val=0, ListNode next=null) {
 *         this.val = val;
 *         this.next = next;
 *     }
 * }
 */
public class Solution {

    private int GetValueOrZero(ListNode n)
    {
        if (n == null)
        {
            return 0;
        }

        return n.val;
    }

    private bool HasNext(ListNode n)
    {
        return n != null && n.next != null;
    }

    public ListNode AddTwoNumbers(ListNode l1, ListNode l2) {

        var node = new ListNode();
        var zero = new ListNode();
        var start = node;
        int carry = 0;

        while (l1 != null || l2 != null)
        {
            node.val = GetValueOrZero(l1) + GetValueOrZero(l2) + carry;

            if (node.val > 9)
            {
                carry = 1;
                node.val -= 10;
            }
            else
            {
                carry = 0;
            }

            if (HasNext(l1) || HasNext(l2))
            {
                node.next = new ListNode();
                node = node.next;
            }

            if (l1 != null)
            {
                l1 = l1.next;
            }

            if (l2 != null)
            {
                l2 = l2.next;
            }
        }

        if (carry > 0)
        {
            node.next = new ListNode();
            node.next.val = carry;
        }

        return start;
    }
}