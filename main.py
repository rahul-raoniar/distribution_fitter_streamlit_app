# Core package
import streamlit as st
import streamlit.components.v1 as stc
import plotly.express as px
from fitter import Fitter, get_common_distributions, get_distributions
import matplotlib.pyplot as plt
import pandas as pd
import time


# HTML styling
html_temp = """
		<div style="background-color:#3872fb;padding:10px;border-radius:10px">
		<h1 style="color:white;text-align:center;">Distribution Fitter Web App </h1>
		<h4 style="color:white;text-align:center;">Developed by Rahul Raoniar </h4>
		</div>
		"""

# Home page
desc_temp = """

			 #### <span style="color:blue">**App Content** 📑</span>
			 The distribution fitter application will help you compare multiple distributions and 
			   find the best one that fits your data. The application comprised of four sections described as follows: 
			 
			1. <span style="color:lightcoral">**Home** 🏡</span>: Basic Information
			2. <span style="color:lightcoral">**Exploratory Data Analysis**</span> 🧮: Exploratory Data Analysis
			    * Descriptive Statistics
				* Histogram Plotting (using Plotly)
			3. <span style="color:lightcoral">**Distribution Fitting**</span> 🌈: Fitting distribution using Fitter Python Library
			    * Fitting Common Distributions
				* Fitting Distributions by Manual Selection
			4. <span style="color:lightcoral">**About**</span> 📑: About the Application
				  
			### <span style="color:blue">**Purpose of Ditribution Fitter Web Application** 💡</span> 
			Hi! i'm **```Rahul Raoniar```**. I’m a transportation researcher 🧪 and my speciality is pedestrian safety 🚶‍.
			 For that reason, I’m very fortunate that I get to work with lots of data every day. As a pedestrian safety
			  researcher, I often work with pedestrian crossing speed (average speed maintained by pedestrians while
			   crossing a road) or waiting time at intersections. For this type of continuous data, I often need to identify
			    the best-suited distribution. Last week I started searching open-source libraries for fitting distributions.
			     Even though there are several libraries available for R and Python they are fragmented. Fragmented in
			      the sense that they only support very common distributions.
			   
			   After going through so many libraries and their documentation, I came across the ```Fitter``` library developed 
			   by **```Thomas Cokelaer```**. This library is a ```lifesaver```. It uses ```Scipy``` library in the backend for distribution 
			   fitting and supports ```80 distributions```, which is huge. 
			   
			   After using the fitter library I realized that it 
			   is an underrated library, and students and researchers should know about it. For that reason, I wrote the following blog.
			   
			   [Finding the Best Distribution that Fits Your Data using Python’s Fitter Library](https://towardsdatascience.com/finding-the-best-distribution-that-fits-your-data-using-pythons-fitter-library-319a5a0972e9)
			   
			   Later, I developed this app for making distribution fitting easy and free for everyone.
			   
			   **```I hope everyone benefits from it.```**
			   
			   <span style="color:steelblue">Regards</span>
			   
			   <span style="color:darkred">**Rahul Raoniar**</span>
			   
			   Connect with me on 🌍 [Linkedin](https://linkedin.com/in/rahul-raoniar) and [Medium](https://medium.com/@rahul.raoniar)




			#### <span style="color:blue">Fitter Library 📚</span>
			For the distribution fitting part I have used the Python's Fitter Library (developed by **```Thomas Cokelaer```**)
				   
			[Fitter Library Github Page Link](https://github.com/cokelaer/fitter) 
			


			"""

# About page
about_text = """
			### <span style="color:blue">**About Continuous Distribution Fitter Application**</span>
			
			   The distribution fitter application will help you compare multiple distributions and 
			   find the best one that fits your data. The application comprised of four sections described as follows:


			#### <span style="color:blue">1. Home</span>
			The home page provides a basic information regarding the application. Additionally, it provides developer information and site
			 related details.
				   
				   Github Page: https://github.com/cokelaer/fitter
			
			 #### <span style="color:blue">2. Exploratory Data Analysis</span>
			 The ```Exploratory Data Analysis``` section comprised of two subsections, ```Descriptive Stats``` and ```Visualization```.
			 
			 **```1. Descriptive Stats :```** A descriptive statistical analysis part has been added to check the data types and basic
			 statistics to get overall idea about the data.
			 
			 
			 **```2. Visualization :```**
			 Before you start fitting various distributions it is often recommended to plot a histogram, which will help you understand overall
			 distribution your data follows. This will bring down the number of distributions you might need for comparision which
			  eventually save you time.
			 
			 #### <span style="color:blue">3. Distribution Fitting</span>
			  The ```fitter``` class of ```fitter``` library in the backend uses
			  the Scipy library which supports 80 distributions. The Fitter class will scan common distributions or
			  manually selected distributions, call the fit function for you, ignoring those that fail or run forever and finally
			  give you a summary of the best distributions in the sense of sum of the square errors.  
			  
			  In this section two separate distribution fitting methods has been deployed which are described as follows:  
			  
			  **```1. Fit Common Distributions :```** You can select ```Fit Common Distributions``` from the drop down menu which will fit
			    ten common distributions provided by the  ```get_common_distributions( )``` function. The ten common distributions are
			    ```[‘cauchy’, ‘chi2’, ‘expon’, ‘exponpow’, ‘gamma’, ‘lognorm’, ‘norm’, ‘powerlaw’, ‘rayleigh’, ‘uniform’].```
			    
			* Once you click ```process```, the application will start fitting all common distributions and return top five distributions' summary in ascending 
			order of the error [distribution with lowest error on top]. By default the distributions are ranked based on 
			```sumsquare_error```. 
			
			* You can select best distribution parameters by sorting the fitting error based on ```sumsquare_error```, ```aic``` or ```bic```
			criteria
			  
			  
			  **```2. Fit Selected Distributions:```** If you have initial idea about possible distributions that might fit your data
			  then select ```Fit Selected Distributions``` from the drop down menu and select all the distribution that you want to fit.  
			 
			 * Once you click ```process```, the application will start fitting all selected distributions and return top five distributions' summary in ascending 
			order of the error [distribution with lowest error on top]. By default the distributions are ranked based on 
			```sumsquare_error```. 
			
			* Here also you can select best distribution parameters by sorting the fitting error based on ```sumsquare_error```, ```aic``` or ```bic```
			criteria
			 
			#### <span style="color:blue">4. About Application</span>
			The about section provides a breif description of the application's functionality.  

			"""


def load_data():
    data_file = st.file_uploader("Upload a CSV File", type=["csv"])
    return data_file


# def progress_bar(sleep_val = 0.1):
#     pro = st.progress(0)
#     for percent_complete  in range(100):
#         time.sleep(sleep_val)
#         pro.empty()
#         pro.progress(percent_complete + 1)



def main():
    stc.html(html_temp)
    menu = ["Home", "Exploratory Data Analysis", "Distribution Fitting", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.header("Home")
        st.markdown(desc_temp, unsafe_allow_html=True)

    elif choice == "Exploratory Data Analysis":
        st.header("Exploratory Data Analysis")
        data_file = load_data()
        if data_file is not None:
            df = pd.read_csv(data_file)
            st.write(f"The file contains {df.shape[0]} rows and {df.shape[1]} columns")
            st.dataframe(df)

            submenu = st.sidebar.selectbox("Submenu",
                                      ["Descriptive Stats", "Visualization"])

            if submenu == "Descriptive Stats":
                st.header("Descriptive Stats")

                with st.beta_expander("Data Types"):
                        st.dataframe(df.dtypes)

                with st.beta_expander("Descriptive Summary"):
                        st.dataframe(df.describe())

            else:
                st.header("Visualization")
                with st.beta_expander("Histogram"):

                        col = st.selectbox("Select a Numeric Column", df.columns.to_list())
                        no_bins = st.number_input("Insert Number of Bins", min_value= 1, value = 10, step=1)
                        p1 = px.histogram(df, x = col, nbins= no_bins)
                        st.plotly_chart(p1)

    elif choice == "Distribution Fitting":
        st.header("Distribution Fitting")
        data_file = load_data()
        if data_file is not None:
            df = pd.read_csv(data_file)
            task = st.selectbox("Select Type of Distribution Fitting", ["Fit Common Distributions", "Fit Selected Distributions"])

            if task == "Fit Common Distributions":
                col = st.selectbox("Select a Numeric Column", df.columns.to_list())
                selection = st.selectbox("Best Fitted Distribution Parameter Selection Criteria", ["sumsquare_error", "aic", "bic"])

                if st.button("Process"):
                    with st.spinner('Wait for it... ⏳'):
                        time.sleep(5)
                        with st.spinner('Almost done... 👏👏'):
                            time.sleep(2)
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
                            st.dataframe(f.get_best(method = selection))
                            best_name = f.get_best(method = selection)
                            key_name = list(best_name.keys())
                            key_list = ' '.join([str(element) for element in key_name])
                            st.success(f"For More Information on {key_list} Distribution Parameters Visit Scipy Documentation")
                            st.markdown(f"[Scipy's {key_list} Distribution Documentation Link](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.{key_list}.html)", unsafe_allow_html=True)

            else:
                dists = st.multiselect("Select One or More Distributions", get_distributions())
                col = st.selectbox("Select a Numeric Column", df.columns.to_list())
                selection = st.selectbox("Best Fitted Distribution Parameter Selection Criteria", ["sumsquare_error", "aic", "bic"])
                if st.button("Process"):
                    with st.spinner('Wait for it... ⏳'):
                        time.sleep(5)
                        with st.spinner('Almost done... 👏👏'):
                            time.sleep(5)
                            st.success("Top Distributions' Summary")
                            f = Fitter(df[col], distributions = dists)
                            f.fit()
                            fig, ax = plt.subplots()
                            f.fit()
                            st.dataframe(f.summary())
                            st.success("Fitted Distribution Plot")
                            st.pyplot(fig)

                            st.success(f"Best Distribution Parameters Based on {selection} Sorting Criteria")
                            st.dataframe(f.get_best(method = selection))
                            best_name = f.get_best(method = selection)
                            key_name = list(best_name.keys())
                            key_list = ' '.join([str(element) for element in key_name])
                            st.success(f"For More Information on {key_list} Distribution Parameters Visit Scipy Documentation")
                            st.markdown(
                                f"[Scipy's {key_list} Distribution Documentation Link](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.{key_list}.html)",
                                unsafe_allow_html=True)


    else:
        st.header("About")
        st.markdown(about_text, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

