import streamlit as st
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans


st.set_page_config(page_title="Color Palette Generator", page_icon="🎨", layout="centered")

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def extract_dominant_colors(image, k=5):

    image = image.resize((150, 150))
    image_np = np.array(image)
    
    pixels = image_np.reshape(-1, 3)
    
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(pixels)
    
    colors = kmeans.cluster_centers_
    
    labels = kmeans.labels_
    counts = np.bincount(labels)
    
    sorted_indices = np.argsort(counts)[::-1]
    dominant_colors = colors[sorted_indices]
    
    return dominant_colors


st.title("K-Means Color Palette Generator")
st.write("Website ini mengekstrak 5 warna paling dominan dari sebuah gambar menggunakan algoritma **K-Means Clustering**.")

uploaded_file = st.file_uploader("Unggah gambar Anda di sini (JPG/PNG)", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption='Gambar yang diunggah', use_column_width=True)
    
    st.write("---")
    st.subheader("Menghitung Warna Dominan...")
    
    with st.spinner("Algoritma K-Means sedang berjalan..."):
        dominant_colors = extract_dominant_colors(image, k=5)
        
        st.subheader("🎨 5 Palet Warna Dominan:")
        
        cols = st.columns(5)
        
        for i, color in enumerate(dominant_colors):
            hex_color = rgb_to_hex(color)
            with cols[i]:
                st.markdown(
                    f"""
                    <div style="
                        background-color: {hex_color};
                        height: 100px;
                        border-radius: 10px;
                        margin-bottom: 10px;
                        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
                    "></div>
                    """, 
                    unsafe_allow_html=True
                )
                st.code(hex_color)

st.caption("Tugas Artificial Intelligence - Pertemuan 11")