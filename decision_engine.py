
import json
import joblib
import pandas as pd

from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "risk_model.pkl"
CONFIG_PATH = BASE_DIR / "config.json"

# Features expected by the trained model
REQUIRED_FIELDS = [
    "order_value",
    "num_items",
    "customer_prior_orders",
    "customer_prior_rto",
    "city",
    "state",
    "utm_source",
    "courier"
]


def load_resources():

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Model not found. Run python train_model.py first."
        )

    if not CONFIG_PATH.exists():
        raise FileNotFoundError("config.json not found.")

    model = joblib.load(MODEL_PATH)

    with open(CONFIG_PATH, "r") as file:
        config = json.load(file)

    return model, config


def decide_order(order, model=None, config=None):

    # Load model only when required
    if model is None or config is None:
        loaded_model, loaded_config = load_resources()

        if model is None:
            model = loaded_model

        if config is None:
            config = loaded_config

    # Validate input
    missing_fields = [
        field for field in REQUIRED_FIELDS
        if field not in order
    ]

    if missing_fields:
        raise ValueError(
            f"Missing order information: {missing_fields}"
        )

    # Prepare input
    data = pd.DataFrame([order])[REQUIRED_FIELDS]

    # Predict RTO probability
    probabilities = model.predict_proba(data)[0]

    rto_index = list(model.classes_).index(1)
    risk = float(probabilities[rto_index])

    # Read configurable thresholds
    ship_limit = config["ship_threshold"]
    confirm_limit = config["confirm_threshold"]
    prepaid_limit = config["prepaid_threshold"]

    # Decision logic
    if risk < ship_limit:

        action = "Ship as-is"
        reason = "The predicted RTO risk is low."

    elif risk < confirm_limit:

        action = "Ship after confirmation"
        reason = "Customer confirmation is recommended."

    elif risk < prepaid_limit:

        action = "Nudge to prepaid"
        reason = "Offer a prepaid discount to reduce delivery risk."

    else:

        action = "Hold / manual review"
        reason = "High predicted RTO risk. Review before shipping."

    # Add customer history information
    prior_rto = order.get("customer_prior_rto", 0)

    if prior_rto > 0:
        reason += (
            f" Customer has {prior_rto} previous RTO(s)."
        )

    return {
        "risk_percentage": round(risk * 100, 2),
        "action": action,
        "reason": reason
    }


# Test only when this file is run directly
if __name__ == "__main__":

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

    result = decide_order(sample_order)

    print("\nORDER DECISION")
    print("----------------------")
    print("Risk:", result["risk_percentage"], "%")
    print("Action:", result["action"])
    print("Reason:", result["reason"])
