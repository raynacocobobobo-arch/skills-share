# Godot 4.x 点触冒险白盒工程脚手架

适用场景：用户要做《机械迷城 / 银河历险记》式点击冒险，并希望由 Agent 直接生成可运行工程，而不是在 GDevelop GUI 里手工点配置。

## 什么时候选 Godot

优先选 Godot 而不是 GDevelop，当用户表达：
- “你不是有个 Godot 吗？”、“能不能你直接搭工程？”
- 想让 Agent 直接写文件、脚本、场景，而不是手动点 GUI。
- 目标是可持续扩展的 2D 游戏工程：场景切换、背包、热点、状态变量、导出 Mac/Windows/Web。

仍可选 HTML 原型：只想最快看到视觉交互，不追求游戏工程。

## 默认工程路径

遵循用户文件偏好：

```text
~/Desktop/hermes/游戏/<项目名>/GodotDemo/
```

本次《约定与归来》使用：

```text
~/Desktop/hermes/游戏/约定与归来/GodotDemo/
```

## Godot 版本与验证

检查版本：

```bash
/Applications/Godot.app/Contents/MacOS/Godot --version
```

生成项目后验证可加载：

```bash
/Applications/Godot.app/Contents/MacOS/Godot --headless --path <project_dir> --quit
/Applications/Godot.app/Contents/MacOS/Godot --headless --path <project_dir> --check-only --quit
```

Hermes terminal 的 workdir 可能拒绝中文路径；不要把这当成 Godot 不支持中文路径。可临时建 ASCII symlink 再验证：

```bash
ln -sfn '<project_dir>' /tmp/godot_demo
/Applications/Godot.app/Contents/MacOS/Godot --headless --path /tmp/godot_demo --quit
```

## 推荐目录结构

```text
GodotDemo/
├── project.godot
├── scenes/
│   ├── s1_01_castle_square.tscn
│   ├── s1_02_blacksmith.tscn
│   └── ...
├── scripts/
│   ├── game_state.gd
│   ├── scene_controller.gd
│   ├── hotspot.gd
│   ├── inventory.gd
│   └── player.gd
├── ui/
│   ├── inventory_bar.tscn
│   └── thought_bubble.tscn
└── assets/
    ├── placeholder/
    ├── bg/
    ├── characters/
    ├── items/
    └── fx/
```

## 第一版白盒标准

先做能跑通主线，不追美术：
- 16:9 画布，`1280x720`。
- 每个场景用 `ColorRect` + `Label` + 热点色块占位。
- 玩家角色可先用 `ColorRect` 占位。
- 每个可点击物用 `Area2D + CollisionShape2D + ColorRect + Label`。
- 背包用 `CanvasLayer + HBoxContainer + Button`。
- 状态用 Autoload 单例 `GameState`。

## Autoload GameState 模式

`project.godot` 中：

```ini
[autoload]
GameState="*res://scripts/game_state.gd"
```

`game_state.gd` 用布尔变量保存第一版状态，不要一上来做复杂存档/物品数据库：

```gdscript
extends Node

signal inventory_changed
signal selected_item_changed(item_id: String)
signal state_changed

var selected_item: String = "none"

var has_sword := false
var has_map := false
var prop_horn_repaired := false
var npc_princess_blessed := false

func select_item(item_id: String) -> void:
    selected_item = "none" if selected_item == item_id else item_id
    selected_item_changed.emit(selected_item)

func can_open_gate() -> bool:
    return has_sword and has_map and prop_horn_repaired and npc_princess_blessed
```

## 通用 Hotspot 模式

每个热点脚本导出：

```gdscript
@export var hotspot_id: String = ""
@export var label_text: String = "热点"
@export var target_scene: String = ""
@export var required_item: String = "none"
@export var one_shot: bool = false
```

点击时不要把逻辑散在每个热点脚本里，统一交给场景控制器：

```gdscript
func _on_input_event(_viewport: Node, event: InputEvent, _shape_idx: int) -> void:
    if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
        get_tree().call_group("scene_controller", "handle_hotspot", self)
```

## SceneController 模式

每个场景根节点挂 `scene_controller.gd`：
- 加入 `scene_controller` group。
- 接收 `handle_hotspot(hotspot)`。
- 根据 `hotspot_id` 执行状态修改、背包变化、反馈、场景切换。
- 失败反馈用气泡/文字/小动画，第一版可以先用底部反馈文本。

注意 Godot 4.7 GDScript 类型推断：从动态属性读取时不要写 `var id := hotspot.hotspot_id`，可能报 `Cannot infer the type`；写成：

```gdscript
var id: String = hotspot.get("hotspot_id")
```

## 常见坑

1. **脚本字符串换行**：生成 `.gd` 时如果写 `"\n"` 被 Python/脚本展开成真实换行，会导致字符串断裂。写入后必须 read 回看，确认同一行是 `"\\n"`。
2. **动态属性类型推断**：Godot 4.7 对 `:=` 推断更严格，`hotspot.hotspot_id` 这类动态脚本属性建议用显式类型 + `get()`。
3. **中文路径验证**：Hermes terminal 可能拦中文 workdir；用 `/tmp` symlink 验证，别迁移用户项目位置。
4. **第一版不要追正式美术**：先 ColorRect 白盒跑通“点击物品 → 点击目标 → 状态变化 → 解锁出口”。
5. **不要把剧情目标写成游戏目标**：目标必须是可点击完成的动作，例如“打开城门”，不是“理解世界真相”。

## 《约定与归来》第一幕白盒闭环

按总控文档 v3.2，第一幕不是简化版“羽毛→地图→守卫”，而是四条件城门：

```text
订单 → 老橡树提示
水壶 → 浇树根 → 铁匣露出
铁匣 → 没寄出的信 + 戒指
没寄出的信 → 铁匠 → 剑
铁匠解决后 → 铜漏斗
钟楼鸽巢 → 羽毛
羽毛 + 剑 → 制图师画地图 → 地图
戒指 → 公主 → 祝福
铜漏斗 → 钟楼号角 → 号角修好
剑 + 地图 + 祝福 + 号角 → 城门打开
```

第一版场景：
- `S1_01` 城堡广场 / 老橡树视野（枢纽）
- `S1_02` 铁匠铺
- `S1_03` 老橡树 / 旧驿站残迹
- `S1_04` 制图师家 / 绘图室
- `S1_05` 钟楼
- `S1_06` 公主塔楼
- `S1_07` 城门

验收：玩家能拿到剑、地图、祝福、号角并打开城门。