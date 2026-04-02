# 伴读书童 记忆库

## LinkedIn Learning 刷课铁则

**唯一正确方法** → `memory/linkedin_video_approach.md`

核心：用 Promise + 'ended' 事件等视频自然播完，setInterval 每200ms强制保持2x速率。
**禁止** `browser_wait_for(time=N)` 计时——Playwright后台定时器被浏览器节流，完全不准。

---

## Trine 账号凭证

详见 `memory/trine_credentials.md`（本地文件，不纳入版本控制）

- 邮箱：YOUR_NETID@my.trine.edu
- Student ID / PIN 见本地凭证文件

---

## Moodle 登录流程

详见 `memory/moodle_login.md`

- Microsoft SSO → 输入邮箱 → 密码 → SMS验证码（Connor实时提供）
- 登录后直接进课程页

---

## 课程进度

详见 `memory/course_progress.md`

- BAN-5023：W1–W4 完成，W5 视频进行中，W6–W8 待做
- BAN-5003：W2–W8 全部待做

---

## LinkedIn Chapter Quiz 注意

LinkedIn Learning 课程内嵌的 Chapter Quiz 有**10秒自动跳过**倒计时。
这些**不是 Moodle 作业**，跳过了不影响成绩。
真正要做的是 Moodle 里的 Quiz（单独的作业模块）。
