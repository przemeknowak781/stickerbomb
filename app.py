import streamlit as st
from PIL import Image
import io
import random
import math

st.set_page_config(page_title="Stickerbomb Generator", layout="wide")
st.title("🎨 Stickerbomb Generator")

# Upload
uploaded_files = st.file_uploader(
    "Wgraj swoje cliparty (PNG z przezroczystością)", 
    type=["png"], 
    accept_multiple_files=True
)

canvas_width = st.slider("Szerokość kolażu (px)", 500, 3000, 1000, step=100)
canvas_height = st.slider("Wysokość kolażu (px)", 500, 3000, 1000, step=100)


def create_stickerbomb_grid(canvas_size, cliparts):
    canvas_w, canvas_h = canvas_size
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))

    num_images = len(cliparts)
    cols = math.ceil(math.sqrt(num_images * canvas_w / canvas_h))
    rows = math.ceil(num_images / cols)

    cell_w = canvas_w // cols
    cell_h = canvas_h // rows

    for i, file in enumerate(cliparts):
        img = Image.open(file).convert("RGBA")

        # Skalowanie z losowym czynnikiem 80–100%
        scale_factor = random.uniform(0.8, 1.0)
        target_w = int(cell_w * scale_factor)
        target_h = int(cell_h * scale_factor)
        img = img.resize((target_w, target_h), Image.LANCZOS)

        # Rotacja ±15 stopni
        angle = random.uniform(-15, 15)
        img = img.rotate(angle, expand=True)

        # Pozycja w siatce
        row = i // cols
        col = i % cols
        x = col * cell_w + random.randint(-10, 10)
        y = row * cell_h + random.randint(-10, 10)

        canvas.alpha_composite(img, dest=(x, y))

    return canvas


if uploaded_files:
    if st.button("🌹 Generuj kolaż ze siatką optymalizacyjną"):
        collage = create_stickerbomb_grid((canvas_width, canvas_height), uploaded_files)

        st.image(collage, caption="Podgląd Stickerbomby", use_column_width=True)

        buf = io.BytesIO()
        collage.save(buf, format="PNG")
        st.download_button(
            "⬇️ Pobierz jako PNG",
            data=buf.getvalue(),
            file_name="stickerbomb.png",
            mime="image/png"
        )
else:
    st.info("Wgraj kilka plików PNG, aby zacząć.")
