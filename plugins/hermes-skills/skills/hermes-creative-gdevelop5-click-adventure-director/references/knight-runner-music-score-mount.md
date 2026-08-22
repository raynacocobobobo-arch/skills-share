# KnightRunner：音乐、计分、山背景无缝循环修复笔记

适用：GDevelop 5 跑酷项目中，用户反馈“二段跳好了，但评分/音乐/山背景循环有问题”。

## 1. 背景音乐：不要做成对象，直接事件播放

用户明确偏好：背景音乐不要做成场景对象。处理顺序：

1. 将音乐文件复制到项目目录（例如 `ABBB.MP3`）。
2. 在 `data["resources"]["resources"]` 注册音频资源：
   - `kind: "audio"`
   - `name/file: "ABBB.MP3"`
   - `preloadAsMusic: true`
   - `preloadInCache: true`
3. 在事件表添加“场景开始时播放音乐到频道”的原生动作。

本项目验证过的事件动作可双写以兼容不同内部 ID：

```json
{
  "type": "BuiltinCommonInstructions::Standard",
  "conditions": [{"type": {"value": "DepartScene"}, "parameters": [""]}],
  "actions": [
    {"type": {"value": "RePlayMusicCanal"}, "parameters": ["ABBB.MP3", "1", "true", "45", "1"]},
    {"type": {"value": "PlayMusicOnChannel"}, "parameters": ["ABBB.MP3", "1", "true", "45", "1"]}
  ]
}
```

### 自动播放坑

预览/网页端可能因为浏览器自动播放策略，场景开始事件被拦。可加一个非对象的 JS 兜底：首次点击或空格后在同一频道播放音乐。

```js
const input = runtimeScene.getGame().getInputManager();
const left = input.isMouseButtonPressed(0);
const space = input.isKeyPressed(32);
if ((left || space) && !runtimeScene.getVariables().get('ABBBMusicStarted').getAsBoolean()) {
  runtimeScene.getVariables().get('ABBBMusicStarted').setBoolean(true);
  gdjs.evtTools.sound.playMusicOnChannel(runtimeScene, "ABBB.MP3", 1, true, 45, 1);
}
```

注意：这只是解锁兜底，不是把音乐做成对象。

## 2. 计分：不要靠删除 ObstacleHitbox 来“只加一次”

旧做法：`ObstacleHitbox.X() < KnightHorse.X() - 20` 后 `Score += 100` 并删除该 hitbox。

问题：删除 hitbox 会让视觉木桩、碰撞、离屏删除、GameOver 之间失配，导致计分/碰撞互相打架。

更稳做法：给每个 `ObstacleHitbox` 用对象变量 `Scored` 标记，只加一次分；hitbox 继续存在，直到常规离屏删除或 GameOver 删除。

```js
if (runtimeScene.getVariables().get('GameOver').getAsNumber() === 0) {
  const horses = runtimeScene.getObjects('KnightHorse');
  const horseX = horses.length ? horses[0].getX() : 297;
  const scoreVar = runtimeScene.getGame().getVariables().get('Score');
  let score = scoreVar.getAsNumber();
  for (const h of runtimeScene.getObjects('ObstacleHitbox')) {
    const v = h.getVariables().get('Scored');
    if (v.getAsNumber() !== 1 && h.getX() < horseX - 20) {
      v.setNumber(1);
      score += 100;
    }
  }
  scoreVar.setNumber(score);
  for (const t of runtimeScene.getObjects('ScoreText')) {
    if (t.setString) t.setString('Score: ' + Math.round(score));
    else if (t.setText) t.setText('Score: ' + Math.round(score));
  }
}
```

## 3. 山背景无缝循环

如果图片宽度是 3200，两张 `Mount1` 初始位置必须精确：

```text
Mount1 #1 X = 0
Mount1 #2 X = 3200
```

不要用 `1 / 3202` 这类位置，会天然露 1–2 px 缝。

GDevelop 同名对象用表达式回环可能有取值歧义。稳妥做法是 JS 按 X 排序、整数吸附、超过一张图宽后放到最右边：

```js
const W = 3200;
const mounts = runtimeScene.getObjects('Mount1').sort((a, b) => a.getX() - b.getX());
if (mounts.length >= 2) {
  for (const m of mounts) m.setX(Math.round(m.getX()));
  const sorted = runtimeScene.getObjects('Mount1').sort((a, b) => a.getX() - b.getX());
  const left = sorted[0];
  const right = sorted[sorted.length - 1];
  if (left.getX() <= -W) left.setX(right.getX() + W);
  const again = runtimeScene.getObjects('Mount1').sort((a, b) => a.getX() - b.getX());
  if (again.length >= 2 && Math.abs((again[0].getX() + W) - again[1].getX()) > 1) {
    again[1].setX(again[0].getX() + W);
  }
}
```

## 4. 验证注意：别误报视觉木桩 GameOver

检查“是否还存在 KnightHorse 碰 NewSprite12 触发 GameOver”时，只看事件 **conditions** 里的 `CollisionNP` 参数。

GameOver 动作里出现 `Delete NewSprite12` 是正常清场，不代表视觉木桩参与碰撞。不要用整条事件字符串包含 `NewSprite12` 就误判。

正确检查：

- 坏：conditions 中 `CollisionNP` 参数是 `KnightHorse, NewSprite12`。
- 好：conditions 中 `CollisionNP` 参数是 `KnightHorse, ObstacleHitbox`，actions 中可以删除 `NewSprite12` 和 `ObstacleHitbox`。