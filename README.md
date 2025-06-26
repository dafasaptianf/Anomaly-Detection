# Anomaly-Detection

## Aktivasi CICFlowMeter (venv310)
- Simpan CSV Local
python -m cicflowmeter.sniffer -i 'virtual-ethernet' -c 'nama-file.csv'

- Kirim Real-time
python -m cicflowmeter.sniffer -i 'virtual-ethernet' -c 'nama-file.csv' -u 'end-point-API(ex: http://localhost:8000/predict)'


# #Aktivasi Modul Deteksi (venv310)
- Folder Mitigate
uvicorn deteksi:app --reload --port 8000
