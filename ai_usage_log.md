
# AI Usage Log

## Tools Used

1. ChatGPT
   - Understanding assignment requirements.
   - Explaining Python and machine learning.
   - Debugging code.
   - Designing the business decision logic.

2. LLM for Address Validation (if implemented)
   - Identifying incomplete addresses.
   - Understanding Hinglish delivery instructions.
   - Flagging suspicious customer names.

## AI Limitations and Corrections

### Example 1
AI suggested automatically cancelling high-risk orders.
Correction: Changed the policy to manual review to avoid losing genuine customers.

### Example 2
AI treated some regional address instructions as invalid.
Correction: Added an uncertain category for manual review rather than rejecting them.

### Example 3
AI suggested a prepaid discount without considering
the expected RTO cost.
Correction: Calculated the discount using the supplied
COD and prepaid RTO rates.

## Human Verification

All financial calculations, model outputs and
business rules were checked before implementation.
