# 🎮 PokéDex — Tugas 1 Kelompok

**Pemrograman Back-End | Institut Teknologi Tangerang Selatan**

> Dosen: Anas Nasrulloh, S.Kom., M.Kom.

---

## 📌 Deskripsi Proyek

Website ini menampilkan data **Pokémon** secara dinamis dari **API publik PokeAPI**, dibangun menggunakan framework **Flask (Python)**.

---

## ✅ Checklist Tugas

| No | Syarat | Status |
|----|--------|:------:|
| 1 | Halaman Utama menampilkan data dari API publik | ✅ |
| 2 | Pengambilan data menggunakan library `requests` | ✅ |
| 3 | Data ditampilkan dengan HTML template Flask | ✅ |
| 3 | Looping data Jinja2 | ✅ |
| 3 | Tampilan Card | ✅ |
| 4 | Judul halaman | ✅ |
| 4 | Gambar/data/deskripsi | ✅ |
| 4 | Navigasi sederhana | ✅ |

---

## 🗂️ Struktur Proyek

```
flask_tugas/
│
├── app.py                  # File utama Flask
├── requirements.txt        # Dependensi
├── README.md               # Dokumentasi ini
│
├── templates/
│   ├── base.html           # Template dasar (navbar + footer)
│   ├── index.html          # Halaman Utama + Search & Filter
│   ├── detail.html         # Halaman Detail Pokemon
│   ├── ranking.html        # Halaman Ranking
│   ├── compare.html        # Halaman Perbandingan
│   └── tentang.html        # Halaman Tentang
│
└── static/
    └── css/
        └── style.css       # Styling CSS (Futuristic Dark Theme)
```

---

## 🌐 API yang Digunakan

| Informasi | Detail |
|-----------|--------|
| **Nama API** | PokeAPI |
| **URL** | https://pokeapi.co |
| **Endpoint List** | `GET https://pokeapi.co/api/v2/pokemon?limit=151` |
| **Endpoint Detail** | `GET https://pokeapi.co/api/v2/pokemon/{id}` |
| **Autentikasi** | Tidak perlu (Free & Public) |
| **Format** | JSON |

### Contoh Response JSON dari API

```json
{
  "name": "bulbasaur",
  "id": 1,
  "height": 7,
  "weight": 69,
  "types": [
    { "type": { "name": "grass" } },
    { "type": { "name": "poison" } }
  ],
  "stats": [
    { "base_stat": 45, "stat": { "name": "hp" } },
    { "base_stat": 49, "stat": { "name": "attack" } }
  ]
}
```

---

## 🚀 Cara Menjalankan

**1. Pastikan Python sudah terinstall**

```bash
python --version
# Python 3.8 atau lebih baru
```

**2. Install dependensi**

```bash
pip install -r requirements.txt
```

**3. Jalankan aplikasi**

```bash
python app.py
```

**4. Buka di browser**

```
http://127.0.0.1:5000
```

---

## 🔧 Penjelasan Kode

### `app.py` — Flask Backend

```python
import requests
from flask import Flask, render_template

app = Flask(__name__)

def ambil_data_pokemon(limit=151):
    url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}"
    response = requests.get(url)   # Ambil data dari API
    data = response.json()         # Parse JSON
    return data

@app.route('/')
def halaman_utama():
    pokemon_list = ambil_data_pokemon()
    return render_template('index.html', pokemon_list=pokemon_list)
```

### `index.html` — Looping Data dengan Jinja2

```html
{% for pokemon in pokemon_list %}
  <div class="pokemon-card">
    <img src="{{ pokemon.gambar }}" alt="{{ pokemon.nama }}">
    <h3>{{ pokemon.nama }}</h3>
    {% for tipe in pokemon.tipe %}
      <span class="badge">{{ tipe }}</span>
    {% endfor %}
  </div>
{% endfor %}
```

---

## ✨ Fitur Halaman

### Beranda (`/`)
- Menampilkan **151 Pokémon Gen I** dalam format card grid
- **Search** berdasarkan nama atau ID
- **Filter** berdasarkan tipe (Fire, Water, Grass, dll)
- **Sort** berdasarkan ID, Nama, Total BST, HP, ATK, DEF, Speed

### Detail (`/detail/<id>`)
- Gambar resolusi tinggi + tombol **Shiny Mode**
- Stats lengkap: HP, Attack, Defense, Sp.Atk, Sp.Def, Speed
- **Radar Chart** visualisasi stats menggunakan Chart.js
- Grade rank S/A/B/C/D per stat
- Deskripsi Pokédex, abilities, data fisik
- Navigasi prev/next Pokemon

### Ranking (`/ranking`)
- Tabel semua 151 Pokemon sortable by 7 kategori
- Medali 🥇🥈🥉 untuk top 3
- Klik baris langsung ke halaman detail

### Compare (`/compare`)
- Pilih 2 Pokemon dari dropdown
- Bar duel kiri-kanan per stat
- Badge **WINNER** otomatis berdasarkan Total BST

### Tentang (`/tentang`)
- Informasi proyek, teknologi, dan API yang digunakan

---

## 📦 Dependensi

```
flask==3.0.3
requests==2.32.3
```

---

## 👨‍💻 Dibuat oleh

**Kelompok — Pemrograman Back-End**  
Institut Teknologi Tangerang Selatan
