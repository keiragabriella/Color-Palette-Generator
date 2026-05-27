import streamlit as st
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans


st.set_page_config(
    page_title="Color Palette Generator",
    page_icon="💿",
    layout="centered"
)

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

/* Background */
.stApp {
    background:
        radial-gradient(circle at top left, rgba(255,0,200,0.18), transparent 25%),
        radial-gradient(circle at bottom right, rgba(0,255,255,0.15), transparent 25%),
        linear-gradient(135deg, #070b1a, #0f172a, #050816);
    color: white;
}

/* Main Container */
.main-container {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    backdrop-filter: blur(14px);
    padding: 2.2rem;
    border-radius: 28px;
    box-shadow: 0 0 40px rgba(0,255,255,0.08);
    margin-top: 1rem;
}

/* Title */
.title {
    font-size: 3rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 0.3rem;

    background: linear-gradient(90deg, #ff7de9, #8be9fd, #c4b5fd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #cbd5e1;
    font-size: 1rem;
    margin-bottom: 2rem;
    line-height: 1.7;
}

/* Upload box */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.05);
    border: 1px dashed rgba(255,255,255,0.25);
    padding: 1rem;
    border-radius: 18px;
}

/* Section title */
.section-title {
    font-size: 1.2rem;
    font-weight: 600;
    margin-top: 1rem;
    margin-bottom: 1rem;
    color: #ffffff;
}

/* Palette card */
.palette-card {
    border-radius: 18px;
    height: 120px;
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow:
        0 0 15px rgba(255,255,255,0.08),
        inset 0 0 12px rgba(255,255,255,0.08);
}

/* Hex code */
.hex-code {
    text-align: center;
    margin-top: 0.7rem;
    color: #f8fafc;
    font-weight: 600;
    letter-spacing: 1px;
    font-size: 0.9rem;
}

/* Footer */
.footer {
    text-align: center;
    margin-top: 2rem;
    color: #94a3b8;
    font-size: 0.9rem;
}

/* Remove top spacing */
.block-container {
    padding-top: 2rem;
}

/* Image */
img {
    border-radius: 20px !important;
}

</style>
""", unsafe_allow_html=True)

# FUNCTIONS
def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(
        int(rgb[0]),
        int(rgb[1]),
        int(rgb[2])
    )

def extract_dominant_colors(image, k=5):

    image = image.resize((150, 150))
    image_np = np.array(image)

    pixels = image_np.reshape(-1, 3)

    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    kmeans.fit(pixels)

    colors = kmeans.cluster_centers_

    labels = kmeans.labels_
    counts = np.bincount(labels)

    sorted_indices = np.argsort(counts)[::-1]
    dominant_colors = colors[sorted_indices]

    return dominant_colors

# UI
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.markdown(
    '<div class="title">💿 Color Palette Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    Upload gambar favoritmu dan biarkan algoritma 
    <b>K-Means Clustering</b> mengekstrak 5 warna dominan ✨
    </div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload JPG / PNG",
    type=['jpg', 'jpeg', 'png']
)

# PROCESS IMAGE
if uploaded_file is not None:

    image = Image.open(uploaded_file).convert('RGB')

    st.image(
        image,
        caption='Uploaded Image',
        use_column_width=True
    )

    st.markdown(
        '<div class="section-title">🎨 Extracting Dominant Colors...</div>',
        unsafe_allow_html=True
    )

    with st.spinner("Running K-Means Algorithm..."):

        dominant_colors = extract_dominant_colors(image, k=5)

    st.markdown(
        '<div class="section-title">Your Y2K Palette</div>',
        unsafe_allow_html=True
    )

    cols = st.columns(5)

    for i, color in enumerate(dominant_colors):

        hex_color = rgb_to_hex(color)

        with cols[i]:

            st.markdown(
                f"""
                <div class="palette-card"
                    style="background:{hex_color};">
                </div>

                <div class="hex-code">
                    {hex_color}
                </div>
                """,
                unsafe_allow_html=True
            )

st.markdown(
    '<div class="footer">240086 • Gabriella Marie Keira W</div>',
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)
