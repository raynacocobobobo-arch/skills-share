# KnightRunner 跑酷排障复盘要点

适用：GDevelop 5 JSON 直改横版跑酷，尤其是 KnightHorse / NewSprite12 / ObstacleHitbox / ScoreText / go / re 这类结构。

## 本次踩坑

1. **视觉木桩不能参与 GameOver 碰撞**
   - 错误做法：同时添加 `KnightHorse collision ObstacleHitbox` 和 `KnightHorse collision NewSprite12` 作为双保险。
   - 后果：玩家跳过了用户调好的 `ObstacleHitbox`，但仍被 `NewSprite12` 的视觉 Sprite 默认碰撞框误杀。
   - 正确做法：GameOver 只看 `ObstacleHitbox`。`NewSprite12` 只负责显示、移动、删除。

2. **不要覆盖用户在 GUI 里调过的碰撞体**
   - 用户手动修碰撞体后，Agent 再用 JSON 改 mask/x/y 会把用户修正覆盖掉。
   - 改事件前先 Cmd+S 或读取更新后的 `.autosave`，保留用户 GUI 改动。

3. **`re` 对象定义 ≠ 场景里有 `re` 按钮**
   - `re in objects=True` 只表示对象资源存在。
   - `re in instances=False` 表示场景初始没有实例；如果依赖 GameOver 时 `Create re`，运行时创建不生效就看不到按钮。
   - 稳定方案：初始场景预置 `go/re` 实例在屏幕外；GameOver 移入屏幕，Retry 移出屏幕。

4. **分数需求要严格执行“每过一个木桩 +100”**
   - 禁止为了让分数可见临时改成 `TimeDelta()*60`。
   - 用 `ObstacleHitbox.X() < KnightHorse.X() - 100` 后 `Score += 100`，随后 delete 该 hitbox，保证每个木桩只加一次。

## 最小 debug 顺序

1. 先确认当前预览实际打开的项目路径。
2. Cmd+S 保存用户 GUI 改动；比较 `.json` 和 `.autosave`，优先使用最新解析成功文件。
3. 只检查并修一个问题：
   - 误杀：删 `KnightHorse collision NewSprite12 -> GameOver`。
   - 看不到 re：改预置实例，不先改 Retry 逻辑。
   - 分数不加：只查 `Score +=100` 与 hitbox 通过事件，不改速度/跳跃。
4. 写入 formal + autosave 后回读 JSON 结构，但汇报时必须说“待用户预览验证”，不要声称运行成功。
