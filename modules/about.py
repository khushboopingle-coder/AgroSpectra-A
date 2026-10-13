"""
AgroSpectra AI - About Project & Technical Documentation Module
Comprehensive documentation of scientific principles, pipeline architecture, and limitations.
"""

import json
from pathlib import Path
import streamlit as st
from config import (
    KEY_METRICS, DISCLOSURES, PROJECT_RESULTS_PATH, EUROSAT_CLASSES
)


def render_about():
    """Renders the About Project and Technical Documentation view."""
    st.markdown("""
    <div class="hero-header">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
            <span class="pill-badge">System Architecture & Methods</span>
            <span class="pill-badge pill-olive">Peer-Grade Transparency</span>
        </div>
        <h1 style="margin: 0; font-size: 2.3rem;">About AgroSpectra AI</h1>
        <div class="hero-subtitle">
            An integrated remote sensing intelligence and photogrammetry application bridging 
            spaceborne Earth observation, computer vision, and aerial Structure-from-Motion.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Core Architectural Pillars
    st.markdown("### Core Scientific Pillars")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="nature-card" style="height:100%;">
            <div style="font-size:1.8rem; margin-bottom:8px;">🛰️</div>
            <h4 style="margin:0 0 8px 0; color:var(--forest-deep);">1. Earth Observation</h4>
            <div style="font-size:0.86rem; color:var(--text-secondary); line-height:1.5;">
                Leverages ESA Sentinel-2 Multispectral Instrument (MSI) Level-2A surface reflectance data. 
                Utilizes Red (B04, 665 nm) and Near-Infrared (B08, 842 nm) at 10-meter spatial resolution for precision vegetative indexing.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="nature-card" style="height:100%;">
            <div style="font-size:1.8rem; margin-bottom:8px;">🧠</div>
            <h4 style="margin:0 0 8px 0; color:var(--forest-deep);">2. Deep Learning Classification</h4>
            <div style="font-size:0.86rem; color:var(--text-secondary); line-height:1.5;">
                Trained convolutional neural network targeting the EuroSAT benchmark across 10 multi-spectral land-cover classes. 
                Applies feature extraction over 64×64 pixel surface patches to identify crop types and terrain.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="nature-card" style="height:100%;">
            <div style="font-size:1.8rem; margin-bottom:8px;">📐</div>
            <h4 style="margin:0 0 8px 0; color:var(--forest-deep);">3. 3D Photogrammetry</h4>
            <div style="font-size:0.86rem; color:var(--text-secondary); line-height:1.5;">
                Structure-from-Motion (SfM) via COLMAP algorithms. Matches SIFT keypoint constellations across overlapping aerial drone photography 
                to triangulate camera positions and reconstruct 3D surface point clouds.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # Scientific Workflow Stages
    st.markdown("### End-to-End Processing Pipeline")

    st.markdown("""
    <div class="nature-card">
        <div class="step-card">
            <div class="step-num">1</div>
            <strong>Satellite Band Ingestion & Radiometric Preprocessing</strong>
            <p style="margin:4px 0 0 0; color:var(--text-secondary); font-size:0.85rem;">
                Sentinel-2 L2A bottom-of-atmosphere (BOA) surface reflectance tiles are ingested via Rasterio. 
                Bands B04 (Red) and B08 (NIR) are aligned to identical pixel dimensions, filtering out corrupted or masked nodata values.
            </p>
        </div>
        <div class="step-card">
            <div class="step-num">2</div>
            <strong>Normalized Difference Vegetation Index (NDVI)</strong>
            <p style="margin:4px 0 0 0; color:var(--text-secondary); font-size:0.85rem;">
                Calculated pixel-wise as <code>(B08 - B04) / (B08 + B04)</code>. Chlorophyll actively absorbs red light (0.66 µm) for photosynthesis, 
                while healthy plant cell mesophyll structures strongly scatter near-infrared radiation (0.84 µm). High values signify vigorous biomass.
            </p>
        </div>
        <div class="step-card">
            <div class="step-num">3</div>
            <strong>Zonal Health Classification & Float32 Export</strong>
            <p style="margin:4px 0 0 0; color:var(--text-secondary); font-size:0.85rem;">
                NDVI raster is segmented into ecological tiers: Water (&lt;0), Bare Soil (0–0.2), Sparse Canopy (0.2–0.4), Moderate Canopy (0.4–0.6), 
                and Dense Crop (&gt;0.6). Full precision float32 GeoTIFFs and zonal CSV audits are generated for GIS workflows.
            </p>
        </div>
        <div class="step-card">
            <div class="step-num">4</div>
            <strong>Convolutional Land-Cover Inference</strong>
            <p style="margin:4px 0 0 0; color:var(--text-secondary); font-size:0.85rem;">
                Candidate patches are normalized to [0, 1] and passed through a sequential 2-stage Conv2D feature extractor with Dropout (0.3) 
                and dense classification, producing calibrated confidence scores across 10 EuroSAT classes.
            </p>
        </div>
        <div class="step-card">
            <div class="step-num">5</div>
            <strong>Drone Photogrammetry & 3D Spatial Modeling</strong>
            <p style="margin:4px 0 0 0; color:var(--text-secondary); font-size:0.85rem;">
                High-resolution drone aerial photographs undergo SIFT feature matching and COLMAP bundle adjustment to produce 3D coordinate point clouds, 
                enabling spatial topography and surface elevation profiling.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Limitations & Explicit Disclosures
    st.markdown("### Scientific Limitations & Disclosures")

    st.markdown(f"""
    <div class="disclosure-banner" style="border-left-color: #52796F; background-color: #FFFFFF;">
        <div class="disclosure-title" style="color: var(--forest-deep);">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            Transparent Scientific Disclosures
        </div>
        <ul style="margin:8px 0 0 18px; padding:0; color:var(--text-secondary); font-size:0.86rem; line-height:1.6;">
            <li><strong>Model Evaluation Dataset Subset:</strong> {DISCLOSURES['crop_accuracy']} While EuroSAT total collection contains 27,000 images, this model was trained on an accelerated 2,000-image subset to optimize iteration speed during development.</li>
            <li><strong>3D Point Cloud Scene Origin:</strong> {DISCLOSURES['point_cloud_origin']} This demonstrates that the Structure-from-Motion photogrammetry pipeline executes reliably, but the terrain geometry represents a coastal scene rather than agricultural farmland.</li>
            <li><strong>Patch Spatial Resolution (64×64):</strong> EuroSAT patches capture land-cover at a macroscopic 10-meter Ground Sample Distance (GSD). Micro-scale crop row spacing, weed patches, and sub-pixel anomalies require sub-meter drone imagery.</li>
            <li><strong>Optical Satellite Weather Sensitivity:</strong> Sentinel-2 optical imagery cannot penetrate heavy cloud cover, dense smoke, or severe atmospheric haze without radar (SAR / Sentinel-1) multi-sensor fusion.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # System Architecture & Technical Specifications
    st.markdown("### Technical Specifications")

    spec1, spec2 = st.columns(2)

    with spec1:
        st.markdown("""
        <div class="nature-card-sm">
            <h4 style="margin-top:0; margin-bottom:8px;">Model & AI Runtime</h4>
            <div style="font-size:0.84rem; color:var(--text-secondary); line-height:1.5;">
                • <strong>Deep Learning Framework:</strong> Keras 3.15 / TensorFlow 2.21<br>
                • <strong>Input Dimensions:</strong> (1, 64, 64, 3) float32 [0.0, 1.0]<br>
                • <strong>Convolutional Layers:</strong> Conv2D(32), Conv2D(64), MaxPool(2×2)<br>
                • <strong>Dense Layers:</strong> Dense(128, ReLU), Dropout(0.3), Dense(10, Softmax)<br>
                • <strong>Reported Accuracy:</strong> 97.75% on 2,000-image test split<br>
                • <strong>Artifact:</strong> <code>agrospectra_crop_model.keras</code>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with spec2:
        st.markdown("""
        <div class="nature-card-sm">
            <h4 style="margin-top:0; margin-bottom:8px;">Geospatial & 3D Engine</h4>
            <div style="font-size:0.84rem; color:var(--text-secondary); line-height:1.5;">
                • <strong>Raster Processing:</strong> Rasterio 1.4, Tifffile, GDAL, NumPy<br>
                • <strong>Satellite Bands:</strong> Sentinel-2 B04 (Red 665 nm), B08 (NIR 842 nm)<br>
                • <strong>Photogrammetry Engine:</strong> COLMAP Structure-from-Motion (SfM)<br>
                • <strong>3D Point Cloud Vertices:</strong> 7,130 spatial coordinates<br>
                • <strong>Visualization:</strong> Plotly 3D WebGL Scatter & Continuous Shading<br>
                • <strong>Artifacts:</strong> <code>agrospectra_point_cloud.ply</code>, <code>project_results.json</code>
            </div>
        </div>
        """, unsafe_allow_html=True)
