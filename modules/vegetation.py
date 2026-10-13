"""
AgroSpectra AI - Vegetation Health Module (Sentinel-2 NDVI)
Computes real NDVI from Red (B04) and NIR (B08) GeoTIFF bands,
visualizes maps, computes zonal statistics, and exports outputs.
"""

from pathlib import Path
import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

from config import (
    SAMPLE_B04_PATH, SAMPLE_B08_PATH, DISCLOSURES, ASSETS_DIR, PALETTE
)
from utils.geo_utils import (
    read_raster_band, compute_ndvi, compute_ndvi_statistics,
    export_ndvi_geotiff, render_ndvi_preview_png, build_zonal_csv
)


def render_vegetation_health():
    """Renders the Vegetation Health & Sentinel-2 NDVI analysis view."""
    st.markdown("""
    <div class="hero-header">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
            <span class="pill-badge">Multispectral Radiometry</span>
            <span class="pill-badge pill-success">Sentinel-2 MSI Level-2A</span>
        </div>
        <h1 style="margin: 0; font-size: 2.3rem;">Vegetation Health & NDVI Analytics</h1>
        <div class="hero-subtitle">
            Calculate Normalized Difference Vegetation Index (NDVI) from Sentinel-2 Red (B04) and Near-Infrared (B08) 
            bands to evaluate crop biomass, chlorophyll absorption, and canopy vigour.
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
            Multispectral Sensor Specifications
        </div>
        {DISCLOSURES['ndvi_band_info']} NDVI is calculated via 
        <code>(B08_NIR - B04_Red) / (B08_NIR + B04_Red)</code> with floating-point radiometric calibration.
    </div>
    """, unsafe_allow_html=True)

    # Band Input Options
    st.markdown("""
    <div class="nature-card">
        <h3 style="margin-top:0; margin-bottom: 8px;">Sentinel-2 Band Acquisition</h3>
        <p style="color:var(--text-secondary); font-size:0.86rem; margin-bottom:14px;">
            Load our calibrated Nagpur, India agricultural sample bands or upload your own Sentinel-2 GeoTIFF files.
        </p>
    """, unsafe_allow_html=True)

    source_type = st.radio(
        "Band Source:",
        ["Nagpur Agricultural Benchmark Sample (GeoTIFF)", "Upload Custom Sentinel-2 Bands"],
        horizontal=True,
        label_visibility="collapsed"
    )

    red_data = None
    nir_data = None
    raster_meta = None
    dataset_name = ""

    if source_type == "Nagpur Agricultural Benchmark Sample (GeoTIFF)":
        if SAMPLE_B04_PATH.exists() and SAMPLE_B08_PATH.exists():
            st.success("Loaded verified Sentinel-2 L2A sample pair: Nagpur Agricultural District (EPSG:4326, 256×256 pixels, Red + NIR).")
            try:
                red_data, raster_meta = read_raster_band(SAMPLE_B04_PATH)
                nir_data, _ = read_raster_band(SAMPLE_B08_PATH)
                dataset_name = "Nagpur_Sentinel2_L2A"
            except Exception as e:
                st.error(f"Error loading sample bands: {e}")
        else:
            st.warning("Sample GeoTIFF files not found in sample_data/. Please upload custom bands.")

    else:
        u_col1, u_col2 = st.columns(2)
        with u_col1:
            up_red = st.file_uploader(
                "Upload Red Band (B04) GeoTIFF:",
                type=["tif", "tiff", "geotiff", "jp2", "png"],
                key="up_b04"
            )
        with u_col2:
            up_nir = st.file_uploader(
                "Upload Near-Infrared (B08) GeoTIFF:",
                type=["tif", "tiff", "geotiff", "jp2", "png"],
                key="up_b08"
            )

        if up_red and up_nir:
            try:
                red_data, raster_meta = read_raster_band(up_red)
                nir_data, _ = read_raster_band(up_nir)
                dataset_name = f"Custom_{up_red.name.split('.')[0]}"
                st.success(f"Custom bands loaded successfully! Red Shape: {red_data.shape}, NIR Shape: {nir_data.shape}")
            except Exception as ex:
                st.error(f"Error parsing uploaded bands: {ex}")
        else:
            st.info("Please upload both Red (B04) and Near-Infrared (B08) raster files to calculate NDVI.")

    st.markdown("</div>", unsafe_allow_html=True)

    # Process NDVI if data is ready
    if red_data is not None and nir_data is not None:
        with st.spinner("Computing precision floating-point NDVI and zonal health statistics..."):
            ndvi = compute_ndvi(red_data, nir_data)
            stats = compute_ndvi_statistics(ndvi)

        # Statistics Summary Metrics Row
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Mean NDVI</div>
                <div class="metric-value">{stats['mean']:.3f}</div>
                <div class="metric-sub">Average canopy response</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Median NDVI</div>
                <div class="metric-value">{stats['median']:.3f}</div>
                <div class="metric-sub">50th percentile value</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">NDVI Range</div>
                <div class="metric-value">{stats['min']:.2f} to {stats['max']:.2f}</div>
                <div class="metric-sub">Min / Max bounds</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Healthy Canopy</div>
                <div class="metric-value">{stats['high_vegetation_pct']:.1f}%</div>
                <div class="metric-sub">Pixels with NDVI &gt; 0.40</div>
            </div>
            """, unsafe_allow_html=True)

        with col5:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-label">Valid Pixels</div>
                <div class="metric-value">{stats['valid_pixels']:,}</div>
                <div class="metric-sub">{stats['valid_pct']:.1f}% coverage</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

        # Visualization Section: Map & Zonal Breakdown
        map_col, stats_col = st.columns([1.2, 1.0])

        with map_col:
            st.markdown("""
            <div class="nature-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <h3 style="margin:0;">Sentinel-2 NDVI Map</h3>
                    <div style="display:flex; gap:8px;">
            """, unsafe_allow_html=True)

            cmap_choice = st.selectbox(
                "Colormap:",
                ["RdYlGn", "viridis", "YlGn", "plasma"],
                index=0,
                label_visibility="collapsed"
            )

            st.markdown("</div></div>", unsafe_allow_html=True)

            # Interactive Plotly Heatmap
            # Downsample if raster is very large for smooth browser interaction
            h, w = ndvi.shape
            step = max(1, max(h, w) // 512)
            ndvi_view = ndvi[::step, ::step]

            # Custom colorscales for plotly
            colorscale_map = {
                "RdYlGn": [
                    [0.0, "#d73027"],
                    [0.2, "#f46d43"],
                    [0.4, "#fee08b"],
                    [0.6, "#d9ef8b"],
                    [0.8, "#91cf60"],
                    [1.0, "#1a9850"]
                ],
                "viridis": "Viridis",
                "YlGn": "YlGn",
                "plasma": "Plasma"
            }

            fig_map = go.Figure(data=go.Heatmap(
                z=ndvi_view,
                colorscale=colorscale_map.get(cmap_choice, "RdYlGn"),
                zmin=-0.2,
                zmax=1.0,
                colorbar=dict(
                    title=dict(text="NDVI", side="right", font=dict(size=11, color="#1B3B2B")),
                    tickfont=dict(size=10, color="#1B3B2B"),
                    len=0.9
                ),
                hoverongaps=False,
                hovertemplate="Row: %{y}<br>Col: %{x}<br>NDVI: %{z:.3f}<extra></extra>"
            ))

            fig_map.update_layout(
                margin=dict(l=5, r=5, t=10, b=10),
                height=420,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
                yaxis=dict(showgrid=False, showticklabels=False, zeroline=False, autorange="reversed")
            )

            st.plotly_chart(fig_map, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with stats_col:
            st.markdown("""
            <div class="nature-card">
                <h3 style="margin-top:0; margin-bottom: 10px;">Vegetation Health Zonal Breakdown</h3>
                <p style="color:var(--text-secondary); font-size:0.86rem; margin-bottom:12px;">
                    Biomass distribution categorized across agronomic index tiers.
                </p>
            """, unsafe_allow_html=True)

            # Zone Bar / Pie Chart
            zone_names = list(stats["zones"].keys())
            zone_pcts = [z["pct"] for z in stats["zones"].values()]
            zone_colors = [z["color"] for z in stats["zones"].values()]

            fig_donut = go.Figure(data=[go.Pie(
                labels=zone_names,
                values=zone_pcts,
                hole=0.45,
                marker=dict(colors=zone_colors, line=dict(color="#FFFFFF", width=2)),
                textinfo="percent",
                hoverinfo="label+value+percent",
                textfont=dict(size=11)
            )])

            fig_donut.update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                height=240,
                paper_bgcolor="rgba(0,0,0,0)",
                showlegend=False
            )
            st.plotly_chart(fig_donut, use_container_width=True)

            # Zone breakdown table
            for z_name, z_info in stats["zones"].items():
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; align-items:center; padding:5px 0; border-bottom:1px solid #EFECE6; font-size:0.84rem;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="display:inline-block; width:10px; height:10px; border-radius:50%; background:{z_info['color']};"></span>
                        <span style="color:var(--text-primary); font-weight:500;">{z_name}</span>
                    </div>
                    <div>
                        <strong style="color:var(--forest-deep);">{z_info['pct']:.1f}%</strong> 
                        <span style="color:var(--text-muted); font-size:0.78rem;">({z_info['count']:,} px)</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        # Downloads Bar
        st.markdown("""
        <div class="nature-card-sm" style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:14px;">
            <div>
                <strong style="color:var(--forest-deep); font-size:0.95rem;">Export Scientific Deliverables</strong>
                <div style="font-size:0.83rem; color:var(--text-secondary);">Download real GeoTIFF float32 raster, styled PNG preview, or zonal statistics CSV.</div>
            </div>
            <div style="display:flex; gap:10px; flex-wrap:wrap;">
        """, unsafe_allow_html=True)

        d_col1, d_col2, d_col3 = st.columns(3)
        with d_col1:
            try:
                geotiff_bytes = export_ndvi_geotiff(ndvi, raster_meta)
                st.download_button(
                    label="⬇️ Download GeoTIFF (.tif)",
                    data=geotiff_bytes,
                    file_name=f"{dataset_name}_NDVI.tif",
                    mime="image/tiff",
                    use_container_width=True
                )
            except Exception as ex:
                st.error(f"GeoTIFF export error: {ex}")

        with d_col2:
            try:
                png_bytes = render_ndvi_preview_png(ndvi, cmap_choice)
                st.download_button(
                    label="⬇️ Download Preview (.png)",
                    data=png_bytes,
                    file_name=f"{dataset_name}_NDVI_preview.png",
                    mime="image/png",
                    use_container_width=True
                )
            except Exception as ex:
                st.error(f"PNG export error: {ex}")

        with d_col3:
            csv_str = build_zonal_csv(stats)
            st.download_button(
                label="⬇️ Download Stats (.csv)",
                data=csv_str,
                file_name=f"{dataset_name}_NDVI_statistics.csv",
                mime="text/csv",
                use_container_width=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

        # Histogram Tab & Colab Benchmark Reference
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        h_tab1, h_tab2 = st.tabs(["Pixel Distribution Histogram", "Colab Pipeline Verification Assets"])

        with h_tab1:
            st.markdown("""
            <div class="nature-card-sm">
                <h4 style="margin-top:0; margin-bottom:8px;">Radiometric Pixel Histogram</h4>
                <p style="color:var(--text-secondary); font-size:0.85rem; margin-bottom:12px;">
                    Frequency distribution of NDVI reflectance values across the scene. 
                    Peaks above 0.4 indicate vigorous crop canopy cover.
                </p>
            """, unsafe_allow_html=True)

            valid_vals = ndvi[np.isfinite(ndvi)]
            hist_counts, bin_edges = np.histogram(valid_vals, bins=50, range=(-0.2, 1.0))
            bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

            fig_hist = go.Figure(data=[go.Bar(
                x=bin_centers,
                y=hist_counts,
                marker=dict(
                    color=bin_centers,
                    colorscale="RdYlGn",
                    cmin=-0.2,
                    cmax=1.0
                )
            )])
            fig_hist.add_vline(x=0.4, line_width=2, line_dash="dash", line_color="#2B8A3E",
                               annotation_text="High Vigour (>0.4)", annotation_position="top right")
            fig_hist.add_vline(x=0.2, line_width=1, line_dash="dot", line_color="#E03131",
                               annotation_text="Vegetation Threshold (0.2)", annotation_position="top left")

            fig_hist.update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                height=240,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(title="NDVI Value", range=[-0.2, 1.0], gridcolor="#E5DFD7"),
                yaxis=dict(title="Pixel Frequency", gridcolor="#E5DFD7")
            )
            st.plotly_chart(fig_hist, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with h_tab2:
            st.markdown("""
            <div class="nature-card-sm">
                <h4 style="margin-top:0; margin-bottom:8px;">Colab Notebook Verified Sentinel-2 Maps</h4>
                <p style="color:var(--text-secondary); font-size:0.85rem; margin-bottom:14px;">
                    Maps rendered during Step 27 and Step 37 of <code>AgroSpectra_AI.ipynb</code> for the Nagpur agricultural AOI.
                </p>
            """, unsafe_allow_html=True)

            col_a, col_b = st.columns(2)
            with col_a:
                ref_map = ASSETS_DIR / "sentinel_ndvi_map.png"
                if ref_map.exists():
                    st.image(str(ref_map), caption="Real Sentinel-2 L2A NDVI Map (Nagpur)", use_container_width=True)
            with col_b:
                cat_map = ASSETS_DIR / "vegetation_categories.png"
                if cat_map.exists():
                    st.image(str(cat_map), caption="Vegetation Categorization Map (Colab Step 37)", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
