# ai-senior-learning-coach — AI 樂齡學習教練

靜態網頁（`index.html`＋`data.js`＋`manual.html`＋PWA）。對象是不熟科技的長輩。2026-11-04 建立。

- 本機預覽 port **8850**（`.claude/launch.json`）。
- GitHub Pages（Actions workflow `pages.yml`，push master 自動部署）：<https://m255525.github.io/ai-senior-learning-coach/>；visitor-badge `m255525.aiseniorlearningcoach`。

## 設計原則（使用者要求「UI 與 UX 極為簡化」，加功能前先想這條）
- 下方只有三個大按鈕：今天學／問教練／防詐騙。不再加分頁。
- 一個畫面一件事，主要動作只有一顆大按鈕。沒有問卷、註冊、表單、拖曳、hover 才出現的東西。
- 基準字 22px（放大字 25／28px）；按鈕至少約 3.3rem 高；語氣用「您」，句子短。
- 課程順序固定（`data.js` 的 `lessons` 順序＝學習順序），不讓長輩選路線；想重看從「我的印章」進。
- 手機返回鍵要能用：畫面切換都走 `location.hash`。

## 架構重點
- 主視覺＝傳統撕日曆（民國紀年、農曆用 `Intl` chinese calendar、宜忌 `almanac` 依日期輪替）。學完蓋章→「撕下今天的日曆」→`S.torn=今天`，首頁顯示明天那一頁＋「還想學，再學一課」。重看舊課（`LS.again`）不撕日曆。
- 上課 `LS.pages`：[複習?]→say→try→quiz→stamp。答錯也給章。
- 間隔複習 `GAPS=[1,3,7,14,30]` 天，到期時在開新課前自動插一題（`dueReview`，一天一題），不另開入口。
- 問教練 `ask()`：先 `guard()`（身分證／卡號擋下；胸痛中風→119；輕生→1925）→有金鑰走 `callLLM`（Gemini／OpenAI／Claude／OpenRouter，失敗退回內建）→否則 `faq()` 關鍵字→都沒有就 `startHand()`：點擊當下複製問題，顯示步驟倒數 8 秒後同分頁跳到 Gemini（預設；`C.aiPicked` 記使用者是否親自選過，沒選過一律 Gemini）。單問單答，不是聊天串。
- Gemini 網頁版實測不吃 `?q=`／`?prompt=`（2026-11-05），只能複製後請長輩貼上，所以跳走前一定要先顯示步驟。倒數結束用 `location.href` 同分頁跳，計時器裡 `window.open` 會被擋。複製要在開新頁之前同步做（`copy()` 先走 execCommand）。疑似詐騙（`isScam`）的問題不自動跳走，留在畫面給 165 按鈕。
- 防詐騙：`check` 五問（一題一題）、`scenes` 10 題（情境全虛構，簡訊題不放任何連結）。
- 朗讀 `speechSynthesis`（zh-TW、預設 0.85 倍）；語音輸入 `webkitSpeechRecognition`，不支援時隱藏並提示用鍵盤麥克風。
- 加入主畫面：首頁大按鈕（`data-big`，手機或可安裝時才顯示，按過「我加好了」或從桌面開過就收起）＋頁尾／設定小入口。有 `beforeinstallprompt` 就直接跳安裝；否則開 `#inst` 步驟視窗（`instGuide()` 依 iPhone／三星／安卓／電腦分版，不用會消失的 toast）。LINE 內建瀏覽器不能安裝，用 `?openExternalBrowser=1` 換到外部瀏覽器；其他 App 內瀏覽器給步驟＋複製網址。iPhone 桌面版可能和 Safari 不共用 localStorage，已蓋章時在步驟上方提醒先備份。視窗操作鈕 `.inst-act` 黏在底部，小螢幕＋特大字也要看得到。
- 儲存鍵 `alc.state`、`alc.settings`、`alc.api`、`alc.fold`、`alc.warnSeen`、`alc.marquee`、`alc.installDone`。
- 標準配備：跑馬燈（工作區公告 GAS，滑鼠移入暫停，不可關）、⚙ 常用設定（收合式＋關於本工具）、首訪警語、manual.html#creator 完整版、PWA、訪客計數器。
- `manual.html` 由 `tools/build_manual.py` 組出（`tools/manual_body.html`＋賞鳥地圖手冊的創作者區塊），改手冊要改 body 再重跑。
- 改 `index.html`／`data.js` 上線時要升 `service-worker.js` 的 `CACHE_NAME`。
- 測試掛鉤 `window._alc`。

## 內容注意
- 電話只放確認過的：119、110、165、1925、1966、1957。
- 醫療內容只教「怎麼問」與「問真人」，不給判斷；不放真實連結或真實公司名。
