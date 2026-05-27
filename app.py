import streamlit as st
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

st.set_page_config(page_title="Color Palette Generator", page_icon="🎨", layout="centered")

st.markdown("""
    <style>
    /* Mengatur jarak dan font agar lebih clean */
    h1 {
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
        color: #2c3e50;
        margin-bottom: -10px;
    }
    
    .subtitle {
        text-align: center;
        color: #7f8c8d;
        font-size: 16px;
        margin-bottom: 30px;
    }

    /* Efek hover dan bayangan pada kartu warna */
    .color-card {
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 130px;
        width: 100%;
        display: flex;
        align-items: flex-end;
        justify-content: center;
        padding-bottom: 12px;
        margin-bottom: 10px;
        cursor: pointer;
    }
    
    .color-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 25px rgba(0,0,0,0.15);
    }
    
    /* Label teks di dalam warna */
    .hex-label {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 6px 12px;
        border-radius: 20px;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        color: #2c3e50;
        font-size: 14px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

@st.cache_data 
def extract_dominant_colors(image_np, k=5):
    pixels = image_np.reshape(-1, 3)
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(pixels)
    colors = kmeans.cluster_centers_
    labels = kmeans.labels_
    counts = np.bincount(labels)
    sorted_indices = np.argsort(counts)[::-1]
    return colors[sorted_indices]

st.markdown("<h1>Aesthetic Palette</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Ekstrak warna dominan dari gambar favoritmu menggunakan K-Means Clustering</div>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Unggah gambar (JPG/PNG)", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    
    st.image(image, use_column_width=True)
    st.write("---")
    
    with st.spinner("✨ Memproses sentroid algoritma..."):
        resized_image = image.resize((150, 150))
        image_np = np.array(resized_image)
        
        dominant_colors = extract_dominant_colors(image_np, k=5)
        
        st.markdown("<h3 style='text-align: center; color: #34495e; margin-bottom: 25px;'>5 Palet Warna Teratas</h3>", unsafe_allow_html=True)
        
        cols = st.columns(5)
        
        for i, color in enumerate(dominant_colors):
            hex_color = rgb_to_hex(color)
            with cols[i]:
                st.markdown(
                    f"""
                    <div class="color-card" style="background-color: {hex_color};">
                        <span class="hex-label">{hex_color}</span>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("Tugas Artificial Intelligence - Pertemuan 11 | Gabriella Marie Keira Wibawa | 140810240086")
