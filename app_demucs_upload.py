import os
import subprocess
import streamlit as st

st.set_page_config(page_title="Demucs 音訊分離", page_icon="🎧", layout="centered")
st.title("🎧 音訊分離器 (Demucs)")
st.markdown("請上傳一段音樂檔案（mp3 或 wav），系統會使用 [Demucs](https://github.com/facebookresearch/demucs) 自動分離人聲、鼓、貝斯與伴奏。")

uploaded_file = st.file_uploader("🔼 上傳音訊檔案", type=["mp3", "wav"])

if uploaded_file is not None:
    # 儲存上傳的檔案
    os.makedirs("uploads", exist_ok=True)
    input_path = os.path.join("uploads", uploaded_file.name)
    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success(f"✅ 音訊已上傳：{uploaded_file.name}")

    with st.spinner("🪄 Demucs 正在進行音源分離...（請稍候）"):
        try:
            subprocess.run(["demucs", input_path], check=True)
        except FileNotFoundError:
            st.error("❌ 找不到 demucs，請確認已安裝 demucs 套件。")
            st.stop()
        except subprocess.CalledProcessError as e:
            st.error(f"❌ 分離失敗：{e}")
            st.stop()

    st.success("🎉 分離完成！以下是各聲部檔案：")

    # 找出輸出路徑
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_dir = os.path.join("separated", "htdemucs", base_name)

    for part in ["vocals", "drums", "bass", "other"]:
        path = os.path.join(output_dir, f"{part}.wav")
        if os.path.exists(path):
            st.audio(path, format="audio/wav")
            with open(path, "rb") as f:
                st.download_button(f"下載 {part}.wav", f, file_name=f"{part}.wav")
        else:
            st.warning(f"⚠️ 找不到 {part}.wav")
