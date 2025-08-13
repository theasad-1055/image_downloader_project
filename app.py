import streamlit as st
import cv2
import requests
import numpy as np
import tempfile

def download_image(source):
    """Download image from URL or load from local path."""
    source = source.strip().strip('"').strip("'")
    if source.startswith("http://") or source.startswith("https://"):
        try:
            headers = {"User-Agent": "ImageDownloader/1.0"}
            response = requests.get(source, headers=headers, stream=True, timeout=15)
            response.raise_for_status()
            image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            if image is None:
                raise ValueError("Downloaded data is not a valid image")
            return image
        except Exception as e:
            st.error(f"Error downloading image: {e}")
            return None
    else:
        try:
            image = cv2.imread(source)
            if image is None:
                st.error("Local file not found or not a valid image.")
            return image
        except Exception as e:
            st.error(f"Error reading local file: {e}")
            return None

st.title("📷 Image Downloader")
source = st.text_input("Enter image URL or local path:")
option = st.selectbox("Choose option:", ["show", "save", "both"])

if st.button("Process"):
    if not source:
        st.warning("Please enter an image URL or path.")
    else:
        image = download_image(source)
        if image is not None:
            if option in ["show", "both"]:
                st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), channels="RGB")

            if option in ["save", "both"]:
                # Save to a temporary file so Streamlit can provide it for download
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
                cv2.imwrite(temp_file.name, image)
                with open(temp_file.name, "rb") as f:
                    st.download_button(
                        label="⬇️ Download Image",
                        data=f,
                        file_name="downloaded_image.jpg",
                        mime="image/jpeg"
                    )
