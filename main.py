from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

app = FastAPI(title="Minecraft Addon Keys API")

# ---- ATURAN CORS (IZIN AKSES LINTAS DOMAIN) ----
# Mengizinkan website GitHub Pages Anda untuk mengambil data dari Vercel tanpa diblokir browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Mengizinkan semua domain
    allow_credentials=True,
    allow_methods=["*"],  # Mengizinkan semua metode HTTP (GET, POST, dll)
    allow_headers=["*"],  # Mengizinkan semua header
)
# -----------------------------------------------

# Fungsi untuk membaca data dari file keys.tsv
def load_data():
    # Menggunakan os.getcwd() agar Vercel mencari file keys.tsv tepat di folder utama (root) proyek
    file_path = os.path.join(os.getcwd(), "keys.tsv")
    
    try:
        # Membaca file TSV (Tab-Separated Values)
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
        raise HTTPException(status_code=500, detail="Gagal memuat data dari file keys.tsv di server")
    
    # Mengubah isi dataframe menjadi format JSON (List of Dictionary)
    return df.to_dict(orient="records")

# Endpoint 2: Mencari key berdasarkan MarketUUID
# Contoh akses: /keys/001ea2b9-3821-466c-b144-0edb9d07d42c
@app.get("/keys/{market_uuid}")
def get_key_by_market_uuid(market_uuid: str):
    df = load_data()
    if df is None:
        raise HTTPException(status_code=500, detail="Gagal memuat data")
    
    # Filter mencari yang MarketUUID-nya cocok
    result = df[df['MarketUUID'] == market_uuid]
    
    if result.empty:
        raise HTTPException(status_code=404, detail="MarketUUID tidak ditemukan")
    
    return result.to_dict(orient="records")[0]

# Endpoint 3: Memfilter berdasarkan TypePack
# Contoh penggunaan: /keys/filter/type?type_pack=world_template
@app.get("/keys/filter/type")
def filter_by_type(type_pack: str):
    df = load_data()
    if df is None:
        raise HTTPException(status_code=500, detail="Gagal memuat data")
    
    # Filter berdasarkan TypePack (mengabaikan huruf besar/kecil)
    result = df[df['TypePack'].str.lower() == type_pack.lower()]
    
    if result.empty:
        return {"message": f"Tidak ada data dengan TypePack: {type_pack}", "data": []}
        
    return result.to_dict(orient="records")
