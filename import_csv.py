#!/usr/bin/env python3
"""把每日 trend CSV 导入 trends.db（SQLite）。

用法：
    python3 import_csv.py ai-trends-2026-10-01.csv
    python3 import_csv.py csv/*.csv

- 同一个 CSV 重复导入不会产生重复行（按 url + scan_date 去重）
- 每天一条 reel 存一行，scan_date 是时间维度，天然形成时间序列
"""
import csv
import sqlite3
import sys
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "trends.db")
SCHEMA = os.path.join(BASE, "schema.sql")

COLS = ["scan_date", "niche", "rank", "url", "author", "likes", "comments",
        "likes_gained_since_last", "velocity_per_day", "velocity_confidence",
        "days_tracked", "first_seen_date", "posted_date", "recency_days",
        "is_fresh", "title", "description", "mechanic", "replicable",
        "niche_fit", "angle_idea", "format_cluster", "spread_count",
        "feasible", "feasible_note", "saturated", "saturation_reason",
        "geo_fit", "geo_note", "picked_for_tomorrow"]

INTS = {"likes", "spread_count", "recency_days", "rank"}
REALS = {"velocity_per_day"}
BOOLS = {"replicable", "feasible", "is_fresh", "saturated"}


def convert(col, val):
    v = (val or "").strip()
    if col in BOOLS:
        return 1 if v.lower() == "true" else 0
    if col in INTS:
        try:
            return int(float(v))
        except ValueError:
            return None
    if col in REALS:
        try:
            return float(v)
        except ValueError:
            return None
    return v or None


def main(paths):
    if not paths:
        print("用法: python3 import_csv.py <csv文件> [更多csv...]")
        sys.exit(1)
    con = sqlite3.connect(DB)
    con.executescript(open(SCHEMA, encoding="utf-8").read())
    total_new = 0
    for path in paths:
        new = 0
        with open(path, encoding="utf-8-sig") as fh:
            for row in csv.DictReader(fh):
                vals = [convert(c, row.get(c, "")) for c in COLS]
                cur = con.execute(
                    f"INSERT OR IGNORE INTO reels VALUES ({','.join('?' * len(COLS))})",
                    vals,
                )
                new += cur.rowcount
        print(f"{os.path.basename(path)}: 新增 {new} 行")
        total_new += new
    con.commit()
    count = con.execute("SELECT COUNT(*) FROM reels").fetchone()[0]
    print(f"库中总行数: {count}（本次新增 {total_new}）")
    con.close()


if __name__ == "__main__":
    main(sys.argv[1:])
