"""
AgroSpectra AI - 3D Reconstruction Module
Interactive Plotly 3D Point Cloud Visualizer for COLMAP photogrammetry outputs.
"""

from pathlib import Path
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from PIL import Image

from config import (
    POINT_CLOUD_PATH, DISCLOSURES, KEY_METRICS, ASSETS_DIR, PALETTE
)
from utils.ply_loader import load_ply_file


def render_3d_reconstruction():
    """Renders the 3D Point Cloud Photogrammetry visualizer."""
    st.markdown("""
    <div class="hero-header">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
            <span class="pill-badge">Drone Photogrammetry</span>
            <span class="pill-badge pill-olive">COLMAP Structure-from-Motion</span>
        </div>
        <h1 style="margin: 0; font-size: 2.3rem;">3D Photogrammetric Reconstruction</h1>
        <div class="hero-subtitle">
            Explore 3D sparse surface point clouds generated via Structure-from-Motion (SfM) 
            and Multi-View Stereo photogrammetry from overlapping aerial drone photography.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Scientific Transparency Disclosure Banner
    st.markdown(f"""
    <div class="disclosure-banner" style="border-left-color: #D97706; background-color: #FEF3C725;">
        <div class="disclosure-title" style="color: #92400E;">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                <line x1="12" y1="9" x2="12" y2="13"></line>
                <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
            Dataset & Scene Origin Disclosure
        </div>
        <strong>Terrain Benchmark Notice:</strong> {DISCLOSURES['point_cloud_origin']}
        Reconstruction was performed on <strong>18 aerial photos</strong> yielding 
        <strong>7,130 verified 3D points</strong> across 18 registered camera poses.
    </div>
    """, unsafe_allow_html=True)

    # Point Cloud Selection
    st.markdown("""
    <div class="nature-card">
        <h3 style="margin-top:0; margin-bottom: 8px;">Select 3D Point Cloud Source</h3>
    """, unsafe_allow_html=True)

    source_opt = st.radio(
        "Source:",
        ["Verified Project Point Cloud (`agrospectra_point_cloud.ply`)", "Upload Custom PLY File"],
        horizontal=True,
        label_visibility="collapsed"
    )

    points = None
    stats = None

    if source_opt.startswith("Verified Project Point Cloud"):
        if POINT_CLOUD_PATH.exists():
            try:
                points, stats = load_ply_file(POINT_CLOUD_PATH)
                st.success(f"Loaded verified 3D point cloud: `{POINT_CLOUD_PATH.name}` ({stats['num_points']:,} points).")
            except Exception as e:
                st.error(f"Error loading point cloud: {e}")
        else:
            st.error(f"Point cloud file `{POINT_CLOUD_PATH.name}` not found in project folder.")
    else:
        uploaded_ply = st.file_uploader(
            "Upload ASCII PLY Point Cloud file:",
            type=["ply"],
            help="ASCII PLY file with vertex coordinates (X, Y, Z)."
        )
        if uploaded_ply is not None:
            try:
                points, stats = load_ply_file(uploaded_ply)
                st.success(f"Custom PLY loaded: {uploaded_ply.name} ({stats['num_points']:,} points).")
            except Exception as e:
                st.error(f"Error parsing uploaded PLY: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

    if points is not None and stats is not None:
        # Spatial Telemetry Metric Cards
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Reconstructed Points</div>
                <div class="metric-value">{stats['num_points']:,}</div>
                <div class="metric-sub">COLMAP sparse vertices</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">X Dimension Span</div>
                <div class="metric-value">{stats['bbox']['x_span']:.2f} m</div>
                <div class="metric-sub">Range: [{stats['bbox']['x_min']:.2f}, {stats['bbox']['x_max']:.2f}]</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Y Dimension Span</div>
                <div class="metric-value">{stats['bbox']['y_span']:.2f} m</div>
                <div class="metric-sub">Range: [{stats['bbox']['y_min']:.2f}, {stats['bbox']['y_max']:.2f}]</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Z Elevation Span</div>
                <div class="metric-value">{stats['bbox']['z_span']:.2f} m</div>
                <div class="metric-sub">Range: [{stats['bbox']['z_min']:.2f}, {stats['bbox']['z_max']:.2f}]</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

        # 3D Viewer Layout: Controls & Plotly Graph
        ctrl_col, viewer_col = st.columns([0.8, 2.2])

        with ctrl_col:
            st.markdown("""
            <div class="nature-card">
                <h4 style="margin-top:0; margin-bottom:12px;">Display Controls</h4>
            """, unsafe_allow_html=True)

            color_dim = st.selectbox(
                "Color Coordinate:",
                ["Elevation (Z-axis)", "Latitude / Y-axis", "Longitude / X-axis"]
            )

            c_scale = st.selectbox(
                "Color Palette:",
                ["Earth", "Viridis", "Plasma", "Spectral", "Turbo", "Cividis"],
                index=0
            )

            pt_size = st.slider("Point Size:", min_value=1.0, max_value=8.0, value=2.5, step=0.5)
            pt_opacity = st.slider("Opacity:", min_value=0.2, max_value=1.0, value=0.85, step=0.05)

            st.markdown("<div class='nature-divider'></div>", unsafe_allow_html=True)
            st.markdown("<strong style='font-size:0.84rem; color:var(--text-muted);'>Centroid Coordinates:</strong>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style="font-size:0.82rem; color:var(--text-secondary); line-height:1.45; margin-top:4px;">
                <code>X: {stats['centroid']['x']:.3f}</code><br>
                <code>Y: {stats['centroid']['y']:.3f}</code><br>
                <code>Z: {stats['centroid']['z']:.3f}</code>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        with viewer_col:
            st.markdown("""
            <div class="nature-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <h3 style="margin:0;">Interactive 3D Point Cloud View</h3>
                    <span style="font-size:0.8rem; color:var(--text-muted);">Orbit: Click+Drag · Zoom: Scroll · Pan: Right-Click</span>
                </div>
            """, unsafe_allow_html=True)

            # Map color array
            if "Z-axis" in color_dim:
                color_vals = points[:, 2]
                c_title = "Z (Height)"
            elif "Y-axis" in color_dim:
                color_vals = points[:, 1]
                c_title = "Y"
            else:
                color_vals = points[:, 0]
                c_title = "X"

            # Create Plotly 3D Scatter
            scatter3d = go.Scatter3d(
                x=points[:, 0],
                y=points[:, 1],
                z=points[:, 2],
                mode='markers',
                marker=dict(
                    size=pt_size,
                    color=color_vals,
                    colorscale=c_scale,
                    opacity=pt_opacity,
                    colorbar=dict(
                        title=dict(text=c_title, side="right", font=dict(size=11, color="#1B3B2B")),
                        len=0.75,
                        thickness=14
                    )
                ),
                hovertemplate="<b>Point</b><br>X: %{x:.2f}<br>Y: %{y:.2f}<br>Z: %{z:.2f}<extra></extra>"
            )

            fig3d = go.Figure(data=[scatter3d])
            fig3d.update_layout(
                margin=dict(l=0, r=0, t=0, b=0),
                height=560,
                paper_bgcolor="#FAF8F5",
                scene=dict(
                    xaxis=dict(
                        title="X (m)",
                        backgroundcolor="#F3F6F3",
                        gridcolor="#E4DDD5",
                        showbackground=True,
                        zerolinecolor="#CAD2C5"
                    ),
                    yaxis=dict(
                        title="Y (m)",
                        backgroundcolor="#F3F6F3",
                        gridcolor="#E4DDD5",
                        showbackground=True,
                        zerolinecolor="#CAD2C5"
                    ),
                    zaxis=dict(
                        title="Z (m)",
                        backgroundcolor="#EAEFEA",
                        gridcolor="#E4DDD5",
                        showbackground=True,
                        zerolinecolor="#CAD2C5"
                    ),
                    aspectmode="data"
                )
            )

            st.plotly_chart(fig3d, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # Photogrammetry Pipeline & Diagnostic References
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown("### COLMAP Photogrammetry Pipeline & Reference Deliverables")

    p_tab1, p_tab2 = st.tabs(["Structure-from-Motion (SfM) Workflow", "Reconstruction Artifacts"])

    with p_tab1:
        st.markdown("""
        <div class="nature-card-sm">
            <h4 style="margin-top:0; margin-bottom:8px;">Photogrammetric Pipeline Phases</h4>
            <div class="step-card">
                <div class="step-num">1</div>
                <strong>SIFT Feature Detection & Extraction</strong>
                <p style="margin:4px 0 0 0; color:var(--text-secondary); font-size:0.85rem;">
                    Scale-Invariant Feature Transform (SIFT) detects keypoints robust to scale, orientation, and lighting variations across each aerial drone frame.
                </p>
            </div>
            <div class="step-card">
                <div class="step-num">2</div>
                <strong>Exhaustive Feature Matching & Geometric Verification</strong>
                <p style="margin:4px 0 0 0; color:var(--text-secondary); font-size:0.85rem;">
                    Brute-force k-Nearest Neighbor (k-NN) matching with Lowe's ratio test (0.7) and RANSAC epipolar fundamental matrix estimation filters out spurious matches.
                </p>
            </div>
            <div class="step-card">
                <div class="step-num">3</div>
                <strong>Incremental Bundle Adjustment & Camera Pose Estimation</strong>
                <p style="margin:4px 0 0 0; color:var(--text-secondary); font-size:0.85rem;">
                    COLMAP initializes from the most geometrically confident image pair, sequentially triangulating new 3D points and refining intrinsic/extrinsic parameters.
                </p>
            </div>
            <div class="step-card">
                <div class="step-num">4</div>
                <strong>Sparse Point Cloud Generation & PLY Serialization</strong>
                <p style="margin:4px 0 0 0; color:var(--text-secondary); font-size:0.85rem;">
                    Final 3D point coordinates are written into an ASCII PLY format (7,130 vertices) ready for spatial GIS inspection and terrain modeling.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with p_tab2:
        st.markdown("""
        <div class="nature-card-sm">
            <h4 style="margin-top:0; margin-bottom:8px;">Verified Colab Photogrammetry Outputs</h4>
            <p style="color:var(--text-secondary); font-size:0.85rem; margin-bottom:12px;">
                Intermediate outputs extracted from COLMAP execution cells in <code>AgroSpectra_AI.ipynb</code>.
            </p>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            sift_path = ASSETS_DIR / "sift_matching.png"
            if sift_path.exists():
                st.image(str(sift_path), caption="SIFT Keypoint Matching (Step 33)", use_container_width=True)
        with c2:
            sc_path = ASSETS_DIR / "point_cloud_sparse.png"
            if sc_path.exists():
                st.image(str(sc_path), caption="Sparse Point Cloud (Step 35)", use_container_width=True)
        with c3:
            colmap_path = ASSETS_DIR / "colmap_reconstruction.png"
            if colmap_path.exists():
                st.image(str(colmap_path), caption="COLMAP Reconstructed Cloud (Step 62)", use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)
