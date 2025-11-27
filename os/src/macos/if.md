# 分支

```sh
awk '{
  if ($1 >= 90) {
    print "优秀", $1
  } else if ($1 >= 60 && $1 < 90) {
    print "及格", $1
  } else {
    print "不及格", $1
  }
}' scores.txt
```

## 三目运算符

```sh
# 增加一个“状态”列：及格/不及格
awk '{
  status = ($1 >= 60 ? "及格" : "不及格")
  print $0, status
}' scores.txt
```
