---
name: moodle-quiz
description: 为 Trine University Moodle Quiz 做答题操作。核心流程：对每道题 snapshot 读题 → 用 tavily_search 搜索验证正确答案 → 选择验证后的选项 → 全部完成后提交。适用场景：(1) 用户明确说"做quiz"/"答题"；(2) 执行任何 Moodle 课程任务（完成某周作业、刷课、完成课程等）过程中遇到 Quiz 类型作业——无论用户是否提及 quiz，只要 Moodle 页面出现 Quiz/测验入口，必须自动按此流程执行，不得跳过。禁止凭印象或通识猜答案——必须搜索验证后再选。
---

# Moodle Quiz 答题流程

## 核心原则

**每道题必须先搜索验证，再选择。禁止猜答案。**

历史教训：BAN-5023 W6 丢 2 分（14/16）、W8 丢 2 分（16/18），均因未查课程内容直接依赖通识判断。

---

## 执行流程

### 1. 进入 Quiz

```
browser_navigate → quiz 页面
browser_snapshot → 确认页面状态
browser_click → "Attempt quiz" 或 "Start attempt"
```

### 2. 逐题处理（每题重复此循环）

**Step A：读题**
```
browser_snapshot  ← 获取当前题目完整内容（题干 + 所有选项）
```

**Step B：搜索验证**
```
tavily_search(query="<题目关键词> <课程主题>", search_depth="advanced")
```
- 搜索词：提取题干核心概念 + 课程主题关键词（如 "Tableau dashboard filter" / "data visualization best practice"）
- 结果不明确时换关键词再搜一次（最多 2 次）
- 目标：找到明确支持某选项的来源，不接受模糊判断

**Step C：选答案**
```
browser_click → 选择搜索验证后确认正确的选项
记录：题号 | 题干摘要 | 选择的答案 | 依据（一句话）
```

**Step D：翻页**
```
browser_click → "Next page" 或下一题按钮
```

### 3. 提交

```
browser_snapshot → 确认所有题目已作答（无空题）
browser_click → "Submit all and finish"
browser_click → 确认对话框 "Submit"
browser_snapshot → 截图记录最终得分
```

---

## 搜索策略

| 题目类型 | 搜索策略 |
|---------|---------|
| 定义题（"X is defined as..."） | 直接搜术语，找权威定义 |
| 步骤/流程题（"Which is the first step..."） | 搜 "steps of X" 或 "X process" |
| 工具功能题（Tableau/Python/Excel） | 加软件名 + 具体功能描述 |
| 最佳实践题 | 搜 "best practice X" |

**置信度判断：**
- ✅ 高：多个来源一致 → 直接选
- ⚠️ 中：单一来源但逻辑吻合 → 可选，注明
- ❌ 低：结果矛盾或无关 → 换关键词再搜，不猜

---

## 进度记录

每道题做完后记录：
```
Q1: [题干摘要] → 选 [X]（来源：xxx）
Q2: [题干摘要] → 选 [X]（来源：xxx）
```

提交后截图得分，更新 memory 中对应的 `ban5023_assignments.md` 或 `ban5003_assignments.md`。

---

## 注意事项

- 多选题（Multiple select）：每个选项独立搜索验证
- Quiz 有时间限制时搜索要高效，每题搜索不超过 2 次
- 提交后必须截图得分页面并更新 memory
