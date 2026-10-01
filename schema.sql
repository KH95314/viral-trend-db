-- trends.db 建表语句（30 列，和每日 CSV 一一对应）
CREATE TABLE IF NOT EXISTS reels (
  "scan_date" TEXT,
  "niche" TEXT,
  "rank" INTEGER,
  "url" TEXT,
  "author" TEXT,
  "likes" INTEGER,
  "comments" TEXT,
  "likes_gained_since_last" TEXT,
  "velocity_per_day" REAL,
  "velocity_confidence" TEXT,
  "days_tracked" TEXT,
  "first_seen_date" TEXT,
  "posted_date" TEXT,
  "recency_days" INTEGER,
  "is_fresh" INTEGER,
  "title" TEXT,
  "description" TEXT,
  "mechanic" TEXT,
  "replicable" INTEGER,
  "niche_fit" TEXT,
  "angle_idea" TEXT,
  "format_cluster" TEXT,
  "spread_count" INTEGER,
  "feasible" INTEGER,
  "feasible_note" TEXT,
  "saturated" INTEGER,
  "saturation_reason" TEXT,
  "geo_fit" TEXT,
  "geo_note" TEXT,
  "picked_for_tomorrow" TEXT
);
-- 同一条 reel 同一天只存一行，重复导入自动跳过
CREATE UNIQUE INDEX IF NOT EXISTS idx_url_scan ON reels(url, scan_date);
-- 常用查询加速
CREATE INDEX IF NOT EXISTS idx_niche_scan ON reels(niche, scan_date);
