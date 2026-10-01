# Trend DB（Mac 版）使用说明

## 这是什么

`trends.db` 是一个 SQLite 数据库，就是个普通文件，双击不会中毒。
每天的 trend 扫描 CSV 导进来，一条 reel 一天存一行，
`scan_date` 是时间维度，时间一长自然形成"每条爆款的成长曲线"。

包里已有今晚 60 条 demo 数据（4 个赛道），可以直接打开看。

## 文件

| 文件 | 说明 |
|---|---|
| `trends.db` | 数据库本体 |
| `import_csv.py` | 导入脚本 |
| `schema.sql` | 建表语句（脚本会自动执行，不用手动跑） |

## 每天怎么用（30 秒）

1. 把我每天早上发到聊天的 CSV 存到这个文件夹里
2. 打开终端，进到这个文件夹，运行：

```bash
python3 import_csv.py ai-trends-2026-10-01.csv
```

3. 看数据：推荐装免费的 **DB Browser for SQLite**（sqlitebrowser.org），
   图形界面，点开就能看、能筛、能跑 SQL，不用学命令行。

Mac 自带 python3 和 sqlite3，不需要安装任何东西。

## 常用查询（在 DB Browser 的 SQL 标签页里跑）

明日三选（和每天任务里跑的是同一条逻辑）：

```sql
SELECT author, url, velocity_per_day, angle_idea
FROM reels
WHERE replicable = 1
  AND niche_fit = 'strong'
  AND spread_count >= 3
  AND feasible = 1
  AND saturated = 0
  AND is_fresh = 1
  AND geo_fit != 'non-us'
  AND niche = 'ai-tech'
ORDER BY velocity_per_day DESC
LIMIT 3;
```

看某条 reel 的历史曲线：

```sql
SELECT scan_date, likes, velocity_per_day
FROM reels
WHERE url = 'https://www.instagram.com/reel/xxxx/'
ORDER BY scan_date;
```

看某个格式的传播情况：

```sql
SELECT format_cluster, COUNT(DISTINCT author) AS 作者数,
       MAX(velocity_per_day) AS 最高日速
FROM reels
WHERE scan_date = '2026-10-01'
GROUP BY format_cluster
ORDER BY 作者数 DESC;
```

## 说明

- 同一个 CSV 重复导入不会产生重复行（按 url + scan_date 去重）
- 列定义以后不会变，加赛道只是多行数据，跨赛道 UNION 直接能查
- 以后 Mac mini 上的 collector 建起来，这个库和 schema 直接搬过去就能用

---

## 全自动方案（推荐，一次设置，之后不用管）

原理：我在 GitHub 上维护一个 repo，每天的新 CSV 自动 push 进去；
你的 Mac 每天 9 点自动 pull + 导入。两边只需要各设置一次。

**前提**：一个 GitHub repo（比如 `trend-db`），以及 repo 里有这些文件
（`import_csv.py`、`schema.sql`、`fetch_and_import.sh`、
`com.trenddb.daily.plist`、`README.md` 都已在这个包里，直接 push 上去就行；
`csv/` 目录放每天的 CSV，`trends.db` 不用进 repo）。

**Mac 上（在你的 Claude Code 里跑这几行，约 5 分钟）：**

```bash
# 1. 把 repo clone 到 home 目录
cd ~ && git clone https://github.com/KH95314/viral-trend-db.git trend-db

# 2. 装 launchd 定时任务（每天 9 点）
cp ~/trend-db/com.trenddb.daily.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.trenddb.daily.plist

# 3. 验证
launchctl list | grep trenddb
```

装好后每天 9 点自动执行，日志在 `/tmp/trenddb.log`，报错在 `/tmp/trenddb.err`。
想立刻试一次：`bash ~/trend-db/fetch_and_import.sh`

**我这边**：每日任务会自动把 CSV push 到 repo 的 `csv/` 目录。
需要你给我一个 GitHub Personal Access Token（repo 权限即可），
走安全表单填，不要贴在聊天里。
