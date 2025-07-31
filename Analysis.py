import pandas as pd
from sqlalchemy import create_engine, text
import streamlit as st
from utils import (query, load)
import plotly.express as px
from queries import QUERIES
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots


st.title("Analysis")

t1, t2, t3, t4 = st.tabs(['General Exploration', 
                         'Sales Channel Analysis', 
                         'Top Performance',
                         'Operational Efficiency'
                        ])

with t1:

    st.write('Lets first get some general understanding of the dataset')
    col1, col2 = st.columns(2)

    with col1:
        n_suppliers = load('data/unique_suppliers.parquet').iloc[0, 0]
        st.metric(label="Unique Suppliers of 2019", value=n_suppliers)

        sum_retail_sales = load('data/total_retail_sales.parquet').iloc[0, 0]
        st.metric(label="Total Retail Sales (Cases) in 2019", value=sum_retail_sales)

        sum_retail_transfers = load('data/total_retail_transfers.parquet').iloc[0, 0]
        st.metric(label="Total Retail Transfers (Cases) in 2019", value=sum_retail_transfers)

        sum_warehouse_sales = load('data/total_warehouse_sales.parquet').iloc[0, 0]
        st.metric(label="Total Warehouse Sales (Cases) in 2019", value=sum_warehouse_sales)
    
    with col2:
        n_items_df = load('data/unique_item_types.parquet')
        n_items = n_items_df['item_type'].nunique()
        st.metric(label="Unique Item Types of 2019", value=n_items)
        st.dataframe(n_items_df, hide_index=True)
        

    overtime_sales = load('data/overtime_sales.parquet')
    overtime_sales['time'] = pd.to_datetime(overtime_sales['time'], format='%Y-%m')

    fig = px.line(
    overtime_sales,
    x='time',
    y=['retail_sales', 'retail_transfers', 'warehouse_sales'],
    title='Three Metrics Over 2019',
    markers=True
    )
    fig.update_xaxes(
    dtick="M1",                   
    tickformat="%b\n%Y",             
    range=['2018-12-15', '2019-12-31'] 
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
    """
    ---
    💡 **In the Next Tab:** We will be exploring the relationships between 
    these three metrics and analyze how any two or all three metrics correlate or affect each other in the next tab .
    """
    )



with t2:
    st.subheader("So what is the data telling us about these 3 metrics?")

    # Sales Channel Comparison
    st.write("""
    Lets first dive deeper and have a detail view into the porportion of contribution of different sales channels.
    """)
    overtime_sales = load('data/overtime_sales.parquet')
    overtime_sales = overtime_sales.sort_values(by='time')

    # Bigger Picture: Whos the main contributor
    fig = px.area(overtime_sales, x='time', y=['warehouse_sales', 'retail_sales'], 
                title = 'Bigger Pciture: Sales Channels Proportion',   labels={'value': 'Sales (cases)', 'time': 'Month', 'variable': 'Channel'},
                line_group='variable')

    fig.update_xaxes(
    dtick="M1",                   
    tickformat="%b\n%Y",             
    range=['2018-12-15', '2019-12-31'] 
    )

    st.plotly_chart(fig, use_container_width=True)


    # Trends Difference
    fig = px.line(overtime_sales, x='time', y=['warehouse_sales', 'retail_sales'], 
                title = 'Sales Channels Trend Over Time',   labels={'value': 'Sales (cases)', 'time': 'Month', 'variable': 'Channel'},
                line_group='variable')

    fig.update_xaxes(
    dtick="M1",                   
    tickformat="%b\n%Y",             
    range=['2018-12-15', '2019-12-31'] 
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Investigating the Sales Channel Correlation")
    st.write("""
    While the trends look similar, the statistical correlation is moderately positive (0.57).
    A scatterplot helps visualize this relationship more accurately.
    """)

    corr = overtime_sales[['retail_sales', 'warehouse_sales']].corr()
    st.write("Correlation between Retail and Warehouse Sales:")
    st.dataframe(corr)
    fig_corr = px.scatter(
        overtime_sales,
        x='retail_sales',
        y='warehouse_sales',
        title='Warehouse Sales vs. Retail Sales (Monthly, 2019)',
        labels={'retail_sales': 'Total Retail Sales', 'warehouse_sales': 'Total Warehouse Sales'},
        trendline='ols',
        trendline_scope="overall", # This adds a "line of best fit" to show the trend
        color_discrete_sequence=['yellow']
    )
    fig.update_xaxes(
    dtick="M1",                   
    tickformat="%b\n%Y",             
    range=['2018-12-15', '2019-12-31'] 
    )
    
    st.plotly_chart(fig_corr, use_container_width=True)



with t3:
    st.subheader("Which supplier is contributing the most?")
    supplierContribution = load('data/supplierContribution.parquet')
    df_80 = supplierContribution[supplierContribution['rolling_percentage'] <= 80.00]

    st.write("The following chart shows suppliers contributing up to 80% of the total cases of product sold (Pareto Principle):")
    df_plot = df_80.copy()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(
            x=df_plot['supplier'],
            y=df_plot['total_sales'],
            name='Total Sales',
            marker_color='#1f77b4'
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=df_plot['supplier'],
            y=df_plot['rolling_percentage'],
            name='Cumulative Percentage',
            line=dict(color='#FFDB33', width=1.5),
        ),
        secondary_y=True,
    )
    fig.update_layout(
        height=700,
        width=900,
        title_text="Pareto Analysis: Top Suppliers' Contribution to Sales",
        template='plotly_white',
        legend=dict(
            orientation="h", # Horizontal legend
            yanchor="bottom",
            y=1.02, # Position it just above the plot
            xanchor="right",
            x=1
        )
    )
    average_sales = df_plot['total_sales'].mean()

    fig.add_hline(
        y=average_sales,
        line_dash="dash",
        line_color="orange",
        annotation_text=f"Avg Sales (Cases of Products): {average_sales:.0f}",
        annotation_position="top left",
        secondary_y=False
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Supplier", tickangle=-45, showgrid=True)

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Total Sales (Cases)</b>", secondary_y=False, showgrid=False)
    fig.update_yaxes(title_text="<b>Cumulative Percentage (%)</b>", range=[0, 105], secondary_y=True)

    st.plotly_chart(fig, use_container_width=False)

    col1, col2=st.columns([1,2])

    with col1:
        num_suppliers = df_80['supplier'].nunique()
        st.metric(label='Number of suppliers in this chart', value=num_suppliers)

    with col2:
        top_suppliers= round((df_80['supplier'].nunique() / 325) * 100, 2)
        st.metric(label='Percentage of suppliers that make up **80%** of the sales in 2019', value=f'{top_suppliers} %')

        top_suppliers= round((4 / 325) * 100, 2)
        st.metric(label='Percentage of suppliers that make up **56%** of the sales in 2019', value=f'{top_suppliers} %')

    st.divider()
    st.subheader("So What?")

    st.markdown("""
    What we are seeing is a more extreme case of the Pareto Principle, where roughly **1%-5%** of the suppliers make up **56%-80%** of the sales.
    """)

    st.write("""
    This gives us critical insights into how ABS can allocate their resource regarding suppliers. For example, 
    having dedicated account manager for top 1-5% of suppliers, exclusive collaboration contract to secure supply, and discount on volume etc.

    Given the heavy reliance on the top suppliers, ABS also needs risk mitigation plans to ensure constant supplies.
    In addition to making sure such concern is taken care of in the contract with the top providers, develop or identify "fall back" suppliers is also critical. These suppliers
    can be from the 5% or from the remaining 95% who demonstrate a growth potential.While simple methods like comparing monthly or quarterly sales can be effective, 
    I decided to get creative and explore a more unique method.
    """)

    st.subheader('Identifying "Challenger" Suppliers: Can You Surge?')
    st.write("""
    I decided to define fall back suppliers by their ability to surge.
    In this method I look at the total sales each month by supplier for 2019, and try to identify, besides the 18 top suppliers, 
    who take over a spot in the top 18 during any given month.
    This might mean this supplier have the volume potentail to be an effective backups.
    """)

    supplier_monthly = load('data/monthly_sales_by_supplier.parquet')
    overall_top_18_suppliers = df_80['supplier'].unique()
    # print(len(overall_top_18_suppliers)) # comfirming this is 18

    all_challengers = []

    for month_num in range(1, 12):
        month_data = supplier_monthly[supplier_monthly['month'] == month_num]
        monthly_top_18 = month_data.sort_values(by='monthly_sales', 
                                                ascending=False).head(18)['supplier'].tolist()
        for supplier in monthly_top_18:
            if supplier not in overall_top_18_suppliers:
                all_challengers.append(supplier)

    challenger_counts = pd.Series(all_challengers).value_counts().reset_index()
    # print(challenger_counts.head())
    challenger_counts.columns = ['supplier', 'freqency_in_top_18']

    st.write("Top Challenger Suppliers (by number of months in the top 18):")
    st.dataframe(challenger_counts, hide_index=True)


    st.write("""
    Lets visualize the performance of the top 18 vs challengers, plotting the total sales of the top 18
    against the total sales of our newly identified challengers.
    """)
    # Viz of Top 18 v Challengers
    top_challengers = challenger_counts['supplier'].tolist()

    top_18_monthly = supplier_monthly[supplier_monthly['supplier'].isin(overall_top_18_suppliers)]
    challengers_monthly = supplier_monthly[supplier_monthly['supplier'].isin(top_challengers)]

    group_trends = pd.DataFrame({
        'Top 18 Sales': top_18_monthly.groupby('month')['monthly_sales'].sum(),
        'Challenger Sales': challengers_monthly.groupby('month')['monthly_sales'].sum()
    }).reset_index()

    # print(top_18_monthly.head())
    # print(top_18_monthly.groupby('month')['monthly_sales'].sum())
    # print(group_trends.head())

    fig_corr = make_subplots(specs=[[{"secondary_y": True}]])
    fig_corr.add_trace(go.Scatter(x=group_trends['month'], y=group_trends['Top 18 Sales'], name='Top 18 Sales'), secondary_y=False)
    fig_corr.add_trace(go.Scatter(x=group_trends['month'], y=group_trends['Challenger Sales'], name='Challenger Sales', line=dict(color='red')), secondary_y=True)
    fig_corr.update_layout(title_text="Sales Trends: Top 18 vs. Top Challengers")
    fig_corr.update_xaxes(title_text="Month of 2019")
    
    fig_corr.update_xaxes(
        dtick="M1",                   
        tickformat="%b\n%Y",             
        range=['2018-12-15', '2019-12-31'] 
    )
    fig_corr.update_yaxes(title_text="<b>Top 18 Sales (Cases)</b>", secondary_y=True, showgrid=False)
    fig_corr.update_yaxes(title_text="<b>Challenger Sales (Cases)</b>", secondary_y=False)
    st.plotly_chart(fig_corr, use_container_width=True)

    st.write("""Now it seems that while the overall trend might be somewhat similar, implying a shared market effect, we can see that at multiple point
    in time, when the Top 18 sales drop, the Challenger sales do surge (aka backup event). This is interesting. Lets verify by setting up a control group as well.
    """)



    # Viz of Top 18 v All Others
    st.subheader('Control Group: Top 18 vs. "All Other" Suppliers')
    st.write("""
    To confirm that the 'Challengers' are unique, we can compare the Top 18's trend
    against the trend of all other suppliers combined. If we don't see the same
    'backup' effect (or less so),  it strengthens our hypothesis.
    """)

    all_others_monthly = supplier_monthly[~supplier_monthly['supplier'].isin(overall_top_18_suppliers)]

    control_group_trends = pd.DataFrame({
        'Top 18 Sales': top_18_monthly.groupby('month')['monthly_sales'].sum(),
        'All Others Sales': all_others_monthly.groupby('month')['monthly_sales'].sum()
    }).reset_index()

    fig_control = make_subplots(specs=[[{"secondary_y": True}]])

    fig_control.add_trace(
        go.Scatter(
            x=control_group_trends['month'],
            y=control_group_trends['Top 18 Sales'],
            name='Top 18 Sales'
        ),
        secondary_y=False,
    )

    fig_control.add_trace(
        go.Scatter(
            x=control_group_trends['month'],
            y=control_group_trends['All Others Sales'],
            name='"All Others" Sales',
            line=dict(color='green')
        ),
        secondary_y=True,
    )

    fig_control.update_layout(title_text='Sales Trends: Top 18 vs. "All Other" Suppliers')
    fig_control.update_xaxes(title_text="Month of 2019")
    fig_control.update_yaxes(title_text="<b>Top 18 Sales (Cases)</b>", secondary_y=False, showgrid=False)
    fig_control.update_yaxes(title_text="<b>'All Others' Sales (Cases)</b>", secondary_y=False)

    fig_control.update_xaxes(
        dtick="M1",                   
        tickformat="%b\n%Y",             
        range=['2018-12-15', '2019-12-31'] 
    )

    st.plotly_chart(fig_control, use_container_width=True)

    st.write("""
    Our hypothesis seem to be right! The trend with Top 18 vs All Others are comforming, 
    signifying a even stronger shared market effect and less backup effect.
    """)


    st.subheader("Quantitative Proof: Comfirming What We Just Observed")
    st.write("""
    Now lets verify what we just saw by checking the direction of sales changes each month.
    If the Top 18's sales fall while Challenger sales rise, it's a 'Backup Event',
    supporting the hypothesis. We will do this by computing the sales differece between the current month
    and then previous month for each row
    """)

    st.markdown("##### Top 18 vs Challenger")

    group_trends['Top 18 Change'] = group_trends['Top 18 Sales'].diff()
    group_trends['Challenger Change'] = group_trends['Challenger Sales'].diff()

    def classify_event(row):
        top_change = row['Top 18 Change']
        challenger_change = row['Challenger Change']
        
        if pd.isna(top_change): # The first month has no previous month to compare to
            return 'Start (no previous month to compare)'
        elif top_change < 0 and challenger_change > 0:
            return 'Backup Event'
        elif top_change > 0 and challenger_change < 0:
            return 'Inverse Event'
        elif top_change > 0 and challenger_change > 0:
            return 'Shared Growth'
        else:
            return 'Shared Decline'

    group_trends['Event Type'] = group_trends.apply(classify_event, axis=1)
    st.dataframe(group_trends[['month', 'Top 18 Change', 'Challenger Change', 'Event Type']].dropna(), hide_index=True)

    event_counts = group_trends['Event Type'].value_counts()
    st.dataframe(event_counts)

    fig_events = px.bar(
        event_counts,
        title='Frequency of Monthly Sales Events',
        labels={'value': 'Number of Months', 'index': 'Event Type'}
    )
    st.plotly_chart(fig_events, use_container_width=True)

    st.divider()
    st.write("Below is the same month-by-month event analysis, but for the control group:")

    st.markdown("##### Top 18 vs All Others")
    control_group_trends['Top 18 Change'] = control_group_trends['Top 18 Sales'].diff()
    control_group_trends['All Others Change'] = control_group_trends['All Others Sales'].diff()

    def classify_control_event(row):
        top_change = row['Top 18 Change']
        other_change = row['All Others Change']
        
        if pd.isna(top_change):
            return 'Start'
        elif top_change < 0 and other_change > 0:
            return 'Backup Event'
        elif top_change > 0 and other_change < 0:
            return 'Inverse Event'
        elif top_change > 0 and other_change > 0:
            return 'Shared Growth'
        else:
            return 'Shared Decline'

    control_group_trends['Event Type'] = control_group_trends.apply(classify_control_event, axis=1)
    control_event_counts = control_group_trends['Event Type'].value_counts()
    st.dataframe(control_group_trends[['month', 'Top 18 Change', 'All Others Change', 'Event Type']].dropna(), hide_index=True)
    st.write("Summary of Events (Control Group):")
    st.dataframe(control_event_counts)

    fig_control_events = px.bar(
        control_event_counts,
        title='Frequency of Monthly Sales Events (Control Group)',
        labels={'value': 'Number of Months', 'index': 'Event Type'}
    )
    st.plotly_chart(fig_control_events, use_container_width=True)
    st.subheader("Conslusion")
    st.write("To summarize the findings, we can compare the event frequencies between the two groups:")

    data = {
        "Event Type": ["Backup Event", "Shared Growth/Decline"],
        "Challenger Group": ["3 Months", "7 Months"],
        "Control Group (\"All Others\")": ["2 Months", "8 Months"]
    }

    df = pd.DataFrame(data)
    st.dataframe(df, hide_index=True)
    st.write("""
    A pattern emerges: Though the difference seem small, the "Challenger" group shows the backup behavior more frequently than the general population of smaller suppliers (All Others). 
    This confirms they are a unique and strategically important group.
    """)
    st.divider()
    st.subheader("Recommendation")
    st.write("""
    The data proves that for ABS, heavy reliance on top suppliers like "Crown Imports" does exist, which make the top challengers like
    "The Country Vintner, LLC Dba Winebow" and others' contribution a lot more pivotal for business stability. I recommend ABS initiate conversations with this
    short-list of 6 suppliers to further understand what they can offer/ build the next tier of partnership as the supply chain risk mitigation plan.
    """)




with t4:
    st.subheader("Operational Efficiency Analysis")
    st.write("""
        In this section, we will examine the relationship between sales, and transfers. As a recap, retail transfer is, as noted on the dataset
        description, "Cases of product transferred to DLC(ABS) dispensaries", this essentially means restocking events, so this can give us a great perspective
        on how efficient ABS retail stores is at restocking their items. 
    """)

   

    st.write("""
        We can do this by crafting a metric using what's available here: retail sales, and retails transfers. And since what we are
        interested in is about restock operation efficiency, this metric will be calculated as:
        """)

    st.latex(r'''
        \text{Efficiency Metric} = \frac{\text{Retail Transfers}}{\text{Retail Sales}}
        ''')

    st.markdown("""
    Where:
    - A value of **1** indicates optimal efficiency.
    - Values **less than 1** suggest restocking might be too slow.
    - Values **greater than 1** imply the stores are supplying more than they are selling.
    """)

    retail_analysis = load(r'data/retail_analysis.parquet')
    print(retail_analysis.columns)
    retail_analysis['time'] = pd.to_datetime(retail_analysis['time'])
 
    item_type_list = retail_analysis['item_type'].unique()

    selected_item = st.selectbox(
        "Select an Item Type:",
        item_type_list
    )

    df_item = retail_analysis[retail_analysis['item_type'] == selected_item].sort_values(by='time')
    st.subheader(f"Sales vs. Restocking for: {selected_item}")

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_item['time'], y=df_item['retail_sales'], name='Retail Sales'))
    fig.add_trace(go.Scatter(x=df_item['time'], y=df_item['retail_transfers'], name='Restocking Transfers', mode='lines+markers', line=dict(color='red')))

    fig.update_layout(
        xaxis_title='Month of 2019',
        yaxis_title='Cases',
        template='plotly_white',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Efficiency Calculation ---
    st.subheader(f"Inventory Efficiency for {selected_item}")

    # Calculate total sales and transfers for the selected item for the whole year
    total_sales = df_item['retail_sales'].sum()
    total_transfers = df_item['retail_transfers'].sum()

    # Calculate the ratio, handling cases where sales might be zero
    if total_sales > 0:
        efficiency_ratio = total_transfers / total_sales
        st.metric(
            label=f"Annual Transfer-to-Sales Ratio",
            value=f"{efficiency_ratio:.2f}",
            help="For every 1 case sold, this many cases were transferred. A ratio near 1.0 is highly efficient."
        )
    else:
        st.metric(label=f"Annual Transfer-to-Sales Ratio", value="N/A (No Sales)")

    st.markdown("""
    ---
    ### Regarding Sales Prediction
    Your idea to project sales into 2020 is an excellent next step for a more advanced analysis. Given the sparse data for 2020 (only 4 months), you would likely need to use a time-series model that can handle missing data, or focus on creating a forecast based purely on the complete 2019 seasonal pattern. This is a great "stretch goal" for the project!
    """)


    