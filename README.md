> 爬虫与数据库 课后练习
>
> Lambda X
>
> 2022 年 7 月 13 日

# Updates

- 07-15

  - 关于知乎热榜爬虫
    - 对于非典型的问题，如 知乎盐选，`theatre` 等网址不形如 `zhihu.com/question/*` 的热榜内容 **可以无需爬取、直接跳过**。
    - 对于热榜信息的爬取，可以自选 `/hot` `/billboard` 等来源
    - 爬虫的各个部分可以根据自己的想法进行实现，没有固定的实现标准。

  - 关于 WebVPN 爬虫 
    
    **Commit 时务必检查仓库历史中没有 存在学号，密码，Cookie 等个人信息 的文件**
  
    由于练习的设计失误，没有给仓库添加 `.gitignore` ，这造成在提交作业时可能的安全隐患，这点我需要向大家致歉，并且提醒大家注意提交的内容。
    
    如果你的 Commit 记录中已经存在给出一种提交方法

    - 添加 `.gitignore` 文件，将 `settings.json` 等含有个人信息的文件 ignore。

    ```
    Zhihu_crawler/zhihu.json
    WebVPN_crawler/settings.json
    ```

    - 由于先前的 Commit 中可能包含了上述个人信息，可以创建一个独立的分支，例如 `submission`，删除敏感文件

    ```bash
    git checkout --orphan submission # 创建一个没有前驱的 submission 分支
    git add .                        # 添加当前的全部文件
    git rm --cached  WebVPN_crawler/settings.json  Zhihu_crawler/zhihu.json # 删除含有个人信息的文件
    ```

    - 这时使用 `git status` 确认待 Commit 的文件中不含上述两个文件，且包含 `.gitignore`
    - 提交，然后仅推送新分支

    ```bash
    git commit -m "info-purged submission"
    git push origin submission
    ```

    此时仓库中的 `submission` 分支含有新代码；而旧分支保存原状。

    如果 **已经推送** 了含有个人信息的旧分支，可以将代码托管平台上含有个人信息的旧分支删除，然后尽快修改泄露的密码等信息。（应该没有已经推送了密码的吧呜呜呜
    
    - 推送后，可以将 `submission` 置为默认分支。

    此外，也可以参考 [Github 文档](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) ，使用  `bfg`  等工具移除敏感信息，然后对仓库进行 force push。这样无需新建分支且可以保留提交记录。

# requests 练习

本次爬虫练习中，希望你动手实现一个知乎热榜定时跟踪器。使得他可以定期爬取知乎热榜，并记录热榜中问题的一些基本信息，如问题摘要、描述、热度、访问人数、回答数量等等，然后将这些数据存入数据库进行保存。

Choice 1: 删除 `Zhihu_crawler/zhihu.py` 然后从零开始写 :feet:

Choice 2: 阅读 `Zhihu_crawler/zhihu.py`，完成约 40 行的代码填空 :happy: 

## 代码填空介绍

代码填空中已经实现好爬虫的主要逻辑，并实现了数据表的创建与修改语句。但它并不能获取任何数据。这是因为它获取热榜的 `get_board` 方法和 `get_question` 方法尚未实现。

请你按照提示实现这两个方法，给出相应的返回值。然后就可以让它定时跟踪知乎热榜并将内容存入数据库了。

### 推荐实现顺序

1. 在 `Zhihu_crawler/zhihu.json` 中填入

   - 你认为可能会用到的 Headers
   - MySQL 服务器的配置信息

   此时运行结果为

   ```bash
   2022-07-09 18:19:54.295 [INFO] Settings loaded
   2022-07-09 18:19:54.419 [INFO] Begin crawling ...
   2022-07-09 18:19:54.539 [ERROR] Crawl 161 encountered an exception . This crawl stopped.
   Traceback (most recent call last):
     File "zhihu.py", line 96, in watch
       board_entries = self.get_board()
     File "zhihu.py", line 259, in get_board
       raise NotImplementedError
   NotImplementedError
   2022-07-09 18:19:54.543 [INFO] Sleep 599.8760051727295 second(s)
   ```

   提示你应该实现 `get_board`。

2. 在 `Zhihu_crawler/zhihu.py` 中按照提示实现 `get_board` 方法。再运行 `zhihu.py` 此时运行结果类似

   ```bash
   2022-07-09 18:20:38.343 [INFO] Settings loaded
    2022-07-09 18:20:38.496 [INFO] Begin crawling ...
    2022-07-09 18:20:39.534 [INFO] Get 50 items: 安倍晋三遭枪击身亡，按照日本法律行凶者涉,如何看待周杰伦新专辑全部曲目中只有 7 ,化学键断裂要耗能，为什么生物教材上写 A,如何看待报告...
    2022-07-09 18:20:39.535 [INFO] Sleep 2 second(s)
    2022-07-09 18:20:41.549 [ERROR] 
    Traceback (most recent call last):
      File "zhihu.py", line 122, in watch
        detail = self.get_question(item["qid"])
      File "zhihu.py", line 307, in get_question
        raise NotImplementedError
    NotImplementedError
    2022-07-09 18:20:41.677 [INFO] Sleep 2 second(s)
   ```

   此时爬虫已经可以正常获取热榜（`watch` 方法中，会将热榜中每个问题截取 20 个字符进行显示），但还无法获取问题页面中的信息。

   在代码中有一些实现提示。

3. 在 `Zhihu_crawler/zhihu.py` 中按照提示实现 `get_question` 方法。再运行 `zhihu.py` 此时运行结果类似

   ```bash
   2022-07-09 18:26:15.442 [INFO] Settings loaded
   2022-07-09 18:26:15.737 [INFO] Begin crawling ...
   2022-07-09 18:26:16.760 [INFO] Get 50 items: 安倍晋三遭枪击身亡，按照日本法律行凶者涉,如何看待周杰伦新专辑全部曲目中只有 7 ,化学键断裂要耗能，为什么生物教材上写 A,如何看待报告...
   2022-07-09 18:26:16.761 [INFO] Sleep 2 second(s)
   2022-07-09 18:26:19.652 [INFO] Get question detail for 安倍晋三遭枪击身亡，按照日本法律行凶者涉嫌何种罪名？会不会被判处死刑？: raw detail length 498
   2022-07-09 18:26:19.780 [INFO] Sleep 2 second(s)
   2022-07-09 18:26:22.709 [INFO] Get question detail for 如何看待周杰伦新专辑全部曲目中只有 7 首新歌，收录了之前的 5 首老歌？: raw detail length 663
   2022-07-09 18:26:22.834 [INFO] Sleep 2 second(s)
   2022-07-09 18:26:25.708 [INFO] Get question detail for 化学键断裂要耗能，为什么生物教材上写 ATP 高能磷酸键断裂会释放大量能量？: raw detail length 0
   2022-07-09 18:26:25.832 [INFO] Sleep 2 second(s)
   ```

   在代码中有一些实现提示。

4. 实现过程中，建议另开 `Jupyter Notebook` 进行调试。~~甚至可以调好了再把代码复制进去。~~如果需要，可以对给出的代码任意修改。

5. 添加其他好玩的功能



# Selenium 练习

在本次 `Selenium `练习中，希望你动手实现一个 GPA 计算器。

一种参考实现是：使用 `Selenium `模拟点击登录 WebVPN，然后登录 info，进而访问成绩单页面查询到成绩，计算每学期的绩点。

使用 `Selenium` 进行 WebVPN 登录并跳转到校内的指定页面的代码码见 `WebVPN/webvpn.py`。 你需要设计并实现查询过程中可能用到的函数，并补全查询流程。这部分内容在代码中用 `TODO` 标出。当然也可以完全不理会这些东西，自己进行实现。

成绩单的页面的信息编码在了 `HTML` 中。你可能需要使用 `BeautifulSoup` 或 `lxml` 等工具进行解析。



# SQL 练习

SQL 练习希望能帮助你熟悉一些基本的 SQL 语法。

我们同样以知乎爬虫数据为背景，在 MySQL 数据库中进行练习。先下载导入 7 月 8 日至 7 月 12 日的一部分知乎热榜数据。

**注意：不要和你的爬虫共用一个数据库，因为导入的过程中会删除已经存在的数据。**

```bash
curl -fsSL https://cloud.tsinghua.edu.cn/f/a46b322b89064c03b89e/?dl=1 -o exercise.sql.gz 
gzip -dc exercise.sql.gz > exercise.sql
```

然后进入 MySQL，在新建并使用数据库；可以用 `source` 执行 `exercise.sql` ，将预置的数据导入。

```bash
mysql -u <username> -p

mysql> create database s2;
Query OK, 1 row affected (0.02 sec)

mysql> use s2;
Database changed

mysql> source exercise.sql;

mysql> show tables;
+--------------+
| Tables_in_s2 |
+--------------+
| crawl        |
| record       |
+--------------+
2 rows in set (0.00 sec)
```

这样就成功导入了表。

导入数据的字段类型与含义与爬虫部分的设计一致（事实上它们就是我测试爬虫框架时产生的数据），可以在 `zhihu.py` 的 `create_tables` 函数中查看字段设计及含义。

每个问题的提示是一些**可能**对完成这次查询有帮助的 MySQL 关键字；在`SQL_query/example.log` 给出了每个问题的参考查询结果，但将查询语句用 `<Q*>` 隐去，便于你参考自己的查询实现是否正确。



## Q1 添加新列

>  给 `record` 表添加一列 `heat_w`，准备以万为单位为储存 INT 型的热度。

- 提示：
  - ALTER TABLE
  - 使用 `DESC record;` 查看表中的所有列。
  - 使用 `SHOW COLUMNS FROM record LIKE 'heat%';` 查看表中以 `heat` 开头的列。

## Q2 快速填充

> 给 `heat_w` 一列以**万**为单位填入热度。
>
> 如 ` 114514万热度` 时填入 `114514`

- 提示：

  - UPDATE
  - REPLACE

- 可以使用

  ```mysql
  SELECT COUNT(*) cnt FROM record WHERE heat_w is null and heat is not null;
  ```

  检查还有多少列没有填好（即原来非空但 heat_w 为空）

## Q3 查询关键词

> 查询标题中包含 '高考' 的问题标题。每个问题标题仅显示一次

- 提示
  - SELECT 
  - DISTINCT
  - WHERE 
  - LIKE


## Q4 问题走势

> 查询问题 `507238700` 的 `heat`, `hit_at`, `visitCount`, `followerCount` ，从旧到新

- 提示：
  - SELECT
  - WHERE
  - ORDER BY

注1：问题是随便选的

注2：有兴趣的同学可以在 Python 中执行这一查询，然后使用 `matplotlib` 画出相应指标随时间变化的走势图。

## Q5 上榜统计

> 查询每个 `title` 上榜的次数，只返回上榜 100 次以上的 `title` 和 `上榜次数`。由多到少降序排列。

- 提示 
  - SELECT
  - COUNT
  - GROUP BY
  - HAVING
  - ORDER BY


## Q6 最热记录

> 查询浏览次数最多的问题，获取它浏览次数最多的那一次记录中的 `title`, `visitCount`, `hit_at`, `heat`, `ranking` 。

- 提示
  - SELECT
  - WHERE + Sub Query
  - MAX

## Q7 查阅合订本

> 查询哪些问题的**标题至少变化了一次**。对于这些问题，查询其 `qid` 和 `title` ，每个不同的标题仅返回 1 次。每个问题的不同标题连续显示，按 `qid` 升序排列。

- 提示：
  - SELECT
  - JOIN + Sub Query
  - COUNT
  - DISTINCT
  - ORDER BY



# 提交作业

通过 clone / fork 代码仓库 **[sast2022-crawler-SQL-training](https://github.com/Btlmd/sast2022-crawler-SQL-training)** 完成作业

- requests 练习，提交在 `Zhihu_crawler` 目录下
  - 代码
  - README: 简要说明使用方法
  - 爬到的一些数据，导出至少爬 5 次热榜（如果觉得 10 分钟间隔不合适可以自行调整）的数据表，导出为 `sql` 文件。导出后文件较大的，可以使用 gzip 压缩或者上传云盘附上链接。
  - 导出方法见课前准备材料。
- Selenium 练习，提交在 `WebVPN_crawler` 目录下
  - 代码
  - README: 简要说明使用方法
- SQL 练习，提交在 `SQL_query` 目录下
  - 请在练习数据库中使用 `tee` 指令输出查询日志，然后提交上述 7 条查询产生的查询日志文件
- 其他你希望包括的内容

完成作业后，将代码进行托管，如 Github， Tsinghua Git 等，然后在原仓库中新建 Issue，提交代码仓库地址。

可以在 Issue 中附上学号或邮箱，**或** 将 Issue 编号与学号发送至 [liu-md20@mails.tsinghua.edu.cn](mailto:liu-md20@mails.tsinghua.edu.cn) ，便于我们统计大家的参与情况并进行作业奖励的发放。

为了最佳的练习体验，希望您能尽早完成练习。:)
