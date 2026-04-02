---
name: course-scraper
description: 抓取 Trine University 课程资料（EBSCO 论文、Moodle 页面、PDF 文件），并自动生成中英双语备份。触发条件：(1) 需要下载/读取课程论文或阅读材料；(2) 需要抓取 Moodle 作业说明；(3) knowledge-base 中某周资料不完整需要补全。抓取完成后必须同时保存英文原文和中文翻译两份文件到对应 knowledge-base 目录。
---

# Course Scraper

## 目录结构

```
e:\伴读书童\courses\knowledge-base\
└── BAN-5003\
    └── W{N}\
        ├── reads_{paper-name}.md        # 英文原文
        ├── reads_{paper-name}-zh.md     # 中文翻译
        ├── watches_{video-name}.md
        ├── watches_{video-name}-zh.md
        ├── assignments_{task-name}.md
        └── assignments_{task-name}-zh.md
```

## 抓取流程（按优先级执行）

### 方案一：Tavily Extract（首选）

```
mcp__tavily__tavily_extract(url="{目标URL}")
```

- 适用：大多数公开 PDF、Moodle 页面
- 优点：无需翻页，一次提取全文
- 失败条件：返回内容为空、或内容明显不完整（缺少章节）

### 方案二：Playwright 下载 PDF（需登录时）

1. 导航到目标页面（已登录 Moodle/EBSCO）
2. 查找下载按钮：`getByRole('link', { name: /download|pdf|save/i })`
3. 点击下载，文件保存到本地
4. 用 `tavily_extract` 对直接 PDF URL 提取文本

### 方案三：Playwright 逐页翻页（兜底）

```javascript
// 循环翻页提取所有页面文本
let allText = '';
const totalPages = /* 从页面读取总页数 */;
for (let i = 1; i <= totalPages; i++) {
  allText += await page.evaluate(() => document.body.innerText);
  await page.getByRole('button', { name: /next|>/i }).click();
  await page.waitForTimeout(1000);
}
```

## 完整性验证

抓取完成后必须验证：
- 章节数是否与论文目录匹配
- 内容字数是否合理（页数 × 300 字以上）
- 最后一段是否包含 References/参考文献

验证失败 → 降级到下一方案重新抓取。

## 双语备份规范

抓取完英文原文后立即生成中文翻译：

1. 保存英文原文：`reads_{name}.md`
2. 翻译全文，保存：`reads_{name}-zh.md`
3. 中文文件头部注明原文来源、作者、期刊、DOI

翻译要求：
- 学术术语保留英文并括注中文，如：PLEO（产品延寿运营）
- 段落结构与英文版一致，便于对照
- 完整翻译，不压缩不意译

## 参考资料

- EBSCO 代理：`https://research-ebsco-com.tuproxy.palni.edu`（需 Trine 账号）
- Moodle 课程 ID：BAN-5003 = 63116，BAN-5023 = 63172
- 详细登录流程见 [references/ebsco-login.md](references/ebsco-login.md)
