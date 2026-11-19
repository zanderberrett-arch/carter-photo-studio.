from __future__ import annotations

import io
import streamlit as st
from PIL import Image

from src.config import get_settings
from src.image_ops import apply_adjustments, image_to_png_bytes
from src.ai_editor import edit_image
from src.storage import save_output

st.set_page_config(page_title="CART3R Photo Studio", page_icon="🎨", layout="wide")

st.markdown("""
<style>
.stApp { background: #090909; color: #f4f4f5; }
[data-testid="stSidebar"] { background: #111111; }
h1, h2, h3 { color: #ff4545 !important; }
.stButton button, .stDownloadButton button { border-radius: 10px; }
div[data-testid="stFileUploader"] { border: 1px solid #682020; border-radius: 12px; padding: 12px; }
</style>
""", unsafe_allow_html=True)

st.title("CART3R PHOTO STUDIO")
st.caption("AI photo editing workspace · Local adjustments + prompt-based AI edits")

with st.sidebar:
    st.header("Workspace")
    st.write("Upload a photo, describe the edit, and export the result.")
    st.divider()
    st.subheader("AI settings")
    model = st.selectbox(
        "Image model",
        ["gpt-image-2.5-sunburst", "gpt-image-2.5-flare"],
        index=0,
        help="Choose an available GPT Image model. API usage may incur charges."
    )
    st.caption("AI edits use your OpenAI API account and may incur usage charges.")
    st.divider()
    st.subheader("Local adjustments")
    brightness = st.slider("Brightness", 0.2, 2.0, 1.0, 0.05)
    contrast = st.slider("Contrast", 0.2, 2.0, 1.0, 0.05)
    saturation = st.slider("Saturation", 0.0, 2.0, 1.0, 0.05)
    sharpness = st.slider("Sharpness", 0.0, 3.0, 1.0, 0.05)
    effect = st.selectbox("Color effect", ["None", "Grayscale", "Sepia"])

uploaded = st.file_uploader("Choose a photo", type=["png", "jpg", "jpeg", "webp"])
if "ai_result" not in st.session_state:
    st.session_state.ai_result = None
if "source_bytes" not in st.session_state:
    st.session_state.source_bytes = None

if uploaded:
    try:
        raw = uploaded.getvalue()
        if len(raw) > 20 * 1024 * 1024:
            st.error("Please use an image smaller than 20 MB.")
            st.stop()
        original = Image.open(io.BytesIO(raw)).convert("RGB")
        st.session_state.source_bytes = raw
        adjusted = apply_adjustments(
            original, brightness=brightness, contrast=contrast,
            saturation=saturation, sharpness=sharpness, effect=effect
        )
        left, right = st.columns(2)
        with left:
            st.subheader("Original")
            st.image(original, use_container_width=True)
        with right:
            st.subheader("Local preview")
            st.image(adjusted, use_container_width=True)

        st.divider()
        st.subheader("AI edit")
        prompt = st.text_area(
            "Describe exactly what you want changed",
            placeholder="Example: Replace the background with a clean sunset beach. Keep the person, face, pose, clothing, and framing unchanged.",
            height=110
        )
        preserve = st.checkbox("Ask the AI to preserve everything not mentioned", value=True)
        if st.button("✨ Apply AI edit", type="primary", use_container_width=True):
            if not prompt.strip():
                st.warning("Enter an edit instruction first.")
            else:
                try:
                    settings = get_settings()
                    if not settings.openai_api_key:
                        st.error("OPENAI_API_KEY is missing. Add it to your .env file and restart the app.")
                    else:
                        final_prompt = prompt.strip()
                        if preserve:
                            final_prompt += (
                                "\nPreserve the original subject identity, facial features, pose, "
                                "clothing, camera angle, and all details not explicitly requested to change."
                            )
                        with st.spinner("Editing image with AI. This can take a minute..."):
                            result_bytes = edit_image(
                                image_bytes=image_to_png_bytes(adjusted),
                                prompt=final_prompt,
                                api_key=settings.openai_api_key,
                                model=model,
                            )
                        st.session_state.ai_result = result_bytes
                        st.success("AI edit complete.")
                except Exception as exc:
                    st.error(f"AI edit failed: {exc}")

        if st.session_state.ai_result:
            st.divider()
            st.subheader("AI result")
            result_image = Image.open(io.BytesIO(st.session_state.ai_result)).convert("RGB")
            st.image(result_image, use_container_width=True)
            filename = save_output(st.session_state.ai_result)
            st.caption(f"Saved a copy to: {filename}")
            st.download_button(
                "Download edited photo",
                data=st.session_state.ai_result,
                file_name="edited-photo.png",
                mime="image/png",
                use_container_width=True
            )

        st.divider()
        st.subheader("Export local adjustments")
        adjusted_bytes = image_to_png_bytes(adjusted)
        st.download_button(
            "Download local preview",
            data=adjusted_bytes,
            file_name="adjusted-photo.png",
            mime="image/png",
            use_container_width=True
        )
    except Exception as exc:
        st.error(f"Could not open this image: {exc}")
else:
    st.info("Upload a photo to begin. You can use local adjustments without an API key; prompt-based AI edits require one.")

st.caption("CART3R.JAILBREAK · Python Code Lab · v1.0.0")
