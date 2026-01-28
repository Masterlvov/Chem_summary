# Basic
不常用就会忘记，遂在此记录一下经常使用的一些东西。拥抱AI，假借先进tools，提升效率。
## IO相关
- os pathlib


## 正则表达式
模糊匹配导致重复：df_source[target_col].astype(str).str.contains(kw)

## 列表
- 有序、可变、可重复 的序列容器
- # 多种创建方式
list1 = []                    # 空列表
list2 = [1, 2, 3]            # 直接创建
list3 = list("hello")        # 从可迭代对象创建
list4 = [i*2 for i in range(5)]  # 列表推导式
my_list = [10, 20, 30, 40, 50]
print(my_list[0])       # 10 - 正向索引
print(my_list[-1])      # 50 - 负向索引
print(my_list[1:4])     # [20, 30, 40] - 切片
print(my_list[::2])     # [10, 30, 50] - 步长切片

<<<<<<< HEAD
## 
=======
- Python包含以下函数:
1	cmp(list1, list2)
比较两个列表的元素
2	len(list)
列表元素个数
3	max(list)
返回列表元素最大值
4	min(list)
返回列表元素最小值
5	list(seq)
将元组转换为列表
- Python包含以下方法:
1	list.append(obj)
在列表末尾添加新的对象
2	list.count(obj)
统计某个元素在列表中出现的次数
3	list.extend(seq)
在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）
4	list.index(obj)
从列表中找出某个值第一个匹配项的索引位置
5	list.insert(index, obj)
将对象插入列表
6	list.pop([index=-1])
移除列表中的一个元素（默认最后一个元素），并且返回该元素的值
7	list.remove(obj)
移除列表中某个值的第一个匹配项
8	list.reverse()
反向列表中元素
9	list.sort(cmp=None, key=None, reverse=False)
对原列表进行排序
>>>>>>> 76f3de7507bd2b2e79d7b1f75821a2b6eb0a14fb

## 字符

## 元组

<<<<<<< HEAD

=======
## 集合

>>>>>>> 76f3de7507bd2b2e79d7b1f75821a2b6eb0a14fb
# excel操作相关
<<<<<<< HEAD
## pandas
- excel上色，
- 
方法	作用
pd.read_excel()	直接读取 Excel 文件中的一个或多个 sheet，并返回 DataFrame（或字典）
pd.ExcelFile()	打开并解析 Excel 文件，返回一个可重复使用的文件对象，后续再调用 .parse() 或配合 pd.read_excel() 读取具体 sheet
=======
# 打开一次文件
xls = pd.ExcelFile('data.xlsx')

# 查看所有 sheet 名
print(xls.sheet_names)

# 多次读取不同 sheet（共用同一个已打开的文件对象）
df1 = pd.read_excel(xls, sheet_name='Sheet1')
df2 = pd.read_excel(xls, sheet_name='Sheet2')
# 或者用 xls.parse('Sheet1')（旧版写法，现在等价于 read_excel）
>>>>>>> 76f3de7507bd2b2e79d7b1f75821a2b6eb0a14fb