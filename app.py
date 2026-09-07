import streamlit as st
import pickle
import pandas as pd

# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="House Price Predictor",
    page_icon="🏠",
    layout="wide"
)

# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #666;
    margin-bottom: 30px;
}

.prediction-box {
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    background-color: #e8f5e9;
    border: 2px solid #4CAF50;
    margin-top: 25px;
}

.prediction-price {
    font-size: 35px;
    font-weight: bold;
    color: #2e7d32;
}

.info-box {
    padding: 15px;
    border-radius: 10px;
    background-color: #eef3f8;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)


# -------------------------------------------------
# LOAD MODEL
# -------------------------------------------------

@st.cache_resource
def load_model():
    with open("model_Final.pkl", "rb") as file:
        model = pickle.load(file)

    return model


try:
    model = load_model()

except Exception as e:
    st.error("❌ Model load nahi ho raha hai.")
    st.write(e)
    st.stop()


# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.markdown(
    '<div class="title">🏠 House Price Prediction</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Enter property details to estimate the house price'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# -------------------------------------------------
# INPUT SECTION
# -------------------------------------------------

st.subheader("🏡 Property Details")

col1, col2 = st.columns(2)

with col1:

    area_type = st.selectbox(
        "Area Type",
        [
            "Super built-up Area",
            "Built-up Area",
            "Plot Area",
            "Carpet Area"
        ]
    )

    availability = st.selectbox(
        "Availability",
        [
            "Ready To Move",
            "Immediate Possession",
            "19-Dec",
            "18-Dec",
            "21-Dec",
            "20-Dec",
            "22-Dec",
            "17-Dec"
        ]
    )

    location = st.text_input(
        "📍 Location",
        placeholder="Example: Whitefield"
    )

    size_bhk = st.number_input(
        "🛏️ BHK Size",
        min_value=1,
        max_value=20,
        value=2,
        step=1
    )


with col2:

    total_sqft = st.number_input(
        "📐 Total Size (sqft)",
        min_value=100.0,
        max_value=50000.0,
        value=1000.0,
        step=50.0
    )

    bath = st.number_input(
        "🚿 Number of Bathrooms",
        min_value=1,
        max_value=20,
        value=2,
        step=1
    )

    balcony = st.number_input(
        "🌿 Number of Balconies",
        min_value=0,
        max_value=10,
        value=1,
        step=1
    )


# -------------------------------------------------
# PREDICTION BUTTON
# -------------------------------------------------

st.divider()

button_col1, button_col2, button_col3 = st.columns([1, 2, 1])

with button_col2:

    predict_button = st.button(
        "🔮 Predict House Price",
        use_container_width=True
    )


# -------------------------------------------------
# PREDICTION
# -------------------------------------------------

if predict_button:

    if location.strip() == "":
        st.warning("⚠️ Please enter the location.")

    else:

        # Input DataFrame
        input_data = pd.DataFrame(
            [[
                area_type,
                availability,
                location,
                size_bhk,
                total_sqft,
                bath,
                balcony
            ]],
            columns=[
                "area_type",
                "availability",
                "location",
                "size_bhk",
                "total_sqft",
                "bath",
                "balcony"
            ]
        )

        try:

            prediction = model.predict(input_data)

            price = prediction[0]

            # -------------------------------------------------
            # RESULT
            # -------------------------------------------------

            st.markdown(
                f"""
                <div class="prediction-box">
                    <div>Estimated House Price</div>
                    <div class="prediction-price">
                        ₹ {price:.2f} Lakhs
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # -------------------------------------------------
            # PROPERTY SUMMARY
            # -------------------------------------------------

            st.subheader("📋 Property Summary")

            summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

            with summary_col1:
                st.metric("BHK", size_bhk)

            with summary_col2:
                st.metric("Total Sqft", f"{total_sqft:,.0f}")

            with summary_col3:
                st.metric("Bathrooms", bath)

            with summary_col4:
                st.metric("Balconies", balcony)

            st.success("✅ Price prediction generated successfully!")

        except Exception as e:

            st.error("❌ Prediction ke time error aa raha hai.")
            st.write(e)


# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.divider()

st.markdown(
    """
    <div style="text-align:center;color:#777;">
        🏠 House Price Prediction System | Machine Learning Project
    </div>
    """,
    unsafe_allow_html=True
)