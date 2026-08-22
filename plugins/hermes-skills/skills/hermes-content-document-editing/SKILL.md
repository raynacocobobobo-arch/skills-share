---
name: document-editing
description: 中文文档编辑处理——python-docx实现扒词修正（删除语气词/口头禅/错别字）和新闻通稿删改（difflib修订标记、删除线、图片处理）
triggers:
  - 扒词修正
  - 解说词修改
  - 字幕修正
  - 错别字修正
  - 语气词删除
  - 口头禅
  - 新闻通稿删改
  - 通稿删减
  - 删除线修订
  - 差异对比
  - python-docx
---

# 中文文档编辑处理

python-docx 实现两类文档处理工作流：**扒词修正**（只删不改）和**新闻通稿删改**（修订标记）。

---

## 工作流一：扒词修正（只删不改）

### 核心约束

**只能删除，不能增加或替换字词。** 音频已录制，任何添加都会导致文档与音频对不上。删除后句子需仍通顺、意思不变。

### 修正类型（按优先级）

**1. 语气词 → 删除**：呢、啊、呀、嘛、吧、嗯、哦、哈、啦、呗
```
原文：其实啊不止苏轼
修正：其实不止苏轼
```

**2. 口头禅/冗余 → 删除**：这个、那个、就是说、然后、我们的、那、那么、这种、这样、一下、来说
```
原文：那要谈到它的功效
修正：谈到它的功效
```

**3. 重复字词 → 删除多余**
```
原文：是我们能能够看得到的
修正：是我们能够看得到的
```

**4. 句尾残词/口误截断 → 截断处删除**
```
原文：今天节目的主题也是黄芪这个故
      这个故事也让黄芪这味中药
修正：今天节目的主题也是黄芪
```

**5. 孤立半句 → 整行删除**（半句后无补语，音频中断）

**6. 错别字（只删不换）**：只能判断能否删该字使句子通顺，不能换成正确字。

### 输出格式

- Word 文档（`.docx`），不用 Markdown
- 修改处加粗
- 保持源格式：一行原文一行空行
- 字体：宋体 11pt
- 同时输出变更清单

### 代码模板

```python
from docx import Document
from docx.shared import Pt

edits = [
    (line_num, "原文字符串", "修正后"),  # new=None 删除整行
]

doc = Document()
s = doc.styles['Normal']
s.font.name = '宋体'; s.font.size = Pt(11)

for i, line in enumerate(lines, start=1):
    if i in edit_map:
        old, new = edit_map[i]
        if new is None: continue  # 整行删除
        idx = line.find(old)
        p = doc.add_paragraph()
        p.add_run(line[:idx])
        r = p.add_run(new); r.bold = True
        p.add_run(line[idx+len(old):])
    else:
        if line.strip() == "":
            doc.add_paragraph()
        else:
            p = doc.add_paragraph(); p.add_run(line)
```

---

## 工作流二：新闻通稿删改（修订标记）

### 触发条件

- 要求删除线标注删除内容、红色标注修改内容
- 要求处理文档中的图片（保留/删除特定图片）
- 要求限制字数且原则为"只删不改"（仅错别字/措辞差错可改）

### 流程

**1. 读取并分析原文**
```python
from docx import Document
import re
doc = Document(path)

# 统计中文字数
chinese = len(re.findall(r'[\u4e00-\u9fff]', text))

# 识别图片位置
from docx.oxml.ns import qn
for i, para in enumerate(doc.paragraphs):
    drawings = para._element.findall('.//'+qn('w:drawing'))
    for d in drawings:
        blips = d.findall('.//'+qn('a:blip'))
        for blip in blips:
            embed = blip.get(qn('r:embed'))  # 如 rId6
```

**2. 制定删减方案**
- 优先删重复段落（保留信息更完整的）
- 大幅精简技术细节（保留核心结论）
- 删除美化/极端词汇：重磅、权威、最强、极致、卓越、升维、跨越式、全新、行业领先等
- 方案存储为 JSON：`{"P0": "精简后文本", "P2": null}` — null 表示整段删除
- **目标字数预留 ~20 字 buffer**：difflib 可能产生偏差

**3. 仅修正实时性差错**："很好地体现"（的→地）、明显错别字

**4. 生成带修订痕迹的 docx**——difflib.SequenceMatcher 对比原文和精简文本，重建段落 runs：

```python
from difflib import SequenceMatcher
from docx.oxml import OxmlElement
from docx.shared import RGBColor

def add_strikethrough(run):
    rPr = run._element.get_or_add_rPr()
    strike = OxmlElement('w:strike')
    strike.set(qn('w:val'), 'true')
    rPr.append(strike)

def set_red(run):
    run.font.color.rgb = RGBColor(0xCC, 0x00, 0x00)

def get_run_font_info(para):
    if para.runs:
        r = para.runs[0]
        return {
            'name': r.font.name, 'size': r.font.size,
            'bold': r.font.bold,
            'color': r.font.color.rgb if r.font.color and r.font.color.rgb else None,
        }
    return {'name': '宋体', 'size': None, 'bold': None, 'color': None}

def apply_font(run, font_info):
    if font_info['name']: run.font.name = font_info['name']
    if font_info['size']: run.font.size = font_info['size']
    if font_info['bold'] is not None: run.font.bold = font_info['bold']

def rebuild_paragraph(para, old_text, new_text):
    """重建段落：删除文字→删除线，修改文字→原字删除线+新字红色"""
    font_info = get_run_font_info(para)
    # 清除所有 run 元素
    for child in list(para._element):
        if child.tag == qn('w:r'):
            para._element.remove(child)

    matcher = SequenceMatcher(None, old_text, new_text)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            run = para.add_run(old_text[i1:i2])
        elif tag == 'delete':
            run = para.add_run(old_text[i1:i2])
            add_strikethrough(run)
        elif tag == 'replace':
            run1 = para.add_run(old_text[i1:i2])
            add_strikethrough(run1)
            run2 = para.add_run(new_text[j1:j2])
            set_red(run2)
        elif tag == 'insert':
            run = para.add_run(new_text[j1:j2])
            set_red(run)
        apply_font(run, font_info)
```

**5. 图片处理**
```python
# 删除图片
drawings = para._element.findall('.//'+qn('w:drawing'))
for d in drawings:
    d.getparent().remove(d)

# 标记删除（仅纯图片空段落）
if not para.text.strip():
    run = para.add_run('[图片已删除]')
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x99, 0x99, 0x99)
```

**6. 验证**：保存后重新读取，仅统计非删除线文字的中文字数
```python
for run in para.runs:
    rPr = run._element.find(qn('w:rPr'))
    if rPr is not None and rPr.find(qn('w:strike')) is not None:
        continue  # 跳过删除线文字
    ch += len(re.findall(r'[\u4e00-\u9fff]', run.text))
```

---

## 共享 Pitfalls

### 中文字符串引号问题
中文弯引号（\u201c \u201d）在 execute_code 内联字符串中可能触发 SyntaxError。**解决**：将数据写为独立 JSON 文件，脚本中读取。或在 JSON 中用「」替代弯引号，输出时 replace 回来。

### difflib 字数偏差
plan 方案中计算的字数与 difflib 实际输出可能有 ~15-25 字偏差（opcode 边界对齐和标点处理）。**解决**：最终目标预留 buffer，如要求 ≤1200 则 plan 目标控制在 ≤1180。

### 整段删除的标记方式
保留段落结构，清除 runs 后重建全文带删除线的 run。不要直接删除段落——文档结构断开会丢失上下文。

### 弯引号统一
原 docx 中常使用弯引号（\u201c \u201d），JSON 存储不便。在 JSON 中用「」存储，最终 replace 回弯引号。
