# 导入列表质量过滤：章节/解释句不要进待办

## 触发场景
用户粘贴攻略、长文、旅行清单、药品清单等混合内容时，AI 可能把章节标题或说明句误识别为待办，例如：
- “第五部分”
- “欧洲药店买药非常麻烦”
- “为什么要准备这些”
- “注意事项 / 说明 / 总结”

这些内容不是可勾选事项，不能创建成 TaskItem。

## 规则
1. AI prompt 层明确约束：
   - 章节标题/解释句/原因句不要变成 suggestions。
   - 只有可勾选的动作、物品、药品、证件、地点、预约事项才进入 suggestions。
   - 解释性内容只能作为 category/note，或直接忽略。
2. 代码层二次过滤，不能只靠 prompt：
   - `handleAIResult` 解析 AI suggestions 后，创建 `AISuggestion` 前调用过滤函数。
   - `localParseImportedList` 本地兜底也必须调用相同过滤逻辑。
3. 本地兜底遇到短章节标题时：
   - 可更新 `currentCategory`；
   - 但不要 append 成待办。

## 推荐实现形态
```swift
private func isChapterOrExplanationLine(_ text: String) -> Bool {
    let x = text.trimmingCharacters(in: .whitespacesAndNewlines)
    guard !x.isEmpty else { return true }
    if x.range(of: #"^第[一二三四五六七八九十0-9]+[章节部分篇]"#, options: .regularExpression) != nil { return true }
    if x.range(of: #"^[一二三四五六七八九十0-9]+[、.．)）\s]*[章节部分篇]"#, options: .regularExpression) != nil { return true }
    let explanationWords = ["为什么", "为何", "原因", "因为", "所以", "注意", "提醒", "说明", "攻略", "总结", "麻烦", "不方便", "很难", "比较难", "别进去", "不要进去", "什么"]
    if explanationWords.contains(where: { x.contains($0) }) { return true }
    return false
}

private func isImportableTodoTitle(_ title: String) -> Bool {
    let x = title.trimmingCharacters(in: .whitespacesAndNewlines)
    guard x.count >= 2 else { return false }
    if isChapterOrExplanationLine(x) { return false }
    let badTitles = ["前言", "引言", "目录", "结论", "总结", "备注", "说明", "注意事项"]
    if badTitles.contains(where: { x == $0 || x.contains($0) }) { return false }
    return true
}
```

## 验证
- 编译通过后必须覆盖安装到真机，不能只 build。
- 导入测试文本中包含章节标题和解释句时，情境里不应出现这些任务，只保留真正可勾选事项。