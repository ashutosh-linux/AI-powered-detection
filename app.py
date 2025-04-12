
import streamlit as st
import os
import cv2
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
from PIL import Image

st.set_page_config(page_title="AI-Powered Unauthorized Detection", layout="wide")
st.title("🏗️ Real-Time Unauthorized Construction Detection App")

# Upload section
uploaded_file = st.file_uploader("Upload an aerial image (JPG/PNG)", type=["jpg", "jpeg", "png"])
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    with open("uploaded_image.jpg", "wb") as f:
        f.write(uploaded_file.read())

    # Load zoning
    red_zone = gpd.read_file("red_zone_real.geojson")
    yellow_zone = gpd.read_file("yellow_zone_real.geojson")

    image = cv2.imread("uploaded_image.jpg")
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width, _ = image.shape

    min_lat = yellow_zone.total_bounds[1]
    max_lat = red_zone.total_bounds[3]
    min_lon = red_zone.total_bounds[0]
    max_lon = red_zone.total_bounds[2]

    def pixel_to_latlon(x, y):
        lon = min_lon + (x / width) * (max_lon - min_lon)
        lat = max_lat - (y / height) * (max_lat - min_lat)
        return lon, lat

    # Simulated boxes - will be replaced by Mask R-CNN or YOLO predictions
    sample_boxes = [(100, 150, 200, 250), (300, 350, 400, 450)]
    overlay = np.zeros_like(image_rgb, dtype=np.uint8)

    def draw_polygon(poly, color):
        coords = np.array([[(
            int((lon - min_lon) / (max_lon - min_lon) * width),
            int((max_lat - lat) / (max_lat - min_lat) * height)
        ) for lon, lat in poly.exterior.coords]], dtype=np.int32)
        cv2.fillPoly(overlay, coords, color)

    draw_polygon(red_zone.geometry.iloc[0], (255, 0, 0))
    draw_polygon(yellow_zone.geometry.iloc[0], (255, 255, 0))

    image_overlay = cv2.addWeighted(image_rgb, 1, overlay, 0.3, 0)

    for (x1, y1, x2, y2) in sample_boxes:
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        lon, lat = pixel_to_latlon(cx, cy)
        point = Point(lon, lat)
        if red_zone.contains(point).any():
            label = "Unauthorized"
            color = (255, 0, 0)
        elif yellow_zone.contains(point).any():
            label = "Authorized"
            color = (0, 255, 0)
        else:
            label = "Unclassified"
            color = (255, 255, 255)
        cv2.rectangle(image_overlay, (x1, y1), (x2, y2), color, 2)
        cv2.putText(image_overlay, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    cv2.imwrite("overlayed_map.jpg", cv2.cvtColor(image_overlay, cv2.COLOR_RGB2BGR))
    st.image(image_overlay, caption="Overlayed Detection Result", use_column_width=True)
    st.success("✅ Prediction complete. Will be enhanced with real model.")
