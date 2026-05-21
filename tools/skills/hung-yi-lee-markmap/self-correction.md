---
markmap:
  initialExpandLevel: 9
  maxWidth: 500
  colorFreezeLevel: 4
---

# 語言模型的自我修正 (Self-Correction)

## 🎯 核心問題
- 過去：人類給回饋 → 模型修正
- **本課重點**：無人介入下，模型能否自己發現錯誤、自己修正？
- 三大方向
  - 修改 **Inference 過程**
  - 修改 **Workflow** (Harness)
  - 修改 **模型參數** (Reasoning)

## 🔧 方向一：修改 Inference 過程

### 核心概念
- 從生成過程的 representation / 機率分布找出「錯誤訊號」
- 用訊號自動修正最終輸出
- **Detection + Correction 全自動**

### 早期啟發 (需收集額外資料)
- **Binary Classifier (2023)**
  - 收集答對 vs 答錯的 representation
  - 訓練分類器 → 可泛化到新問題
  - 證明「對錯訊號」可從 representation 抽出
- **TruFacts (2024)**
  - 答錯 representation 平均 vs 答對 representation 平均 → 相減得「修正向量」
  - 把修正向量加回錯誤的 representation → 修正答案

### Contrastive Decoding (不需額外資料)
- **基本概念**
  - 正常輸入 → 得到 representation A
  - 「弄壞」輸入 → 得到必錯的 representation B
  - 公式：output = (1+α)·A − α·B
  - 每個 token 都做一次
- **優點**：不動模型參數，inference 階段直接套用
- **缺點**：需要額外運算 (多跑一次 inference)
- **常見操作位置**：最終輸出的 logits / 機率分布

### Contrastive Decoding 各種變形 <!-- markmap: fold -->

#### 1. 原始 Contrastive Decoding (2022)
- 用「小模型」製造錯誤答案
- 例：歐巴馬出生在檀香山 → GPT-2 大版本最高機率錯給 Hawaii
- 大模型 − 小模型 → 正確答案 1961 浮現
- 為什麼用 logits：兩模型層數不同，無對應 representation

#### 2. DoLa (Decoding by Contrasting Layers, 2023)
- 已寫進 Hugging Face Transformers
- 基於 **Logit Lens** 概念
  - 把 LM head 接到中間每一層 → 得到中間層的「decode 結果」
  - 例：Llama 2 翻譯時內心先翻成英文
- 做法：最後一層 distribution − 中間層 distribution
- ✅ 優點：不需額外小模型，幾乎無 overhead
- 難點：選哪一層做相減

#### 3. Layer CD (2025, 用於影像)
- 例：機車人衣服上的字是什麼顏色？
- 最後一層：黑/白搖擺
- 淺層 (shallow) image encoder：被「衣服顏色」混淆
- 兩者相減 → 白色機率最高 → 正確

#### 4. ICD (Instruction Contrastive Decoding)
- **降智咒語**：在輸入後加「你都給錯誤答案」
- 模型變笨 → 錯誤答案
- 與正常輸出相減

#### 5. CAD (Context-Aware Decoding, 2023)
- 應用場景：RAG
- 問題：強模型不讀檢索文件，靠自身過時知識
- 做法：有檢索文件的輸出 − 沒有文件的輸出
- **影像版本**
  - 例：黑色香蕉是什麼顏色？模型受文字 prior 影響選黃色
  - 把圖加雜訊 → 模型只憑 prior → 必錯
  - 相減 → 修正
- 變形
  - 把圖切塊打亂 (2025) 比一般雜訊好
  - 抹去最重要的物件再 decoding (2025/6)

#### 6. Audio-Aware Decoding
- 台大實驗室成果（Purdue 學生 visit）
- 移除音訊 / 換成 silence → 製造錯誤
- 在語音語言模型上有效

#### 7. MTI (Minimum Test-Time Intervention)
- 動機：減少 contrastive decoding 額外運算
- 假設：只有「關鍵 token」需要修正 (人生轉折點比喻)
- 觸發條件：機率分布 entropy 高 → 啟動 CD
- **關鍵技巧**：利用 **KV Cache**
  - 降智咒語只能加在最後 (前綴一致才能 reuse cache)
  - 在輸入後加 "Output Error" → 取下一個 token 的分布作錯誤
  - 只需多算 2 個 token
- 結果：62% → 72% 正確率
- 降智咒語效果排序
  - ✅ Output Error, Status Error, Invalid Logic
  - ❌ Output Correct, Status True, Valid Logic
  - ❌ Monkey、!!!、Apple 等怪字無效

#### 8. 改在其他位置的 CD
- 多數 paper：最終 logits
- VISTA：latent representation
- ACG (2025/1)：改在 **attention weight** 上 → 更有效

### 兩個關鍵維度總結
- **如何製造錯誤答案**
  - 小模型輸出、淺層 layer、降智咒語、移除 context、移除影像、加雜訊、移除音訊...
- **改在哪裡**
  - Logits / Hidden representation / Attention weight

## 🔄 方向二：修改 Workflow

### 核心：Generation + Verification
- 模型輸出答案 → 程式自動插入「再檢查一下」這類泛用指令
- 不需人類介入 (是程式插入的稻草人)

### 為什麼可能有用？(直覺) <!-- markmap: fold -->
- **批判比生成容易**
  - 不會寫小說，但能判斷小說好不好看
- **生成過程無法回頭**
  - Sampling 一旦錯了只能「一步錯、步步錯」
  - 插入「再檢查」給模型機會接出修正內容
- ⚠️ 但這只是直覺
  - 有 paper 顯示模型批判能力 ≤ 生成能力
  - 但該 paper 把批判做成選擇題，可能只是不會做選擇題

### 實證結果 (2024)
- **大規模實驗 (24/10 paper)**
  - Internal (自我反思)：有時有用，**不穩定**，有些 case 反而變差
  - External (外部回饋，如執行 code、網路搜尋)：**穩定有效**
- **RefineBench (24/11)**
  - Claude 3.5 Sonnet / Gemini 1.5 Pro：自我反思進步極小
  - 給 checklist 一半 → 大幅進步
  - 給完整回饋 → 最佳
  - 結論：**外部回饋才是關鍵**

### 自我修正的四種狀況
- 錯 → 對 ✅ 最樂見
- 對 → 對 (浪費算力)
- 錯 → 錯 (浪費算力)
- 對 → 錯 ❌ 最不樂見

### 兩個關鍵指標
- **Confidence Level (CL)**：對 → 對的機率（信心程度）
- **Critic Score (CS)**：錯 → 對的機率（接受批評能力）
- 公式：ACC2 = ACC1·CL + (1−ACC1)·CS

### 模型個性差異
- 頑固型：DeepSeek、Mixtral → CS 低
- 彈性型：Llama 3 70B、GPT-3.5/4 → 改答案多但 CL 較低
- ⚠️ 頑固 ↔ 接受批判 互斥

### 反思指令的選擇影響行為
- 中性「再做一次」：基準
- 肯定「你應該是對的」→ CL ↑、CS ↓ (更頑固)
- 質疑「你確定嗎」→ CL ↓、CS ↑ (更易改)
- 💡 不同模型需要不同的指令 → 文獻結論為何 mixed 的可能原因

### 關鍵反問：算力划算嗎？

#### 比較對象：Reflection vs Majority Vote
- 用同樣算力多 sample 幾次再投票，是否比反思更好？

#### 實驗結果 (paper)
- **橫軸 = sample 次數**：加反思看似贏
- **橫軸 = 總算力**：majority vote 贏
- 結論
  - **Verification 像奢侈品**：算力達到極限後才值得加
  - 算力有限時：先多樣化 sample 比反思更划算
  - 要 3.8% 進步 → 需 100× 算力
- ⚠️ 論文 baseline 一定要比 Majority Vote

## 🧠 方向三：修改參數 (Reasoning)

### Reasoning vs Workflow 差別
- Workflow：硬插指令，每次都被迫思考 (浪費)
- Reasoning：模型**學會**何時該修正、何時不該
- → Reasoning 更 intelligent、更省算力

### 關鍵發現：知識 ≠ 自我修正能力
- 例：模型答「希拉蕊出生在紐約」(錯)
- 但問「希拉蕊在哪出生」→ 答對是芝加哥
- 知識在但無法觸發修正
- 自我修正是獨立能力，可抽成 **steering vector**

### 直接教自我修正：REVISE 法
- 拆兩步學
  - **Step 1 錯誤偵測**：錯誤答案 → 輸出 Refine Token；正確答案 → 輸出 EOS
  - **Step 2 錯誤修正**：給輸入+錯誤輸出+Refine → 學輸出正確答案

### 直接教的問題 (2024 paper)
- Fine-tune 後模型參數變了 → 犯的錯也變了
- 訓練時學會修正「綠色錯誤」
- Inference 時模型給「紅色錯誤」(沒看過)
- → 反而做得更差

### 業界主流：RLVR
- **Reinforcement Learning with Verifiable Reward**
- 流程：輸入 → reasoning (任意 token) → 答案
  - 對 → positive reward
  - 錯 → negative reward
- 適用場景
  - 數學 (答案是數字，一翻兩瞪眼)
  - 程式 (可執行驗證)
- 中間 reasoning 過程不重要，**只看最終答案**
- 神奇現象：模型自然學會 verification 與自我修正

### 為什麼 Reasoning 有用？

#### 直覺：思考的代價 (Cost of Thinking)
- 心理學論文：模型 reasoning token 數 ⟂ 人類解題時間
- 不論碳基/矽基，思考都需要代價
- ⚠️ 批評：token 數 vs 時間是否真能類比？

#### 理論：拆步驟 = 降低資料需求 <!-- markmap: fold -->
- 一步到位：K^(T+1) 種變化 (指數爆炸)
- 拆 T+1 步、每步 K 種變化：只要 K·(T+1) 筆資料
- **Parity Check 例子**
  - 6 位元二進位 → 直接做需 64 筆資料
  - 拆成連續 XOR (5 步、每步 4 變化) → 只需 20 筆
- **In-domain**：背答案就好，不需 reasoning
- **Generalization**：reasoning 才有泛化能力

### 大爭論：RL 學到了什麼？

#### 派別一：模型本具能力，RL 只是放大
- 樹狀 sampling 圖：正確路徑早就存在於 base model
- RL 只是提高那條路徑的機率
- **證據 (24/4 paper)**
  - 用 pass@k 評估
  - k=1：RL 模型遠勝 base
  - k=256：兩者幾乎一樣 (RL 甚至略差)
- **禪宗類比 (老師原話)**
  - 華嚴經：「奇哉奇哉，大地眾生本具如來智慧德相，只因妄想執著而不能得證」
  - 模型本具 reasoning，被其他可能性覆蓋
- **延伸**：24/10 有人提出新 sampling 演算法
  - 不訓練、純改 sampling → 逼近甚至超越 RL 結果

#### 派別二：RL 確實教會新能力
- **證據 (24/6 paper)**
  - 上半圖：只看最終答案 → pass@k 高 sample 量下 base 接近 RL
  - 下半圖：用 **COTPath** (檢查計算過程)
    - 答案對 + 過程也對才算對
    - Base model 大幅落後 RL 模型
- 反駁批評：1024 次 sample 中很多是「猜對」
- ⚠️ 自我批評：過程對錯由另一個 LLM 判斷，可信度？

#### 折衷觀點 (Debate paper)
- **訓練初期**：利用既有路徑、改變機率
- **訓練後期**：訓練夠久 → 學到新能力
- 開放問題：什麼 RL 演算法 / reward signal 最能激發新能力？

## 📌 三大方向總比較

### Inference 修改 (Contrastive Decoding)
- ✅ 不用訓練、隨插即用
- ❌ 額外運算成本

### Workflow 修改 (Generation + Verification)
- ✅ 不用訓練
- ⚠️ 不穩定、外部回饋更有效
- ⚠️ 可能不如 majority vote 划算

### 參數修改 (Reasoning / RL)
- ✅ 模型自主、更 intelligent
- ✅ 泛化能力強
- ❌ 需訓練成本
- 🔬 仍有爭議（本具 vs 學新）

## 🔑 重要 Takeaways
- 自我修正 ≠ 知識完備
- 批判比生成容易 (對人) ≠ 對模型也成立
- 反思指令本身會塑造模型行為
- 比較 baseline 一定要包含 Majority Vote
- Reasoning 的本質是把組合爆炸拆成線性
- RL 是放大本具能力？還是創造新能力？仍是開放問題