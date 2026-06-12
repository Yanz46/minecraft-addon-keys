from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # <-- Tambahkan ini
import pandas as pd
import os

app = FastAPI(title="Minecraft Addon Keys API")

# ---- ATURAN CORS (IZIN AKSES) ----
# Kode ini memberi tahu browser bahwa website apa pun boleh mengakses API ini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # "*" artinya mengizinkan semua domain termasuk github.io Anda
    allow_credentials=True,
    allow_methods=["*"],  # Mengizinkan semua metode (GET, POST, dll)
    allow_headers=["*"],  # Mengizinkan semua header
)
# ----------------------------------

# Fungsi untuk membaca data dari file keys.tsv
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "keys.tsv")
    
    try:
        df = pd.read_csv(file_path, sep="\t")
        return df
    except Exception as e:
        print(f"Error membaca file: {e}")
        return None

@app.get("/")
def home():
    return {
        "message": "API Berhasil Berjalan!",
        "status": "Online",
        "docs": "/docs"
    }

# Endpoint 1: Mengambil semua data keys
@app.get("/keys")
def get_all_keys():
    df = load_data()
    if df is None:
        raise HTTPException(status_code=500, detail="Gagal memuat data dari file keys.tsv")
    return df.to_dict(orient="records")

# Endpoint 2: Mencari key berdasarkan MarketUUID
@app.get("/keys/{market_uuid}")
def get_key_by_market_uuid(market_uuid: str):
    df = load_data()
    if df is None:
        raise HTTPException(status_code=500, detail="Gagal memuat data")
    
    result = df[df['MarketUUID'] == market_uuid]
    if result.empty:
        raise HTTPException(status_code=404, detail="MarketUUID tidak ditemukan")
    return result.to_dict(orient="records")[0]

# Endpoint 3: Memfilter berdasarkan TypePack
@app.get("/keys/filter/type")
def filter_by_type(type_pack: str):
    df = load_data()
    if df is None:
        raise HTTPException(status_code=500, detail="Gagal memuat data")
    
    result = df[df['TypePack'].str.lower() == type_pack.lower()]
    if result.empty:
        return {"message": f"Tidak ada data dengan TypePack: {type_pack}", "data": []}
        
    return result.to_dict(orient="records")
