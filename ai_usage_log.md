
# AI Usage Log

## Project
COD Risk Prevention System – Associate Software Engineer Take-Home Assignment

## 1. AI-Assisted Development

AI assistance was used during development for:

- Understanding the assignment requirements and breaking them into modules.
- Planning the risk-based decision engine.
- Developing and debugging Python and Streamlit code.
- Understanding Random Forest model training and evaluation.
- Designing the WhatsApp confirmation simulation.
- Creating address-validation rules.
- Structuring the founder dashboard and financial impact calculations.
- Preparing project documentation.

## 2. Machine Learning Usage

A Random Forest classifier was implemented using historical order data to estimate the probability of an order becoming an RTO.

The model uses order and customer-related features, including:

- Order value
- Number of items
- Customer's previous orders
- Customer's previous RTOs
- City
- State
- Marketing source
- Courier

The model was evaluated using a customer-grouped train/test split.

## 3. Where AI/ML Is Used in the Application

- Predicting the probability of RTO using a trained machine learning model.
- Supporting risk-based order recommendations.

## 4. Where Traditional Python Logic Is Used

The following tasks use deterministic Python rules rather than an LLM:

- Applying configurable risk thresholds.
- Selecting the recommended order action.
- Calculating estimated financial impact.
- Validating missing or suspicious customer names and addresses.
- Processing simulated WhatsApp responses.
- Recording test-order decisions.
- Generating dashboard metrics and analytics.

## 5. LLM Usage and Limitations

No live LLM API integration is currently implemented in the application.

An LLM could be introduced in a future version to interpret informal or Hinglish address descriptions and identify ambiguous customer details. Such outputs should be used to request clarification or manual review, not automatically reject an order.

## 6. Human Oversight

The system is designed as a decision-support tool.

High-risk orders should be reviewed by an operations team. Automatic cancellation is disabled because the current model has limited predictive performance and can incorrectly flag genuine orders.

## 7. Development and Testing

AI assistance was used to explain errors, suggest improvements and guide testing. Application behaviour was checked through local execution and manual testing of the dashboard, risk settings, order prediction and WhatsApp simulator.
