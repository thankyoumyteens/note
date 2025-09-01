# 用栈实现队列

[232. Implement Queue using Stacks](https://leetcode.com/problems/implement-queue-using-stacks/description/)

请你仅使用两个栈实现先入先出队列。队列应当支持一般队列支持的所有操作（push、pop、peek、empty）：

实现 MyQueue 类：

- void push(int x) 将元素 x 推到队列的末尾
- int pop() 从队列的开头移除并返回元素
- int peek() 返回队列开头的元素
- boolean empty() 如果队列为空，返回 true ；否则，返回 false

说明：

- 你 只能 使用标准的栈操作 —— 也就是只有 push to top, peek/pop from top, size, 和 is empty 操作是合法的。
- 你所使用的语言也许不支持栈。你可以使用 list 或者 deque（双端队列）来模拟一个栈，只要是标准的栈操作即可。

示例 1：

```
输入：
["MyQueue", "push", "push", "peek", "pop", "empty"]
[[], [1], [2], [], [], []]
输出：
[null, null, null, 1, 1, false]

解释：
MyQueue myQueue = new MyQueue();
myQueue.push(1); // queue is: [1]
myQueue.push(2); // queue is: [1, 2] (leftmost is front of the queue)
myQueue.peek(); // return 1
myQueue.pop(); // return 1, queue is [2]
myQueue.empty(); // return false
```

提示：

- 1 <= x <= 9
- 最多调用 100 次 push、pop、peek 和 empty
- 假设所有操作都是有效的 （例如，一个空的队列不会调用 pop 或者 peek 操作）

```java
import java.util.Stack;

class MyQueue {

    private Stack<Integer> stack;
    /**
     * 记录队首元素
     */
    private Integer front;

    public MyQueue() {
        stack = new Stack<>();
    }

    /**
     * 入队
     * 栈顶作为队尾
     */
    public void push(int x) {
        if (stack.isEmpty()) {
            front = x;
        }
        stack.push(x);
    }

    public int pop() {
        Stack<Integer> tmp = new Stack<>();
        // 把stack中除了栈底的元素都转移到tmp中
        while (stack.size() > 1) {

            tmp.push(stack.pop());
        }
        // 此时tmp中的元素顺序和之前的stack正好是相反的
        // 记录队首元素
        front = tmp.isEmpty() ? null : tmp.peek();

        // 弹出栈底元素
        int res = stack.pop();
        // 把tmp中的元素都转移回stack中
        while (!tmp.isEmpty()) {
            push(tmp.pop());
        }
        return res;
    }

    public int peek() {
        return front;
    }

    public boolean empty() {
        return stack.isEmpty();
    }

    /**
     * 测试方法
     */
    public static void main(String[] args) {
        MyQueue myQueue = new MyQueue();
        myQueue.push(1);
        myQueue.push(2);
        System.out.println(myQueue.peek());
        System.out.println(myQueue.pop());
        System.out.println(myQueue.empty());
    }
}
```

## 进阶

你能否实现每个操作均摊时间复杂度为 O(1) 的队列？换句话说，执行 n 个操作的总时间复杂度为 O(n) ，即使其中一个操作可能花费较长时间。

每次调用 pop，都会将 stack 的元素放进 tmp,再从 tmp 挪回来。如果用户连续调用 pop 的话，这个过程相当于重复了。所以把 stack 的元素转移到 tmp 后, 不再把元素转移回 stack。下次再调用 pop，如果发现 tmp 不为空，就直接拿 tmp 的栈顶元素。

把 stack 改名成 stack1, tmp 改名成 stack2。stack1 和 stack2 一起组成完整的队列。

假设某次 push 后, stack1 中的元素为 `[1,2,3,4,5]<-top`, stack2 中的元素为 `[]<-top`, front 为 1
则:

1. 执行一次 pop 后, stack1 中的元素变为 `[]<-top`, stack2 中的元素变为 `[5,4,3,2]<-top`, front 还是 1
2. 再执行一次 pop 后, stack1 中的元素变为 `[]<-top`, stack2 中的元素变为 `[5,4,3]<-top`, front 还是 1
3. 执行一次 push 后, stack1 中的元素变为 `[6]<-top`, stack2 中的元素变为 `[5,4,3]<-top`, front 还是 1

```java
import java.util.Stack;

class MyQueue {

    private Stack<Integer> stack1;
    private Stack<Integer> stack2;

    /**
     * 记录队首元素
     */
    private Integer front;

    public MyQueue() {
        stack1 = new Stack<>();
        stack2 = new Stack<>();
    }

    /**
     * 入队
     * 栈顶作为队尾
     */
    public void push(int x) {
        if (stack1.isEmpty()) {
            // 只有stack2为空时, front才是正确的队首元素
            front = x;
        }
        stack1.push(x);
    }

    public int pop() {
        // stack2中的元素顺序和之前的stack1正好是相反的
        // 所以stack2的栈顶元素就是队首元素
        if (!stack2.isEmpty()) {
            return stack2.pop();
        }
        // 把stack1中除了栈底的元素都转移到stack2中
        while (stack1.size() > 1) {
            stack2.push(stack1.pop());
        }

        // 弹出栈底元素
        return stack1.pop();
    }

    public int peek() {
        if (!stack2.isEmpty()) {
            return stack2.peek();
        }
        return front;
    }

    public boolean empty() {
        return stack1.isEmpty() && stack2.isEmpty();
    }
}
```
