# GDevelop 5 项目 JSON 直改与点击冒险/跑酷原型排障

适用：GDevelop GUI 自动化不稳定、用户允许接管项目，或需要批量调整对象/行为/事件时。优先备份和回读验证，不要盲点界面。

## 安全流程

1. 如果 GDevelop 窗口标题有 `*`，先保存：`Cmd+S`。
2. 写文件前关闭 GDevelop，避免编辑器内存里的旧状态覆盖 JSON。
3. 备份当前 `.json`：`<project>.json.bak_<purpose>_<timestamp>`。
4. 读取并修改项目 JSON。
5. 回读验证对象、实例、行为、事件。
6. 再重新打开 GDevelop。

## 常见 JSON 结构

- 项目文件：`/Users/rayna/Documents/GDevelop projects/.../*.json`
- 场景：`data["layouts"][0]`
- 场景对象定义：`layout["objects"]`
- 场景实例：`layout["instances"]`
- 场景事件：`layout["events"]`
- 资源：`data["resources"]["resources"]`

对象定义是资源/行为；实例才有 `x/y/width/height/zOrder/opacity`。

## Chrome Dino 骑士骑马版最小原型规则

目标只做：骑士固定 X + 地面无限滚动。

对象：
- `KnightHorse`：骑士骑马 Sprite。
- `Ground_A` / `Ground_B`：视觉地面，只滚动，不添加 Platform 行为。
- `Ground_Physics`：不可见物理地面，只碰撞，固定不动，不滚动。

行为：
- `KnightHorse` 添加 `PlatformBehavior::PlatformerObjectBehavior`。
- 如果要用空格跳跃，`ignoreDefaultControls=false`；同时 `maxSpeed=0`，再用事件固定 X，这样左右不会跑。
- `jumpSpeed=700`，`gravity=1400`。
- `Ground_Physics` 添加 `PlatformBehavior::PlatformBehavior`，`platformType=NormalPlatform`。

事件原则：
- 允许：固定 `KnightHorse` X。
- 禁止：任何 `SetY` / `SetXY` / `MettreY` / `MettreXY` / `Y()` 动作或条件来锁角色 Y。
- 视觉地面 `Ground_A/B` 只改 X。
- `Ground_Physics` 不移动。

事件示例（GDevelop 原生指令名可能是法语内部 ID）：
- 固定骑士 X：`MettreX` 参数 `['KnightHorse', '=', '200']`
- 地面滚动：`MettreX` 参数 `['Ground_A', '-', '6']`、`['Ground_B', '-', '6']`
- 循环条件：`PosX` 参数 `['Ground_A', '<', '-1280']`
- 循环动作：`MettreX` 参数 `['Ground_A', '=', 'Ground_B.X() + 1280']`

## 地面图层坑

不要为了视觉地面和碰撞对齐，把 `Ground_A/B` 高度压成 40 或 120；这会把背景/地面图层压扁。

正确拆法：
- `Ground_A/B` 保持原图比例和合适视觉高度（例如用户原实例 `1280×642`）。
- `Ground_Physics` 单独设置为 `1280×40`、`Y≈600`、`opacity=0`。
- 骑士浮空/下陷时，调整 `Ground_Physics.y` 或碰撞盒，不要写 `Set KnightHorse Y`。

## 跑酷背景视差循环层

当用户新增整张背景/山体图（如 `Mount1`）并希望“骑士运动时背景也动但慢一点、循环播放”时，按视觉层处理，不加碰撞行为、不改角色 Y：

1. 先保存并关闭 GDevelop，再备份 `.json`。
2. 回读对象名、实例数量、图片原始尺寸；不要只按用户口头大小写猜对象名（例如用户说 `mount1`，JSON 里可能是 `Mount1`）。
3. 双实例循环推荐：两张同对象实例相隔一张图宽，例如图片宽 `W=3200`，初始 `X≈0` 和 `X≈3200`。
4. 速度用地面速度的 1/3～1/4 做视差：地面 `-6/帧` 时，远山可用 `-2/帧`。
5. 事件写法：
   - 无条件：`MettreX` 参数 `['Mount1', '-', '2']`。
   - 条件：`PosX` 参数 `['Mount1', '<', '-3200']`。
   - 回环动作优先用相对移动：`MettreX` 参数 `['Mount1', '+', '6400']`，即 `2*W`。
6. 避免用 `Mount1.X() + 6400` 这类表达式给同名双实例回环；同名对象实例可能有取值歧义。`PosX` 条件会选中离屏实例，随后 `X += 2*W` 更稳。
7. 回读验证：只新增/保留一个背景滚动事件和一个背景回环事件；`BAD_Y_EVENTS []`；地面事件和 `Ground_Physics` 不变；最后重新打开 GDevelop。

## PNG 白边/毛边处理

AI 生成 PNG 的白边可能不是半透明白边，而是不透明近白像素贴着透明区。处理流程：
1. 备份原始 PNG。
2. 检测 alpha 透明区附近 3–5 px 的近白像素：读取 RGBA，统计 `alpha<10` 的透明区，使用 `ImageFilter.MaxFilter(5)` 扩张透明区，再统计贴边近白像素。
3. 只对贴近透明区的白色污染动手，避免伤主体：例如 `r/g/b > 212` 且低饱和（`max-min < 35`）直接透明；较弱灰白边缘可降 alpha。
4. 生成 `_clean.png`，不覆盖原图。
5. 替换 GDevelop 中对应视觉对象动画 sprite 的 `image` 字段，并在 `resources.resources` 里追加 clean 图资源，建议 `kind='image'`、`smoothed=false`、`userAdded=true`。
6. 回读验证所有目标对象都指向 `_clean.png`，并验证文件存在、资源已注册。

### 跑酷原型里的地面图白边

地面视觉层和物理碰撞层分开处理：
- `Ground_A / Ground_B` 是视觉滚动层，白边修复后可切到 `1213123223_clean.png` 这类 clean 图。
- `Ground_Physics` 是透明固定碰撞层，不负责显示；除非需要统一资源，否则不必替换它的图片。
- 不要为了清白边改变 `Ground_A/B` 的实例尺寸、Y 坐标、滚动事件或 `Ground_Physics` 参数。
- 替换后必须再次验证：`Ground_A/B` 引用 clean 图；`Ground_Physics` 仍固定不动；`BAD_Y_EVENTS []`；GDevelop 重新打开。

## 跑酷障碍 / 分数 / Game Over 系统

给横版自动跑酷原型加障碍时，按“视觉移动 + Sprite 碰撞 + 状态门控”处理，不要给障碍加 Platformer/Physics。

**硬约束：不要把“JSON 里存在事件”当成功。分数、Retry、GameOver、音乐这类基础功能必须用 GDevelop 事件表里实际可见、且用户已手动验证/预览确认能运行的动作格式；如果用户反馈预览不生效，先判定为事件内部 ID/参数格式或 autosave/打开路径问题，不要继续堆新事件。修复时优先保留最近用户确认可运行的部分，再做最小增量：一次只改一个功能，写入 formal+autosave，重新打开并让用户验证。用户只是转述外部建议/让分析时，不得自动重构事件系统；“重构成稳定版”必须等用户明确下令。任何跑酷修改都禁止新增或改写 `KnightHorse` 的 `MettreY` / `SetY` / `SetXY`，即使是开局重置也不允许。**

**屎山清理 / 用户已验证模块保护：**
- 用户说“我做好了/这个能用了/不要再碰”时，该模块进入保护态。后续清理 JSON 只能删明确历史残留，不能重写该模块的条件、动作或结构。
- 清理前必须先 `Cmd+S` 保存 GUI 最新改动，然后在正式 `.json` 与 `.autosave` 中选择最新可解析文件为底稿；清理后同步写回两者。若正式与 autosave 不一致，不要盲目用旧正式文件覆盖 autosave。
- 不要把“看起来重复”的事件直接删掉。GDevelop 同一功能可能需要两套兼容参数（例如 `KeyPressed ['Space']` 与 `KeyPressed ['', 'Space']`）；如果用户已验证功能可用，清理重复事件前必须先判断哪套实际生效，不能凭 JSON 美观删除。
- Retry 最终若采用 `GameOver=1 + MouseButtonReleased Left + SourisSurObjet(re) -> ChangeScene 当前场景`，则不要再混入硬重置动作（`Score=0`、`RunSpeed=6`、删除障碍、ResetTimer 等）。反过来，如果采用原地硬重置，就不要再 `ChangeScene`。两套混在一起就是屎山。
- Retry 历史残留清理优先级：删除无用 `RetryDelayTimer` reset；删除开局/GameOver 中作为保险的 `Delete go/re`；保留 GameOver UI 的 `Create go/re`；保留用户手动有效的 Retry 主事件。
- 开局事件不要越堆越肥：保留 PlayMusic 与必要初始化即可；空 `JsCode`、废变量、无引用 timer 应删。移动系统应拆成世界滚动（Ground/Mount）与障碍移动（NewSprite/Hitbox）两个事件，不要混在一条里。

**分数/Retry/音乐 特别坑：**
- GDevelop JSON 中 `Text`、`MouseButtonReleased`、`KeyReleased`、`ModVarGlobal`、`RePlayMusicCanal` 等内部动作/条件名可能因版本/语言/事件来源不同而不生效；不能凭字符串存在断言运行成功。
- 音乐：用户手动验证有效的是事件表动作 `Play the music ABBB.MP3` / JSON `PlayMusic`，不要用“已注册资源”“写了 JS 兜底”“写了 RePlayMusicCanal”冒充已加音乐。若用户已手动加好音乐，后续修改必须保留该事件，不要替换成 bgm.aac 或其他动作名。
- Retry：用户指定并验证方向为 `GameOver = 1` + `鼠标左键松开` + `Cursor/touch is on object -> re`，动作 `Scene -> Change scene -> 当前场景(this scene)`。不要用任意点击原地重置冒充按钮 Retry。
- 分数如果用户要求“过一个木桩 +100”，禁止临时改成 TimeDelta 计分冒充可见。
- 每次改动后汇报必须区分：已回读 JSON 结构 ✅ / 已经用户预览验证 ✅。没有用户预览验证，只能说“已写入，待预览验证”。



1. **障碍对象**：如 `NewSprite12`，保持 Sprite，无 `PlatformBehavior`、无 `Physics2`。碰撞用 Sprite 默认 collision mask / collision condition。
2. **贴地高度不要把 Y 当脚底**：GDevelop 实例/创建坐标通常是对象左上角。用户说“地面 Y=600”通常是视觉脚底线，不是对象 top-left。必须根据素材透明边界和缩放后高度算：`ObstacleTopY = GroundVisualY - ObstacleVisibleHeight + 下压修正`。如果用户说“悬空，像在石子高度上”，优先把生成 Y 往下压（例如 511 → 550），不要改 `KnightHorse` 的 Y。
3. **生成节奏**：不要固定均匀节拍。推荐 `ObstacleSpawnDelay = RandomFloatInRange(0.8, 2.4)`，同屏上限 `ObstacleMaxCount = 3`。
4. **统一速度变量**：新增 `GlobalVariable(RunSpeed)`，地面和障碍都使用它：
   - `Ground_A.X -= GlobalVariable(RunSpeed)`
   - `Ground_B.X -= GlobalVariable(RunSpeed)`
   - `NewSprite12.X -= GlobalVariable(RunSpeed)`
5. **分数**：先确认用户要哪种计分。跑酷原型里用户当前偏好是“每过一个木桩 `Score += 100`”，不要默认按 `TimeDelta() * 60` 持续增长。实现方式：独立 `ObstacleHitbox` 通过 `KnightHorse.X() - 100` 后 `Score += 100`，随后删除该 hitbox，保证每个木桩只加一次。`ScoreText = "Score: " + ToString(Round(GlobalVariable(Score)))`。若用户明确要生存时间分，再用 `TimeDelta()`。
6. **平滑难度曲线**：推荐 `RunSpeed = min(8.2, 6 + sqrt(GlobalVariable(Score) / 100) * 0.22)`。初始 6，上限 8.2，避免线性爆炸。
7. **Game Over 门控**：新增场景变量 `GameOver=0`。碰撞事件：`GameOver=0` 且 `KnightHorse` collision `NewSprite12` → `GameOver=1`、`RunSpeed=0`、`ScoreText="GAME OVER  Score: " + score`。
8. **停止所有运动系统**：所有持续运动/生成/计分事件都加 `GameOver=0` 条件，包括：分数、动态速度、地面滚动、障碍生成、障碍移动、远景视差层（如 `Mount1`）。否则 Game Over 后画面还会继续动。
9. **删除离屏障碍**：`NewSprite12.X < -200` → delete。删除事件可不受 GameOver 限制，避免残留失控。
10. **碰撞体积坑**：如果用户反馈树桩/障碍“视觉不对、碰撞体积肥、跳不过、GameOver 后有重影”，不要继续用视觉 Sprite 做碰撞。改成视觉对象 + 独立隐形碰撞体：
   - 视觉对象如 `NewSprite12` 只显示、移动、删除。
   - 新增 `ObstacleHitbox` Sprite，使用透明 PNG（如 `transparent_hitbox_82x38.png`），自带合适尺寸/碰撞遮罩，和视觉对象同速移动。
   - 碰撞事件只能用 `KnightHorse` collision `ObstacleHitbox`，不要再加 `KnightHorse` collision `NewSprite12` 作为“保险”。视觉 Sprite 的默认碰撞框通常比玩家看到的大，会导致“明明跳过去了还是 GameOver”。
   - 如果用户已经在 GDevelop GUI 手动调过 `ObstacleHitbox` 碰撞体，不要再覆盖碰撞 mask / x / y；只排查事件链。改文件前先触发保存或读取最新 `.autosave`，保留用户手动修改。
   - GameOver 时同时 delete `NewSprite12` 和 `ObstacleHitbox`，避免残影/重影。
11. **GameOver UI / Retry 坑**：不要依赖不确定的 `SetOpacity` 内部指令显示 `go/re`，容易运行时不生效。更稳做法：场景初始就放 `go/re` 实例但移到屏幕外或隐藏层；GameOver 时把 `go/re` 移到屏幕内并设置 zOrder；Retry 后再移回屏幕外。只有确认 `Create go/re` 在当前项目预览中可靠时，才用动态 Create。若原图尺寸大于用户实例尺寸，先生成缩放后的 PNG（如 `ABCE_482x414.png`、`ABCE3_169x47.png`）并替换对象引用，避免运行时创建尺寸变大。
   - 回读时要区分 `re` 对象定义和场景实例：`re in objects=True` 只说明对象资源存在，`re in instances=False` 表示初始场景没有实例；动态创建不稳定时，必须改成预置实例方案。
   - Retry 事件优先做两条：点击 `re` 或 GameOver 后鼠标释放重置；R 键重试仅作测试辅助。不要把“任意时刻鼠标释放都重置”作为最终方案。
12. **障碍密度**：如果用户嫌“同屏只有一个、没挑战性”，开局 Begin event 可预填两组视觉/碰撞障碍（如 X=1000 和 X=1500），后续生成间隔可用 `RandomFloatInRange(0.6, 1.15)`，上限 `ObstacleMaxCount=3`。
13. **验证项**：回读确认 `NewSprite12 behaviors=[]`，`ObstacleHitbox` 存在且透明图尺寸正确，碰撞事件是 `CollisionNP KnightHorse ObstacleHitbox`，GameOver 事件会 create `go/re` 并 delete 障碍/碰撞体，场景无手动 `NewSprite12/ObstacleHitbox/go/re` 实例，`BAD_KNIGHT_Y_EVENTS []`。

## Autosave 合并 / 外部 JSON 替换坑

外部工具改好完整 JSON 后再由用户上传、要求替换本机项目时，按 `references/gdevelop-uploaded-json-replacement.md` 流程执行：先验证上传 JSON，备份正式文件与 `.autosave`，同时替换正式 `.json` 和 `.json.autosave`，打开后再回读确认没有被 autosave 恢复旧逻辑。

用户刚在 GDevelop 里新增对象后，如果主 `.json` 里读不到对象名，但用户确认对象已存在，必须检查同目录 `.json.autosave`：

- 路径通常是：`<project>.json.autosave`。
- 先比较主文件和 autosave 的 mtime、对象列表、事件数量。
- 如果对象只在 autosave 中，例如 `NewSprite12`，可以从 autosave 合并对象定义和对应资源到正式 `.json`。
- 合并前必须备份正式 `.json`。
- 生成型对象不要把 autosave 里的手动实例直接带入正式场景，除非用户明确要保留；跑酷障碍这类对象应由事件生成。
- 合并后回读验证：对象存在、图片资源存在、行为未误加、事件引用正确，再打开 GDevelop。

反过来也会发生：正式 `.json` 已经改对，但 GDevelop 继续恢复旧 `.json.autosave`，用户会看到“一点没改”。这时不要争辩“JSON 已写入”，要同时验证正式文件和 autosave 的关键事件；若 autosave 旧，先备份旧 autosave，再用正式 JSON 覆盖 autosave，然后用 `open ... --args <project>.json` 重新打开，并用 `pgrep -fl 'GDevelop'` 验证进程参数带了正式路径。详细流程见 `references/gdevelop-autosave-open-sync.md`。

## 汇报格式

完成后至少汇报：
- 当前场景对象与实例尺寸。
- `KnightHorse` 行为参数。
- `Ground_Physics` 是否固定不动。
- `Ground_A/B` 是否只有 X 事件。
- 是否删除/不存在所有 Set Y / SetXY 相关事件。
