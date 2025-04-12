# 🏗️ AI-Powered Unauthorized Construction Detection

This project uses AI (Mask R-CNN and YOLO) to detect unauthorized construction from aerial imagery. It features a real-time interactive **Streamlit web app** that overlays zoning regions (Red/Yellow) and generates heatmaps, classification reports, and downloadable PDFs.

---

## 🚀 Features

- 🧠 Powered by **Mask R-CNN** trained on aerial satellite data
- 📦 Real-time detection directly on uploaded images
- 🟥 Unauthorized zone detection using red/yellow GeoJSON overlays
- 🔥 Predictive heatmap showing future risk areas
- 🧾 Auto-generated PDF report with building classification
- 🌐 Fully responsive Streamlit-based web UI
- 🛠️ Designed for public deployment on **Streamlit Cloud**

---

## 🗂️ Files in this Repo

| File                     | Purpose                                               |
|--------------------------|-------------------------------------------------------|
| `app.py`                 | Streamlit app source code                             |
| `model_final.pth`        | Your trained **Mask R-CNN** model                     |
| `red_zone_real.geojson`  | GeoJSON polygon marking red (illegal) zones           |
| `yellow_zone_real.geojson`| GeoJSON polygon marking yellow (legal) zones        |
| `requirements.txt`       | Python dependencies for app                           |

---

## ⚙️ Setup & Run Locally

```bash
# Clone the repo
git clone https://github.com/ashutosh-linux/AI-powered-detection.git
cd AI-powered-detection

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
