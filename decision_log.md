
# Decision Log

## 1. Machine Learning Model
Decision: Random Forest Classifier.
Reason: Beginner-friendly and suitable for mixed numerical and categorical data.
Alternative: Logistic Regression.

## 2. Risk Thresholds
Decision: Start with 15%, 30% and 50%.
Reason: Create four different risk-based actions.
Note: Thresholds will be tested and adjusted using financial results.

## 3. Prepaid Discount
Decision: ₹20.
Reason: Expected RTO cost reduction is approximately ₹40.66 per converted order.

## 4. Customer History
Decision: Use previous orders and previous RTOs.
Reason: Previous RTO history is strongly associated with future RTO risk.

## 5. Address Validation
Decision: Use an LLM for ambiguous names and addresses.
Reason: Simple rules cannot reliably understand regional and Hinglish addresses.

## 6. Cancellation Policy
Decision: High-risk orders go to manual review initially.
Reason: Avoid losing genuine customers through automatic cancellation.

## 7. Dashboard
Decision: Use Streamlit.
Reason: Easy to run, interactive and beginner-friendly.
