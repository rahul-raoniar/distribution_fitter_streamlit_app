# Core package
import streamlit as st
import streamlit.components.v1 as stc
import plotly.express as px
from fitter import Fitter, get_common_distributions, get_distributions
import matplotlib.pyplot as plt
import pandas as pd
import time


from all_params import dist_list, dist_parm_dict
from all_texts import html_temp, desc_temp, about_text



param_val = []

def load_data():
    data_file = st.file_uploader("Upload a CSV File", type=["csv"])
    return data_file

def search_parm(keyword):
    for key in dist_parm_dict:
        if key == keyword:
            return dist_parm_dict[key]


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

            submenu = st.sidebar.selectbox("Submenu",
                                           ["Descriptive Stats", "Visualization"])

            if submenu == "Descriptive Stats":
                st.header("Descriptive Stats")
                st.dataframe(df)

                with st.beta_expander("Data Types"):
                    st.dataframe(df.dtypes)

                with st.beta_expander("Descriptive Summary"):
                    st.dataframe(df.describe())

            else:
                st.header("Visualization")
                with st.beta_expander("Histogram"):

                    col = st.selectbox("Select a Numeric Column", df.columns.to_list())
                    no_bins = st.number_input("Insert Number of Bins", min_value=1, value=10, step=1)
                    p1 = px.histogram(df, x=col, nbins=no_bins)
                    st.plotly_chart(p1)

    elif choice == "Distribution Fitting":
        st.header("Distribution Fitting")
        data_file = load_data()
        if data_file is not None:
            df = pd.read_csv(data_file)
            task = st.selectbox("Select Type of Distribution Fitting",
                                ["Fit Common Distributions", "Fit Selected Distributions"])

            if task == "Fit Common Distributions":
                col = st.selectbox("Select a Numeric Column", df.columns.to_list())
                bins_input = st.number_input("Insert Number of Bins", min_value=1, value=100, step=1)
                selection = st.selectbox("Best Fitted Distribution Parameter Selection Criteria",
                                         ["sumsquare_error", "aic", "bic"])

                if st.button("Process"):
                    with st.spinner('Wait for it... ⏳'):
                        time.sleep(5)
                        with st.spinner('Almost done... 👏👏'):
                            time.sleep(2)
                            st.success("Top Five Distribution Summary Based on Sum Squared Error Sorting Criteria")
                            data = df[col].values
                            f = Fitter(data, distributions = get_common_distributions(), bins=bins_input)
                            fig, ax = plt.subplots()
                            f.fit()
                            st.dataframe(f.summary())
                            st.success("Fitted Distribution Plot")
                            st.pyplot(fig)

                            st.success(f"Best Fitted Distribution and Parameters Based on {selection} Sorting Criteria")
                            best_name = f.get_best(method = selection)
                            key_name = list(best_name.keys())
                            key_list = ' '.join([str(element) for element in key_name])

                            # Joining parameters and values
                            st.write(f"The Best Distribution is '{key_list}' and Fitted Parameters Are:")
                            tuple_val = f.get_best(method = selection)[key_list]
                            for i in tuple_val:
                                param_val.append(i)
                            parm_key = search_parm(key_list)
                            res = {parm_key[i]: param_val[i] for i in range(len(parm_key))}
                            st.write(res)


                            st.success(
                                f"For More Information on {key_list} Distribution Parameters Visit Scipy Documentation")

                            st.markdown(
                                f"[Scipy's {key_list} Distribution Documentation Link](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.{key_list}.html)",
                                unsafe_allow_html = True)

            else:
                dists = st.multiselect("Select One or More Distributions", dist_list)
                col = st.selectbox("Select a Numeric Column", df.columns.to_list())
                bins_input = st.number_input("Insert Number of Bins", min_value = 1, value = 100, step = 1)
                selection = st.selectbox("Best Fitted Distribution Parameter Selection Criteria",
                                         ["sumsquare_error", "aic", "bic"])

                if st.button("Process"):
                    with st.spinner('Wait for it... ⏳'):
                        time.sleep(5)
                        with st.spinner('Almost done... 👏👏'):
                            time.sleep(5)
                            st.success("Top Distributions' Summary Based on Sum Squared Error Sorting Criteria")
                            f = Fitter(df[col], distributions = dists, bins = bins_input)
                            f.fit()
                            fig, ax = plt.subplots()
                            f.fit()
                            st.dataframe(f.summary())
                            st.success("Fitted Distribution Plot")
                            st.pyplot(fig)

                            st.success(f"Best Fitted Distribution and Parameters Based on {selection} Sorting Criteria")
                            best_name = f.get_best(method=selection)
                            key_name = list(best_name.keys())
                            key_list = ' '.join([str(element) for element in key_name])

                            # Joining parameters and values
                            st.write(f"The Best Distribution is '{key_list}' and Fitted Parameters Are:")
                            tuple_val = f.get_best(method = selection)[key_list]
                            for i in tuple_val:
                                param_val.append(i)
                            parm_key = search_parm(key_list)
                            res = {parm_key[i]: param_val[i] for i in range(len(parm_key))}
                            st.write(res)

                            st.success(
                                f"For More Information on {key_list} Distribution Parameters Visit Scipy Documentation")

                            if key_list == "frechet_l":
                                st.markdown(
                                    f"[Scipy's {key_list} Distribution Documentation Link](https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.frechet_l.html)",
                                    unsafe_allow_html=True)

                            elif key_list == "frechet_r":
                                st.markdown(
                                    f"[Scipy's {key_list} Distribution Documentation Link](https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.frechet_r.html)",
                                    unsafe_allow_html=True)

                            elif key_list == "reciprocal":
                                st.markdown(
                                    f"[Scipy's {key_list} Distribution Documentation Link](https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.reciprocal.html)",
                                    unsafe_allow_html=True)

                            else:
                                st.markdown(
                                    f"[Scipy's {key_list} Distribution Documentation Link](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.{key_list}.html)",
                                    unsafe_allow_html = True)


    else:
        st.header("About")
        st.markdown(about_text, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

