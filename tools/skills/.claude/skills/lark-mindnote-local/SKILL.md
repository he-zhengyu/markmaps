---
name: lark-mindnote-local
description: Generate structured outline text for Lark MindNote (飞书思维笔记). Use this skill whenever the user wants to create a mind map, mindnote, 思维导图, or 思维笔记 in Lark/Feishu, or wants to convert notes, outlines, or structured content into a Lark-compatible format. Also use when the user says "转成思维笔记", "生成思维导图", "mindmap this", or asks to visualize hierarchical content in Lark. Trigger especially when converting book chapters, lecture transcripts, video subtitles (.srt/.vtt), meeting notes, or any long-form content into a tree-structured mind map. If the user uploads a PDF chapter, transcript file, or subtitle file and wants a mind map or outline, use this skill.
---

# Lark MindNote Skill

Convert structured or unstructured content (notes, book chapters, lecture transcripts, video subtitles, outlines, documents) into a Lark MindNote-compatible tab-indented outline, with optional emoji highlights.

---

## How Lark MindNote Works

Lark MindNote has two views:
- **大纲视图 (Outline view)** — tab-indented bullet list, URL ends with `#outline`
- **思维导图视图 (Mind map view)** — visual tree, URL ends with `#mindmap`

The outline view accepts **tab-indented plain text**. Each line = one node. Indentation level = hierarchy depth. Switching to mind map view auto-renders the tree.

---

## Output Format

Always output a tab-indented outline. Use **actual tab characters** (not spaces) for indentation.

```
Root Topic
	Level 1 Node
		Level 2 Node
			Level 3 Node
		Level 2 Node
	Level 1 Node
```

**Rules:**
- First line = root node (center of mind map)
- Each indent level = one Tab character
- No bullet characters, no markdown `#` headers — plain text only
- Keep node text concise: aim for under 40 characters per node, but clarity wins over brevity — don't sacrifice meaning to hit a number
- Recommended depth: 3–5 levels. Go to 6 only for genuinely complex material. Shallower is usually better for readability.

---

## Input Types and Preprocessing

Different source materials need different treatment before building the tree. Identify the input type first, then follow the corresponding strategy.

### Book Chapters / Articles

Book chapters have explicit or implicit structure — use it directly.

1. **Identify the argument spine**: What is the chapter's main thesis? This becomes the root or a prominent Level 1 node.
2. **Map sections to branches**: Each major section or heading becomes a Level 1 node. Subsections become Level 2.
3. **Extract key concepts, not sentences**: Convert paragraphs into their core idea. A 3-paragraph argument about "why caching fails at scale" becomes a single node like "缓存在大规模下的失效" with child nodes for each reason.
4. **Preserve examples and evidence as leaf nodes**: Important examples, data points, or quotes that support an argument go one level below the claim they support. Label them concisely (e.g., "例: Netflix 2015年事故").
5. **Capture definitions**: If the chapter introduces terminology, give it a dedicated node with the definition as a child.

### Lecture / Video Transcripts and Subtitles (.srt, .vtt, .txt)

Transcripts are messy — they contain filler words, repetition, tangents, and non-linear flow. The goal is to extract the *intellectual structure*, not mirror the speaking order.

1. **Read the full transcript first** before building any hierarchy. Speakers often introduce a topic, digress, then return to it. You need the full picture to group correctly.
2. **Identify topic segments**: Find where the speaker shifts topics. These become Level 1 nodes. Ignore the chronological order if the speaker revisits a topic — merge those segments under one branch.
3. **Strip verbal noise**: Ignore filler phrases, self-corrections, repetition ("so basically what I'm saying is..."), and off-topic tangents unless they contain a genuinely useful insight.
4. **Reconstruct the logical structure**: A lecturer might explain concept A, give example B, then state the principle C that connects them. In the mind map, C is the parent, A and B are children — even though C was said last.
5. **Preserve the speaker's key phrases when memorable**: If the speaker coins a term or uses a particularly vivid phrase, use it as the node text (e.g., "技术债的雪球效应").

### Already-Structured Notes / Outlines / Markdown

These are the simplest case — the hierarchy often maps directly.

1. Convert headings to tree levels (# → L1, ## → L2, ### → L3)
2. Collapse deeply nested bullet lists if they exceed 5 levels
3. Merge near-duplicate points

---

## Emoji Highlighting Rules

Only add emoji to nodes that need visual emphasis. Default: no emoji.

Use **only these four categories** unless the user specifies otherwise:

| Emoji | Meaning | When to use |
|-------|---------|-------------|
| ⚠️ | Risk / limitation | Warnings, constraints, things that can go wrong |
| 💥 | Failure mode | Known failure patterns, anti-patterns, pitfalls |
| ✅ / ❌ | Pro / Con comparison | When two sibling nodes contrast (good vs bad, works vs doesn't) |
| 🚀 | Cutting-edge / highlight | Frontier ideas, key insights, most important takeaways |

Do not add emoji to every node — this defeats the purpose. Aim for ~10–20% of nodes having emoji at most.

---

## Step-by-Step Process

### 1. Read and understand the source material
- If an uploaded file is provided, read it fully first (use the file-reading skill for PDF, .srt, .vtt, etc.)
- Identify the input type (book chapter, transcript, structured notes)
- Find the root topic — the single phrase that captures the whole piece

### 2. Extract the logical skeleton
- For book chapters: follow the argument spine (thesis → supporting sections → evidence)
- For transcripts: group by topic, not by speaking order; merge revisited topics
- For notes: respect existing hierarchy, clean up redundancy

### 3. Build the hierarchy
- Keep nodes concise but meaningful (under 40 chars when possible)
- If a node needs more context, split it: label as parent, details as children
- Prefer breadth over depth when in doubt — a 5-branch × 3-level tree reads better than a 2-branch × 6-level tree

### 4. Apply emoji selectively
- Only mark nodes that fall into the four categories above
- For ✅/❌: apply to sibling nodes that form a direct comparison pair
- For ⚠️/💥: apply to the node itself (not its children)
- For 🚀: use sparingly — 1–3 times per map maximum

### 5. Output language
Match the output language to the input:
- Chinese input → all node text in Chinese
- English input → all node text in English
- Mixed input → use the dominant language; keep proper nouns/acronyms as-is

### 6. Write output to file
If the input was a file (e.g. `/path/to/notes.md`), write the outline to a file in the **same directory** with the suffix `_mindnote.txt`:
- Input: `/path/to/notes.md` → Output file: `/path/to/notes_mindnote.txt`
- Input: `/path/to/lecture.srt` → Output file: `/path/to/lecture_mindnote.txt`

The output file contains only the raw tab-indented outline (no code fences, no paste instructions).

If the input was pasted text (no file path), output the outline in a code block in the chat as before.

---

## Paste Instructions (always include after the outline)

> **如何导入飞书思维笔记：**
> 1. 打开飞书思维笔记，切换到**大纲视图**（左上角列表图标）
> 2. 全选现有内容并删除
> 3. 粘贴以上内容（确保使用 Tab 缩进，不是空格）
> 4. 切换回**思维导图视图**即可

---

## Examples

### Example 1: Book Chapter → MindNote

**Input:** A chapter on microservice patterns discussing decomposition strategies, communication patterns, and failure handling.

**Output:**
```
微服务设计模式
	服务拆分策略
		按业务能力拆分
			例: 订单服务 vs 支付服务
		按子域拆分 (DDD)
			识别限界上下文
			⚠️ 上下文边界划错代价高
		🚀 Strangler Fig 模式
			渐进式替换遗留系统
			适合大型单体迁移
	服务间通信
		同步: REST / gRPC
			✅ gRPC 性能优于 REST
			❌ REST 调试更方便
		异步: 消息队列
			事件驱动架构
			⚠️ 消息顺序性难保证
	故障处理
		熔断器模式
			防止级联故障
		重试与退避策略
			💥 无退避的重试导致雪崩
		服务降级
			优雅降级 vs 快速失败
```

### Example 2: Lecture Transcript → MindNote

**Input:** A 45-min lecture transcript where the professor discusses neural network optimization, jumping between gradient descent variants, learning rate scheduling, and batch size effects, with several tangents about historical context.

**Output:**
```
神经网络优化方法
	梯度下降变体
		批量梯度下降 (BGD)
			使用全部数据计算梯度
			⚠️ 大数据集下极慢
		随机梯度下降 (SGD)
			每次用单样本
			噪声大但收敛快
		🚀 小批量梯度下降 (Mini-batch)
			兼顾效率与稳定性
			实践中最常用
	学习率策略
		固定学习率
			💥 太大振荡, 太小卡住
		学习率衰减
			阶梯式 vs 指数衰减
		Warmup 策略
			先小后大再衰减
			Transformer 训练必备
	Batch Size 的影响
		大 Batch
			✅ 训练更稳定
			❌ 泛化能力可能下降
		小 Batch
			✅ 正则化效果好
			❌ GPU 利用率低
	关键结论
		🚀 没有万能配置, 需要实验调参
```

### Example 3: Simple Structured Notes

**Input (markdown notes):**
```
# Database Choices
## SQL
- ACID compliant
- Best for structured data
- Hard to scale horizontally
## NoSQL
- Flexible schema
- Scales easily
- Risk: eventual consistency issues
```

**Output:**
```
Database Choices
	SQL
		ACID compliant
		Best for structured data
		⚠️ Hard to scale horizontally
	NoSQL
		Flexible schema
		🚀 Scales easily
		💥 Eventual consistency issues
```

---

## Browser Automation (if Chrome extension is connected)

If the user is already on a Lark MindNote page and the Chrome extension is connected:

1. Get tab context with `tabs_context_mcp`
2. Navigate to the outline view: change URL fragment to `#outline`
3. Use `read_page` to find the editable outline area
4. Use `javascript_tool` to clear existing content and insert the new outline text
5. Switch back to `#mindmap` view

If the extension is not connected, output the plain text outline and ask the user to paste it manually.
