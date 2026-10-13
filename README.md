# 🌿 AgroSpectra AI

> **Geospatial Remote Sensing Intelligence, AI Crop Classification & 3D Photogrammetry Platform**

AgroSpectra AI is an advanced, production-grade application engineered for precision agricultural monitoring, multi-spectral satellite analytics, and aerial terrain modeling. Designed with a calm, nature-inspired aesthetic (deep forest green, soft sage, warm ivory, and subtle olive accents), it delivers peer-grade scientific rigor alongside an intuitive, responsive user experience.

---

## 🧭 System Overview & Features

AgroSpectra AI integrates spaceborne Earth observation data, deep convolutional neural networks, and Structure-from-Motion (SfM) photogrammetry into 5 modular interfaces:

### 1. 📊 Executive Dashboard
* **Real-Time Project KPIs:** Displays core project metrics including the verified **97.75% EuroSAT test accuracy**, **10-class land-cover taxonomy**, Sentinel-2 NDVI pipeline status, and **7,130 3D reconstructed points**.
* **Visual Artifacts:** Embeds original verified milestone graphics (`agrospectra_dashboard.png`) and land-cover taxonomy distributions.
* **Transparent Scientific Disclosures:** Discloses model evaluation subset bounds and photogrammetry scene origin upfront.

### 2. 🌾 AI Crop & Land-Cover Classification
* **Deep Neural Network Inference:** Powered by the trained Keras CNN model (`agrospectra_crop_model.keras`).
* **Calibrated Input Specifications:** Standardized on **64×64×3** pixel Sentinel-2 RGB patches normalized to `[0.0, 1.0]`.
* **10 EuroSAT Classes:**
  1. `Annual Crop`
  2. `Forest`
  3. `Herbaceous Vegetation`
  4. `Highway`
  5. `Industrial Buildings`
  6. `Pasture`
  7. `Permanent Crop`
  8. `Residential Buildings`
  9. `River`
  10. `SeaLake`
* **Interactive Testing:** Choose from a curated gallery of verified benchmark test crops or upload custom satellite/aerial imagery (PNG, JPG, TIFF, WebP).
* **Rich Confidence Scoring:** Instant top-1 identification with confidence percentage, top-5 class distribution horizontal bar chart, complete 10-class probability breakdown, and confusion matrix diagnostics.

### 3. 🌱 Vegetation Health & Sentinel-2 NDVI Analytics
* **Real Radiometric Calculation:** Ingests Sentinel-2 MSI Level-2A **Red (Band 4, 665 nm)** and **Near-Infrared (Band 8, 842 nm)** GeoTIFF rasters:
  $$\text{NDVI} = \frac{\text{B08 (NIR)} - \text{B04 (Red)}}{\text{B08 (NIR)} + \text{B04 (Red)}}$$
* **1-Click Benchmark Ingestion:** Pre-loaded with authentic Sentinel-2 GeoTIFF bands over the Nagpur, India agricultural district for instant testing.
* **Custom GeoTIFF Upload:** Upload individual single-band or multi-band GeoTIFF rasters.
* **Zonal Health Classification:**
  * **Water & Non-Vegetated:** $\text{NDVI} < 0.0$
  * **Bare Soil & Fallow:** $0.0 \le \text{NDVI} < 0.2$
  * **Sparse / Emerging Canopy:** $0.2 \le \text{NDVI} < 0.4$
  * **Moderate Canopy:** $0.4 \le \text{NDVI} < 0.6$
  * **Dense / High Vigour Crop:** $\text{NDVI} \ge 0.6$
* **Interactive Visualizations:** Zoomable Plotly heatmaps with dynamic colormaps (`RdYlGn`, `viridis`, `YlGn`, `plasma`), interactive donut breakdown, and radiometric pixel frequency histogram.
* **Full-Resolution Scientific Exports:**
  * ⬇️ **GeoTIFF Raster (`.tif`)**: True 32-bit floating-point GeoTIFF preserving coordinate metadata.
  * ⬇️ **Colored Preview (`.png`)**: High-resolution publication-ready preview.
  * ⬇️ **Zonal Statistics (`.csv`)**: Full tabular breakdown of pixel counts, percentages, and metrics.

### 4. 📐 3D Photogrammetry Viewer
* **Interactive 3D Point Cloud:** Visualizes `agrospectra_point_cloud.ply` with **7,130 vertices** reconstructed using COLMAP Structure-from-Motion (SfM) from 18 registered aerial drone photographs.
* **Plotly 3D WebGL Rendering:** Full 360° orbit rotation, fluid zooming, panning, and coordinate inspection.
* **Elevation & Coordinate Shading:** Select between Z-elevation, X-coordinate, or Y-coordinate color mapping with palettes like `Earth`, `Viridis`, `Plasma`, `Spectral`, and `Turbo`.
* **Telemetry & Bounding Geometry:** Displays live metric cards for X, Y, Z spans, coordinate ranges, and scene centroid.
* **Custom Upload Support:** Upload any custom ASCII `.ply` point cloud for instant inspection.

### 5. 📖 About & Scientific Methods
* **Comprehensive Technical Guide:** Deep dive into Sentinel-2 multispectral MSI sensors, chlorophyll absorption physics, CNN feature extraction, and COLMAP epipolar bundle adjustment.
* **Full Pipeline Walkthrough:** 5-phase visual architecture diagram from raw tile ingestion to 3D point cloud serialization.

---

## 🔬 Scientific Disclosures & Verification Notice

In strict adherence to peer-grade academic honesty:
1. **EuroSAT Test Accuracy (97.75%):** Evaluated on a **2,000-image subset** of the EuroSAT dataset (80/20 stratified split; 400 test images) to accelerate experimental iteration.
2. **Photogrammetry Point Cloud Origin:** The 7,130-point 3D point cloud was reconstructed from 18 aerial drone photographs from the **Brighton Beach benchmark dataset**. It serves as an algorithmic proof-of-concept demonstrating Structure-from-Motion photogrammetry viability, not an active agricultural farm field.

---

## 📁 Repository Structure

```
AgroSpectra_AI_App/
│
├── app.py                          # Streamlit application entry point
├── config.py                       # Global constants, paths, EuroSAT taxonomy, disclosures
├── styles.py                       # Nature-inspired custom CSS design system
├── verify_app.py                   # Automated end-to-end verification test suite
├── requirements.txt                # Production Python dependencies
├── run_app.bat                     # Windows 1-click batch launcher
│
├── modules/                        # Feature interface modules
│   ├── dashboard.py                # Executive dashboard & KPIs
│   ├── classifier.py               # Deep learning crop classification
│   ├── vegetation.py               # Sentinel-2 NDVI analysis & GeoTIFF export
│   ├── reconstruction.py           # 3D PLY point cloud visualizer
│   └── about.py                    # Scientific documentation & disclosures
│
├── utils/                          # Core engine utilities
│   ├── model_loader.py             # Keras CNN model caching & inference
│   ├── geo_utils.py                # GeoTIFF I/O, NDVI formula, zonal stats
│   └── ply_loader.py               # Fast ASCII PLY point cloud parser
│
├── sample_data/                    # Benchmark sample data for instant testing
│   ├── sentinel2_B04_red_sample.tif    # Sentinel-2 Red band (B04) GeoTIFF
│   ├── sentinel2_B08_nir_sample.tif    # Sentinel-2 NIR band (B08) GeoTIFF
│   └── crops/                          # Verified EuroSAT test crop patches
│
├── assets/                         # Evaluation artifacts extracted from notebook
│   ├── confusion_matrix.png        # EuroSAT 10-class confusion matrix
│   ├── sentinel_ndvi_map.png       # Real Sentinel-2 NDVI reference map
│   ├── vegetation_categories.png   # Zonal classification map
│   ├── sift_matching.png           # SIFT keypoint matching output
│   ├── point_cloud_sparse.png      # COLMAP sparse reconstruction projection
│   └── colmap_reconstruction.png   # 3D model visualization
│
├── agrospectra_crop_model.keras    # Preserved original trained Keras model
├── agrospectra_point_cloud.ply     # Preserved original 7,130-point COLMAP cloud
├── agrospectra_dashboard.png       # Preserved original summary graphic
├── project_results.json            # Preserved original project results JSON
└── AgroSpectra_AI.ipynb            # Preserved original Jupyter notebook
```

---

## 🚀 Getting Started

### Prerequisites
* **Python 3.10 or 3.11** (Recommended for native TensorFlow 2.16+ and Keras 3.x compatibility on Windows).
* Windows, macOS, or Linux.

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd "c:\Users\khushboo pingle\Desktop\AgroSpectra_AI_App"
   ```

2. **(Optional but Recommended) Create a virtual environment:**
   ```bash
   # Using Python 3.11
   py -3.11 -m venv venv
   
   # Activate virtual environment
   # Windows:
   .\venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🏃 Exact Commands to Run the Application

### Option 1: Using the 1-Click Windows Launcher
Double-click `run_app.bat` or execute in PowerShell:
```powershell
.\run_app.bat
```

### Option 2: Running Directly via Terminal
If you have multiple Python versions installed, run with Python 3.11:
```bash
py -3.11 -m streamlit run app.py
```

Or if your active Python environment has the dependencies installed:
```bash
streamlit run app.py
```

The application will start immediately and automatically open your default browser at:
👉 **`http://localhost:8501`**

---

## 🧪 Automated Verification Suite

To verify all components (model loading, neural inference, GeoTIFF I/O, NDVI calculation, PLY parsing, and UI module imports), run:

```bash
py -3.11 verify_app.py
```

Expected output:
```
========================================
 AgroSpectra AI - End-to-End Verification
========================================
[1/5] Testing config & constants... Passed!
[2/5] Testing Crop Classifier Model & Preprocessing... Passed!
[3/5] Testing Sentinel-2 NDVI Calculation & Exports... Passed!
[4/5] Testing 3D Point Cloud PLY Loader... Passed!
[5/5] Testing Module Imports... Passed!
========================================
 ALL TESTS PASSED SUCCESSFULLY!
========================================
```

---

## 🌿 Technical Specifications & Palette

* **Primary Palette:** Deep Forest Green (`#1B3B2B`), Sage Green (`#6B8E7B`), Warm Ivory (`#FAF8F5`), Subtle Olive (`#757B69`).
* **Typography:** Plus Jakarta Sans (UI body), Lora (scientific headings), JetBrains Mono (radiometric values & coordinates).
* **Frameworks:** Streamlit 1.40+, Keras 3.15, TensorFlow 2.21, Rasterio 1.4, Plotly 5.24, NumPy 2.x, Pillow 11.x.
