from datetime import datetime
from flask import Blueprint, jsonify, request
from .models import Helth

# Inisialisasi blueprint Flask
bp = Blueprint('predict', __name__)

@bp.route('/predict', methods=['POST'])
def predict():
    data = request.json

    # Validasi input JSON dan memeriksa setidaknya 1 gejala
    if not any(['gejala1' in data, 'gejala2' in data, 'gejala3' in data]):
        return jsonify({'error': 'Minimal 1 gejala diperlukan'}), 400

    # Menangani input gejala yang kurang dari 3
    gejala1 = data.get('gejala1', None)  # Default None jika gejala1 tidak ada
    gejala2 = data.get('gejala2', None)  # Default None jika gejala2 tidak ada
    gejala3 = data.get('gejala3', None)  # Default None jika gejala3 tidak ada

    try:
        # Panggil fungsi prediksi di model
        prediksi, saran = Helth.predict_penyakit(gejala1, gejala2, gejala3)

        return jsonify({
            'prediksi_penyakit': prediksi,
            'saran_tindakan': saran
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
