import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_comparison_chart():
    # 1. Load the results we just generated
    print("Loading results and generating chart...")
    df = pd.read_csv('data/peer_comparison_results.csv')
    
    # Format the date for better looking charts
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')

    # 2. Set up the professional chart style
    sns.set_theme(style="whitegrid", palette="muted")
    plt.figure(figsize=(12, 7))

    # 3. Prepare the data for a side-by-side bar chart
    # We want to compare 'Profit_Surprise_%' and '5-Day_CAR_%' for each event
    df_melted = df.melt(id_vars=['Ticker', 'Date'], 
                        value_vars=['Profit_Surprise_%', '5-Day_CAR_%'],
                        var_name='Metric', value_name='Percentage')

    # 4. Create the bar plot
    # We use a custom color palette: Blue for Surprise, Orange for Market Reaction
    chart = sns.barplot(x='Date', y='Percentage', hue='Metric', data=df_melted, 
                        palette=['#2c3e50', '#e67e22'])

    # 5. Add titles and labels
    plt.title('Earnings Intelligence: Profit Surprise vs. 5-Day Market Reaction (CAR)\nInfosys vs. Wipro', 
              fontsize=14, fontweight='bold', pad=20)
    plt.ylabel('Percentage (%)', fontsize=12)
    plt.xlabel('Earnings Announcement Date', fontsize=12)
    plt.legend(title='Metric', fontsize=10)
    plt.xticks(rotation=45)

    # Add a horizontal line at 0% to clearly show positive vs negative
    plt.axhline(0, color='black', linewidth=1.5)

    # Add value labels on top of the bars for clarity
    for p in chart.patches:
        chart.annotate(format(p.get_height(), '.2f') + '%', 
                       (p.get_x() + p.get_width() / 2., p.get_height()), 
                       ha = 'center', va = 'center', 
                       xytext = (0, 10), textcoords = 'offset points',
                       fontsize=9)

    # 6. Save the chart as a high-quality image
    plt.tight_layout()
    plt.savefig('data/peer_comparison_chart.png', dpi=300, bbox_inches='tight')
    print("Success! Chart saved to: data/peer_comparison_chart.png")
    
    # Show the chart on your screen
    plt.show()

if __name__ == "__main__":
    generate_comparison_chart()