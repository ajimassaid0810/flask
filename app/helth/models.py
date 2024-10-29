import pandas as pd
import joblib
import os

class Helth:
    @staticmethod
    def predict_penyakit(gejala1=None, gejala2=None, gejala3=None):
        try:
            # Load model dan encoder yang sudah disimpan
            base_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(base_dir, 'model_penyakit.pkl')
            gejala_path = os.path.join(base_dir, 'gejala_encoder.pkl')
            penyakit_path = os.path.join(base_dir, 'penyakit_encoder.pkl')
            model = joblib.load(model_path)
            le_gejala = joblib.load(gejala_path)
            le_penyakit = joblib.load(penyakit_path)

            # Load dataset asli untuk mendapatkan saran dan tingkat urgensi
            file_path = os.path.join(base_dir, 'Penyakit_Gejala_3_Saran.csv')
            data = pd.read_csv(file_path)

            # Encode input gejala (handle gejala yang kurang dari 3)
            gejala_encoded1 = le_gejala.transform([gejala1])[0] if gejala1 else -1
            gejala_encoded2 = le_gejala.transform([gejala2])[0] if gejala2 else -1
            gejala_encoded3 = le_gejala.transform([gejala3])[0] if gejala3 else -1

        except ValueError:
            return 'Gejala tidak valid', 'Periksa input gejala yang benar.', 'Tidak Diketahui'

        # Siapkan input untuk model
        input_data = pd.DataFrame([[
            gejala_encoded1, gejala_encoded2, gejala_encoded3
        ]], columns=['Gejala 1', 'Gejala 2', 'Gejala 3'])

        # Prediksi penyakit
        penyakit_encoded = model.predict(input_data)[0]
        penyakit_prediksi = le_penyakit.inverse_transform([penyakit_encoded])[0]

        # Cari saran dan tingkat urgensi dari dataset asli
        hasil = data[data['Penyakit'] == penyakit_prediksi]
        if not hasil.empty:
            saran = hasil['Saran'].iloc[0]
            # tingkat_urgensi = hasil['Tingkat Urgensi'].iloc[0]
        else:
            saran = "Tidak ada saran yang tersedia."
            # tingkat_urgensi = "Tidak Diketahui"

        return penyakit_prediksi, saran
