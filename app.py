import streamlit as st
from PIL import Image
import io
import random
import math

st.set_page_config(page_title='Stickerbomb Generator', layout='wide')
st.title('🎨 Stickerbomb Generator')

# Upload clipart files (PNG with transparency)
uploaded_files = st.file_uploader(
    'Upload your cliparts (PNG with transparency)',
    type=['png'],
    accept_multiple_files=True
)

# Canvas dimensions sliders
canvas_width = st.slider('Collage Width (px)', 500, 3000, 1000, step=100)
canvas_height = st.slider('Collage Height (px)', 500, 3000, 1000, step=100)


def create_stickerbomb_grid(canvas_size, cliparts):
    """
    Creates a stickerbomb collage by placing cliparts in a grid pattern.
    Applies random scaling, rotation, and small positional offsets.
    Adjusted parameters to encourage more overlap and reduce visible background.

    Args:
        canvas_size (tuple): A tuple (width, height) for the canvas size.
        cliparts (list): A list of file-like objects (uploaded files).

    Returns:
        PIL.Image.Image: The generated stickerbomb image.
    """
    canvas_w, canvas_h = canvas_size
    # Create a new transparent canvas
    canvas = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))

    num_images = len(cliparts)
    # Calculate grid dimensions based on the number of images and canvas aspect ratio
    cols = math.ceil(math.sqrt(num_images * canvas_w / canvas_h))
    rows = math.ceil(num_images / cols)

    # Calculate cell size for each image in the grid
    cell_w = canvas_w // cols
    cell_h = canvas_h // rows

    # Process and place each clipart
    for i, file in enumerate(cliparts):
        # Open and ensure image is RGBA
        img = Image.open(file).convert('RGBA')

        # Scale with a random factor (increased range: 70-110%) relative to cell size
        scale_factor = random.uniform(0.7, 1.1) # Increased range
        target_w = int(cell_w * scale_factor)
        target_h = int(cell_h * scale_factor)
        # Resize using LANCZOS filter for quality
        img = img.resize((target_w, target_h), Image.LANCZOS)

        # Rotate by a random angle (±15 degrees)
        angle = random.uniform(-15, 15)
        # Rotate image, expanding canvas to fit rotated image
        img = img.rotate(angle, expand=True)

        # Calculate grid position
        row = i // cols
        col = i % cols

        # Calculate base position within the cell and add increased random offset (±20)
        x = col * cell_w + random.randint(-20, 20) # Increased offset
        y = row * cell_h + random.randint(-20, 20) # Increased offset

        # Composite the processed image onto the canvas
        canvas.alpha_composite(img, dest=(x, y))

    return canvas

# Main application logic
if uploaded_files:
    # Button to generate the collage
    if st.button('🌹 Generate Collage with Optimization Grid'):
        # Create the stickerbomb collage
        collage = create_stickerbomb_grid((canvas_width, canvas_height), uploaded_files)

        # Display the generated image preview
        st.image(collage, caption='Stickerbomb Preview', use_column_width=True)

        # Prepare image for download
        buf = io.BytesIO()
        collage.save(buf, format='PNG')
        # Provide download button
        st.download_button(
            '⬇️ Download as PNG',
            data=buf.getvalue(),
            file_name='stickerbomb.png',
            mime='image/png'
        )
else:
    # Info message when no files are uploaded
    st.info('Upload some PNG files to get started.')
