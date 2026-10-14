"""
AgroSpectra AI - Configuration and Global Constants
Nature-inspired aesthetic tokens and scientific project parameters.
"""

from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
SAMPLE_DATA_DIR = BASE_DIR / "sample_data"
CROPS_DIR = SAMPLE_DATA_DIR / "crops"

# Project Artifacts
MODEL_PATH = BASE_DIR / "agrospectra_crop_model.keras"
POINT_CLOUD_PATH = BASE_DIR / "agrospectra_point_cloud.ply"
PROJECT_RESULTS_PATH = BASE_DIR / "project_results.json"
DASHBOARD_IMG_PATH = BASE_DIR / "agrospectra_dashboard.png"

# Sentinel-2 Sample Bands
SAMPLE_B04_PATH = SAMPLE_DATA_DIR / "sentinel2_B04_red_sample.tif"
SAMPLE_B08_PATH = SAMPLE_DATA_DIR / "sentinel2_B08_nir_sample.tif"

# EuroSAT 10 Classes in exact training order
EUROSAT_CLASSES = [
    "Annual Crop",
    "Forest",
    "Herbaceous Vegetation",
    "Highway",
    "Industrial Buildings",
    "Pasture",
    "Permanent Crop",
    "Residential Buildings",
    "River",
    "SeaLake"
]

# Agronomic & Land-Cover descriptions for each EuroSAT class
CLASS_DESCRIPTIONS = {
    "Annual Crop": "Regularly cultivated agricultural fields planted with seasonal crops (e.g., wheat, maize, pulses, cotton) that undergo seasonal sowing and harvesting cycles.",
    "Forest": "Dense canopy tree cover and woodland ecosystems critical for carbon sequestration, moisture retention, and regional biodiversity.",
    "Herbaceous Vegetation": "Wild natural grasses, perennial weeds, and non-woody flowering plants commonly found along field borders and uncultivated grasslands.",
    "Highway": "Paved transportation corridors, road networks, and rural transport infrastructure facilitating agricultural product logistics.",
    "Industrial Buildings": "Agricultural processing facilities, grain silos, warehousing complexes, and manufacturing infrastructure.",
    "Pasture": "Grasslands specifically managed and maintained for livestock grazing and rotational forage production.",
    "Permanent Crop": "Long-term perennial plantings including fruit orchards, vineyards, berry bushes, and nut groves that do not require annual replanting.",
    "Residential Buildings": "Rural settlements, farm homesteads, housing clusters, and human habitation structures adjacent to cultivated areas.",
    "River": "Natural freshwater streams and river drainage networks providing crucial irrigation water and watershed connectivity.",
    "SeaLake": "Large natural open surface water reservoirs, retention ponds, lakes, or coastal water bodies essential for regional hydrology."
}

# Scientific Disclosures & Transparency Notes
DISCLOSURES = {
    "crop_accuracy": "The CNN was trained on the 16,200-image EuroSAT RGB training split (10% held out for validation) and evaluated on the separate 5,400-image test split covering all 10 land-cover classes, achieving 93.41% test accuracy.",
    "point_cloud_origin": "The 3D point cloud (7,130 vertices) was reconstructed using COLMAP Structure-from-Motion (SfM) on 18 aerial drone photos from the Brighton Beach benchmark dataset. It serves as an algorithmic proof-of-concept for drone photogrammetry and topographical modeling, not active agricultural cropland.",
    "ndvi_band_info": "Vegetation index calculated using Sentinel-2 MSI Level-2A surface reflectance: Band 4 (Red, center ~665 nm, 10 m resolution) and Band 8 (Near-Infrared, center ~842 nm, 10 m resolution)."
}

# Key Metrics from project_results.json
KEY_METRICS = {
    "test_accuracy": "93.41%",
    "num_classes": 10,
    "eval_subset_size": "5,400 images (test split)",
    "model_input_dim": "64 × 64 × 3",
    "ndvi_bands": "B04 (Red) + B08 (NIR)",
    "photogrammetry_points": "7,130",
    "photogrammetry_photos": "18 drone photos",
    "colmap_registered_cameras": "18 / 18 (100%)"
}

# Nature-inspired palette hex codes
PALETTE = {
    "forest_deep": "#1B3B2B",
    "forest_mid": "#254D38",
    "forest_accent": "#2E5C44",
    "sage_dark": "#52796F",
    "sage_main": "#6B8E7B",
    "sage_light": "#96AF9F",
    "sage_mist": "#E8EEEA",
    "warm_ivory": "#FAF8F5",
    "warm_card": "#FFFFFF",
    "warm_border": "#E4DDD5",
    "olive_muted": "#757B69",
    "text_dark": "#1A2520",
    "text_muted": "#53645A",
    "ndvi_green": "#2B8A3E",
    "ndvi_yellow": "#FAB005",
    "ndvi_red": "#E03131"
}
