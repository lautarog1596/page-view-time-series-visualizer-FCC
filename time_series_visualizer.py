import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Clean the data by filtering out days when the page views were in the top 2.5% 
# of the dataset or bottom 2.5% of the dataset.
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]
print(df.head())

# Create a draw_line_plot function that uses Matplotlib to draw a line chart similar 
# to "examples/Figure_1.png". The title should be "Daily freeCodeCamp Forum Page Views 5/2016-12/2019". 
# The label on the x axis should be "Date" and the label on the y axis should be "Page Views".
def draw_line_plot():
    # Draw line plot
    fig = plt.figure(figsize=(10, 5))
    plt.plot(df.index, df.value, color='r', linewidth=1) 
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


# Create a draw_bar_plot function that draws a bar chart similar to "examples/Figure_2.png". 
# It should show average daily page views for each month grouped by year. 
# The legend should show month labels and have a title of "Months". On the chart, the label 
# on the x axis should be "Years" and the label on the y axis should be "Average Page Views".
def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df['month'] = df.index.month
    df['year'] = df.index.year
    print(df.head())
    df_bar = df.groupby(['year', 'month'])['value'].mean()
    print(df_bar.head())
    df_bar = df_bar.unstack()
    print(df_bar.head())

    # Draw bar plot
    fig = df_bar.plot.bar(legend=True, figsize=(8,6), ylabel='Average Page Views', xlabel='Years').figure
    plt.legend(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 
                'September', 'October', 'November', 'December'], title="Months")
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


# Create a draw_box_plot function that uses Seaborn to draw two adjacent box plots similar to 
# "examples/Figure_3.png". These box plots should show how the values are distributed within 
# a given year or month and how it compares over time. The title of the first chart should be 
# "Year-wise Box Plot (Trend)" and the title of the second chart should be 
# "Month-wise Box Plot (Seasonality)". Make sure the month labels on bottom start at "Jan" and the 
# x and x axis are labeled correctly. The boilerplate includes commands to prepare the data.
def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    df_box['month_num'] = df_box['date'].dt.month  # dt: Accessor object for datetimelike properties of the Series values.
    df_box = df_box.sort_values('month_num')
    
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10,5))
    axes[0] = sns.boxplot(x=df_box['year'], y=df_box['value'], ax=axes[0])
    axes[1] = sns.boxplot(x=df_box['month'], y=df_box['value'], ax=axes[1])
    
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
