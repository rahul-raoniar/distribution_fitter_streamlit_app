# Core package
import streamlit as st
import streamlit.components.v1 as stc
import plotly.express as px
from fitter import Fitter, get_common_distributions, get_distributions
import matplotlib.pyplot as plt
import pandas as pd


# HTML styling
html_temp = """
		<div style="background-color:#3872fb;padding:10px;border-radius:10px">
		<h1 style="color:white;text-align:center;">Distribution Fitter Web App </h1>
		<h4 style="color:white;text-align:center;">App Developed by Rahul Raoniar </h4>
		</div>
		"""

desc_temp = """
			### Continuous Distribution Fitter App
			This app helps you to identify the best distributions that fits your data.
			#### Fitter Library
				- https://github.com/cokelaer/fitter
			#### App Content
				1. Home: Basic Information
				2. EDA Section: Exploratory Data Analysis
							- Descriptive Statistics
							- Histogram Plotting (using Plotly)
				3. Distribution Fitting: Fitting distribution using Fitter Python Library
							- Fitting Common Distributions
							- Fitting Distributions by Manual Selection
				4. About: About the App

			"""

"""
This function load csv data from streamlit app input
"""

def load_data():
    data_file = st.file_uploader("Upload a CSV", type=["csv"])
    return data_file


"""
Main function contains all the functions
"""

def main():
    stc.html(html_temp)
    menu = ["Home", "EDA", "DistFitting", "About"]
    choice = st.sidebar.selectbox("Menu", menu)


    if choice == "Home":
        st.subheader("Home")
        st.markdown(desc_temp, unsafe_allow_html=True)


    elif choice == "EDA":
        st.subheader("EDA")
        data_file = load_data()
        if data_file is not None:
            df = pd.read_csv(data_file)
            st.write(f"The file contains {df.shape[0]} rows and {df.shape[1]} columns")
            st.dataframe(df)


            submenu = st.sidebar.selectbox("Submenu",
                                      ["Descriptive", "Plots"])

            if submenu == "Descriptive":
                st.subheader("Descriptive stats")

                with st.beta_expander("Data Types"):
                        st.dataframe(df.dtypes)

                with st.beta_expander("Descriptive Summary"):
                        st.dataframe(df.describe())


            else:
                st.subheader("Plots")
                with st.beta_expander("Histogram"):

                        col = st.selectbox("Select a numeric column", df.columns.to_list())
                        no_bins = st.number_input("Insert number of bins", min_value= 1, value = 10, step=1)
                        p1 = px.histogram(df, x = col, nbins= no_bins)
                        st.plotly_chart(p1)

    elif choice == "DistFitting":
        st.subheader("DistFitting")
        data_file = load_data()
        if data_file is not None:
            df = pd.read_csv(data_file)
            task = st.selectbox("Select Type of Distribution Fitting", ["Fit common distributions", "Fit selected distributions"])

            if task == "Fit common distributions":
                col = st.selectbox("Select a numeric column", df.columns.to_list())
                selection = st.selectbox("Best Fitted Distribution Parameter Selection Criteria", ["sumsquare_error", "aic", "bic"])

                if st.button("Process"):
                    st.success("Top Five Distribution Summary")
                    data = df[col].values
                    f = Fitter(data,
                               distributions = get_common_distributions())
                    fig, ax = plt.subplots()
                    f.fit()
                    st.dataframe(f.summary())
                    st.success("Fitted Distribution Plot")
                    st.pyplot(fig)

                    st.success(f"Best Distribution Parameters Based on {selection} Sorting Criteria")
                    st.write(f.get_best(method = selection))

            else:
                dists = st.multiselect("Select multiple distribution", get_distributions())
                col = st.selectbox("Select a numeric column", df.columns.to_list())
                selection = st.selectbox("Best Fitted Distribution Parameter Selection Criteria", ["sumsquare_error", "aic", "bic"])
                if st.button("Process"):
                    st.success("Top Five Distribution Summary")
                    f = Fitter(df[col],
                               distributions=dists)
                    f.fit()
                    fig, ax = plt.subplots()
                    f.fit()
                    st.dataframe(f.summary())
                    st.success("Fitted Distribution Plot")
                    st.pyplot(fig)

                    st.success(f"Best Distribution Parameters Based on {selection} Sorting Criteria")
                    st.write(f.get_best(method = selection))


    else:
        st.subheader("About")


if __name__ == "__main__":
    main()

