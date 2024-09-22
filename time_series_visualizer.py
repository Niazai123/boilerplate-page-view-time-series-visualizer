import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col="date", parse_dates=True)

# Clean data
# Filter out days in the top 2.5% or bottom 2.5%
df = df[(df['value'] >= df['value'].quantile(0.025)) &
        (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    fig = plt.figure(figsize=(12,6))
    plt.plot(df.index, df['value'], color='tab:red')  # Specify color for better readability
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    plt.title('Daily freeCodeCamp Forum Page Views ' +
              df.index[0].strftime('%-m/%Y') + '-' + df.index[-1].strftime('%-m/%Y'))

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df.index.year
    df_bar['month'] = df.index.month

    # Group by year and month, and calculate the mean for each group
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Get month names and sort correctly
    months = pd.date_range('2020-01', '2020-12', freq='MS').strftime('%B').tolist()

    # Draw bar plot
    fig = plt.figure(figsize=(12,6))
    
    # Plot the bar chart
    df_bar.plot(kind='bar', ax=plt.gca(), legend=True)
    
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months', labels=months, loc='upper left')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')

    # Get month order (for correct sorting in box plot)
    months = pd.date_range('2020-01', '2020-12', freq='MS').strftime('%b').tolist()

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(16, 4))

    # Year-wise Box Plot (Trend)
    sns.boxplot(x="year", y="value", data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Month-wise Box Plot (Seasonality)
    sns.boxplot(x="month", y="value", data=df_box, order=months, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
