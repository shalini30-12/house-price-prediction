import pickle
import pandas as pd
import gradio as gr
# =========================
# Load Model
# =========================
with open("model_Final.pkl", "rb") as file:
    model = pickle.load(file)

with open("locations.pkl", "rb") as file:
    locations = pickle.load(file)
    locations = list(locations)

with open("area_type.pkl", "rb") as file:
    area_types = pickle.load(file)
    area_types= list(area_types)


with open("avalibility.pkl", "rb") as file:
    available = pickle.load(file)
    available =list(available)

# =========================
# Prediction Function
# =========================
def predict_house_price(area_type,availability,location,size_bhk,total_sqft,bath,balcony):
    try:
        # Create input data
        data = [[area_type,availability,location,int(size_bhk),float(total_sqft),int(bath),int(balcony)]]

        # IMPORTANT:
        # These column names must be exactly the same
        # as the columns used during model training.
        columns = ["area_type","availability","location","size_bhk","total_sqft","bath","balcony"]

        df = pd.DataFrame(data, columns=columns)

        # Prediction
        prediction = model.predict(df)

        price = round(prediction[0], 2)

        return f"🏠 Estimated House Price: ₹{price} Lakh"

    except Exception as e:
        return f"❌ Error: {str(e)}"
# =========================
# Gradio Interface
# =========================
with gr.Blocks(title="House Price Prediction") as app:

    gr.Markdown(
        """
        # 🏠 House Price Prediction

        Enter the property details below to predict the
        estimated house price.
        """
    )
    with gr.Row():

        with gr.Column():
            area_type = gr.Dropdown(choices=area_types,
                        label="Area Type",value="Super built-up Area")

            availability = gr.Dropdown(choices=available, label="Availability")
            location = gr.Dropdown (choices= locations, label="Location")
            size_bhk = gr.Number(label="BHK Size",minimum=1,value=2)

        with gr.Column():

            total_sqft = gr.Number(label="Total Size (sqft)",minimum=100,value=1000)
            bath = gr.Number(label="Number of Bathrooms",minimum=1,maximum=10,value=2)
            balcony = gr.Number(label="Number of Balconies",minimum=0,maximum=10,value=1)

    predict_button = gr.Button("Predict House Price",variant="primary")

    output = gr.Textbox(label="Prediction",interactive=False)

    predict_button.click(
        fn=predict_house_price,
        inputs=[area_type,availability,location,size_bhk,total_sqft,bath,balcony],
        outputs=output)
# =========================
# Launch App
# =========================

if __name__ == "__main__":
    app.launch()