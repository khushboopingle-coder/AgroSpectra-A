"""
AgroSpectra AI - Main Streamlit Application Entrypoint
A nature-inspired, scientific geospatial and photogrammetry application.
"""

import streamlit as st

# Configure page layout and title
st.set_page_config(
    page_title="AgroSpectra AI — Geospatial Crop Intelligence & 3D Photogrammetry",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply nature-inspired design system
from styles import apply_custom_styles
st.markdown(apply_custom_styles(), unsafe_allow_html=True)

# Import feature modules
from modules.dashboard import render_dashboard
from modules.classifier import render_classifier
from modules.vegetation import render_vegetation_health
from modules.reconstruction import render_3d_reconstruction
from modules.about import render_about
from config import KEY_METRICS, MODEL_PATH, POINT_CLOUD_PATH


def main():
    # Sidebar Navigation & Branding
    with st.sidebar:
        st.markdown("""
        <div style="padding: 10px 0 16px 0; border-bottom: 1px solid #E5DFD7; margin-bottom: 16px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 1.6rem;">🌿</span>
                <div>
                    <h2 style="margin: 0; font-size: 1.35rem; color: #1B3B2B; line-height: 1.15;">AgroSpectra AI</h2>
                    <span style="font-size: 0.76rem; color: #6B7D74; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em;">
                        Satellite & 3D Vision
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Primary Navigation
        navigation_options = [
            "Executive Dashboard",
            "AI Crop Classification",
            "Vegetation Health (NDVI)",
            "3D Photogrammetry Viewer",
            "About & Scientific Methods"
        ]

        icons = {
            "Executive Dashboard": "📊",
            "AI Crop Classification": "🌾",
            "Vegetation Health (NDVI)": "🌱",
            "3D Photogrammetry Viewer": "📐",
            "About & Scientific Methods": "📖"
        }

        selected_page = st.radio(
            "Navigation:",
            navigation_options,
            format_func=lambda x: f"{icons.get(x, '•')}  {x}",
            label_visibility="collapsed"
        )

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("<div class='nature-divider'></div>", unsafe_allow_html=True)

        # Sidebar Telemetry & System Status
        st.markdown("""
        <div style="font-size: 0.76rem; font-weight: 700; text-transform: uppercase; color: #52796F; letter-spacing: 0.06em; margin-bottom: 8px;">
            Verified Model Telemetry
        </div>
        """, unsafe_allow_html=True)

        model_loaded = MODEL_PATH.exists()
        ply_loaded = POINT_CLOUD_PATH.exists()

        st.markdown(f"""
        <div style="font-size: 0.82rem; color: #34423D; line-height: 1.5; background: #FFFFFF; border: 1px solid #E5DFD7; border-radius: 8px; padding: 12px;">
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                <span>EuroSAT Test Acc:</span>
                <strong style="color:#2B8A3E;">{KEY_METRICS['test_accuracy']}</strong>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                <span>Classes:</span>
                <strong>{KEY_METRICS['num_classes']} Classes</strong>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                <span>Sentinel-2 NDVI:</span>
                <span class="pill-badge pill-success" style="padding:1px 6px; font-size:0.7rem;">Active</span>
            </div>
            <div style="display:flex; justify-content:space-between;">
                <span>3D Reconstructed:</span>
                <strong>{KEY_METRICS['photogrammetry_points']} pts</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

        # Scientific Transparency Footnote
        st.markdown("""
        <div style="font-size: 0.74rem; color: #757B69; line-height: 1.4; border-top: 1px solid #E5DFD7; padding-top: 12px;">
            <strong>AgroSpectra AI Platform</strong><br>
            Multi-modal remote sensing, Keras deep learning, and COLMAP photogrammetry.<br>
            <span style="color:#96AF9F;">Designed for precision agricultural analysis.</span>
        </div>
        """, unsafe_allow_html=True)

    # Route to selected page
    if selected_page == "Executive Dashboard":
        render_dashboard()
    elif selected_page == "AI Crop Classification":
        render_classifier()
    elif selected_page == "Vegetation Health (NDVI)":
        render_vegetation_health()
    elif selected_page == "3D Photogrammetry Viewer":
        render_3d_reconstruction()
    elif selected_page == "About & Scientific Methods":
        render_about()


if __name__ == "__main__":
    main()
