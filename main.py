# Core package
import streamlit as st
import streamlit.components.v1 as stc
import plotly.express as px
from fitter import Fitter, get_common_distributions, get_distributions
import matplotlib.pyplot as plt

# EDA Packages
import pandas as pd


html_temp = """
		<div style="background-color:#3872fb;padding:10px;border-radius:10px">
		<h1 style="color:white;text-align:center;">Distribution Fitter Web App </h1>
		<h4 style="color:white;text-align:center;">Fitter Library </h4>
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

distribution_list = ['alpha',
 'anglit',
 'arcsine',
 'argus',
 'beta',
 'betaprime',
 'bradford',
 'burr',
 'burr12',
 'cauchy',
 'chi',
 'chi2',
 'cosine',
 'crystalball',
 'dgamma',
 'dweibull',
 'erlang',
 'expon',
 'exponnorm',
 'exponpow',
 'exponweib',
 'f',
 'fatiguelife',
 'fisk',
 'foldcauchy',
 'foldnorm',
 'frechet_l',
 'frechet_r',
 'gamma',
 'gausshyper',
 'genexpon',
 'genextreme',
 'gengamma',
 'genhalflogistic',
 'geninvgauss',
 'genlogistic',
 'gennorm',
 'genpareto',
 'gilbrat',
 'gompertz',
 'gumbel_l',
 'gumbel_r',
 'halfcauchy',
 'halfgennorm',
 'halflogistic',
 'halfnorm',
 'hypsecant',
 'invgamma',
 'invgauss',
 'invweibull',
 'johnsonsb',
 'johnsonsu',
 'kappa3',
 'kappa4',
 'ksone',
 'kstwo',
 'kstwobign',
 'laplace',
 'levy',
 'levy_l',
 'levy_stable',
 'loggamma',
 'logistic',
 'loglaplace',
 'lognorm',
 'loguniform',
 'lomax',
 'maxwell',
 'mielke',
 'moyal',
 'nakagami',
 'ncf',
 'nct',
 'ncx2',
 'norm',
 'norminvgauss',
 'pareto',
 'pearson3',
 'powerlaw',
 'powerlognorm',
 'powernorm',
 'rayleigh',
 'rdist',
 'recipinvgauss',
 'reciprocal',
 'rice',
 'rv_continuous',
 'rv_histogram',
 'semicircular',
 'skewnorm',
 't',
 'trapz',
 'triang',
 'truncexpon',
 'truncnorm',
 'tukeylambda',
 'uniform',
 'vonmises',
 'vonmises_line',
 'wald',
 'weibull_max',
 'weibull_min',
 'wrapcauchy']



def main():
    stc.html(html_temp)
    menu = ["Home", "EDA", "DistFitting", "About"]
    choice = st.sidebar.selectbox("Menu", menu)
    st.cache()
    data_file = st.file_uploader("Upload a CSV", type=["csv"])
    if data_file is not None:
        df = pd.read_csv(data_file)
        st.write(f"The file contains {df.shape[0]} rows and {df.shape[1]} columns")



    if choice == "Home":
        st.subheader("Home")
        st.markdown(desc_temp, unsafe_allow_html=True)



    elif choice == "EDA":
        st.subheader("EDA")
        if data_file is not None:
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
                no_bins = st.number_input("Insert a Number", min_value= 1, value = 10, step=1)
                p1 = px.histogram(df, x = col, nbins= no_bins)
                st.plotly_chart(p1)

    elif choice == "DistFitting":
        st.subheader("DistFitting")

        task = st.selectbox("Select Type of Fitting", ["Fit common distributions", "Fit selected distributions"])

        if task == "Fit common distributions":
            col = st.selectbox("Select a numeric column", df.columns.to_list())
            data = df[col].values
            f = Fitter(data,
                       distributions = get_common_distributions())
            fig, ax = plt.subplots()
            f.fit()
            st.dataframe(f.summary())

            st.pyplot(fig)

        else:
            dists = st.multiselect("Select multiple distribution", distribution_list)
            col = st.selectbox("Select a numeric column", df.columns.to_list())
            f = Fitter(df[col],
                       distributions=dists)
            f.fit()
            fig, ax = plt.subplots()
            f.fit()
            st.dataframe(f.summary())

            st.pyplot(fig)





    else:
        st.subheader("About")



if __name__ == "__main__":
    main()

