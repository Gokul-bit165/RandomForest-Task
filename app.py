import gradio as gr
import pickle
import numpy as np

# Load trained model
with open("customer_churn_model.pkl", "rb") as f:
    model = pickle.load(f)

def predict_churn(monthly_charges, tenure, support_calls, contract):
    # Encode contract type
    if contract == "Month-to-Month":
        contract_val = 0
    elif contract == "One Year":
        contract_val = 1
    else:
        contract_val = 2

    # Prepare feature vector
    features = np.array([[monthly_charges, tenure, support_calls, contract_val]])
    
    prediction = model.predict(features)[0]
    prob = model.predict_proba(features)[0][1]

    if prediction == 1:
        return f"⚠️ This customer is likely to churn! (Probability: {prob:.2f})"
    else:
        return f"✅ This customer is not likely to churn. (Probability: {prob:.2f})"

# Gradio Interface
iface = gr.Interface(
    fn=predict_churn,
    inputs=[
        gr.Number(label="Monthly Charges", value=50.0),
        gr.Number(label="Tenure (months)", value=1),
        gr.Number(label="Number of Support Calls", value=0),
        gr.Radio(["Month-to-Month", "One Year", "Two Year"], label="Contract Type")
    ],
    outputs=gr.Textbox(label="Churn Prediction"),
    title="📊 Customer Churn Prediction App",
    description="Enter customer details to predict whether they will churn."
)

if __name__ == "__main__":
    iface.launch()
