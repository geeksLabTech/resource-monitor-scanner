import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def launch_gui(csv_name='system_usage_log.csv'):
    st.set_option('deprecation.showPyplotGlobalUse', False)

    # Read the CSV file
    data = pd.read_csv(csv_name)

    # Convert the 'Time' column to datetime format
    data['Time'] = pd.to_datetime(data['Time'])

    # Set the 'Time' column as the index
    data.set_index('Time', inplace=True)

    # Plotting the data
    st.title('System Usage Log')
    st.subheader('Network I/O, CPU, Memory, and GPU Usage over Time')

    # Select the chart type
    chart_type = st.selectbox('Select Chart Type', [
                            'Line Chart', 'Area Chart', 'Bar Chart', 'Pie Chart', 'Scatter Plot', 'Heatmap', 'Violin Plot'])

    # Select the columns to display

    # Plot the selected columns
    if chart_type not in ['Violin Plot']:
        columns = st.multiselect('Select Columns', list(data.columns))
        if columns:
            if chart_type == 'Line Chart':
                data[columns].plot(kind='line')
            elif chart_type == 'Area Chart':
                data[columns].plot(kind='area', stacked=False)
            elif chart_type == 'Bar Chart':
                data[columns].plot(kind='bar', stacked=False)
            elif chart_type == 'Pie Chart':
                # Calculate the average value for each column
                average_values = data[columns].mean()
                plt.pie(average_values, labels=average_values.index, autopct='%1.1f%%')
            elif chart_type == 'Scatter Plot':
                for column in columns:
                    plt.scatter(data.index, data[column], label=column)

            elif chart_type == 'Heatmap':
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.heatmap(data[columns].corr(), annot=True,
                            fmt=".2f", cmap='coolwarm', ax=ax)
                plt.title('Correlation Heatmap')
                
            # Display the plot using Streamlit
            plt.legend()
            st.pyplot()
            
    elif chart_type == 'Violin Plot':
            fig, ax = plt.subplots()
            
            x_axis = st.selectbox('Select Variable', list(data.columns))
            y_axis = st.selectbox('Select Class', list(data.columns))
            
            if x_axis and y_axis:
                sns.violinplot(x=data[x_axis], y=data[y_axis], ax=ax)

                plt.xlabel(x_axis)
                plt.ylabel(y_axis)
                plt.title('Violin Plot')
                
                plt.legend()
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

if __name__ == '__main__':
    launch_gui()