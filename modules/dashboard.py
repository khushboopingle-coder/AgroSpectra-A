"""
AgroSpectra AI — Executive Dashboard
Agricultural intelligence, satellite remote sensing and photogrammetry.
"""

import base64
import io
import textwrap
from pathlib import Path

import streamlit as st
import plotly.graph_objects as go
from PIL import Image

from config import (
    KEY_METRICS,
    DISCLOSURES,
    DASHBOARD_IMG_PATH,
    EUROSAT_CLASSES,
    ASSETS_DIR,
)


def html(block: str) -> None:
    """Render HTML safely. Removes indentation so Markdown never treats it as a code block."""
    cleaned = "\n".join(line.strip() for line in textwrap.dedent(block).splitlines() if line.strip())
    st.markdown(cleaned, unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def _image_data_uri(path: str) -> str:
    """Embed local image as an optimized data URI for fast, crisp browser rendering."""
    p = Path(path)
    if not p.exists():
        return ""
    try:
        with Image.open(p) as img:
            buf = io.BytesIO()
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            # Shrink big photos so the page loads fast
            img.thumbnail((1600, 1600))
            img.save(buf, format="JPEG", quality=92, optimize=True)
            encoded = base64.b64encode(buf.getvalue()).decode()
            return f"data:image/jpeg;base64,{encoded}"
    except Exception:
        mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
        return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def _find_hero_image():
    """Finds the hero farmland aerial image using project-relative resolution."""
    candidates = [
        ASSETS_DIR / "farmland_aerial.png",
        ASSETS_DIR / "farmland_aerial.jpg",
        Path("assets/farmland_aerial.png").resolve(),
        Path("assets/farmland_aerial.jpg").resolve(),
    ]
    return next((p for p in candidates if p.exists()), None)


def render_hero() -> None:
    """Renders the responsive aerial farmland hero banner at the top of the dashboard."""
    hero_image = _find_hero_image()

    if hero_image and hero_image.exists():
        data_uri = _image_data_uri(str(hero_image))
        if data_uri:
            overlay = "linear-gradient(90deg, rgba(16, 40, 25, 0.85) 0%, rgba(16, 40, 25, 0.45) 55%, rgba(16, 40, 25, 0.12) 100%)"
            html(f"""
                <div class="hero-banner" style="background-image: {overlay}, url('{data_uri}'); background-size: cover, cover; background-position: center 48%, center 48%; background-repeat: no-repeat, no-repeat;">
                    <div class="hero-eyebrow">Earth Observation & Precision Agriculture</div>
                    <div class="hero-title">AgroSpectra AI</div>
                    <div class="hero-description">Intelligent Agriculture. Powered by AI.</div>
                </div>
            """)
            return

    # Graceful fallback if image is missing: elegant forest-to-sage gradient card
    html("""
        <div class="hero-banner" style="background: linear-gradient(135deg, #16301F 0%, #254D38 50%, #2F6B3F 100%);">
            <div class="hero-eyebrow">Earth Observation & Precision Agriculture</div>
            <div class="hero-title">AgroSpectra AI</div>
            <div class="hero-description">Intelligent Agriculture. Powered by AI.</div>
        </div>
    """)


def render_dashboard():
    """Render the AgroSpectra AI executive dashboard."""

    # 1. Aerial hero (photo is now the actual banner background)
    render_hero()

    html("""
        <div class="hero-header">
            <h2 style="font-size:1.65rem; margin-bottom:5px;">Your Agricultural Intelligence Workspace</h2>
            <div class="hero-subtitle">
                Monitor land-cover categories, explore vegetation indices and inspect
                3D reconstruction results. Pick a tool from the sidebar to begin.
            </div>
        </div>
    """)

    # 2. Scientific transparency
    html(f"""
        <div class="disclosure-banner">
            <div class="disclosure-title">&#9432; Scientific transparency</div>
            <strong>Crop classification evaluation:</strong> {DISCLOSURES['crop_accuracy']}<br>
            <strong>3D reconstruction dataset:</strong> {DISCLOSURES['point_cloud_origin']}<br><br>
            Results depend on the input data, model and processing conditions. Review dataset
            details before treating outputs as farm-specific findings.
        </div>
    """)

    # 3. Key metrics
    st.markdown("### Platform at a glance")
    st.caption("The configured model, land-cover categories, vegetation analysis and 3D reconstruction.")

    metrics = [
        ("MODEL TEST ACCURACY", str(KEY_METRICS["test_accuracy"]), "EuroSAT test split (5,400 images)"),
        ("LAND-COVER CLASSES", f'{KEY_METRICS["num_classes"]} classes', "Land-use and land-cover categories"),
        ("VEGETATION ANALYSIS", "NDVI", "Red B04 + near-infrared B08"),
        ("RECONSTRUCTED 3D POINTS", str(KEY_METRICS["photogrammetry_points"]), "COLMAP point-cloud output"),
    ]
    for column, (label, value, description) in zip(st.columns(4), metrics):
        with column:
            html(f"""
                <div class="metric-box">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-sub">{description}</div>
                </div>
            """)

    st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)

    # 4. Model evaluation and land-cover chart
    left_col, right_col = st.columns([1.05, 0.95], gap="large")

    with left_col:
        html(f"""
            <div class="nature-card">
                <h3 style="margin-top:0;">Model Evaluation</h3>
                <p>The CNN was evaluated on the separate EuroSAT test split, which it never saw during training.</p>
                <p style="margin-bottom:4px;"><strong>Test accuracy:</strong> {KEY_METRICS['test_accuracy']}</p>
                <p style="margin-bottom:4px;"><strong>Correct predictions:</strong> 5,044 of 5,400 images</p>
                <p style="margin-bottom:4px;"><strong>Land-cover classes tested:</strong> all {KEY_METRICS['num_classes']}</p>
                <p style="margin-bottom:0;">Open <strong>AI Crop Classification</strong> in the sidebar to see the full confusion matrix.</p>
            </div>
        """)

    with right_col:
        html("""
            <div class="nature-card">
                <h3 style="margin-top:0;">Land-Cover Categories</h3>
                <p>The EuroSAT categories used to train and evaluate the classifier.</p>
            </div>
        """)
        configured_classes = (
            list(EUROSAT_CLASSES) if EUROSAT_CLASSES else [
                "Annual Crop", "Permanent Crop", "Forest", "Herbaceous Vegetation", "Pasture",
                "Highway", "Industrial", "Residential", "River", "Sea and Lake",
            ]
        )
        fig = go.Figure(go.Bar(
            x=[1] * len(configured_classes),
            y=configured_classes,
            orientation="h",
            marker=dict(color="#2F6B3F", line=dict(width=0)),
            hovertemplate="%{y}<extra></extra>",
        ))
        fig.update_layout(
            height=max(300, len(configured_classes) * 30),
            margin=dict(l=5, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            xaxis=dict(visible=False, range=[0, 1.05]),
            yaxis=dict(autorange="reversed", tickfont=dict(size=12, color="#16301F")),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Equal bar lengths are illustrative. They do not show sample counts, class frequency or model performance.")

    # 5. Feature guide
    st.markdown("---")
    st.markdown("### Explore the platform")
    st.caption("Choose a feature from the sidebar. Each tool may need a different input dataset.")

    features = [
        ("🌾", "AI Crop Classification", "Upload a supported image to predict its land-cover category with the trained model."),
        ("🌱", "Vegetation Health (NDVI)", "Explore vegetation greenness using red and near-infrared satellite bands."),
        ("🛰️", "Satellite Remote Sensing", "See how satellite imagery supports land-cover and agricultural monitoring."),
        ("📐", "3D Photogrammetry", "Explore point clouds reconstructed from overlapping photographs of one scene."),
        ("📊", "Executive Dashboard", "Review project metrics and experiment artifacts in one place."),
        ("📚", "Scientific Methods", "Read about the models, datasets, evaluation methods and limitations."),
    ]
    for start in range(0, len(features), 3):
        for column, (icon, title, description) in zip(st.columns(3, gap="medium"), features[start:start + 3]):
            with column:
                html(f"""
                    <div class="feature-card">
                        <div class="feature-icon">{icon}</div>
                        <div class="feature-title">{title}</div>
                        <div class="feature-description">{description}</div>
                    </div>
                """)
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # 6. Milestones
    st.markdown("---")
    st.markdown("### Project milestones")

    milestones = [
        ("Crop classifier", "CNN image classification",
         "A trained CNN, evaluated on the 5,400-image EuroSAT test split across all 10 classes.",
         "Review the reported evaluation before relying on predictions."),
        ("Vegetation analysis", "Sentinel-2 NDVI",
         "NDVI uses red and near-infrared reflectance to assess greenness.",
         "Use compatible, correctly aligned satellite bands."),
        ("3D reconstruction", "COLMAP photogrammetry",
         "Structure-from-Motion estimates camera poses and rebuilds scene geometry.",
         "Images must show the same scene with enough overlap."),
    ]
    for column, (heading, title, description, note) in zip(st.columns(3, gap="medium"), milestones):
        with column:
            html(f"""
                <div class="nature-card-sm">
                    <div class="metric-label">{heading.upper()}</div>
                    <div class="feature-title">{title}</div>
                    <div class="feature-description">{description}</div>
                    <p style="font-size:0.82rem; margin-top:12px;"><strong>Note:</strong> {note}</p>
                </div>
            """)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    html("""
        <div class="disclosure-banner">
            <div class="disclosure-title">Responsible interpretation</div>
            Satellite land-cover classification, NDVI analysis and 3D reconstruction have different
            data requirements. A displayed metric alone does not establish the health or
            productivity of a particular farm.
        </div>
    """)
