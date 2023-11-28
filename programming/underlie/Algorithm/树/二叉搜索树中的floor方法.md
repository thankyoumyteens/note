# 二叉搜索树中的floor方法

寻找floor , ceil需保证

- 若key值存在, 那么floor , ceil就是key值自身。
- 若key值不存在: floor是最接近key值且**小于**key的节点。ceil是最接近key值且**大于**key的节点

这里寻找floor的逻辑主要分为3个步骤

- 如果node的key值和要寻找的key值相等: 则node本身就是key的floor节点。
- 如果node的key值比要寻找的key值大: 则要寻找的key的floor节点一定在node的左子树中。
- 如果node的key值比要寻找的key值小: 则node有可能是key的floor节点, 也有可能不是, 需要尝试向node的右子树寻找一下还有没有比key值小的节点。

```java
public Key floor(Key key){
    if( count == 0 || key.compareTo(minimun()) < 0 )
        return null;

    Node floorNode = floor(root, key);
    return floorNode.key;
}
 
private Node floor(Node node, Key key){
    if(node == null) return null;
    // 如果该node的key和key相等, 就是本身
    if(node.key.compareTo(key) == 0){
        return node;
    }
    // 如果该node比key要大的话, 去node的左子树寻找
    if(node.key.compareTo(key) > 0){
        return floor(node.left, key);
    }
    // 如果node比key小, 可能是, 也能是不是
    // 先去node的右子树寻找
    Node tempNode = floor(node.right, key);
    if(tempNode != null)
        return tempNode;
    // node的右子树没找到, 则node是key的floor节点
    return node;   
}
```
