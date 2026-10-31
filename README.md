# COD Risk Prevention System

An AI-assisted Cash on Delivery (COD) Return-to-Origin (RTO) prevention system for a D2C haircare brand.

## 1. Project Overview

This project analyses historical COD orders and predicts the likelihood of an order becoming an RTO.

Based on the predicted risk, the system recommends one of four actions:

- **Ship as-is:** Low-risk orders.
- **Ship after confirmation:** Request customer confirmation through a simulated WhatsApp workflow.
- **Nudge to prepaid:** Offer a discount to encourage prepaid payment.
- **Hold for review:** High-risk orders requiring manual verification.

The system also provides a founder dashboard, historical RTO analytics and editable decision thresholds.

## 2. Key Features

- Machine learning-based COD risk prediction using Random Forest.
- Configurable risk thresholds.
- Address and suspicious-name validation.
- WhatsApp confirmation and prepaid offer simulation.
- Founder dashboard with order categories and estimated financial impact.
- Historical analytics by courier, marketing source and customer RTO history.

## 3. Technology Stack

- Python
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Plotly
- Joblib

## 4. Project Structure

```text
cod-rto-intelligence/
│
├── app.py
├── train_model.py
├── decision_engine.py
├── whatsapp_simulator.py
├── address_validator.py
├── config.json
├── requirements.txt
├── README.md
│
├── data/
│   ├── orders_sample.csv
│   └── processed_orders.csv
│
└── models/
    └── risk_model.pkl
```

## 5. Installation and Setup

### Prerequisites

- Python 3.10 or later
- pip

### Step 1: Clone the repository

```bash
git clone https://github.com/annolivia22-cpu/COD-Risk-Prevention-System.git
cd COD-Risk-Prevention-System
```

### Step 2: Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Train the model (if required)

```bash
python train_model.py
```

This generates the trained model in the `models/` folder.

### Step 5: Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 6. Model Evaluation

The Random Forest model was evaluated using a customer-grouped train/test split.

| Metric | Result |
|---|---:|
| Training records | 1,590 |
| Testing records | 397 |
| Accuracy | 66% |
| ROC-AUC | 0.654 |
| RTO precision | 43% |
| RTO recall | 49% |

The model is intended for decision support. Its current performance does not justify automatic order cancellation.

## 7. Decision Configuration

Decision thresholds and business assumptions can be adjusted through the Risk Settings page.

The default risk thresholds are:

- Below 15%: Ship as-is.
- 15% to below 30%: Request confirmation.
- 30% to below 50%: Encourage prepaid payment.
- 50% or above: Hold for manual review.

## 8. WhatsApp Simulation

The application simulates customer responses such as:

- YES — Customer confirms.
- NO — Customer declines.
- PAY — Customer chooses the prepaid option.
- No response — Simulated 24-hour timeout.

This is a demonstration workflow. It does not send actual WhatsApp messages or process real payments.

## 9. Limitations

- Model predictions are not guaranteed outcomes.
- The dataset may contain missing values and duplicate order IDs.
- Address validation uses basic rules and does not verify an address against a live postal database.
- WhatsApp interactions are simulated.
- Financial impact figures are estimates based on supplied business assumptions.
- Processed test-order records are stored locally in CSV format.

## 10. Future Improvements

- Integrate the official WhatsApp Business API.
- Add persistent database storage.
- Improve model performance using more historical data.
- Add model monitoring and threshold optimisation.
- Validate financial impact through controlled experiments.

## 11. Author

**Olivia Ann**

Associate Software Engineer — Take-Home Assignment
