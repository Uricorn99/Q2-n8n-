import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="URL 摘要 → TXT", page_icon="📝")
st.title("📝 丟網址 → 摘要條列")

N8N_WEBHOOK_URL = "https://uricorn99.app.n8n.cloud/webhook/summarize-to-txt"

url = st.text_input("貼上文章網址", placeholder="https://...")

col1, col2 = st.columns([1, 1])
with col1:
    run_btn = st.button("生成摘要", type="primary")

if run_btn:
    if not url.strip():
        st.error("請先輸入網址")
        st.stop()

    with st.spinner("摘要生成中...（可能 10~60 秒）"):
        try:
            res = requests.post(
                N8N_WEBHOOK_URL,
                json={"url": url},
                timeout=180,
            )
        except requests.exceptions.RequestException as e:
            st.error(f"呼叫 n8n 失敗：{e}")
            st.stop()

    if res.status_code != 200:
        st.error(f"n8n 回傳非 200（{res.status_code}）")
        st.code(res.text)
        st.stop()

    raw_text = res.text.strip()
    if not raw_text:
        st.error("n8n 回傳空內容")
        st.stop()

    # ====== 解析 n8n 回傳文字 ======
    lines = raw_text.splitlines()

    parsed_url = ""
    generated_at = ""
    bullets = []

    for line in lines:
        line = line.strip()
        if line.startswith("=URL:"):
            parsed_url = line.replace("=URL:", "").strip()
        elif line.startswith("GeneratedAt:"):
            generated_at = line.replace("GeneratedAt:", "").strip()
        elif line.startswith("-"):
            bullets.append(line)

    bullets_text = "\n".join(bullets)

    # ====== 顯示 ======
    st.success("完成 ✅")

    meta_col1, meta_col2 = st.columns(2)
    with meta_col1:
        st.markdown("**🔗 文章網址**")
        st.write(parsed_url or "（未解析）")

    with meta_col2:
        st.markdown("**🕒 生成時間**")
        st.write(generated_at or "（未解析）")

    st.markdown("### 📌 摘要重點")
    st.text_area(
        label="",
        value=bullets_text,
        height=320
    )

    # 下載 TXT
    st.download_button(
        "⬇️ 下載 TXT",
        data=raw_text,
        file_name="summary.txt",
        mime="text/plain"
    )