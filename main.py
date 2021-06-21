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
			### <span style="color:blue">**Continuous Distribution Fitter App**</span>
			
			   Compare multiple distributions and find the best that fits your data.


			#### <span style="color:blue">Fitter Library</span>
			For the distribution fitting part I have used the Python's Fitter Library (developed by Thomas Cokelaer)
				   
				   Github Page: https://github.com/cokelaer/fitter
			
			 #### <span style="color:blue">App Content</span>
			 The Application comprised of four sections described as follows: 
			 
				  1. Home: Basic Information
				  2. EDA Section: Exploratory Data Analysis
							    - Descriptive Statistics
							    - Histogram Plotting (using Plotly)
				  3. Distribution Fitting: Fitting distribution using Fitter Python Library
							    - Fitting Common Distributions
							    - Fitting Distributions by Manual Selection
				  4. About: About the App

			"""

about_text = """
			### <span style="color:red">**About Continuous Distribution Fitter Application**</span>
			
			   The distribution fitter application will help you compare multiple distributions and 
			   find the best one that fits your data. The application comprised of four sections described as follows:


			#### <span style="color:blue">1. Home</span>
			The home page provides a basic information regarding the application. It provides developer information and site
			 related details.
				   
				   Github Page: https://github.com/cokelaer/fitter
			
			 #### <span style="color:blue">2. Exploratory Data Analysis</span>
			 The ```Exploratory Data Analysis``` This part comprised of two sections an ```Exploratory Analysis``` and ```Visualization```
			 of overall distribution.
			 
			 **```1. Exploratory Analysis :```** An exploratory analysis part has been added to check the data types and basic
			 statistics to get overall idea about the data.
			 
			 
			 **```2. Plot Visualization :```**
			 Before you start fitting various distribution it is often recommended to plot a histogram, which help you understand overall
			 distribution your data follows. This will bring down the number of distributions you might need for comparision which
			  eventually save you time.
			 
			 #### <span style="color:blue">3. Distribution Fitting</span>
			  The fitter class of fitter library in the backend uses
			  the Scipy library which supports 80 distributions. The Fitter class will scan common distributions or
			  manually selected distributions, call the fit function for you, ignoring those that fail or run forever and finally
			  give you a summary of the best distributions in the sense of sum of the square errors.  
			  
			  In this section two separate distribution fitting methods have been deployed.  
			  
			  **```1. Fit Common Distributions :```** You can select ```Fit Common Distributions``` from the drop down menu which will fit
			    ten common distributions provided by the  ```get_common_distributions( )``` function. The ten common distributions are
			    ```[‘cauchy’, ‘chi2’, ‘expon’, ‘exponpow’, ‘gamma’, ‘lognorm’, ‘norm’, ‘powerlaw’, ‘rayleigh’, ‘uniform’].```
			    
			* The application will starts fitting all common distributions and return top five distributions' summary in ascending 
			order of the error [distribution with lowest error on top]. By default the distributions are ranked based on 
			```sumsquare_error```. 
			
			* You can select best distribution parameters by sorting the error based on ```sumsquare_error```, ```aic``` or ```bic```
			criteria
			  
			  
			  **```2. Fit Selected Distributions:```** If you have initial idea about possible distributions that might fit your data
			  then select ```Fit Selected Distributions``` from the drop down menu and select all the distribution that you want to fit.  
			 
			 * The application will starts fitting all selected distributions and return top five distributions' summary in ascending 
			order of the error [distribution with lowest error on top]. By default the distributions are ranked based on 
			```sumsquare_error```. 
			
			* Here also you can select best distribution parameters by sorting the error based on ```sumsquare_error```, ```aic``` or ```bic```
			criteria
			 
			 #### <span style="color:blue">4. About Application</span>
			 The about section provides a breif description of the application's functionality.  

			"""
			
			#### <span style="color:blue">App Content</span>

            #
            #
            #   About
            #
			#
			# """


def load_data():
    data_file = st.file_uploader("Upload a CSV", type=["csv"])
    return data_file


def main():
    stc.html(html_temp)
    menu = ["Home", "EDA", "DistFitting", "About"]
    choice = st.sidebar.selectbox("Menu", menu)


    if choice == "Home":
        st.header("Home")
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
        st.markdown(about_text, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

