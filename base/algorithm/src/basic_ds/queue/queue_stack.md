# 用队列实现栈

[225. Implement Stack using Queues](https://leetcode.com/problems/implement-stack-using-queues/description/)

请你仅使用两个队列实现一个后入先出（LIFO）的栈，并支持普通栈的全部四种操作（push、top、pop 和 empty）。

实现 MyStack 类：

- void push(int x) 将元素 x 压入栈顶。
- int pop() 移除并返回栈顶元素。
- int top() 返回栈顶元素。
- boolean empty() 如果栈是空的，返回 true ；否则，返回 false 。

注意：

- 你只能使用队列的标准操作 —— 也就是 push to back、peek/pop from front、size 和 is empty 这些操作。
- 你所使用的语言也许不支持队列。 你可以使用 list （列表）或者 deque（双端队列）来模拟一个队列 , 只要是标准的队列操作即可。

示例：

```
输入：
["MyStack", "push", "push", "top", "pop", "empty"]
[[], [1], [2], [], [], []]
输出：
[null, null, null, 2, 2, false]

解释：
MyStack myStack = new MyStack();
myStack.push(1);
myStack.push(2);
myStack.top(); // 返回 2
myStack.pop(); // 返回 2
myStack.empty(); // 返回 False
```

提示：

- 1 <= x <= 9
- 最多调用 100 次 push、pop、top 和 empty
- 每次调用 pop 和 top 都保证栈不为空

```java
import java.util.LinkedList;
import java.util.Queue;

class MyStack {

    private Queue<Integer> queue;
    /**
     * 记录栈顶元素
     */
    private Integer top;

    public MyStack() {
        queue = new LinkedList<>();
    }

    /**
     * 入栈
     * 把入队的方向作为栈顶
     */
    public void push(int x) {
        queue.add(x);
        // 记录栈顶元素
        top = x;
    }
    /**
     * 出栈
     */
    public int pop() {
        Queue<Integer> tmp = new LinkedList<>();
        // 把queue中除了栈顶的元素都放到tmp队列中
        while (queue.size() > 1) {
            tmp.add(queue.remove());
        }
        // 弹出栈顶元素
        int res = queue.remove();
        // 用tmp替代queue
        queue = tmp;
        // 更新栈顶元素
        top = tmp.isEmpty() ? null : tmp.peek();
        return res;
    }

    public int top() {
        return top;
    }

    public boolean empty() {
        return queue.isEmpty();
    }

    /**
     * 测试方法
     */
    public static void main(String[] args) {
        MyStack myStack = new MyStack();
        myStack.push(1);
        myStack.push(2);
        System.out.println(myStack.top());
        System.out.println(myStack.pop());
        System.out.println(myStack.empty());
    }
}
```

## 进阶：你能否仅用一个队列来实现栈

只需要修改 pop 方法的逻辑: 把 queue 的元素不断出队后再重新入队, 直到栈顶元素位于队首。

```java
/**
 * 出栈
 */
public int pop() {
    int size = queue.size();
    // 把queue 的元素不断出队后再重新入队, 直到栈顶元素位于队首。
    // 出队size-1次, 栈顶元素就位于队首了
    // 示例: queue = [1,2,3,4,5]
    // 循环1次后: [2,3,4,5,1]
    // 循环2次后: [3,4,5,1,2]
    // 循环3次后: [4,5,1,2,3]
    // 循环4次后: [5,1,2,3,4]
    for (int i = 0; i < size - 1; i++) {
        queue.add(queue.remove());
    }
    // 弹出栈顶元素
    int res = queue.remove();
    // 更新栈顶元素
    top = queue.isEmpty() ? null : queue.peek();
    return res;
}
```
