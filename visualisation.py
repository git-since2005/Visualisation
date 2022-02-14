
# Import modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

@st.cache()
def load_data():
	# Load the Adult Income dataset into DataFrame.

	df = pd.read_csv('adult (1).csv', header=None)
	df.head()

	# Rename the column names in the DataFrame using the list given above. 

	# Create the list
	column_name =['age', 'workclass', 'fnlwgt', 'education', 'education-years', 'marital-status', 'occupation', 'relationship', 'race','gender','capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income']

	# Rename the columns using 'rename()'
	for i in range(df.shape[1]):
	  df.rename(columns={i:column_name[i]},inplace=True)

	# Print the first five rows of the DataFrame
	df.head()

	# Replace the invalid values ' ?' with 'np.nan'.

	df['native-country'] = df['native-country'].replace(' ?',np.nan)
	df['workclass'] = df['workclass'].replace(' ?',np.nan)
	df['occupation'] = df['occupation'].replace(' ?',np.nan)

	# Delete the rows with invalid values and the column not required 

	# Delete the rows with the 'dropna()' function
	df.dropna(inplace=True)

	# Delete the column with the 'drop()' function
	df.drop(columns='fnlwgt',axis=1,inplace=True)

	return df

census_df = load_data()

# Filter warnings for streamlit web app
st.set_option("deprecation.showPyplotGlobalUse", False)

# Start designing the app
st.title("Graph visualisation app for data")
st.sidebar.title("Graph visualisation app for data")
if st.sidebar.checkbox("Show Data"):
	st.dataframe(census_df)
st.sidebar.subheader("Visualisation Selector")
plots = st.sidebar.multiselect("Input visualisations", ('Countplot', 'Box Plot', 'Pie Chart', 'Correlation Heatmap', 'Pair Plot'))
plt.figure(figsize = (17, 6))
cols_count = st.sidebar.multiselect("Input columns need to plot for countplot", tuple(census_df.columns))
cols_pie = st.sidebar.multiselect("Input columns need to plot for pie", ('gender', 'income'))
cols_boxplot = st.sidebar.multiselect("Input columns need to plot for boxplot", ("hours-per-week", 'capital-loss', 'capital-gain'))
if 'Pie Chart' in plots:
	for i in cols_pie:
		st.subheader(f"Pie chart for {i}")
		plt.pie(census_df[i].value_counts(), autopct = '%1.2f%%', explode = np.linspace(.05, .15, len(census_df[i].value_counts())), labels = census_df[i].value_counts().index)
		st.pyplot()
if 'Countplot' in plots:
	for i in cols_count:
		st.subheader(f"Countplot for {i}")
		sns.countplot(x = census_df[i], hue = 'income', data = census_df)
		st.pyplot()
if 'Box Plot' in plots:
	for i in cols_boxplot:
		st.subheader(f"Box plot for {i} employers work")
		sns.boxplot(x = i, y = 'gender', hue = census_df['gender'], data = census_df)
		st.pyplot()
		sns.boxplot(x = i, y = 'income', hue = census_df['income'], data = census_df)
		st.pyplot()
if 'Correlation Heatmap' in plots:
	st.subheader("Correlation heatmap for dataset")
	sns.heatmap(census_df.corr(), annot = True)
	st.pyplot()
if 'Pair Plot' in plots:
	st.subheader("Pair Plot for dataset")
	sns.pairplot(census_df)
	st.pyplot()
# print(census_df.info())
