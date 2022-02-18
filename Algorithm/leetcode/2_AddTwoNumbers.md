# Add Two Numbers

You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order and each of their nodes contain a single digit. Add the two numbers and return it as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.

# 例子

```
Input: (2 -> 4 -> 3) + (5 -> 6 -> 4)
Output: 7 -> 0 -> 8
Explanation: 342 + 465 = 807.
```

# 解

建立一个新链表，然后把输入的两个链表从头往后每两个相加，添加到新链表后面。为了避免两个输入链表同时为空，建立一个虚拟头结点dummy，将两个结点相加生成的新结点按顺序加到dummy结点之后，由于dummy结点指向链表的头不能变，所以用一个临时指针cur来指向新链表的最后一个结点。在遍历链表的同时按从低到高的顺序直接相加。while循环的条件是两个链表中只要有一个不为空行。由于链表两个链表的长度可能不同，所以在取当前结点值的时候，先判断一下，若为空则取0，否则取结点值。然后把两个结点值相加，同时还要加上进位carry。然后更新 carry，sum大于10就进1，然后以sum%10取个位数建立一个新结点，连到新链表后面。while 循环退出之后，最高位的进位问题要最后特殊处理一下，若 carry 为1，则再建一个值为1的结点。

```java
public class Solution {
    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(-1);
        ListNode cur = dummy;
        int carry = 0;
        while (l1 != null || l2 != null) {
            int d1 = l1 == null ? 0 : l1.val;
            int d2 = l2 == null ? 0 : l2.val;
            int sum = d1 + d2 + carry;
            carry = sum >= 10 ? 1 : 0;
            cur.next = new ListNode(sum % 10);
            cur = cur.next;
            if (l1 != null) l1 = l1.next;
            if (l2 != null) l2 = l2.next;
        }
        if (carry == 1) cur.next = new ListNode(1);
        return dummy.next;
    }
}
```
