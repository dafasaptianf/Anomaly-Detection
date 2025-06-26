# Anomaly Detection for DDoS Attacks in SDN Environments

This repository contains a project for detecting DDoS attacks in Software-Defined Networking (SDN) environments. The system uses CICFlowMeter to capture and analyze network traffic, which is then sent to a machine learning model for real-time prediction.

## Key Features
-   Real-time and offline network traffic analysis.
-   Integration with a prediction API for anomaly detection.
-   Designed for SDN environments.

## Technologies Used
-   **SDN Controller**: [ONOS](https://opennetworking.org/onos/)
-   **Network Emulator**: [Mininet](http://mininet.org/)
-   **Traffic Analysis**: [CICFlowMeter](https://github.com/hieulw/cicflowmeter/tree/master)
-   **Prediction API**: Python with [FastAPI](https://fastapi.tiangolo.com/) / [Uvicorn](https://www.uvicorn.org/)

---

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

-   Python 3.10 or newer
-   pip (Python package installer)
-   A virtual environment manager (e.g., `venv`)

## Usage

The system consists of two main components: the **Detection Module (API)** and the **Network Sniffer (CICFlowMeter)**. You need to run both for the system to work in real-time.

### Step 1: Run the Detection Module (API Server)

This module serves the machine learning model via an API endpoint.

1.  Navigate to the `mitigate` folder (or the relevant folder containing the API code).
    ```bash
    cd Mitigate/
    ```

2.  Start the Uvicorn server. It will listen for incoming prediction requests on port 8000.
    ```bash
    uvicorn detection_module:app --reload --port 8000
    ```
    *Note: Replace `detection_module:app` with the correct path to your FastAPI application instance.*

### Step 2: Run the Network Sniffer (CICFlowMeter)

This module captures network traffic and sends it to the Detection Module. It can run in two modes:

#### Option A: Real-time Analysis

This mode captures live traffic from a network interface, processes it, and sends it to the `/predict` endpoint for immediate analysis.

```bash
python -m cicflowmeter.sniffer -i 'your-network-interface' -c 'output.csv' -u 'http://localhost:8000/predict'
