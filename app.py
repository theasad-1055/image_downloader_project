import streamlit as st
import pickle
import cv2
from utils import download_image, resize_to_screen
import tempfile
import os

HISTORY_FILE = "history.pkl"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "rb") as f:
            return pickle.load(f)
    return {"last_url": "", "last_filename": "downloaded_image.jpg"}

def save_history(history):
    with open(HISTORY_FILE, "wb") as f:
        pickle.dump(history, f)

# Streamlit UI
st.title("📷 Image Downloader & Viewer")
st.write("Download an image from a URL or local path, view it, and save it.")

history = load_history()

url_or_path = st.text_input("Enter image URL or local path:", history["last_url"])
option = st.selectbox("Choose option:", ["show", "save", "both"])
save_filename = st.text_input("Save file name:", history["last_filename"])

if st.button("Run"):
    if not url_or_path.strip():
        st.error("Please enter a valid URL or file path.")
    else:
        image = download_image(url_or_path)
        if image is None:
            st.error("Failed to load image.")
        else:
            history["last_url"] = url_or_path
            history["last_filename"] = save_filename
            save_history(history)

            if option in ["show", "both"]:
                resized_image = resize_to_screen(image)
                st.image(cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB), caption="Resized Image", use_container_width=True)

            if option in ["save", "both"]:
                cv2.imwrite(save_filename, image)
                st.success(f"Image saved as `{save_filename}`")
