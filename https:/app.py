import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import yfinance as yf
import pandas as pd
import urllib.parse
import re
import streamlit.components.v1 as components

st.set_page_config(page_title="Supreme 32 AI Commander", page_icon="⚡", layout="centered")

# सीक्रेट पासवर्ड
MY_PASSWORD = "8899"

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔒 सुप्रीम AI एजेंट लॉगिन")
    pwd = st.text_input("अपना सीक्रेट पासवर्ड दर्ज करें:", type="password")
    if st.button("लॉगिन करें"):
        if pwd == MY_PASSWORD:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("गलत पासवर्ड! कृपया सही पासवर्ड (8899) डालें।")
    st.stop()

st.title("⚡ सुप्रीम 32 AI कमांडर")
st.caption("🔊 बोलकर पूछें व सुनें • 🎨 असली AI फोटो • 🏏 फैंटेसी 2026 • 📈 शेयर मार्केट • 💼 बिजनेस एजेंसी")

# आपकी तीनों चाभियां पहले से सुरक्षित सेट हैं
GROQ_KEY = "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"
GEMINI_KEY = "AQ.Ab8RN6Kx2uNI-EuYt71tUNODmEIC1ySUBZqXhhrChxdVkNPVIw"
GITHUB_TOKEN = "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"

tab1, tab2, tab3 = st.tabs(["💬 वॉयस व ऑल-राउंडर चैट", "🎨 AI फोटो स्टूडियो", "📈 शेयर मार्केट रडार"])

def search_web(query):
    try:
        with DDGS() as ddgs:
            res = list(ddgs.text(query, max_results=4))
            return "\n".join([f"- {r['title']}: {r['body']}" for r in res])
    except Exception:
        return ""

def generate_image_url(prompt):
    clean_p = urllib.parse.quote(prompt.strip())
    return f"https://image.pollinations.ai/prompt/{clean_p}?width=1024&height=1024&nologo=true"

def get_audio_tts_url(text):
    # आवाज में बोलकर सुनाने के लिए टेक्स्ट को साफ करना
    clean = re.sub(r'\[IMAGE:.*?\]', '', text)
    clean = re.sub(r'```.*?```', '', clean, flags=re.DOTALL)
    clean = clean.replace('\n', ' ')[:250].strip()
    encoded = urllib.parse.quote(clean)
    return f"https://translate.google.com/translate_tts?ie=UTF-8&q={encoded}&tl=hi&client=tw-ob"

# TAB 1: मुख्य ऑल-राउंडर वॉयस व चैट
with tab1:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
            if "audio_url" in m:
                st.audio(m["audio_url"])
            if "image_url" in m:
                st.image(m["image_url"], caption="AI जनरेटेड इमेज", use_container_width=True)
            if "html_code" in m:
                st.caption("📱 लाइव इंटरएक्टिव ऐप:")
                components.html(m["html_code"], height=450, scrolling=True)

    user_query = st.chat_input("हुकुम दें भाई (बोलकर या लिखकर)...")

    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            status = st.empty()
            status.text("सुप्रीम कमांडर काम कर रहा है...")
            
            web_info = search_web(user_query)
            
            system_instruction = f"""
तुम यूजर के 100% वफादार, सुप्रीम 32 AI कमांडर हो।
यूजर ज्यादा पढ़ा-लिखा नहीं है, इसलिए तुम्हारा जवाब सरल, देसी, आत्मीय और एकदम स्पष्ट होना चाहिए।

विशेष नियम व शक्तियां:
1. क्रिकेट फैंटेसी: केवल आज की तारीख (2026 सीजन) की आधिकारिक 15-खिलाड़ी स्क्वॉड और टॉस प्लेइंग-11 में से ही टीम चुनो। पुराने रिटायर्ड खिलाड़ी कभी मत डालो। 'बल्लेबाज vs गेंदबाज' हेड-टू-हेड मैच-अप और पिच रिपोर्ट के आधार पर बेस्ट C व VC बताओ।
2. अगर यूजर कोई फोटो, इमेज, पोस्टर या कार्टून मांगे: तो जवाब में यह टैग जरूर लगाओ:
[IMAGE: detailed english prompt for 8k visual generation]
3. अगर यूजर कोई ऐप, गेम या टूल बनाने को कहे: तो पूरा कोड एक ही ```html ... ``` ब्लॉक में लिखो ताकि वह स्क्रीन पर तुरंत लाइव चल सके।
4. ग्राहक व बिजनेस डील्स: ग्राहक से पूरी बातचीत व मोलभाव खुद करो, और जब डील फाइनल करनी हो तो यूजर से 'हरी झंडी' मांगो।
5. शेयर मार्केट: ताजा कीमतें, 52-वीक हाई और स्टॉप-लॉस जरूर बताओ।

लाइव इंटरनेट संदर्भ:
{web_info}
"""
            models_to_try = [
                "openai/gpt-oss-120b",
                "openai/gpt-oss-20b",
                "llama-3.1-8b-instant",
                "llama3-70b-8192",
                "llama3-8b-8192"
            ]

            client = Groq(api_key=GROQ_KEY)
            reply_text = ""
            for model_name in models_to_try:
                try:
                    chat_completion = client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": system_instruction},
                            {"role": "user", "content": user_query}
                        ]
                    )
                    reply_text = chat_completion.choices[0].message.content
                    break
                except Exception:
                    continue
            
            status.empty()
            if reply_text:
                msg_data = {"role": "assistant", "content": reply_text}
                st.markdown(reply_text)
                
                # आवाज में बोलकर सुनाने वाला ऑडियो प्लेयर
                audio_link = get_audio_tts_url(reply_text)
                st.caption("🔊 आवाज में सुनें:")
                st.audio(audio_link)
                msg_data["audio_url"] = audio_link
                
                # क्या इमेज बनानी है?
                img_match = re.search(r'\[IMAGE:\s*(.*?)\]', reply_text)
                if img_match:
                    img_prompt = img_match.group(1)
                    img_url = generate_image_url(img_prompt)
                    st.image(img_url, caption=f"तैयार इमेज: {img_prompt}", use_container_width=True)
                    msg_data["image_url"] = img_url
                
                # क्या कोई लाइव ऐप रेंडर करना है?
                html_match = re.search(r'```html(.*?)```', reply_text, re.DOTALL)
                if html_match:
                    html_code = html_match.group(1).strip()
                    st.caption("📱 लाइव इंटरएक्टिव ऐप:")
                    components.html(html_code, height=450, scrolling=True)
                    msg_data["html_code"] = html_code
                
                st.session_state.messages.append(msg_data)
            else:
                st.error("कृपया 10 सेकंड बाद पुनः प्रश्न पूछें।")

# TAB 2: 1-क्लिक AI फोटो स्टूडियो
with tab2:
    st.subheader("🎨 1-क्लिक AI फोटो स्टूडियो")
    img_idea = st.text_input("कैसी फोटो या कार्टून चाहिए?", placeholder="जैसे: 3D Pixar funny Indian villager Phulena Chacha with red gamcha and sunglasses")
    style = st.selectbox("स्टाइल चुनें:", ["3D Pixar Animation", "Realistic Photo", "Cinematic Film", "Anime / Comic"])
    
    if st.button("🚀 फोटो तैयार करें"):
        if img_idea:
            with st.spinner("फोटो बन रही है..."):
                final_prompt = f"{style} style, {img_idea}, ultra high quality, 8k render, vibrant colors"
                img_gen_url = generate_image_url(final_prompt)
                st.image(img_gen_url, caption=img_idea, use_container_width=True)
                st.markdown(f"[📥 फोटो डाउनलोड करें]({img_gen_url})")
        else:
            st.warning("कृपया बताएं कि कैसी फोटो बनानी है।")

# TAB 3: शेयर मार्केट लाइव चार्ट
with tab3:
    st.subheader("📈 शेयर मार्केट लाइव चार्ट व रडार")
    stock_input = st.text_input("शेयर कोड डालें (जैसे: RELIANCE.NS, TATAMOTORS.NS):", value="RELIANCE.NS")
    if st.button("📊 चार्ट देखें"):
        try:
            with st.spinner("डेटा लोड हो रहा है..."):
                ticker = yf.Ticker(stock_input)
                df = ticker.history(period="1mo")
                if not df.empty:
                    lp = df['Close'].iloc[-1]
                    ch = lp - df['Close'].iloc[-2]
                    st.metric(label=f"{stock_input} ताजा भाव", value=f"₹{lp:.2f}", delta=f"₹{ch:.2f}")
                    st.line_chart(df['Close'])
                else:
                    st.error("शेयर डेटा नहीं मिला।")
        except Exception as e:
            st.error(f"एरर: {e}")
