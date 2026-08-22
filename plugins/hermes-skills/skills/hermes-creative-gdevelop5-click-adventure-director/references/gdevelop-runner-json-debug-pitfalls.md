# GDevelop 跑酷 JSON 直改排障：跳跃 / 分数 / Retry 失效

适用：直接修改 GDevelop 项目 JSON 后，用户反馈“不能跳了 / 分数没有 / Retry 不行 / Game Over 没反应”。

## 本次沉淀的硬教训

1. **不要把聊天里描述的 GDevelop 事件名直接当 JSON 内部名写入。**
   - `MouseButtonFromTextReleased`、`KeyFromTextReleased`、`PlatformBehavior::SetCanJump`、`PlatformBehavior::SimulateJumpKey` 等必须先用同版本 GDevelop 导出的真实事件验证。
   - 只在 app.asar 里搜到字符串，不等于 JSON 事件能这样写并被编辑器/运行时正确编译。

2. **不要为了二段跳贸然关闭默认平台控制。**
   - 如果把 `KnightHorse.PlatformerObject.ignoreDefaultControls=true`，但自定义跳跃事件写错，结果就是完全不能跳。
   - 跑酷原型救火优先：恢复 `ignoreDefaultControls=false`，保留 `maxSpeed=0` 防止左右移动，再用平台行为字段/GUI配置实现双跳。

3. **分数和 Retry 排障时先做“肉眼可见的保底版”。**
   - 分数先无条件每帧增长：`Score += TimeDelta() * 60`。
   - `ScoreText` 设为醒目：黄色/大字号/高 `zOrder`，先排除“事件执行了但看不见”。
   - Retry 先做无条件触发：鼠标左键释放或 R 键直接重置，确认重置动作本身可用；再逐步加回 `GameOver=1` 条件。

4. **Retry 不要依赖透明贴图或对象命中做第一版判定。**
   - `SourisSurObjet(re)` 容易因为透明区/碰撞遮罩/层级导致点不到。
   - 稳定路线：GameOver 后左键释放全屏重置，或做独立透明按钮热区，不用 re 图片本身当按钮。

5. **GameOver 碰撞用双保险。**
   - 如果使用独立 `ObstacleHitbox`，碰撞事件应以 `KnightHorse` vs `ObstacleHitbox` 为主。
   - 排障期可再加一条 `KnightHorse` vs `NewSprite12`，避免 hitbox 生成/移动/删除链路失效导致 GameOver 不触发。

5. **清理事件表时，用户已确认可用的“重复事件”不要按代码洁癖删。**
   - 本项目二段跳曾依赖两套兼容键盘参数：`KeyPressed ['Space']` 和 `KeyPressed ['', 'Space']`。
   - 删除“看起来重复”的 `['', 'Space']` 后，用户反馈二段跳坏了；恢复后才正常。
   - 结论：GDevelop JSON 清理必须以用户预览验证为准；事件表可读性让位于运行有效性。要清理重复事件，先复制备份、只删一组、让用户预览确认，再继续。

6. **Retry 清理要二选一：ChangeScene 或硬重置，不能叠加。**
   - `GameOver=1 + MouseButtonReleased Left + SourisSurObjet(re) -> ChangeScene 当前场景` 是干净方案。
   - 如果 Retry 事件里既有 `Score=0/RunSpeed=6/Delete obstacles/ResetTimer/Text` 又有 `ChangeScene`，这是历史屎山，应清掉硬重置动作，只保留 ChangeScene，除非用户明确要原地硬重置。
   - `RetryDelayTimer` 若不参与 Retry 条件，应从开局/GameOver/Retry 事件中删除。

## 推荐救火顺序

1. 关闭 GDevelop，备份正式 JSON 和 `.autosave`。
2. 恢复跳跃：`ignoreDefaultControls=false`，`maxSpeed=0`，不要写任何 `SetY/SetXY`。
3. 把 `ScoreText` 调到可见：`x=30,y=20,zOrder=9999`，对象文本黄字大号。
4. 分数事件先无条件：`Score += TimeDelta() * 60`，`ScoreText = "Score: " + ToString(Round(GlobalVariable(Score)))`。
5. Retry 事件先无条件：`MouseButtonReleased(Left)` / `KeyReleased(r)` → 执行完整 reset actions。
6. GameOver 碰撞加双保险：`ObstacleHitbox` 和 `NewSprite12` 两条 collision。
7. 同步写入 `.autosave`，重新打开项目路径，并回读正式/autosave SHA。
8. 用户确认基本可用后，再收窄：Retry 加回 `GameOver=1`，分数加回 GameOver 门控。

## 回报口径

如果用户已经反馈“不行”，不要继续说“我验证通过”。应承认：

- “我验证的是 JSON 结构，不等于运行时有效。”
- “先改成保底可见版，确认分数/Retry链路能动，再收窄逻辑。”

汇报只给用户可测试结果、备份路径和现在要测的最小点，不展开长篇解释。