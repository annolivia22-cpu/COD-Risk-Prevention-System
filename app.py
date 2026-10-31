
import streamlit as st
import pandas as pd
import plotly.express as px
import json
import csv

from pathlib import Path
from datetime import date, datetime, timedelta

from decision_engine import decide_order, load_resources
from address_validator import validate_address


# --------------------------------------------------
# 1. APPLICATION CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data" / "orders_sample.csv"
LOG_PATH = BASE_DIR / "data" / "processed_orders.csv"
CONFIG_PATH = BASE_DIR / "config.json"

RTO_COST = 169.40
GROSS_MARGIN = 0.62
PREPAID_RTO_RATE = 0.04

st.set_page_config(
    page_title="COD Intelligence",
    page_icon="📦",
    layout="wide"
)


# --------------------------------------------------
# 2. LOAD MODEL AND CONFIGURATION
# --------------------------------------------------

@st.cache_resource
def get_model():

    model, _ = load_resources()
    return model


def get_config():

    with open(CONFIG_PATH, "r") as file:
        config = json.load(file)

    # Defaults for financial scenarios
    config.setdefault("confirmation_effectiveness", 0.50)
    config.setdefault("prepaid_conversion_rate", 0.30)

    return config


model = get_model()
config = get_config()


# --------------------------------------------------
# 3. HELPER FUNCTIONS
# --------------------------------------------------

def load_history():

    if not DATA_PATH.exists():
        return pd.DataFrame()

    df = pd.read_csv(DATA_PATH)

    df["final_status"] = (
        df["final_status"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    return df


def load_processed_orders():

    if LOG_PATH.exists():
        df = pd.read_csv(LOG_PATH)

        if not df.empty:
            df["processed_at"] = pd.to_datetime(
                df["processed_at"],
                errors="coerce"
            )

        return df

    return pd.DataFrame()


def save_order(record):

    new_record = pd.DataFrame([record])

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    if LOG_PATH.exists():
        new_record.to_csv(
            LOG_PATH,
            mode="a",
            header=False,
            index=False
        )
    else:
        new_record.to_csv(
            LOG_PATH,
            index=False
        )


def estimate_financial_impact(
    risk,
    action,
    order_value,
    config
):

    # These are illustrative scenario estimates,
    # not confirmed real-world savings.

    savings = 0
    discount_cost = 0

    if action == "Ship after confirmation":

        savings = (
            risk
            * config["confirmation_effectiveness"]
            * RTO_COST
        )

    elif action == "Nudge to prepaid":

        conversion = config["prepaid_conversion_rate"]

        savings = (
            conversion
            * max(risk - PREPAID_RTO_RATE, 0)
            * RTO_COST
        )

        discount_cost = (
            conversion * config["prepaid_discount"]
        )

    # No automatic cancellation.
    # Genuine cancellation losses remain zero.

    return {
        "estimated_savings": round(savings, 2),
        "discount_cost": round(discount_cost, 2),
        "cancelled_genuine_loss": 0.0,
        "potential_profit_at_risk": round(
            (1 - risk) * order_value * GROSS_MARGIN,
            2
        ) if action == "Hold / manual review" else 0.0
    }


# --------------------------------------------------
# 4. APPLICATION HEADER
# --------------------------------------------------

st.title("📦 COD Intelligence")
st.caption(
    "AI-powered Cash on Delivery Risk & RTO Prevention System"
)

st.divider()


# --------------------------------------------------
# 5. NAVIGATION
# --------------------------------------------------

pages = [
    "Founder Dashboard",
    "Test New Order",
    "WhatsApp Simulator",
    "RTO Analytics",
    "Risk Settings"
]

selected_page = st.sidebar.radio(
    "Navigation",
    pages
)

st.sidebar.divider()

st.sidebar.caption("COD Intelligence v1.0")


# --------------------------------------------------
# 6. FOUNDER DASHBOARD
# --------------------------------------------------

if selected_page == "Founder Dashboard":

    st.header("Founder Dashboard")

    orders = load_processed_orders()

    report_date = st.date_input(
    "Select reporting date",
    value=date.today()
    )

    if orders.empty:

        daily = pd.DataFrame()

    else:

        daily = orders[
            orders["processed_at"].dt.date == report_date
        ].copy()

    total = len(daily)

    st.subheader("Daily Order Overview")

    col1, col2, col3, col4 = st.columns(4)

    buckets = {
        "Ship as-is": 0,
        "Ship after confirmation": 0,
        "Nudge to prepaid": 0,
        "Hold / manual review": 0
    }

    if total > 0:

        for action in buckets:

            buckets[action] = int(
                (daily["action"] == action).sum()
            )

    col1.metric("Orders Processed", total)
    col2.metric("Ship as-is", buckets["Ship as-is"])
    col3.metric("Confirmation", buckets["Ship after confirmation"])
    col4.metric("Prepaid / Hold",
                buckets["Nudge to prepaid"] +
                buckets["Hold / manual review"])

    st.divider()

    st.subheader("Decision Distribution")

    if total > 0:

        bucket_data = pd.DataFrame({
            "Action": list(buckets.keys()),
            "Orders": list(buckets.values())
        })

        fig = px.bar(
            bucket_data,
            x="Action",
            y="Orders",
            color="Action",
            title="Orders by Decision Category"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # Financial impact
        savings = daily["estimated_savings"].sum()
        discounts = daily["discount_cost"].sum()
        cancellation_loss = daily[
            "cancelled_genuine_loss"
        ].sum()

        net_impact = (
            savings - discounts - cancellation_loss
        )

        st.subheader("Estimated Financial Impact")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Estimated RTO Savings",
            f"₹{savings:,.2f}"
        )

        c2.metric(
            "Discount Cost",
            f"₹{discounts:,.2f}"
        )

        c3.metric(
            "Genuine Cancellation Loss",
            f"₹{cancellation_loss:,.2f}"
        )

        c4.metric(
            "Net Estimated Impact",
            f"₹{net_impact:,.2f}"
        )

        st.info(
            "Financial figures are illustrative estimates. "
            "They use configurable intervention assumptions, "
            "not verified prevented RTOs. No automatic "
            "cancellations are performed."
        )

        st.subheader("Orders Processed")

        st.dataframe(
            daily[
                [
                    "order_id",
                    "risk_percentage",
                    "action",
                    "address_status"
                ]
            ],
            use_container_width=True
        )

    else:

        st.info(
            "No orders have been processed on this date yet. "
            "Go to Test New Order to try your system."
        )

        st.metric("Orders Processed", 0)
        st.metric("Estimated RTO Savings", "₹0.00")
        st.metric("Net Estimated Impact", "₹0.00")


# --------------------------------------------------
# 7. TEST NEW ORDER
# --------------------------------------------------

elif selected_page == "Test New Order":

    st.header("Test a New COD Order")

    st.write(
        "Enter customer and order information to "
        "predict the likelihood of an RTO."
    )

    with st.form("order_form"):

        col1, col2 = st.columns(2)

        with col1:

            customer_name = st.text_input(
                "Customer Name"
            )

            order_value = st.number_input(
                "Order Value (₹)",
                min_value=1.0,
                value=649.0
            )

            num_items = st.number_input(
                "Number of Items",
                min_value=1,
                value=2
            )

            prior_orders = st.number_input(
                "Previous Orders",
                min_value=0,
                value=0
            )

            prior_rto = st.number_input(
                "Previous RTOs",
                min_value=0,
                value=0
            )

        with col2:

            city = st.text_input("City", value="Kochi")

            state = st.text_input("State", value="Kerala")

            pincode = st.text_input("Pincode")

            courier = st.selectbox(
                "Courier",
                ["Delhivery", "Xpressbees", "Other"]
            )

            source = st.selectbox(
                "Marketing Source",
                ["meta_ads", "direct", "organic", "google_ads", "other"]
            )

        address = st.text_area(
            "Delivery Address",
            placeholder="Enter complete delivery address"
        )

        submitted = st.form_submit_button(
            "Analyse Order",
            use_container_width=True
        )

    if submitted:

        if not customer_name.strip() or not address.strip():

            st.error(
                "Please enter the customer name and address."
            )

        elif prior_rto > prior_orders:

            st.error(
                "Previous RTOs cannot exceed previous orders."
            )

        else:

            order = {
                "order_value": order_value,
                "num_items": num_items,
                "customer_prior_orders": prior_orders,
                "customer_prior_rto": prior_rto,
                "city": city,
                "state": state,
                "utm_source": source,
                "courier": courier
            }

            # ML prediction
            result = decide_order(
                order,
                model=model,
                config=config
            )

            # Address validation
            address_result = validate_address(
                customer_name,
                address
            )

            action = result["action"]
            reason = result["reason"]

            # Apply conservative validation overrides
            if (
                address_result["name_status"] == "suspicious"
                or address_result["address_status"] == "suspicious"
            ):

                action = "Hold / manual review"

                reason += (
                    " Address/name validation requires review."
                )

            elif (
                address_result["name_status"] == "review"
                or address_result["address_status"] in [
                    "incomplete",
                    "review"
                ]
            ):

                if action == "Ship as-is":
                    action = "Ship after confirmation"

                reason += (
                    " Additional address verification is recommended."
                )

            # Financial estimates
            financial = estimate_financial_impact(
                result["risk_percentage"] / 100,
                action,
                order_value,
                config
            )

            st.divider()

            st.subheader("Order Risk Assessment")

            c1, c2 = st.columns(2)

            c1.metric(
                "Predicted RTO Risk",
                f"{result['risk_percentage']}%"
            )

            c2.metric(
                "Recommended Action",
                action
            )

            st.write("**Decision Explanation:**")
            st.write(reason)

            st.subheader("Address Validation")

            st.write(
                "Name status:",
                address_result["name_status"]
            )

            st.write(
                "Address status:",
                address_result["address_status"]
            )

            for message in address_result["reason"]:
                st.write("•", message)

            st.subheader("Estimated Financial Impact")

            st.write(
                f"Potential RTO savings: ₹{financial['estimated_savings']:.2f}"
            )

            st.write(
                f"Expected discount cost: ₹{financial['discount_cost']:.2f}"
            )

            # Save result without customer PII
            order_id = (
                "TEST-" +
                datetime.now().strftime("%Y%m%d%H%M%S%f")
            )

            record = {
                "order_id": order_id,
                "processed_at": datetime.now().isoformat(),
                "order_value": order_value,
                "risk_percentage": result["risk_percentage"],
                "action": action,
                "reason": reason,
                "address_status": address_result["address_status"],
                "estimated_savings": financial["estimated_savings"],
                "discount_cost": financial["discount_cost"],
                "cancelled_genuine_loss": financial["cancelled_genuine_loss"],
                "potential_profit_at_risk": financial["potential_profit_at_risk"]
            }

            save_order(record)

            st.success(
                "Order analysed and decision recorded successfully!"
            )


# --------------------------------------------------
# 8. WHATSAPP SIMULATOR
# --------------------------------------------------

elif selected_page == "WhatsApp Simulator":

    st.header("WhatsApp Confirmation Simulator")

    flow = st.radio(
        "Choose a message flow",
        [
            "COD Confirmation",
            "Prepaid Offer"
        ]
    )

    order_amount = st.number_input(
        "Order Amount (₹)",
        min_value=1,
        value=649
    )

    discount = config["prepaid_discount"]

    if flow == "COD Confirmation":

        st.info(
            f"Business: Hi! Your order of ₹{order_amount} "
            "is ready. Please reply YES to confirm delivery "
            "or NO to cancel."
        )

        reply = st.radio(
            "Simulate customer reply",
            ["YES", "NO", "Random reply", "No reply"]
        )

        if st.button("Process Reply"):

            if reply == "YES":

                st.success(
                    "Order confirmed. Proceed to shipping."
                )

            elif reply == "NO":

                st.warning(
                    "Customer declined. Record cancellation."
                )

            elif reply == "Random reply":

                st.info(
                    "Please reply YES or NO to confirm your order."
                )

            else:

                st.warning(
                    "No response. Order remains pending."
                )

    else:

        st.info(
            f"Business: Pay online and receive ₹{discount} "
            f"off. Your new total is ₹{order_amount - discount}."
        )

        reply = st.radio(
            "Simulate customer response",
            ["PAY", "NO", "Random reply", "No reply"]
        )

        if st.button("Process Reply"):

            if reply == "PAY":

                st.success(
                    "Payment link requested. Verify payment "
                    "before converting to prepaid."
                )

            elif reply == "NO":

                st.info(
                    "Offer the customer the option to continue with COD confirmation."
                )

            elif reply == "Random reply":

                st.info(
                    "Please choose PAY or NO."
                )

            else:

                st.warning(
                    "No response. Order remains pending."
                )

    st.divider()

    st.caption(
        "This is a simulated conversation, not a live WhatsApp integration."
    )

    if st.button("Simulate 24-hour timeout"):

        st.warning(
            "24 hours elapsed. Move the pending order "
            "to manual review according to the order policy."
        )


# --------------------------------------------------
# 9. RTO ANALYTICS
# --------------------------------------------------

elif selected_page == "RTO Analytics":

    st.header("Historical RTO Analytics")

    df = load_history()

    if df.empty:

        st.warning("Historical dataset not found.")

    else:

        completed = df[
            df["final_status"].isin(
                ["RTO", "DELIVERED"]
            )
        ].copy()

        rto_rate = (
            completed["final_status"].eq("RTO").mean()
            * 100
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("Completed Orders", len(completed))

        col2.metric(
            "RTO Orders",
            int((completed["final_status"] == "RTO").sum())
        )

        col3.metric(
            "Historical RTO Rate",
            f"{rto_rate:.2f}%"
        )

        if "courier" in completed.columns:

            st.subheader("RTO Rate by Courier")

            courier_data = (
                completed.groupby("courier")["final_status"]
                .apply(lambda x: (x == "RTO").mean() * 100)
                .reset_index(name="RTO Rate")
            )

            fig = px.bar(
                courier_data,
                x="courier",
                y="RTO Rate",
                title="Courier-wise RTO Percentage"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        if "utm_source" in completed.columns:

            st.subheader("RTO Rate by Marketing Source")

            source_data = (
                completed.groupby("utm_source")["final_status"]
                .apply(lambda x: (x == "RTO").mean() * 100)
                .reset_index(name="RTO Rate")
            )

            fig2 = px.bar(
                source_data,
                x="utm_source",
                y="RTO Rate",
                title="Marketing Source-wise RTO Percentage"
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

        if "customer_prior_rto" in completed.columns:

            st.subheader("Previous RTO History")

            history_data = (
                completed.groupby("customer_prior_rto")["final_status"]
                .apply(lambda x: (x == "RTO").mean() * 100)
                .reset_index(name="RTO Rate")
            )

            fig3 = px.bar(
                history_data,
                x="customer_prior_rto",
                y="RTO Rate",
                title="RTO Rate by Previous Customer RTOs"
            )

            st.plotly_chart(
                fig3,
                use_container_width=True
            )


# --------------------------------------------------
# 10. RISK SETTINGS
# --------------------------------------------------

elif selected_page == "Risk Settings":

    st.header("Risk Threshold Settings")

    st.write(
        "Change the risk thresholds without editing Python code."
    )

    with st.form("settings_form"):

        ship = st.slider(
            "Ship as-is threshold",
            0.0, 1.0,
            float(config["ship_threshold"]),
            0.01
        )

        confirm = st.slider(
            "Confirmation threshold",
            0.0, 1.0,
            float(config["confirm_threshold"]),
            0.01
        )

        prepaid = st.slider(
            "Prepaid threshold",
            0.0, 1.0,
            float(config["prepaid_threshold"]),
            0.01
        )

        discount = st.number_input(
            "Prepaid discount (₹)",
            min_value=0,
            max_value=100,
            value=int(config["prepaid_discount"])
        )

        confirmation_effectiveness = st.slider(
            "Assumed confirmation effectiveness",
            0.0, 1.0,
            float(config["confirmation_effectiveness"]),
            0.05
        )

        conversion_rate = st.slider(
            "Assumed prepaid conversion rate",
            0.0, 1.0,
            float(config["prepaid_conversion_rate"]),
            0.05
        )

        save_settings = st.form_submit_button(
            "Save Settings"
        )

    if save_settings:

        if not ship < confirm < prepaid:
            st.error(
                "Thresholds must be in increasing order."
            )

        else:

            config.update({
                "ship_threshold": ship,
                "confirm_threshold": confirm,
                "prepaid_threshold": prepaid,
                "prepaid_discount": discount,
                "confirmation_effectiveness": confirmation_effectiveness,
                "prepaid_conversion_rate": conversion_rate
            })

            with open(CONFIG_PATH, "w") as file:
                json.dump(config, file, indent=4)

            st.success(
                "Settings saved successfully!"
            )

            st.rerun()
