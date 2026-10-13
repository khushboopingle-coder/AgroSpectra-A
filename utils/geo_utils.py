"""
AgroSpectra AI - Geospatial & NDVI Analysis Engine
Calculates Sentinel-2 NDVI, performs zonal classification, statistics, and GeoTIFF export.
"""

import io
from typing import Tuple, Dict, Any, Optional
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

try:
    import rasterio
    from rasterio.io import MemoryFile
    HAS_RASTERIO = True
except ImportError:
    HAS_RASTERIO = False

try:
    import tifffile
    HAS_TIFFFILE = True
except ImportError:
    HAS_TIFFFILE = False


def read_raster_band(file_source) -> Tuple[np.ndarray, Optional[Dict[str, Any]]]:
    """
    Reads a single-band or first-band 2D array from an uploaded file or path.
    Supports GeoTIFF, TIFF, and standard image formats.
    Returns:
        band_array: np.ndarray (2D float32)
        metadata: dict with CRS/transform if available
    """
    meta = {}
    
    # Try rasterio first
    if HAS_RASTERIO:
        try:
            if hasattr(file_source, "read"):
                file_bytes = file_source.read()
                if hasattr(file_source, "seek"):
                    file_source.seek(0)
                mem = MemoryFile(file_bytes)
                with mem.open() as src:
                    arr = src.read(1).astype(np.float32)
                    meta = src.profile.copy()
            else:
                with rasterio.open(file_source) as src:
                    arr = src.read(1).astype(np.float32)
                    meta = src.profile.copy()
            return arr, meta
        except Exception:
            # Fall back to alternative readers
            if hasattr(file_source, "seek"):
                file_source.seek(0)

    # Try tifffile
    if HAS_TIFFFILE:
        try:
            if hasattr(file_source, "read"):
                file_bytes = file_source.read()
                if hasattr(file_source, "seek"):
                    file_source.seek(0)
                arr = tifffile.imread(io.BytesIO(file_bytes)).astype(np.float32)
            else:
                arr = tifffile.imread(file_source).astype(np.float32)

            if arr.ndim == 3:
                # If shape is (bands, H, W) or (H, W, bands)
                if arr.shape[0] < arr.shape[-1]:
                    arr = arr[0]
                else:
                    arr = arr[:, :, 0]
            return arr, meta
        except Exception:
            if hasattr(file_source, "seek"):
                file_source.seek(0)

    # Fallback to PIL
    try:
        if hasattr(file_source, "read"):
            img = Image.open(file_source)
        else:
            img = Image.open(str(file_source))
        arr = np.array(img, dtype=np.float32)
        if arr.ndim == 3:
            arr = arr[:, :, 0]
        return arr, meta
    except Exception as e:
        raise ValueError(f"Could not read satellite band file: {str(e)}")


def compute_ndvi(red_band: np.ndarray, nir_band: np.ndarray) -> np.ndarray:
    """
    Computes Normalized Difference Vegetation Index (NDVI):
    NDVI = (NIR - Red) / (NIR + Red)
    Returns:
        ndvi: 2D np.ndarray float32, with NaN for invalid/unmeasured pixels.
    """
    if red_band.shape != nir_band.shape:
        # Resize if dimensions differ slightly due to resampling
        nir_img = Image.fromarray(nir_band)
        nir_resized = nir_img.resize((red_band.shape[1], red_band.shape[0]), Image.Resampling.BILINEAR)
        nir_band = np.array(nir_resized, dtype=np.float32)

    red_float = red_band.astype(np.float32)
    nir_float = nir_band.astype(np.float32)

    denominator = nir_float + red_float
    numerator = nir_float - red_float

    # Create empty array with NaN
    ndvi = np.full(red_band.shape, np.nan, dtype=np.float32)

    # Valid mask: denominator > 0 and finite values
    valid_mask = (denominator > 0) & np.isfinite(red_float) & np.isfinite(nir_float)

    ndvi[valid_mask] = numerator[valid_mask] / denominator[valid_mask]
    # Bound between -1.0 and 1.0
    ndvi[valid_mask] = np.clip(ndvi[valid_mask], -1.0, 1.0)

    return ndvi


def compute_ndvi_statistics(ndvi: np.ndarray) -> Dict[str, Any]:
    """
    Computes comprehensive scientific summary and zonal statistics from an NDVI array.
    """
    valid = np.isfinite(ndvi)
    valid_vals = ndvi[valid]

    total_pixels = int(ndvi.size)
    valid_pixels = int(len(valid_vals))

    if valid_pixels == 0:
        return {
            "total_pixels": total_pixels,
            "valid_pixels": 0,
            "valid_pct": 0.0,
            "min": 0.0,
            "max": 0.0,
            "mean": 0.0,
            "median": 0.0,
            "std": 0.0,
            "zones": {},
            "high_vegetation_pct": 0.0
        }

    valid_pct = (valid_pixels / total_pixels) * 100.0
    min_val = float(np.min(valid_vals))
    max_val = float(np.max(valid_vals))
    mean_val = float(np.mean(valid_vals))
    median_val = float(np.median(valid_vals))
    std_val = float(np.std(valid_vals))

    # Vegetation Zonal Breakdown
    # 1. Water & Shadows: < 0.0
    # 2. Bare Soil / Barren: 0.0 <= NDVI < 0.2
    # 3. Sparse Canopy: 0.2 <= NDVI < 0.4
    # 4. Moderate Vegetation: 0.4 <= NDVI < 0.6
    # 5. Dense / High Vigour Crop: NDVI >= 0.6
    c_water = int(np.sum(valid_vals < 0.0))
    c_bare = int(np.sum((valid_vals >= 0.0) & (valid_vals < 0.2)))
    c_sparse = int(np.sum((valid_vals >= 0.2) & (valid_vals < 0.4)))
    c_mod = int(np.sum((valid_vals >= 0.4) & (valid_vals < 0.6)))
    c_dense = int(np.sum(valid_vals >= 0.6))

    zones = {
        "Water & Non-Vegetated (< 0.0)": {
            "count": c_water,
            "pct": (c_water / valid_pixels) * 100.0,
            "color": "#1f77b4"
        },
        "Bare Soil & Barren (0.0 - 0.2)": {
            "count": c_bare,
            "pct": (c_bare / valid_pixels) * 100.0,
            "color": "#d6604d"
        },
        "Sparse / Emerging (0.2 - 0.4)": {
            "count": c_sparse,
            "pct": (c_sparse / valid_pixels) * 100.0,
            "color": "#fee08b"
        },
        "Moderate Canopy (0.4 - 0.6)": {
            "count": c_mod,
            "pct": (c_mod / valid_pixels) * 100.0,
            "color": "#91cf60"
        },
        "Dense / High Vigour (> 0.6)": {
            "count": c_dense,
            "pct": (c_dense / valid_pixels) * 100.0,
            "color": "#1a9850"
        }
    }

    # Healthy Canopy Percentage (NDVI > 0.4)
    high_veg_count = c_mod + c_dense
    high_vegetation_pct = (high_veg_count / valid_pixels) * 100.0

    return {
        "total_pixels": total_pixels,
        "valid_pixels": valid_pixels,
        "valid_pct": valid_pct,
        "min": min_val,
        "max": max_val,
        "mean": mean_val,
        "median": median_val,
        "std": std_val,
        "zones": zones,
        "high_veg_count": high_veg_count,
        "high_vegetation_pct": high_vegetation_pct
    }


def export_ndvi_geotiff(ndvi: np.ndarray, meta: Optional[Dict[str, Any]] = None) -> bytes:
    """
    Exports the NDVI float32 array as a true GeoTIFF in memory bytes.
    Preserves spatial transform & CRS if provided.
    """
    h, w = ndvi.shape
    if HAS_RASTERIO:
        profile = {
            "driver": "GTiff",
            "height": h,
            "width": w,
            "count": 1,
            "dtype": "float32",
            "nodata": np.nan
        }
        if meta:
            if "crs" in meta:
                profile["crs"] = meta["crs"]
            if "transform" in meta:
                profile["transform"] = meta["transform"]

        with MemoryFile() as mem:
            with mem.open(**profile) as dst:
                dst.write(ndvi.astype(np.float32), 1)
            return mem.read()

    # Fallback to tifffile
    if HAS_TIFFFILE:
        buf = io.BytesIO()
        tifffile.imwrite(buf, ndvi.astype(np.float32))
        return buf.getvalue()

    raise RuntimeError("No GeoTIFF export engine available (neither rasterio nor tifffile).")


def render_ndvi_preview_png(ndvi: np.ndarray, colormap: str = "RdYlGn") -> bytes:
    """
    Renders an NDVI map to high-resolution PNG bytes with colorbar and title.
    """
    # Downsample if image is huge for preview rendering performance
    max_dim = 1000
    h, w = ndvi.shape
    step = max(1, max(h, w) // max_dim)
    preview = ndvi[::step, ::step]

    fig, ax = plt.subplots(figsize=(8, 6), dpi=150)
    fig.patch.set_facecolor("#FAF8F5")
    ax.set_facecolor("#FFFFFF")

    im = ax.imshow(preview, cmap=colormap, vmin=-0.2, vmax=1.0)
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("NDVI Value", fontsize=10, color="#1B3B2B")
    cbar.ax.tick_params(labelsize=8)

    ax.set_title("Sentinel-2 NDVI Vegetation Map", fontsize=12, fontweight="bold", color="#1B3B2B", pad=10)
    ax.axis("off")
    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return buf.getvalue()


def build_zonal_csv(stats: Dict[str, Any]) -> str:
    """
    Generates CSV text representation of the NDVI zonal health statistics.
    """
    lines = [
        "Metric,Value",
        f"Total Pixels,{stats['total_pixels']}",
        f"Valid Pixels,{stats['valid_pixels']}",
        f"Valid Pixel Percentage,{stats['valid_pct']:.2f}%",
        f"Minimum NDVI,{stats['min']:.4f}",
        f"Maximum NDVI,{stats['max']:.4f}",
        f"Mean NDVI,{stats['mean']:.4f}",
        f"Median NDVI,{stats['median']:.4f}",
        f"Standard Deviation,{stats['std']:.4f}",
        f"High Vigour Canopy (>0.4),{stats['high_vegetation_pct']:.2f}%",
        "",
        "Zone Name,Pixel Count,Percentage"
    ]
    for zone, z_data in stats["zones"].items():
        lines.append(f'"{zone}",{z_data["count"]},{z_data["pct"]:.2f}%')

    return "\n".join(lines)
