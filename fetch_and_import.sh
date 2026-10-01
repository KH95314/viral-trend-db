#!/bin/bash
# 每天自动：git pull 最新 CSV -> 导入 trends.db
# 由 launchd 每天定时调用，平时不用管它
set -u
cd "$(dirname "$0")"

if command -v git >/dev/null 2>&1; then
  git pull --quiet 2>>/tmp/trenddb.err || echo "$(date): git pull 失败，用本地文件继续" >>/tmp/trenddb.err
fi

# csv/ 目录下有新 CSV 就导入；没有也不报错
shopt -s nullglob
files=(csv/*.csv)
if [ ${#files[@]} -gt 0 ]; then
  python3 import_csv.py "${files[@]}" >>/tmp/trenddb.log 2>&1
else
  echo "$(date): 没有新的 CSV" >>/tmp/trenddb.log
fi
