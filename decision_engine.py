
import json
import joblib
import pandas as pd

# Load model and configuration
model = joblib.load("models/risk_model.pkl")

with open("config.json", "r") as f:
    config = json.load(f)


def decide_order(order):

    # Convert input into DataFrame
    data = pd.DataFrame([order])

    # Predict RTO probability
    risk = model.predict_proba(data)[0][1]

    # Get customer information
    prior_rto = order.get("customer_prior_rto", 0)

    if risk < config["ship_threshold"]:
        action = "Ship as-is"
        reason = "Low predicted RTO risk."

    elif risk < config["confirm_threshold"]:
        action = "Ship after confirmation"
        reason = "Customer confirmation is recommended."

    elif risk < config["prepaid_threshold"]:
        action = "Nudge to prepaid"
        reason = "Prepaid payment can reduce delivery risk."

    else:
        action = "Hold / manual review"
        reason = "High predicted RTO risk. Review before shipping."

    # Additional customer-history explanation
    if prior_rto > 0:
        reason += f" Customer has {prior_rto} previous RTO(s)."

    return {
        "risk_percentage": round(risk * 100, 2),
        "action": action,
        "reason": reason
    }


# Test order
sample_order = {
    "order_value": 649,
    "num_items": 2,
    "customer_prior_orders": 1,
    "customer_prior_rto": 1,
    "city": "Kochi",
    "state": "Kerala",
    "utm_source": "meta_ads",
    "courier": "Delhivery"
}

print(decide_order(sample_order))
