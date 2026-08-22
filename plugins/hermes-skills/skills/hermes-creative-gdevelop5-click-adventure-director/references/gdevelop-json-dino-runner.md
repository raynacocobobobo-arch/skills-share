# GDevelop 5 JSON 直改：Chrome Dino 骑士骑马版最小原型

适用：用户要求接管 GDevelop 5 项目，做“骑士固定位置 + 地面无限滚动”的最小可玩原型。优先保存/备份当前 `.json` 项目，再直改 JSON，最后回读验证并重启 GDevelop。

## 目标规格

- 窗口：`1280 × 720`
- 骑士对象：`KnightHorse`
- 视觉地面：`Ground_A`、`Ground_B`
- 物理地面：`Ground_Physics`
- 当前阶段只做：骑士固定 X + 视觉地面无限左滚。
- 不做：障碍、分数、Game Over、图片重生成、替换美术。

## 关键原则

1. `KnightHorse` 只固定 X，不固定 Y。
2. 禁止事件里出现 `SetY`、`SetXY`、`MettreY`、`MettreXY` 或任何 `Y()` 相关动作。
3. `Ground_A / Ground_B` 只负责视觉滚动，不加 Platform 行为。
4. `Ground_Physics` 只负责碰撞，固定不动，不参与滚动，通常 `opacity=0`。
5. 如果用户已经手动调整了画面，先保存当前 GDevelop 项目再读 JSON，避免读到旧版本。
6. 修改 JSON 前必须备份：`<project>.bak_<timestamp>`。

## 推荐对象配置

### KnightHorse

- 类型：Sprite
- 行为：`PlatformBehavior::PlatformerObjectBehavior`
- 参数：
  - `maxSpeed = 0`
  - `jumpSpeed = 700`
  - `gravity = 1400`
  - `ignoreDefaultControls = false`（如果没有手写空格跳事件，必须打开默认控制，否则空格不能跳）
- 初始实例：
  - `x ≈ 200`
  - `y` 放在地面上方，让平台行为自然落地；不要用事件锁 Y。

### Ground_Physics

- 类型：可用 Sprite 克隆已有地面素材对象，便于有碰撞盒；也可用矩形/Shape。
- 行为：`PlatformBehavior::PlatformBehavior`
- 实例建议：
  - `x = 0`
  - `y = 600`
  - `width = 1280`
  - `height = 40`
  - `opacity = 0`
  - `zOrder = -10`

### Ground_A / Ground_B

- 类型：Sprite，复用已有地面图片。
- 不要添加 Platform 行为。
- 视觉尺寸不要硬压扁：保留用户原图比例/高度。若原图实例是 `1280 × 642`，就继续用 `1280 × 642`，不要改成 `1280 × 120`。
- 常见放置：
  - `Ground_A: x=0, y=<用户调整后的视觉Y>, width=1280, height=<原视觉高度>`
  - `Ground_B: x=1280, y=<同A>, width=1280, height=<同A>`

## GDevelop JSON 事件写法（已验证识别符）

事件使用 GDevelop 原生指令标识：

```json
[
  {
    "type": "BuiltinCommonInstructions::Standard",
    "conditions": [],
    "actions": [
      {"type": {"value": "MettreX"}, "parameters": ["KnightHorse", "=", "200"]}
    ]
  },
  {
    "type": "BuiltinCommonInstructions::Standard",
    "conditions": [],
    "actions": [
      {"type": {"value": "MettreX"}, "parameters": ["Ground_A", "-", "6"]},
      {"type": {"value": "MettreX"}, "parameters": ["Ground_B", "-", "6"]}
    ]
  },
  {
    "type": "BuiltinCommonInstructions::Standard",
    "conditions": [
      {"type": {"value": "PosX"}, "parameters": ["Ground_A", "<", "-1280"]}
    ],
    "actions": [
      {"type": {"value": "MettreX"}, "parameters": ["Ground_A", "=", "Ground_B.X() + 1280"]}
    ]
  },
  {
    "type": "BuiltinCommonInstructions::Standard",
    "conditions": [
      {"type": {"value": "PosX"}, "parameters": ["Ground_B", "<", "-1280"]}
    ],
    "actions": [
      {"type": {"value": "MettreX"}, "parameters": ["Ground_B", "=", "Ground_A.X() + 1280"]}
    ]
  }
]
```

## 验证脚本要点

回读 JSON 后至少检查：

- `windowWidth/windowHeight = 1280/720`
- `KnightHorse` 行为：Platformer Character；`maxSpeed=0`；`jumpSpeed=700`；`gravity=1400`；`ignoreDefaultControls=false`（除非另有跳跃事件）
- `Ground_Physics` 有 Platform 行为，实例固定，透明。
- `Ground_A / Ground_B` 无 Platform 行为。
- 所有事件不包含：`SetY`、`SetXY`、`MettreY`、`MettreXY`、`Y()`。
- `Ground_A / Ground_B` 事件只改 X。

## 常见坑

### 1. 空格不能跳

如果 `ignoreDefaultControls=true`，但没有单独写“按 Space 模拟跳跃”事件，空格不会跳。最小原型阶段更稳的修法是：

- `ignoreDefaultControls=false`
- `maxSpeed=0`
- 保留事件 `KnightHorse X = 200`

这样空格能跳，左右速度仍为 0，Y 由重力/跳跃控制。

### 2. 地面视觉被压扁

不要把视觉地面强行改成 `1280 × 40/120`。物理碰撞层才是薄矩形；视觉层应保留原图比例和用户调整后的高度。

### 3. GDevelop 内存状态覆盖文件

如果窗口标题带 `*`，说明项目未保存。读 JSON 前先 `Cmd+S`。写 JSON 后最好关闭/重开 GDevelop，避免编辑器内存里的旧状态再次保存覆盖文件。

### 4. `SetXY` 会误锁 Y

旧项目里常见事件：`SetXY KnightHorse = 200 = 200`。必须删除/替换为只改 X 的 `MettreX KnightHorse = 200`。