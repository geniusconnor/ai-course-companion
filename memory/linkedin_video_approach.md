---
name: LinkedIn Learning 刷课方法
description: 2x速播放视频直到自然结束的唯一可靠方法
type: feedback
---

每个视频用 `browser_evaluate` 执行 Promise，等待 'ended' 事件自然触发。

**为什么不用 browser_wait_for(time=N)：**
Playwright 的 `browser_wait_for` 内部用浏览器 JS setTimeout，在后台标签页被浏览器节流（Chrome background throttling），导致 N "秒" 实际只过了 N/~16 真实秒。视频时长无法用它准确计时。

**正确 JS（每个视频页面 verbatim 执行）：**

```javascript
() => new Promise((resolve) => {
  const v = document.querySelector('video');
  if(!v) { resolve('no video'); return; }
  if(window._rateKeeper) clearInterval(window._rateKeeper);
  window._rateKeeper = setInterval(() => {
    const vid = document.querySelector('video');
    if(vid && vid.playbackRate !== 2) vid.playbackRate = 2;
  }, 200);
  v.playbackRate = 2; v.currentTime = 0; v.play();
  v.addEventListener('ended', () => resolve('ended:' + Math.round(v.duration)), {once: true});
  setTimeout(() => resolve('timeout:' + Math.round(v.currentTime) + '/' + Math.round(v.duration)), 900000);
})
```

**Why setInterval：**
LinkedIn 的播放器会周期性把 playbackRate 重置回 1x。setInterval 每200ms强制检查并还原2x，保证全程2x播放。

**返回值：**
- `"ended:XXX"` = 正常播完，XXX是时长（秒）
- `"timeout:CT/DUR"` = 15分钟超时（正常不会触发）
- `"no video"` = 视频元素未找到（页面未加载完，等几秒重试）

**流程：**
1. 导航到视频页（URL带 `?autoSkip=true&leis=LTI13&resume=false&u=130423532`）
2. 执行上述 JS
3. 等 resolve → 页面自动跳转下一个视频
4. 重复，直到课程全部 (Viewed)
