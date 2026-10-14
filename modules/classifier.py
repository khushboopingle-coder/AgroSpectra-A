"""
AgroSpectra AI - Crop Classification Module
Uses trained Keras CNN model on EuroSAT 10 classes with confidence analytics.
"""

from pathlib import Path
import glob
import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

from config import (
    MODEL_PATH, EUROSAT_CLASSES, CLASS_DESCRIPTIONS, DISCLOSURES,
    CROPS_DIR, ASSETS_DIR, PALETTE
)
from utils.model_loader import predict_crop, load_crop_model


def render_classifier():
    """Renders the AI Crop Classification interface."""
    st.markdown("""
    <div class="hero-header">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
            <span class="pill-badge">Deep Learning Inference</span>
            <span class="pill-badge pill-success">EuroSAT 10 Classes</span>
        </div>
        <h1 style="margin: 0; font-size: 2.3rem;">AI Crop & Land-Cover Classification</h1>
        <div class="hero-subtitle">
            Classify multi-spectral satellite imagery patches using a trained deep convolutional neural network 
            calibrated for European agricultural land-cover monitoring.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Scientific Disclosure
    st.markdown(f"""
    <div class="disclosure-banner">
        <div class="disclosure-title">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="16" x2="12" y2="12"></line>
                <line x1="12" y1="8" x2="12.01" y2="8"></line>
            </svg>
            Model Verification Notice
        </div>
        {DISCLOSURES['crop_accuracy']} Model inputs are preprocessed to 64×64 pixels and normalized to [0, 1].
    </div>
    """, unsafe_allow_html=True)

    # Check model existence
    if not MODEL_PATH.exists():
        st.error(f"Model file not found at {MODEL_PATH}. Please ensure `agrospectra_crop_model.keras` is in the project folder.")
        return

    # Two column layout: Input on Left, Results on Right
    left_col, right_col = st.columns([1.0, 1.2])

    selected_image = None
    image_name = "Sample"

    with left_col:
        st.markdown("""
        <div class="nature-card">
            <h3 style="margin-top:0; margin-bottom: 8px;">Select or Upload Image</h3>
            <p style="color:var(--text-secondary); font-size:0.86rem; margin-bottom:14px;">
                Choose an image from our verified test set or upload your own satellite/aerial photo.
            </p>
        """, unsafe_allow_html=True)

        input_mode = st.radio(
            "Input Mode:",
            ["Preset Test Images", "Upload Custom Image"],
            horizontal=True,
            label_visibility="collapsed"
        )

        if input_mode == "Preset Test Images":
            crop_files = sorted(list(CROPS_DIR.glob("*.png")))
            if crop_files:
                sample_labels = {
                    crop_files[0].name: "Test Image 1 (Annual Crop)",
                    crop_files[1].name: "Test Image 2 (Annual Crop)",
                    crop_files[2].name: "Test Image 3 (Annual Crop)",
                    crop_files[3].name: "Test Image 4 (Forest / Woodland)",
                    crop_files[4].name: "Test Image 5 (Annual Crop)",
                }
                
                selected_filename = st.selectbox(
                    "Choose benchmark satellite patch:",
                    options=[f.name for f in crop_files],
                    format_func=lambda x: sample_labels.get(x, x)
                )

                chosen_path = CROPS_DIR / selected_filename
                selected_image = Image.open(str(chosen_path))
                image_name = sample_labels.get(selected_filename, selected_filename)

                # Show preview
                st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                st.image(
                    selected_image.resize((256, 256), Image.Resampling.NEAREST),
                    caption=f"{image_name} (Rescaled 256×256 preview from 64×64 native)",
                    use_container_width=True
                )
            else:
                st.warning("No preset test images found in sample_data/crops.")

        else:
            uploaded_file = st.file_uploader(
                "Upload Satellite Patch (PNG, JPG, TIFF):",
                type=["png", "jpg", "jpeg", "tif", "tiff", "webp"],
                help="Recommended: 64x64 or higher resolution aerial/satellite patch."
            )
            if uploaded_file is not None:
                try:
                    selected_image = Image.open(uploaded_file)
                    image_name = uploaded_file.name
                    st.image(
                        selected_image.resize((256, 256), Image.Resampling.NEAREST),
                        caption=f"Uploaded: {image_name}",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Error opening uploaded image: {e}")

        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        st.markdown("""
        <div class="nature-card">
            <h3 style="margin-top:0; margin-bottom: 8px;">Inference & Confidence Scoring</h3>
            <p style="color:var(--text-secondary); font-size:0.86rem; margin-bottom:14px;">
                Real-time neural network predictions computed through the 10 EuroSAT softmax logits.
            </p>
        """, unsafe_allow_html=True)

        if selected_image is not None:
            with st.spinner("Executing neural inference..."):
                try:
                    res = predict_crop(selected_image)
                    top_class = res["top_class"]
                    top_conf = res["top_confidence"]
                    all_preds = res["all_predictions"]

                    # Result Card
                    conf_color = "#2B8A3E" if top_conf > 80 else ("#D97706" if top_conf > 50 else "#DC2626")
                    st.markdown(f"""
                    <div style="background: linear-gradient(145deg, #FFFFFF, #F6FAF7); border: 1px solid var(--warm-border); border-left: 4px solid {conf_color}; border-radius: var(--radius-sm); padding: 18px; margin-bottom: 18px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                            <span style="font-size:0.78rem; font-weight:700; text-transform:uppercase; color:var(--text-muted); letter-spacing:0.06em;">Primary AI Detection</span>
                            <span class="pill-badge" style="background:{conf_color}18; color:{conf_color}; border-color:{conf_color}40; font-size:0.8rem;">
                                {top_conf:.2f}% Confidence
                            </span>
                        </div>
                        <div style="font-family:'Lora',serif; font-size:1.9rem; font-weight:600; color:var(--forest-deep); margin-bottom:8px;">
                            {top_class}
                        </div>
                        <div style="font-size:0.85rem; color:var(--text-secondary); line-height:1.45;">
                            {CLASS_DESCRIPTIONS.get(top_class, "Detected land cover category.")}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Plain-English summary
                    st.info(f"In simple words: the model is **{top_conf:.1f}% sure** this photo shows **{top_class}**.")
                    if top_conf > 99.9:
                        st.caption("100% means the model is very confident. It does not guarantee the answer is correct.")

                    # Confidence Distribution Horizontal Bar Chart
                    st.markdown("<strong style='font-size:0.88rem; color:var(--forest-deep);'>Class Confidence Distribution:</strong>", unsafe_allow_html=True)
                    st.caption("The model shares 100 points between the land types. The longest bar is its answer.")
                    
                    df_plot = [
                        {"Class": p["class"], "Confidence": p["confidence"]}
                        for p in all_preds[:5] # Top 5 classes
                    ]
                    df_plot.reverse() # For correct vertical top-down order in Plotly

                    fig_bar = go.Figure(go.Bar(
                        x=[p["Confidence"] for p in df_plot],
                        y=[p["Class"] for p in df_plot],
                        orientation='h',
                        marker=dict(
                            color=[
                                conf_color if p["Class"] == top_class else "#8FA998"
                                for p in df_plot
                            ]
                        ),
                        text=[f"{p['Confidence']:.1f}%" for p in df_plot],
                        textposition="outside",
                        cliponaxis=False
                    ))
                    fig_bar.update_layout(
                        margin=dict(l=10, r=45, t=10, b=10),
                        height=210,
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        xaxis=dict(
                            range=[0, max(100, max([p["Confidence"] for p in df_plot]) * 1.15)],
                            showgrid=True,
                            gridcolor="#E5DFD7",
                            tickfont=dict(size=10, color="#6B7D74")
                        ),
                        yaxis=dict(tickfont=dict(size=11, color="#1A2520"))
                    )
                    # staticPlot stops users from dragging/zooming the chart
                    st.plotly_chart(fig_bar, use_container_width=True, config={"staticPlot": True})

                    # Full breakdown expander
                    with st.expander("View All 10 Class Probabilities"):
                        for p in all_preds:
                            st.write(f"- **{p['class']}**: `{p['confidence']:.3f}%` (prob: `{p['probability']:.5f}`)")

                except Exception as ex:
                    st.error(f"Inference error: {ex}")
        else:
            st.info("Please select or upload an image to view predictions.")

        st.markdown("</div>", unsafe_allow_html=True)

    # Technical Details & Model Evaluation Insights
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown("### Model Diagnostics & Training Architecture")

    tab1, tab2 = st.tabs(["Confusion Matrix & Evaluation", "Model Architecture Specifications"])

    with tab1:
        st.markdown("""
        <div class="nature-card-sm">
            <h4 style="margin-top:0; margin-bottom:8px;">EuroSAT Confusion Matrix Evaluation</h4>
            <p style="color:var(--text-secondary); font-size:0.86rem; margin-bottom:14px;">
                Evaluated on the separate 5,400-image EuroSAT test split, which the model never saw during training. 
                The model got <strong>5,044 of 5,400 correct (93.41%)</strong>. 
                The test set covers all 10 land-cover classes. 
                The most common mix-up was Herbaceous Vegetation predicted as Permanent Crop (42 images), 
                two land types that look similar from above.
            </p>
        """, unsafe_allow_html=True)

        cm_path = ASSETS_DIR / "confusion_matrix.png"
        if cm_path.exists():
            cm_img = Image.open(str(cm_path))
            st.image(cm_img, caption="AgroSpectra AI - Confusion Matrix (5,400-image test split, all 10 EuroSAT classes)", use_container_width=True)
        else:
            st.info("Confusion matrix asset not found.")

        # Simple explanation
        st.caption("This is a fixed report card. It was made once on test images, so it does not change when you pick a different photo above.")
        with st.expander("How to read this table"):
            st.markdown(
                "- **Each row** is the real land type.\n"
                "- **Each column** is what the model guessed.\n"
                "- **The diagonal** (top-left to bottom-right) shows correct answers. Bigger numbers there are better.\n"
                "- **Any number outside the diagonal** is a mistake. Example: a 42 in the *Herbaceous Vegetation* row and *Permanent Crop* column means 42 grassland photos were wrongly called Permanent Crop."
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class="nature-card-sm">
            <h4 style="margin-top:0; margin-bottom:8px;">Keras CNN Architecture Layers</h4>
            <table style="width:100%; font-size:0.86rem; border-collapse:collapse; color:var(--text-primary);">
                <tr style="border-bottom:1px solid var(--warm-border); text-align:left;">
                    <th style="padding:6px;">Layer Type</th>
                    <th style="padding:6px;">Output Shape</th>
                    <th style="padding:6px;">Parameters</th>
                </tr>
                <tr style="border-bottom:1px solid var(--warm-border);">
                    <td style="padding:6px;">RandomFlip (training only)</td>
                    <td style="padding:6px;">(64, 64, 3)</td>
                    <td style="padding:6px;">0</td>
                </tr>
                <tr style="border-bottom:1px solid var(--warm-border);">
                    <td style="padding:6px;">RandomRotation (training only)</td>
                    <td style="padding:6px;">(64, 64, 3)</td>
                    <td style="padding:6px;">0</td>
                </tr>
                <tr style="border-bottom:1px solid var(--warm-border);">
                    <td style="padding:6px;">Conv2D (32 filters, 3×3)</td>
                    <td style="padding:6px;">(64, 64, 32)</td>
                    <td style="padding:6px;">896</td>
                </tr>
                <tr style="border-bottom:1px solid var(--warm-border);">
                    <td style="padding:6px;">BatchNormalization</td>
                    <td style="padding:6px;">(64, 64, 32)</td>
                    <td style="padding:6px;">128</td>
                </tr>
                <tr style="border-bottom:1px solid var(--warm-border);">
                    <td style="padding:6px;">MaxPooling2D (2×2)</td>
                    <td style="padding:6px;">(32, 32, 32)</td>
                    <td style="padding:6px;">0</td>
                </tr>
                <tr style="border-bottom:1px solid var(--warm-border);">
                    <td style="padding:6px;">Conv2D (64 filters, 3×3)</td>
                    <td style="padding:6px;">(32, 32, 64)</td>
                    <td style="padding:6px;">18,496</td>
                </tr>
                <tr style="border-bottom:1px solid var(--warm-border);">
                    <td style="padding:6px;">BatchNormalization</td>
                    <td style="padding:6px;">(32, 32, 64)</td>
                    <td style="padding:6px;">256</td>
                </tr>
                <tr style="border-bottom:1px solid var(--warm-border);">
                    <td style="padding:6px;">MaxPooling2D (2×2)</td>
                    <td style="padding:6px;">(16, 16, 64)</td>
                    <td style="padding:6px;">0</td>
                </tr>
                <tr style="border-bottom:1px solid var(--warm-border);">
                    <td style="padding:6px;">Conv2D (128 filters, 3×3)</td>
                    <td style="padding:6px;">(16, 16, 128)</td>
                    <td style="padding:6px;">73,856</td>
                </tr>
                <tr style="border-bottom:1px solid var(--warm-border);">
                    <td style="padding:6px;">BatchNormalization</td>
                    <td style="padding:6px;">(16, 16, 128)</td>
                    <td style="padding:6px;">512</td>
                </tr>
                <tr style="border-bottom:1px solid var(--warm-border);">
                    <td style="padding:6px;">MaxPooling2D (2×2)</td>
                    <td style="padding:6px;">(8, 8, 128)</td>
                    <td style="padding:6px;">0</td>
                </tr>
                <tr style="border-bottom:1px solid var(--warm-border);">
                    <td style="padding:6px;">GlobalAveragePooling2D</td>
                    <td style="padding:6px;">(128)</td>
                    <td style="padding:6px;">0</td>
                </tr>
                <tr style="border-bottom:1px solid var(--warm-border);">
                    <td style="padding:6px;">Dense (128 units)</td>
                    <td style="padding:6px;">(128)</td>
                    <td style="padding:6px;">16,512</td>
                </tr>
                <tr style="border-bottom:1px solid var(--warm-border);">
                    <td style="padding:6px;">Dropout</td>
                    <td style="padding:6px;">(128)</td>
                    <td style="padding:6px;">0</td>
                </tr>
                <tr>
                    <td style="padding:6px;">Dense (10 units, Softmax)</td>
                    <td style="padding:6px;">(10)</td>
                    <td style="padding:6px;">1,290</td>
                </tr>
            </table>
            <div style="margin-top:12px; font-size:0.83rem; color:var(--text-muted);">
                <strong>Trainable Parameters:</strong> 111,498 (435.54 KB) · <strong>Non-trainable:</strong> 448 (BatchNorm statistics) · Optimizer: Adam · Loss: Sparse Categorical Crossentropy
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Simple explanation
        with st.expander("What is a CNN? (simple words)"):
            st.markdown(
                "A **CNN** (Convolutional Neural Network) is an AI built to understand pictures. Reading the table top to bottom:\n"
                "- **RandomFlip / RandomRotation:** during training, photos are randomly flipped and turned so the model learns to recognize land from any angle.\n"
                "- **Conv2D:** small filters slide over the photo and find patterns like edges and textures.\n"
                "- **BatchNormalization:** keeps the numbers in a steady range so the model learns faster and more reliably.\n"
                "- **MaxPooling:** shrinks the picture and keeps only the strongest patterns.\n"
                "- **GlobalAveragePooling:** squeezes each pattern map into one average number, giving a short list of 128 numbers.\n"
                "- **Dense:** the thinking layer that combines all the patterns.\n"
                "- **Dropout:** switches off some neurons while training so the model does not just memorize.\n"
                "- **Dense (10) + Softmax:** gives the final score for each of the 10 land types."
            )
