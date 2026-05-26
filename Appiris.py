import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# Page Config
st.set_page_config(
    page_title = "Iris Flowe Predictor",
    page_icon = "🌸",
    layout = "wide",
    initial_sidebar_state = "expanded",
    menu_items = {
        'About': "Iris Flower Prediction App - Built with Streamlit"
    }
)

# Load Model
@st.cache_resource
def load_model():
    return joblib.load('iris_model.pkl')

model = load_model()

# Sidebar Navigation
st.sidebar.title("🌸 Iris Predictor")
st.sidebar.markdown("---")
page = st.sidebar.radio("Go To", ["🏠 Home", "🔍 Predict", "📊 Data Explorer"])


#-------------------------------
# HOME PAGE
#------------------------------
if page == "🏠 Home":
    st.title("🌸 Iris Flowe Species Predictor")
    st.markdown('---')

    col1, col2, col3 = st.columns(3)
    col1.metric("Model", "Random Forest")
    col2.metric("Accuracy", "90%")
    col3.metric("Classes", "3 Species")

    st.markdown('---')
    st.subheader("About this Web")
    st.write("""
    This app predicts the species of an Iris flower based on 4 measurement:
    - **Sepal Length** and **Sepal Width**
    - **Petal Length** and **Petal Width**
             
    The model was trained using a **Random Forest Classifier** Wrapped in a **Sklearn Pipeline**
    with StandardScaler Preprocessing.
    """)

    st.subheader("The 3 Iris Species")
    tab1, tab2, tab3 = st.tabs(["Iris Setosa", "Iris Versicolor", "Iris Virginica"])
    with tab1:
        st.write("**Iris Setosa** - small petals, easy to identify")
        st.write("Sepal Length: -5cm | Petal Length: -1.5cm")
    with tab2:
        st.write("**Iris Versicolor** - Medium size, blue-violet petals")
        st.write("Sepal Length: -6cm | Petal Length: -4cm")
    with tab3:
        st.write("**Iris Virginica** - Largest petals of the three")
        st.write("Sepal Length: -6.5cm | Petal Length: -5.5cm")


#--------------------
# PREDICT PAGE
#-------------------
elif page == "🔍 Predict":
    st.title("🔍 Predict Iris Species")
    st.markdown('---')
    st.subheader("Enter Flower Measurement")

    col1, col2 = st.columns(2)

    with col1:
        sepal_length = st.slider("Sepal Length (cm)", min_value=4.0, max_value=8.0, value=5.4, step=0.1)
        sepal_width = st.slider("Sepal width (cm)", min_value=2.0, max_value=5.0, value=3.4, step=0.1)

    with col2:
        petal_length = st.slider("Petal Length", min_value=1.0, max_value=7.0, value=1.5, step=0.1)
        petal_width = st.slider("Petal Width", min_value=0.1, max_value=2.5, value=0.2, step=0.1)

    st.markdown('---')

    if st.button("🌸 Predict Species", use_container_width=True):
        input_data = pd.DataFrame([[sepal_length, sepal_width, petal_length, petal_width]],
                                  columns = ['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm'])
        
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0]
        classes = model.classes_

        #Result
        species_emoji = {
            'Iris-setosa': '🌼',
            'Iris-Versicolor': '💜',
            'Iris-Verginica': '🌺'
        }
        emoji = species_emoji.get(prediction, '🌸')

        st.success(f"{emoji} Predicted Species: **{prediction}")

        # Probability bar chart
        prob_df = pd.DataFrame({'Species': classes, 'Probability': probability})

        fig, ax = plt.subplots()
        ax.bar(classes, probability, color=['#4C72B0','#DD8456','#55A868'])
        ax.set_title('Prediction Probability')
        ax.set_ylabel('Probability')
        ax.set_ylim(0,1)
        st.pyplot(fig)

        # show input summart
        st.subheader("Your Input")
        st.dataframe(input_data)

#-----------------------------
# DATA EXPLORER PAGE
#-----------------------------
elif page == "📊 Data Explorer":
    st.title("📊 Data Dataset Explorer")
    st.markdown('---')

    df = pd.read_csv('Iris.csv').drop('Id', axis=1)

    st.subheader("Raw Data")
    st.dataframe(df)
    st.metric("Total Rows", len(df))

    st.markdown('---')
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Species Distribution")
        fig, ax = plt.subplots()
        counts = df['Species'].value_counts()
        ax.pie(counts, labels=counts.index, autopct='%1.1f%%',
               colors=['#4C72B0','#DD8452','#55A868'])
        ax.set_title('Species Count')
        st.pyplot(fig)
    

    with col2:
        st.subheader("Feature Boxplot")
        feature = st.selectbox("Select Feature", ['SepalLengthCm','SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm'])
        fig, ax = plt.subplots()
        df. boxplot(column=feature, by='Species', ax=ax,
                    patch_artist=True)
        ax.set_title(feature)
        ax.set_xlabel('Species')
        ax.set_ylabel(feature)
        plt.suptitle('')

    st.subheader("Scatter Plot")
    col3, col4 = st.columns(2)
    x_axis = col3.selectbox("X Axis", df.columns[:-1], index=0)
    y_axis = col4.selectbox("Y Axis", df.columns[:-1], index=2)

    fig, ax = plt.subplots()
    for species, group in df.groupby('Species'):
        ax.scatter(group[x_axis], group[y_axis], label=species, alpha=0.8)
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.set_title(f'{x_axis} vs {y_axis}')
    ax.legend()
    st.pyplot(fig)


    st.subheader("Correlation Heatmap")
    numeric_df = df.drop('Species', axis=1)
    fig2, ax = plt.subplots(figsize=(6,4))
    sns.heatmap(numeric_df.corr(), annot=True, cmap='Blues', ax=ax)
    ax.set_title("Feature Correlation")
    st.pyplot(fig2)