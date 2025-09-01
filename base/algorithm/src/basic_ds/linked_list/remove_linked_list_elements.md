# 移除链表元素

[203. Remove Linked List Elements](https://leetcode.com/problems/remove-linked-list-elements/description/)

给你一个链表的头节点 head 和一个整数 val ，请你删除链表中所有满足 Node.val == val 的节点，并返回 新的头节点 。

示例 1：

```
输入：head = [1,2,6,3,4,5,6], val = 6
输出：[1,2,3,4,5]
```

示例 2：

```
输入：head = [], val = 1
输出：[]
```

示例 3：

```
输入：head = [7,7,7,7], val = 7
输出：[]
```

提示：

- 列表中的节点数目在范围 `[0, 104]` 内
- 1 <= Node.val <= 50
- 0 <= val <= 50

```java
public class RemoveLinkedListElements {
    public ListNode removeElements(ListNode head, int val) {
        // 处理头节点的值等于val的情况
        while (head != null && head.val == val) {
            // 删除头节点
            ListNode delNode = head;
            head = head.next;
            delNode.next = null;
        }

        // 处理所有节点都是val的情况
        if (head == null) {
            return head;
        }

        // 处理中间节点的值等于val的情况
        ListNode prev = head;
        while (prev.next != null) {
            if (prev.next.val == val) {
                // 删除prev.next节点
                ListNode delNode = prev.next;
                prev.next = delNode.next;
                delNode.next = null;
            } else {
                prev = prev.next;
            }
        }

        return head;
    }

    /**
     * 测试用例
     */
    public static void main(String[] args) {
        ListNode head = new ListNode(1);
        head.next = new ListNode(2);
        head.next.next = new ListNode(6);
        head.next.next.next = new ListNode(3);
        head.next.next.next.next = new ListNode(4);
        head.next.next.next.next.next = new ListNode(5);
        head.next.next.next.next.next.next = new ListNode(6);
        RemoveLinkedListElements removeLinkedListElements = new RemoveLinkedListElements();
        ListNode newHead = removeLinkedListElements.removeElements(head, 6);
        while (newHead != null) {
            System.out.println(newHead.val);
            newHead = newHead.next;
        }
    }
}
```

## 使用虚拟头节点解决

```java
public class RemoveLinkedListElements {
    public ListNode removeElements(ListNode head, int val) {
        // 创建虚拟头节点
        ListNode dummyHead = new ListNode(-1, head);

        // 由于有虚拟头节点, 所以无需专门处理头节点
        ListNode prev = dummyHead;
        while (prev.next != null) {
            if (prev.next.val == val) {
                // 删除prev.next节点
                ListNode delNode = prev.next;
                prev.next = delNode.next;
                delNode.next = null;
            } else {
                prev = prev.next;
            }
        }

        // 虚拟头节点不对外暴露
        return dummyHead.next;
    }
}
```
