import streamlit as st
from PIL import Image
import io
import random

st.set_page_config(page_title="Stickerbomb Generator", layout="wide")
st.title("🎨 Stickerbomb Generator")

# Upload
uploaded_files = st.file_uploader("Wgraj swoje cliparty (PNG z przezroczystością)", type=["png"], accept_multiple_files=True)

canvas_width = st.slider("Szerokość kolażu (px)", 500, 3000, 1000, step=100)
canvas_height = st.slider("Wysokość kolażu (px)", 500, 3000, 1000, step=100)

if uploaded_files:
    if st.button("🎲 Generuj losowy układ"):
        canvas = Image.new("RGBA", (canvas_width, canvas_height), (0, 0, 0, 0))

        for uploaded_file in uploaded_files:
            img = Image.open(uploaded_file).convert("RGBA")
            scale = random.uniform(0.4, 1.2)
            angle = random.uniform(-30, 30)

            w, h = img.size
            img = img.resize((int(w * scale), int(h * scale)))
            img = img.rotate(angle, expand=True)

            x = random.randint(0, max(1, canvas_width - img.size[0]))
            y = random.randint(0, max(1, canvas_height - img.size[1]))

            canvas.alpha_composite(img, dest=(x, y))

        st.image(canvas, caption="Podgląd Stickerbomby", use_column_width=True)

        buf = io.BytesIO()
        canvas.save(buf, format="PNG")
        st.download_button("⬇️ Pobierz jako PNG", data=buf.getvalue(), file_name="stickerbomb.png", mime="image/png")

else:
    st.info("Wgraj kilka plików PNG, aby zacząć.")
