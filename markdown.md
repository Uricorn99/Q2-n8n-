# URL 摘要條列工具（n8n + OpenAI + Streamlit）

本專案實作一個簡單的網頁摘要系統，使用者只需輸入文章網址，即可自動擷取網頁內容，透過大型語言模型（LLM）整理為條列式重點，並以純文字格式回傳與下載。

---

## 功能說明

- 輸入任意公開網頁 URL
- 自動擷取並清洗網頁文字內容
- 使用 LLM 生成條列式摘要（繁體中文）
- 顯示原始網址與摘要生成時間
- 支援下載 TXT 檔案

---

## 系統架構

本專案由三個主要部分組成：

1. **Streamlit（前端）**
   - 提供使用者輸入網址與顯示摘要結果
   - 透過 HTTP POST 呼叫 n8n Webhook

2. **n8n Workflow（後端流程）**
   - Webhook Trigger：接收網址
   - Fetch HTML：取得網頁原始內容
   - Extract Main Text：清洗 HTML 並擷取文字
   - Call OpenAI：呼叫 LLM 生成摘要
   - Format TXT：整理輸出格式
   - Respond to Webhook：回傳結果

3. **OpenAI API**
   - 使用 LLM 進行內容理解與條列摘要