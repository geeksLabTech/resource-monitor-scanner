import streamlit as st
import pandas as pd

st.set_option('deprecation.showPyplotGlobalUse', False)

# Read the CSV file
data = pd.read_csv('system_usage_log.csv')

# Convert the 'Time' column to datetime format
data['Time'] = pd.to_datetime(data['Time'])

# Set the 'Time' column as the index
data.set_index('Time', inplace=True)

# Plotting the data
st.title('System Usage Log')
st.subheader('CPU, Memory, and GPU Usage over Time')

# Select the chart type
chart_type = st.selectbox('Select Chart Type', [
                          'Line Chart', 'Area Chart', 'Bar Chart'])

# Select the columns to display
columns = st.multiselect('Select Columns', list(data.columns))

# Plot the selected columns
if columns:
    if chart_type == 'Line Chart':
        data[columns].plot(kind='line')
    elif chart_type == 'Area Chart':
        data[columns].plot(kind='area', stacked=False)
    elif chart_type == 'Bar Chart':
        data[columns].plot(kind='bar', stacked=False)

    # Display the plot using Streamlit
    st.pyplot()

st.subheader('Summary')
statistics = {
    'Minimum': data.min(),
    'Maximum': data.max(),
    'Average': data.mean()
}
# Create a new DataFrame with the statistics
st.write(pd.DataFrame(statistics))

# Display the raw data
st.subheader('Raw Data')
st.write(data)
