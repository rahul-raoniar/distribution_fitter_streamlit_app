The distribution fitter application will help you compare multiple distributions and find the best one that fits your data. The application comprised of four sections described as follows:


1. <span style="color:lightcoral">**Home** 🏡</span>: Basic Information
2. <span style="color:lightcoral">**Exploratory Data Analysis**</span> 🧮: Exploratory Data Analysis
			    * Descriptive Statistics
				* Histogram Plotting (using Plotly)
 3. <span style="color:lightcoral">**Distribution Fitting**</span> 🌈: Fitting distribution using Fitter Python Library
			    * Fitting Common Distributions
				* Fitting Distributions by Manual Selection
4. <span style="color:lightcoral">**About**</span> 📑: About the Application

### <span style="color:blue">1. Home</span>
The home page provides a basic information regarding the application. Additionally, it provides developer information and site related details.

		Github Page: https://github.com/cokelaer/fitter

### <span style="color:blue">2. Exploratory Data Analysis</span>
The ```Exploratory Data Analysis``` section comprised of two subsections, ```Descriptive Stats``` and ```Visualization```.

**2.1 Descriptive Stats:**
A descriptive statistical analysis part has been added to check the data types and basic statistics to get overall idea about the data.


**2.2 Visualization:** 
Before you start fitting various distributions it is often recommended to plot a histogram, which will help you understand overall distribution your data follows. This will bring down the number of distributions you might need for comparision which eventually save you time.

### <span style="color:blue">3. Distribution Fitting</span>
The ```fitter``` class of ```fitter``` library in the backend uses the Scipy library which supports 80 distributions. The Fitter class will scan common distributions or manually selected distributions, call the fit function for you, ignoring those that fail or run forever and finally give you a summary of the best distributions in the sense of sum of the square errors.  

In this section two separate distribution fitting methods has been deployed which are described as follows:  

**3.1. Fit Common Distributions :** You can select ```Fit Common Distributions``` from the drop down menu which will fit ten common distributions provided by the ```get_common_distributions( )``` function. The ten common distributions are ```[‘cauchy’, ‘chi2’, ‘expon’, ‘exponpow’, ‘gamma’, ‘lognorm’, ‘norm’, ‘powerlaw’, ‘rayleigh’, ‘uniform’].```

* Once you click ```process```, the application will start fitting all common distributions and return top five distributions' summary in ascending order of the error [distribution with lowest error on top]. By default the distributions are ranked based on ```sumsquare_error```. 

* You can select best distribution parameters by sorting the fitting error based on ```sumsquare_error```, ```aic``` or ```bic```
			criteria


**3.2. Fit Selected Distributions:** If you have initial idea about possible distributions that might fit your data then select ```Fit Selected Distributions``` from the drop down menu and select all the distribution that you want to fit.  

* Once you click ```process```, the application will start fitting all selected distributions and return top five distributions' summary in ascending order of the error [distribution with lowest error on top]. By default the distributions are ranked based on ```sumsquare_error```. 

* Here also you can select best distribution parameters by sorting the fitting error based on ```sumsquare_error```, ```aic``` or ```bic``` criteria

### <span style="color:blue">4. About Application</span>
The about section provides a breif description of the application's functionality.  
