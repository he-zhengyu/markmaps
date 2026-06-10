---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Codex 從 0 到 1 全攻略

## 概覽
- 🔑 **Codex**：OpenAI 核心產品，對標 Claude Code
- 能力：寫代碼、排查 bug、執行測試、管理 Git、操作瀏覽器、控制電腦
- 視頻結構
  - 基礎篇：快速上手、核心配置、避坑
  - 進階篇：版本控制、會話管理、任務組織
  - 擴展篇:Plugin / Skill / Automation / Mobile

## 基礎篇：安裝與登錄
### 下載安裝
- 官網下載，macOS 拖入 Applications 即完成
### 登錄方式
- **ChatGPT 賬號登錄**（推薦）
  - 套餐：免費版 / Go / Plus / Pro，價格越高額度越大
  - 免費版與 Go 額度相近且極少，僅夠試水
  - 💡 想真正體驗建議 **Plus（$20/月）**，額度適中
- **API Key 登錄**（Sign in another way）
  - ❌ 不如套餐划算
  - ❌ 門檻高：通常需海外信用卡
### 初始設置
- 選擇職業 → 跳過導入 Claude Code/Cursor 配置 → 手機版先 Setup Later

## 實戰：第一版「馬克筆記」
### 建立項目
- 新建文件夾 → **Work in the Project** → Use an existing folder
- 需求：HTML 筆記軟件，左側列表、右側內容，做好測試
### 授權彈窗的選項
- **Yes**：本次同意，下次同類請求仍需授權
- **Yes + 以後自動執行**：同類命令不再詢問
- **輸入框**：告知自定義處理方式（如只檢查不啓動）
- **Skip**：弱化的第四選項，直接跳過
### 預覽區域
- 點擊 `index.html` 直接預覽
- 收起左側欄放大預覽；三個點 → **Hide Composer** 隱藏底部
### 🔑 Annotate 標註修改
- 點擊 annotate 圖標 → 框選區域 → 輸入修改意見
- 自動附帶截圖 + 文字要求，✅ 比純文字描述更精準
### ⚠️ 預覽區的安全限制
- 點「+」加筆記無反應 → 排查發現 **local storage 被禁用**
- 預覽區有安全限制，獨立瀏覽器中功能完全正常
- 📌 做外部應用時別被預覽區「假 bug」騙了，改用真實瀏覽器測試

## 三種安全模式（權限選項）
- **Default permissions**
  - 改項目外文件 / 危險命令需逐次授權
  - ✅ 絕對安全 ❌ 離不開人
- **Autoreview**（自動審查）
  - 專門的安全審查 agent 把關：安全放行、危險拒絕、拿不準才彈窗
  - 💡 效率與安全平衡最佳，演示全程採用
- **Full access**
  - 全自動同意，完全放飛
  - ⚠️ 無任何安全校驗，誤刪數據攔不住，開啓前三思

## 模型配置（輸入框旁）
- **思考深度**：low / medium / high / extra high
  - 越高耗時與 token 越多，代碼質量通常更好
- **模型切換**：GPT-5.5、GPT-5.4 等，按任務難度選
- **輸出速度**：standard / fast
  - fast 提速 1.5 倍，⚠️ token 消耗增加（GPT-5.5 下爲標準 2 倍）

## 進階篇：版本控制與會話管理
### 內置終端
- 快捷鍵 `Cmd+J` 開關終端面板
- `git init` → `git add` → `git commit` 建立安全備份版本
### 編輯消息（Edit）
- 用新請求**替換上一條消息**，清除無用內容
- 💡 避免無效消息佔用上下文、干擾後續執行
- ⚠️ 只支持編輯**最後一條**消息，更早的需借助 fork
### Codex 內置 Git 功能
- Environment → **Changes** → unstaged 查看未提交改動
- 對某行點「+」評論，讓 Codex 針對性修改
- **Commit 按鈕**：填寫 message → continue 直接提交
- 終端 `git log` 驗證提交記錄
### 🔑 Fork（會話分叉）
- 在某條消息處複製出新會話，**之後的消息全部丟棄**
- 兩種形式
  - **Fork into local**：沿用原項目目錄
  - **Fork into new worktree**：基於 `git worktree` 開闢隔離新目錄
    - ✅ 適合兩個會話並行開發不同功能，最後合併
- ⚠️ 兩種 fork 都**只回滾會話、不回滾代碼**
  - 需配合 `git log` + `git reset` 手動回滾代碼
### 會話歸檔（Archive）
- 歸檔 = 暫時隱藏；刪除 = 徹底消失
- `Cmd+,` 設置 → Archived chats：可解除歸檔或徹底刪除

## AGENTS.md：跨會話指令
- 🔑 項目根目錄的配置文件，**每個新會話自動讀取並執行**
- 對比：輸入框直接交代 ❌ 只在當前會話生效
- 示例：「每次完成代碼修改後提交一次 Git commit」→ 新會話驗證生效
- 還可寫：代碼風格、命名規範、技術棧要求、項目背景
- 💡 AGENTS.md 寫得越好，Codex 用起來越順手
- ⚠️ Codex 只提交當前需求相關改動，AGENTS.md 本身需手動 commit

## Plan Mode（計劃模式）
- 場景：HTML 改造爲 **Electron + React + TypeScript** 桌面客戶端的大工程
- 「+」→ Plan Mode：先出計劃、確認後再寫代碼
- 流程：Codex 先提問（數據存儲、交付程度）→ 撰寫含測試方案與架構設計的計劃
- 兩個選項：直接同意實現 / 提修改意見讓它重新出計劃
### Side Chat
- 輸入 `-side` 開啓
- 💡 主任務執行期間問輕量問題，**不干擾左側主任務**
### 修 Bug 經驗
- 啓動白屏 → 看控制檯報錯 → 反饋給 Codex 並要求「修復後測好再交付」

## 同時運行多個任務
- 多個會話可並行工作（如：加 Markdown 支持 + 生成 SVG logo）
- 🔑 **Steer 按鈕**：默認新消息要等上一請求完成；點 Steer 可**立即插入補充要求**
- 排查 logo 不顯示：文件存在、SVG 格式正常 → 定位爲 Electron 加載方式問題
- `Cmd+G` 喚起會話列表快速切換會話

## 擴展篇:Plugin / Skill
### Plugin 簡介
- 🔑 Codex 的「外掛」，賦予額外能力
- 側邊欄 → Plugins：✓ 已安裝，+ 可安裝
- 組成（以 Gmail plugin 爲例）
  - **App**：連接外部服務，提供 24 個 action（本質類似 MCP 工具）
  - **Skill**：給大模型看的說明文檔（如何總結郵件、何時用哪些工具）
### Presentations Plugin（做 PPT）
- 僅含一個 skill，說明如何做高質量 PPT
- `@presentations` 可顯式指定；不加 Codex 也會自動找到
- 產出中規中矩，是不錯的迭代起點
### Chrome Plugin（操作瀏覽器）
- 需同時在 Chrome 安裝對應擴展
- 實戰：打開 Product Hunt → 找當日最熱 3 個新品 → 總結特點附鏈接
- Codex 自建標籤組，逐頁訪問並彙總
### Computer Use Plugin（控制電腦）
- 可選 **don't work in the project**（請求與項目無關時）
- 實戰：打開系統日曆，新建指定日期、標題的日程
- 💡 Codex 使用**獨立虛擬鼠標**，與用戶鼠標互不干擾，可後臺默默幹活
### Skill 使用
- Plugins → Skills 標籤查看;plugin 安裝時會連帶安裝其 skill
- **ImageGen**（王牌 skill，無對應 plugin）
  - 生成美觀真實的圖片
  - 實戰：用真實軟件截圖做宣傳海報
  - 截圖技巧：「+」→ attach electron 抓取應用截圖；或**同時按左右 Cmd 鍵**快速截傳
### 自己寫 Skill
- 直接提需求：「寫一個代碼審覈 skill，包含如下規則」
- 新會話中 `@` 該 skill 即可調用，按規則檢查項目代碼

## Automation（定時任務）
- 三個點 → **Add automation**
- 執行環境三選一
  - **local**：綁定某項目目錄運行（本例選此）
  - **worktree**：基於項目新建 worktree 運行
  - **chats**:不綁定任何項目目錄
- 配置：標題、任務指令、頻率（daily 9:00）、模型與推理強度
- 左側欄 Automations 查看；每次運行新建一個會話，可手動試運行

## Codex Mobile（手機操縱電腦）
- 設置流程:Codex mobile → Get started → Allow → 掃二維碼 → 進入 ChatGPT 的 Codex 頁面
- 實戰：手機下指令，用 computer use 刪除電腦日曆中的日程
- 📌 與項目無關的請求記得選「不使用項目」
- 💡 在外也能遠程驅動電腦端 Codex 幹活

## Key Takeaways
- 💡 新手入門首選 **ChatGPT Plus 套餐**，比 API 划算
- 💡 **Autoreview** 是效率與安全的最佳平衡點
- ⚠️ 預覽區有安全限制（如禁用 local storage），務必在真實瀏覽器測試
- 📌 養成 **Git 提交習慣**；fork 只回滾會話，代碼回滾靠 Git
- 📌 **AGENTS.md** 讓規則跨會話持久生效，越完善越順手
- 💡 大工程先用 **Plan Mode** 出計劃再動工；多會話 + Steer 並行推進
- 💡 Plugin（App + Skill）+ 自定義 Skill + Automation + Mobile 持續擴展能力邊界