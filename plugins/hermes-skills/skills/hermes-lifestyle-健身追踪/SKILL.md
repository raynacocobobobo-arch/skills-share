---
name: 健身追踪
description: 个人健身追踪，记录运动自动计算卡路里消耗，包含完整训练计划、减脂目标跟踪
version: 13.0.0
triggers:
  - 健身
  - 运动
  - 跑步
  - 消耗
  - 卡路里
  - 体重
  - 今天练什么
  - 做了
  - 练了
  - 游泳
  - 椭圆机
  - 仰卧起坐
migrated_from: OpenClaw Custis Ordo v13
---

# Fitness Tracker - 健身追踪

## 用户档案
- **体重**: 65.6kg
- **可用场地**: 游泳馆、健身房、居家
- **偏好**: ⚠️ 不喜欢膝盖负荷大的动作（深蹲幅度小，膝盖不超过脚尖太多）

## 可用器材

### 游泳馆
- 蛙泳

### 健身房
- 椭圆机（有氧，膝盖友好）
- Dip/Chin Assist（引体向上，65kg 配重，**5 秒/次**）
- Chest Press Vertical（推胸/划船，12kg 配重，**3 秒/次**）
- Lat Machine（拉背，25kg 配重，**3 秒/次**）

### 居家
- 3kg 杠铃
- 臀桥（自重）
- 平板支撑（自重）
- 侧卧抬腿（自重）
- 原地高抬腿（自重）
- **靠墙静蹲（自重，膝盖康复）**

## 训练计划（每周循环）

### 周一 | 游泳馆 | 消耗：~350 卡
- 蛙泳：1000-1250 米

### 周二 | 健身房 | 消耗：~450 卡
- 椭圆机：30 分钟
- 推胸 (Chest Press)：4 组×12 次 @ 12kg
- 拉背 (Lat Machine)：4 组×12 次 @ 25kg
- 引体向上 (Chin Assist)：4 组×12 次 @ 65kg

### 周三 | 家 | 消耗：~120 卡
- 3kg 杠铃弯举：4 组×15 次
- 3kg 杠铃推举：4 组×15 次
- 臀桥：4 组×15 次
- 平板支撑：4 组×45 秒
- 仰卧起坐：4 组×15 次

### 周四 | 游泳馆 | 消耗：~350 卡
- 蛙泳：1000-1250 米

### 周五 | 健身房 | 消耗：~400 卡
- 椭圆机：30 分钟
- 推胸 (Chest Press)：4 组×12 次 @ 12kg
- 拉背 (Lat Machine)：4 组×12 次 @ 25kg
- 引体向上 (Chin Assist)：4 组×12 次 @ 65kg

### 周六 | 家 | 消耗：~120 卡
- 3kg 杠铃弯举：4 组×15 次
- 3kg 杠铃推举：4 组×15 次
- 臀桥：4 组×15 次
- 平板支撑：4 组×45 秒
- 仰卧起坐：4 组×15 次

### 周日 | 家 | 消耗：0 卡
- 休息

**周总计**: 约 1790 卡

## 靠墙静蹲康复计划

针对左膝盖旧伤，4 周渐进：
- 第1周：20-30秒，3组，每天，角度45°
- 第2周：30-45秒，3组，每天，角度60°
- 第3周：45-60秒，4组，每天，角度75°
- 第4周：60秒+，4组，每天，角度90°

注意：膝盖疼就停，练完热敷10分钟，阴冷天戴护膝，别蹲太深

## Hermes 使用说明

### 记录运动
当用户说"做了XX"、"练了XX"等，使用 Python 脚本计算卡路里：

```python
# 调用统一接口
from hermes_tools import terminal

# 记录散步
result = terminal("python3 ~/.hermes/scripts/fitness.py record walking --steps 7000")

# 记录游泳
result = terminal("python3 ~/.hermes/scripts/fitness.py record swimming --stroke 蛙泳 --distance 1000")

# 记录椭圆机
result = terminal("python3 ~/.hermes/scripts/fitness.py record cardio --exercise 椭圆机 --duration 30")

# 记录仰卧起坐
result = terminal("python3 ~/.hermes/scripts/fitness.py record situps --reps 60")

# 查询
result = terminal("python3 ~/.hermes/scripts/fitness.py daily")
result = terminal("python3 ~/.hermes/scripts/fitness.py weekly")
result = terminal("python3 ~/.hermes/scripts/fitness.py weight")
```

### 解析规则
1. 提取数字（时长/次数/距离/步数）
2. 识别运动类型（椭圆机/划船/仰卧起坐/臀桥/平板支撑/散步/游泳/靠墙静蹲等）
3. 调用 `python3 ~/.hermes/scripts/fitness.py record ...` 记录
4. 输出标准格式（今日合计 + 本周累计 + 周目标进度 1500卡）

### 快速对照表

| 场景 | 版本 | 关键动作 |
|------|------|---------|
| 正常周 | 完整版 | 游泳 + 健身房 |
| 去不了健身房 | A（有器械） | 3kg 杠铃全套 |
| 去不了健身房 | B（无器械） | 俯卧撑 + 臀桥 + 靠墙静蹲 |
| 去不了游泳馆 | A 或 B | 椭圆机改原地高抬腿 |

### 卡路里计算公式

| 运动 | 公式 |
|------|------|
| 散步 | 0.04 × (体重/70) × 步数 |
| 游泳 | MET × 3.5 × kg ÷ 200 × 时间(min) |
| 有氧 | MET × 3.5 × kg ÷ 200 × 时间(min) |
| 仰卧起坐 | 0.15 × (体重/68) × 次数 |
| 器械力量 | 次数 × 0.2~0.25 cal/次 |

### 数据存储
- 运动记录：`~/.hermes/data/fitness/records.json`
- 减脂目标：`~/.hermes/data/fitness/goals.json`
- 脚本位置：`~/.hermes/scripts/fitness.py`
