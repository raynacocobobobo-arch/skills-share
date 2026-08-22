# GDevelop 5 新手 GUI 操作速查

用于用户在 GDevelop 里实际点击制作时。用户要的是“点哪里、选什么、填什么”，不要只讲概念。

## 回答方式

- 按当前界面一步步说：先找哪个面板，再点哪个按钮，再填什么名字。
- 每次只推进一个小步骤；用户完成后再给下一步。
- 如果用户说“没搞懂”，立刻拆成更细步骤，并列出 2～3 个常见卡点让用户选。
- 不要一上来给完整长教程；除非用户明确要完整流程。

## 从零做点触冒险最小闭环的点击路径

### 1. 新建项目
1. 首页点 `Create a new project`
2. 选 `Empty game`
3. 项目名：`ClickAdventureDemo`
4. 点 `Create`

### 2. 新建场景
1. 左侧 `Scenes` 点 `+`
2. 场景名：`S1_CastleSquare`
3. 双击打开场景

### 3. 添加背景 Sprite
1. 找 `Objects` 面板
2. 点 `Click to add an object` / `+`
3. 选 `Sprite`
4. 名字：`OBJ_BG_CastleSquare`
5. 进入 Sprite 编辑器后点 `Add an animation` → `Add sprite` / `Add image`
6. 选择背景 PNG/JPG
7. 回到场景，把 `OBJ_BG_CastleSquare` 从 Objects 列表拖到画布
8. 选中背景实例，设置 `X=0`、`Y=0`、`Z Order=0`

常见卡点：
- 找不到 `Click to add an object`：让用户找 Objects 面板或右侧/左侧的 `+`。
- 创建了 Sprite 但没图：双击对象重新进 Sprite 编辑器，加图片。
- 没有背景图：可以先跳过背景，用白底继续搭逻辑。

### 4. 添加主角
1. `Objects` → `Click to add an object` → `Sprite`
2. 名字：`OBJ_Player`
3. `Add an animation` → `Add sprite`，加主角 PNG
4. 从 Objects 列表拖到画面下方中间
5. 选中实例，设置大概 `X=500`、`Y=500`、`Z Order=10`
6. 双击 `OBJ_Player` → `Behaviors` → `Add a behavior` → 搜 `Tween` → 添加

### 5. PNG/GIF 资源规则
- GDevelop 支持 PNG，且 PNG 是主角、道具、UI 图标最推荐格式。
- 添加 PNG 要在 Sprite 对象编辑器里：双击对象 → Animation → Add sprite/Add image；不是直接把图片拖到场景里。
- 文件名建议英文、数字、下划线：`player_idle.png`，避免中文、空格、括号。
- 主角/道具图片建议先压到 256×256 或 512×512；背景可用 1920×1080。
- GIF 不建议直接当 Sprite 动画。更稳做法：把 GIF 拆成 PNG 帧，再在同一个 Animation 里 `Add multiple sprites/images`。
- 第一版可只用 GIF 第一帧导出的 PNG 做静态占位，先跑通逻辑。

### 6. 添加钥匙、背包图标、门、出口
- 钥匙：Sprite `OBJ_Item_Key`，放场景里，`Z Order=20`
- 背包钥匙：Sprite `UI_ItemIcon_Key`，放底部 UI 区，`Z Order=100`，开局隐藏
- 门：Sprite `OBJ_Hotspot_Door`，放右侧/目标位置，`Z Order=15`
- 出口：Sprite `OBJ_Exit_NextScene`，放门后/右侧，开局隐藏，`Z Order=30`

### 7. 事件表最小闭环

事件顺序：初始化 → 拾取钥匙 → 选中背包钥匙 → 用钥匙点门 → 点出口切场景。

- 初始化：条件 `At the beginning of the scene`；动作隐藏 `UI_ItemIcon_Key`、隐藏 `OBJ_Exit_NextScene`、设置 `G_HasKey=false`、`G_SelectedItem="None"`、`S_DoorOpen=false`。
- 拾取钥匙：条件左键点击 + cursor/touch on `OBJ_Item_Key`；动作隐藏场景钥匙、显示背包钥匙、`G_HasKey=true`。
- 选中钥匙：条件左键点击 + cursor/touch on `UI_ItemIcon_Key`；动作 `G_SelectedItem="Key"`，可把图标 scale 设为 1.2。
- 用钥匙点门：条件左键点击 + cursor/touch on `OBJ_Hotspot_Door` + `G_SelectedItem="Key"`；动作 `S_DoorOpen=true`、显示出口、`G_SelectedItem="None"`、钥匙图标 scale 还原 1。
- 切场景：先建 `S2_ForestEntrance`；条件左键点击 + cursor/touch on `OBJ_Exit_NextScene` + `S_DoorOpen=true`；动作 `Change the scene` 到 `S2_ForestEntrance`。

## 重要沟通约定

当用户在软件操作中卡住时，优先让用户发截图/拍屏，然后只指下一下该点哪里。不要一次性塞完整制作理论。