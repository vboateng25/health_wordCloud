import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.set_page_config(page_title="Public Health Dashboard", layout="wide")
st.title("Public Health Insights Dashboard")

df = pd.read_csv("health_data.csv")

st.sidebar.header("Filter Options")
states = df['State'].unique().tolist()
selected_state = st.sidebar.selectbox("Select State", states)

cities = df[df['State'] == selected_state]['City'].unique().tolist()
selected_city = st.sidebar.selectbox("Select City", cities)

filtered_df = df[(df['State'] == selected_state) & (df['City'] == selected_city)]

st.subheader(f" Data for {selected_city}, {selected_state}")
st.dataframe(filtered_df)

st.subheader("Health Metrics Over Time")
if 'Year' in df.columns:
    metrics = ['Smoking (%)', 'Obesity (%)', 'Diabetes (%)']
    selected_metric = st.selectbox("Choose a metric", metrics)
    line_data = df[df['City'] == selected_city][['Year', selected_metric]].dropna()
    st.line_chart(line_data.set_index('Year'))

st.subheader("Community Health Concerns (Word Cloud)")
if 'Concern' in df.columns:
    text = ' '.join(filtered_df['Concern'].dropna().astype(str))
    if text:
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
    else:
        st.info("No concerns available for this location.")

st.subheader(" Submit Your Health Survey (Demo Form)")
with st.form("health_form"):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=120)
    gender = st.radio("Gender", ['Male', 'Female', 'Other'])
    exercise = st.selectbox("Exercise Frequency", ['Daily', 'Weekly', 'Rarely', 'Never'])
    concern = st.text_area("Biggest Health Concern in Your Community")
    submitted = st.form_submit_button("Submit")

    if submitted:
        st.success("Thank you for your input! (Form submission is simulated in this demo.)")
