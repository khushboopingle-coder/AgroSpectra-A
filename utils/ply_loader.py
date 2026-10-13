"""
AgroSpectra AI - 3D Point Cloud PLY Parser & Telemetry
Parses ASCII PLY files and extracts spatial bounding geometry and coordinates.
"""

from pathlib import Path
from typing import Dict, Any, Tuple
import numpy as np
import streamlit as st


@st.cache_data(show_spinner="Parsing 3D Point Cloud PLY file...")
def load_ply_file(file_path_or_buffer) -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Parses an ASCII PLY point cloud file and returns:
    - points: np.ndarray of shape (N, 3) with [X, Y, Z]
    - stats: dict containing vertex count, bounding box, centroid, and ranges
    """
    lines = []
    
    # Handle file path or buffer
    if isinstance(file_path_or_buffer, (str, Path)):
        with open(file_path_or_buffer, "r", encoding="latin1") as f:
            for line in f:
                if line.strip() == "end_header":
                    break
            points = np.loadtxt(f, dtype=np.float32)
    else:
        # File-like object (BytesIO or UploadedFile)
        content = file_path_or_buffer.read()
        if hasattr(file_path_or_buffer, "seek"):
            file_path_or_buffer.seek(0)
            
        if isinstance(content, bytes):
            text = content.decode("latin1", errors="ignore")
        else:
            text = str(content)
            
        parts = text.split("end_header\n", 1)
        if len(parts) == 1:
            parts = text.split("end_header\r\n", 1)
            
        if len(parts) > 1:
            data_text = parts[1]
        else:
            data_text = text

        points = np.fromstring(data_text, sep=" ", dtype=np.float32)
        if points.size % 3 != 0:
            # Reshape only complete coordinates
            rem = points.size % 3
            points = points[:-rem]
        points = points.reshape(-1, 3)

    if points.ndim != 2 or points.shape[1] != 3:
        raise ValueError("Invalid PLY format: expected (N, 3) 3D coordinate array.")

    # Spatial Geometry and Bounding Box
    x_min, x_max = float(points[:, 0].min()), float(points[:, 0].max())
    y_min, y_max = float(points[:, 1].min()), float(points[:, 1].max())
    z_min, z_max = float(points[:, 2].min()), float(points[:, 2].max())

    centroid = {
        "x": float(np.mean(points[:, 0])),
        "y": float(np.mean(points[:, 1])),
        "z": float(np.mean(points[:, 2]))
    }

    stats = {
        "num_points": int(points.shape[0]),
        "bbox": {
            "x_min": x_min, "x_max": x_max, "x_span": x_max - x_min,
            "y_min": y_min, "y_max": y_max, "y_span": y_max - y_min,
            "z_min": z_min, "z_max": z_max, "z_span": z_max - z_min
        },
        "centroid": centroid,
        "std_dev": {
            "x": float(np.std(points[:, 0])),
            "y": float(np.std(points[:, 1])),
            "z": float(np.std(points[:, 2]))
        }
    }

    return points, stats
