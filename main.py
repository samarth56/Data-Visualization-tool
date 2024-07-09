import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
import matplotlib.pyplot as plt
import plotly.express as px

sidebar_items = {
    'Home': '/',
    'Contact': '/contact'
}

def display_data_preview(df):
    with st.expander("Preview of Uploaded Data", expanded=False):
        st.write(df.head())

def select_features(df):
    selected_features = st.multiselect("Select Features for Comparison", df.columns)
    if not selected_features:
        st.warning("Please select at least one feature for comparison")
    return selected_features

def validate_features(df, selected_features):
    if not all(df[feature].dtype in (int, float) for feature in selected_features):
        st.error("Selected features must be numeric for visualization")
        return False
    return True

def select_chart_type():
    with st.sidebar:
        st.header("Chart Selection")
        return st.selectbox(
            "Select the type of chart",
            ["Line Chart", "Bar Chart", "Scatter Plot", "Pie Chart", "Histogram", "Heatmap"]
        )

def display_chart(df, selected_features, chart_type):
    st.subheader(f"{chart_type}")
    if chart_type == "Line Chart":
        generate_line_chart(df, selected_features)
    elif chart_type == "Bar Chart":
        generate_bar_chart(df, selected_features)
    elif chart_type == "Scatter Plot":
        generate_scatter_plot(df, selected_features)
    elif chart_type == "Pie Chart":
        generate_pie_chart(df, selected_features)
    elif chart_type == "Histogram":
        generate_histogram(df, selected_features)
    elif chart_type == "Heatmap":
        generate_heatmap(df, selected_features)

def generate_line_chart(df, selected_features):
    fig, ax = plt.subplots(figsize=(15, 8))
    for feature in selected_features:
        ax.plot(df.index, df[feature], label=feature)

    ax.set_xlabel("Index")
    ax.set_ylabel("Values")
    ax.set_title("Line Chart")
    ax.legend()
    st.pyplot(fig)

def generate_bar_chart(df, selected_features):
    fig = px.bar(df, x=df.index, y=selected_features, barmode="group")
    fig.update_layout(title="Bar Chart", xaxis_title="Index", yaxis_title="Values", height=600, width=1000)
    st.plotly_chart(fig)

def generate_scatter_plot(df, selected_features):
    fig = px.scatter(
        df,
        x=selected_features[0],
        y=selected_features[1],
        title="Scatter Plot",
        labels={
            selected_features[0]: selected_features[0],
            selected_features[1]: selected_features[1],
        },
        height=600,
        width=1000
    )
    st.plotly_chart(fig)

def generate_pie_chart(df, selected_features):
    fig = px.pie(df, names=selected_features, title="Pie Chart", hole=0.3, height=600, width=1000)
    st.plotly_chart(fig)

def generate_histogram(df, selected_feature):
    fig, ax = plt.subplots(figsize=(15, 8))
    ax.hist(df[selected_feature], bins=20, edgecolor="black")
    ax.set_xlabel(selected_feature)
    ax.set_ylabel("Frequency")
    ax.set_title("Histogram")
    st.pyplot(fig)

def generate_heatmap(df, selected_features):
    fig = px.imshow(df[selected_features].corr(), title="Heatmap", height=600, width=1000)
    st.plotly_chart(fig)

def render_sidebar():
    st.sidebar.title('Sidebar')
    selection = st.sidebar.radio('Go to', list(sidebar_items.keys()))
    return selection

def main():
    selection = render_sidebar()

    if selection == 'Home':
        st.title("Data Visualization Tool")

        with st.sidebar:
            st.header("Upload Data")
            uploaded_file = st.file_uploader("Upload a CSV file", type=['csv','xlsx'])


        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            display_data_preview(df)
            selected_features = select_features(df)

            if selected_features:
                if validate_features(df, selected_features):
                    chart_type = select_chart_type()
                    display_chart(df, selected_features, chart_type)

    elif selection == "Contact":
        st.header('Profile')

        img = Image.open('profile.jpg')
        col1, col2 = st.columns([1, 2])

        col1.image(img, width=200, caption="Profile Picture")
        col2.title("Samarth Ghodake")
        col2.header("Software Engineer")
        col2.write("Email: samarthghodake56@gmail.com")

if __name__ == '__main__':
    main()
