from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import joblib
import pandas as pd
import json
import numpy as np
import logging
from datetime import datetime
from mitigasi import monitor_anomalies_and_mitigate
from mitigasi import get_last_mitigated_for
from threading import Thread

logging.basicConfig(level=logging.DEBUG)
app = FastAPI()

current_reset_id = str(datetime.now().timestamp())

# List untuk menyimpan data anomali terakhir
recent_anomalies = []

# Load model dan fitur
model = joblib.load("best_isolation_forest_model.pkl")
with open("feature_columns.json") as f:
    FEATURES = json.load(f)

class FlowData(BaseModel):
    columns: list
    data: list

@app.post("/predict")
async def predict(flow: FlowData):
    df = pd.DataFrame(flow.data, columns=flow.columns)

    # Jika reset_id tidak cocok, abaikan
    if "reset_id" in df.columns and not (df["reset_id"] == current_reset_id).all():
        return JSONResponse(content=[])

    try:
        X = df[FEATURES]
        result = model.predict(X)
        score = model.decision_function(X)
    except Exception as e:
        return {"error": str(e)}

    response_list = []

    for i in range(len(df)):
        flow_result = {
            "result": int(result[i]),
            "score": float(score[i]),
            "src_ip": str(df.get("src_ip", ["N/A"])[i]),
            "src_mac": str(df.get("src_mac", ["N/A"])[i]),
            "src_port": int(df.get("src_port", ["N/A"])[i]) if str(df.get("src_port", ["N/A"])[i]).isdigit() else str(df.get("src_port", ["N/A"])[i]),
            "dst_ip": str(df.get("dst_ip", ["N/A"])[i]),
            "dst_mac": str(df.get("dst_mac", ["N/A"])[i]),
            "dst_port": int(df.get("dst_port", ["N/A"])[i]) if str(df.get("dst_port", ["N/A"])[i]).isdigit() else str(df.get("dst_port", ["N/A"])[i]),
            "protocol": str(df.get("protocol", ["N/A"])[i])
        }

        if flow_result["result"] == -1:
            recent_anomalies.append(flow_result)
            if len(recent_anomalies) > 50:  # batasi 50 anomali terakhir
                recent_anomalies.pop(0)

        response_list.append(flow_result)

    # Monitor anomali dan lakukan mitigasi
    Thread(target=monitor_anomalies_and_mitigate, args=(response_list,), daemon=True).start()

    return JSONResponse(content=response_list)

@app.get("/anomalies")
def get_anomalies(mac: str = None):
    return {
        "recent": recent_anomalies[-20:], 
        "last_mitigated": get_last_mitigated_for(mac) if mac else None
    }

@app.post("/reset")
def reset_anomaly_buffer():
    global current_reset_id
    recent_anomalies.clear()
    current_reset_id = str(datetime.now().timestamp())
    return {"status": "anomaly buffer cleared", "reset_id": current_reset_id}


# def get_anomalies():
#     return JSONResponse(content=recent_anomalies[-20:])