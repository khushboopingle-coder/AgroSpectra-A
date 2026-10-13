import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
from PIL import Image
import numpy as np

print("========================================")
print(" AgroSpectra AI - End-to-End Verification")
print("========================================")

# 1. Config Test
print("\n[1/5] Testing config & constants...")
import config
print(f" EuroSAT classes: {len(config.EUROSAT_CLASSES)} classes")
print(f" Model path exists: {config.MODEL_PATH.exists()}")
print(f" Point cloud exists: {config.POINT_CLOUD_PATH.exists()}")
print(f" Dashboard image exists: {config.DASHBOARD_IMG_PATH.exists()}")
print(f" Results JSON exists: {config.PROJECT_RESULTS_PATH.exists()}")
assert len(config.EUROSAT_CLASSES) == 10
assert config.MODEL_PATH.exists()
assert config.POINT_CLOUD_PATH.exists()
print(" Config check passed!")

# 2. Crop Classifier Test
print("\n[2/5] Testing Crop Classifier Model & Preprocessing...")
from utils.model_loader import load_crop_model, preprocess_image, predict_crop
model = load_crop_model()
print(" Model loaded successfully!")

# Test inference on sample image
sample_img_path = config.CROPS_DIR / "sample_test_crop_1.png"
if sample_img_path.exists():
    img = Image.open(str(sample_img_path))
    res = predict_crop(img)
    print(f" Inference on {sample_img_path.name}:")
    print(f"   Top Class: {res['top_class']}")
    print(f"   Confidence: {res['top_confidence']:.2f}%")
    assert res['top_confidence'] > 0
    assert len(res['all_predictions']) == 10
    print(" Inference pipeline verified!")
else:
    print(" Warning: Sample image not found.")

# 3. Geospatial & NDVI Test
print("\n[3/5] Testing Sentinel-2 NDVI Calculation & Exports...")
from utils.geo_utils import (
    read_raster_band, compute_ndvi, compute_ndvi_statistics,
    export_ndvi_geotiff, render_ndvi_preview_png, build_zonal_csv
)
assert config.SAMPLE_B04_PATH.exists(), "Sample B04 does not exist"
assert config.SAMPLE_B08_PATH.exists(), "Sample B08 does not exist"

red, meta_red = read_raster_band(config.SAMPLE_B04_PATH)
nir, meta_nir = read_raster_band(config.SAMPLE_B08_PATH)
print(f" Read Red Band: shape={red.shape}, dtype={red.dtype}")
print(f" Read NIR Band: shape={nir.shape}, dtype={nir.dtype}")

ndvi = compute_ndvi(red, nir)
print(f" Computed NDVI: shape={ndvi.shape}, range=[{np.nanmin(ndvi):.3f}, {np.nanmax(ndvi):.3f}]")

stats = compute_ndvi_statistics(ndvi)
print(f" NDVI Mean: {stats['mean']:.3f}, Median: {stats['median']:.3f}")
print(f" Valid Pixels: {stats['valid_pixels']:,} ({stats['valid_pct']:.1f}%)")
print(f" High Vigour Canopy (>0.4): {stats['high_vegetation_pct']:.2f}%")
assert stats['valid_pixels'] > 0
assert -1.0 <= stats['min'] <= stats['max'] <= 1.0

# Test Exports
gtiff_bytes = export_ndvi_geotiff(ndvi, meta_red)
print(f" Exported GeoTIFF bytes: {len(gtiff_bytes):,} bytes")
assert len(gtiff_bytes) > 0

png_bytes = render_ndvi_preview_png(ndvi)
print(f" Exported PNG bytes: {len(png_bytes):,} bytes")
assert len(png_bytes) > 0

csv_str = build_zonal_csv(stats)
print(f" Generated CSV lines: {len(csv_str.splitlines())} lines")
assert len(csv_str.splitlines()) > 5
print(" Geospatial & NDVI pipeline verified!")

# 4. 3D Point Cloud PLY Test
print("\n[4/5] Testing 3D Point Cloud PLY Loader...")
from utils.ply_loader import load_ply_file
points, ply_stats = load_ply_file(config.POINT_CLOUD_PATH)
print(f" Loaded PLY: {ply_stats['num_points']} points")
print(f" Bounding Box X: [{ply_stats['bbox']['x_min']:.2f}, {ply_stats['bbox']['x_max']:.2f}] (span: {ply_stats['bbox']['x_span']:.2f}m)")
print(f" Bounding Box Y: [{ply_stats['bbox']['y_min']:.2f}, {ply_stats['bbox']['y_max']:.2f}] (span: {ply_stats['bbox']['y_span']:.2f}m)")
print(f" Bounding Box Z: [{ply_stats['bbox']['z_min']:.2f}, {ply_stats['bbox']['z_max']:.2f}] (span: {ply_stats['bbox']['z_span']:.2f}m)")
print(f" Centroid: ({ply_stats['centroid']['x']:.2f}, {ply_stats['centroid']['y']:.2f}, {ply_stats['centroid']['z']:.2f})")
assert ply_stats['num_points'] == 7130
print(" 3D Point Cloud loader verified!")

# 5. App Module Imports Test
print("\n[5/5] Testing Module Imports...")
from modules.dashboard import render_dashboard
from modules.classifier import render_classifier
from modules.vegetation import render_vegetation_health
from modules.reconstruction import render_3d_reconstruction
from modules.about import render_about
from styles import apply_custom_styles
css = apply_custom_styles()
assert len(css) > 100
print(" All modules and CSS imported successfully!")

print("\n========================================")
print(" ALL TESTS PASSED SUCCESSFULLY! ")
print("========================================")
