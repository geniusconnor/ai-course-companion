# ai-course-companion

An AI agent that autonomously completes online coursework on Trine University's Moodle platform — watching LinkedIn Learning videos, answering quizzes, writing forum posts, and uploading certificates.

Built on [Claude Code](https://claude.ai/code) with Playwright browser automation.

---

## What It Does

| Task | How |
|---|---|
| LinkedIn Learning videos | Playwright `browser_evaluate` — plays at 2x, waits for `ended` event |
| Moodle Quizzes | Navigates quiz pages, selects answers based on course content |
| Discussion Forum posts | Generates 150–250 word academic English responses |
| Certificate upload | Downloads LinkedIn certificate PDF, submits to Moodle assignment |

---

## Project Structure

```
.
├── CLAUDE.md                    # Agent instructions (system prompt)
├── memory/                      # Persistent agent memory
│   ├── MEMORY.md                # Memory index
│   ├── trine_credentials.template.md  # Credential template (copy → trine_credentials.md)
│   ├── moodle_login.md          # Login flow reference
│   ├── linkedin_video_approach.md     # Video playback technique
│   └── course_progress.md       # Week-by-week progress tracking
├── trine-info/                  # Trine University knowledge base
│   ├── 00_README.md
│   ├── 02_cisi_forms.md         # CISI × Trine forms & tools
│   ├── 06_cpt_employers.md      # CPT employer info
│   └── 07–11_course_reviews_*.md  # Course reviews by program
├── courses/
│   ├── knowledge-base/          # Per-week task notes (BAN-5003, BAN-5023)
│   ├── templates/               # APA DOCX generation scripts
│   └── BAN-5003/                # Course-specific scripts & drafts
└── gen_script.py                # Utility scripts
```

---

## Setup

### 1. Clone & configure credentials

```bash
git clone https://github.com/YOUR_USERNAME/ai-course-companion.git
cd ai-course-companion
cp memory/trine_credentials.template.md memory/trine_credentials.md
# Edit trine_credentials.md and fill in your email, password, student ID, and PIN
```

### 2. Requirements

- [Claude Code CLI](https://claude.ai/code)
- MCP Playwright server (for browser automation)

Install the Playwright MCP server:

```bash
npm install -g @playwright/mcp
```

Add it to your Claude Code MCP config (`~/.claude/mcp.json`):

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp"]
    }
  }
}
```

### 3. Run

Open Claude Code in this directory:

```bash
claude
```

Then tell it what to do, e.g.:

```
完成 BAN-5023 W5 的所有任务
```

The agent will log in to Moodle, complete videos, quiz, forum, and certificate upload automatically. It will pause and ask you for the SMS verification code when MFA is required.

---

## Key Technical Notes

### Why not `browser_wait_for(time=N)` for videos?

Chrome throttles JavaScript timers in background tabs. A `setTimeout(N * 1000)` call does **not** actually wait N seconds in a background tab — it can be throttled by 16x or more. The correct approach is to await the video's `ended` DOM event:

```javascript
() => new Promise((resolve) => {
  const v = document.querySelector('video');
  if (!v) { resolve('no video'); return; }
  if (window._rateKeeper) clearInterval(window._rateKeeper);
  // LinkedIn's player resets playbackRate periodically — fight it
  window._rateKeeper = setInterval(() => {
    const vid = document.querySelector('video');
    if (vid && vid.playbackRate !== 2) vid.playbackRate = 2;
  }, 200);
  v.playbackRate = 2; v.currentTime = 0; v.play();
  v.addEventListener('ended', () => resolve('ended:' + Math.round(v.duration)), { once: true });
  setTimeout(() => resolve('timeout:' + Math.round(v.currentTime) + '/' + Math.round(v.duration)), 900000);
})
```

### LinkedIn Chapter Quizzes

LinkedIn Learning has in-video chapter quizzes with a 10-second auto-skip timer. These are **not** Moodle assignments — skipping them has no effect on course grades.

---

## Credentials & Privacy

`memory/trine_credentials.md` is listed in `.gitignore` and never committed. Use the `.template.md` file as a starting point.

The `trine-info/` carpooling files (containing other students' contact info) are also excluded from git.

---

## License

MIT
