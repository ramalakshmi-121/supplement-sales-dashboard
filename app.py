import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Reading the data from csv file
@st.cache_data
def load_data():
    df = pd.read_csv("Supplement_Sales_Weekly_Expanded.csv")
    
    # Cleaning the dataframe
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True,inplace=True)

    # Changing the datatype
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Creating a year and month column
    df['Year'] = pd.to_datetime(df['Date']).dt.year
    df['Month'] = pd.to_datetime(df['Date']).dt.strftime('%b')
    df['Discount Value'] = df['Discount']*df['Revenue']
    return df

# Page config
st.set_page_config(page_title="Supplement Sales Dashboard",layout="wide")

df = load_data()

# Supplement Sales Dashboard
st.title("Supplement Sales Dashboard")

filtered_df = df.copy()

filter_cols = ['Category','Product Name', 'Location','Platform']

st.sidebar.title("Filters")

for col in filter_cols:
    options = ["All"]+sorted(filtered_df[col].unique())
    selected = st.sidebar.selectbox(f"Select {col}",options)

    if selected != "All":
        filtered_df = filtered_df[filtered_df[col]==selected]

# Date range filter

date_range = st.sidebar.date_input("Select Date Range",
                                   value = (df["Date"].min(),df["Date"].max()),
                                    min_value = df["Date"].min(),
                                    max_value = df["Date"].max())

if len(date_range) == 2:
    filtered_df = filtered_df[(filtered_df["Date"] >= pd.to_datetime(date_range[0])) & 
                          (filtered_df["Date"] <= pd.to_datetime(date_range[1]))
                          ]
    
else:
    st.warning("Please select a date range")

st.write("Filtered rows:", filtered_df.shape[0])


# KPIs
total_revenue = filtered_df['Revenue'].sum()
total_units = filtered_df['Units Sold'].sum()
units_returned = filtered_df['Units Returned'].sum()
tot_dis = filtered_df['Discount Value'].sum()

avg_sp = (total_revenue+tot_dis)/total_units
return_rate = (units_returned/total_units)*100
net_revenue = total_revenue - tot_dis
discount_impact = (tot_dis/total_revenue)*100

col1, col2, col3, col4 = st.columns([3,2,2,2])

# KPI Display
col1.metric("Total Revenue",f"${total_revenue:,.2f}",border=True)
col2.metric("Total Units Sold",f"{total_units:,}",border=True)
col3.metric("Average Revenue",f"${filtered_df['Revenue'].mean():,.0f}",border=True)
col4.metric("Return Rate", f"{return_rate:.2f}%",border=True)

col1.metric("Net Revenue", f"${net_revenue:,.2f}",border=True)
col2.metric("Total Units Returned", f"{units_returned:,}",border=True)
col3.metric("Average Selling Price", f"${avg_sp:,.2f}",border=True)
col4.metric("Discount Impact", f"{discount_impact:.2f}%",border=True)

st.divider()

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Sales Overview", "Category Analysis", "Product Analysis", 
                                        "Platform Analysis", "Analysis Over Time",
                                        "Discount & Pricing Impact"])

# Sales Overview

with tab1:
    st.header("Sales Overview")
    fig, ax = plt.subplots(figsize=(15,6))
    category_df = filtered_df.groupby("Category", as_index = False)[["Units Sold", "Units Returned"]].sum()

    st.subheader("Units Sold by Category")
    sns.barplot(data = category_df, x = "Category", y = "Units Sold", palette = "crest", ax = ax)
    for container in ax.containers:
       ax.bar_label(container,fmt="{:,.0f}")
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(15,6))
    product_df = filtered_df.groupby("Product Name", as_index=False)[["Units Sold", "Units Returned"]].sum()
    st.subheader("Units Sold by Product")
    sns.barplot(data = product_df, x = "Product Name", y = "Units Sold",palette = "magma", ax = ax)    
    ax.tick_params(axis="x", labelsize=16)  
    ax.tick_params(axis="y", labelsize=16)
    ax.set_xlabel("Product", fontsize=16)
    ax.set_ylabel("Units Sold", fontsize=16)
    plt.xticks(rotation=90)
    for container in ax.containers:
       ax.bar_label(container,fmt="{:,.0f}")
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(fig)

    location_df = filtered_df.groupby("Location", as_index=False)[["Units Sold", "Units Returned"]].sum()
    platform_df = filtered_df.groupby("Platform", as_index=False)[["Units Sold", "Units Returned"]].sum()

    chart1, chart2 = st.columns(2)
    with chart1:
        st.subheader("Units Sold by Location")
        st.bar_chart(location_df, x ="Location", y = "Units Sold", color = "#55ba49e2")

    with chart2:
        st.subheader("Units Sold by Platform")
        st.bar_chart(platform_df, x = "Platform", y = "Units Sold", color = "#d23c3ee4")

# Category Wise Analysis

with tab2:
   st.header("Category-wise Analysis")
   original_df = df.copy()

   st.subheader("Units Sold Contribution (%)")
   category_units = original_df.groupby("Category", as_index=False)["Units Sold"].sum()
   units_total = original_df["Units Sold"].sum()
   category_units["Percent"]= (category_units["Units Sold"]/ units_total)*100

   fig, ax = plt.subplots(figsize=(15,7))
   colors = sns.color_palette("Accent")
   ax.pie(category_units["Percent"], labels = category_units["Category"], autopct="%1.2f%%", 
          colors=colors, startangle=90)
   ax.axis("equal")
   st.pyplot(fig)

# Category vs Revenue

   category_rev_sum = filtered_df.groupby("Category", as_index=False)["Revenue"].sum()
   st.subheader("Total Revenue")
   fig, ax = plt.subplots(figsize=(15,6))
   sns.barplot(data=category_rev_sum, x="Category",y="Revenue", palette = 'magma')
   ax.set_ylabel("Revenue ($)")
   for container in ax.containers:
      ax.bar_label(container,fmt="{:,.02f}")
   plt.yscale("log")
   st.pyplot(fig)

# Category vs Revenue

   category_rev = filtered_df.groupby("Category", as_index=False)["Revenue"].mean()
   category_order = sorted(df["Category"].unique())
   st.subheader("Average Revenue")
   fig, ax = plt.subplots(figsize=(15,6))
   sns.pointplot(data=filtered_df,x="Category",y="Revenue", color = 'teal',order=category_order)
   for i, point in enumerate(category_rev.itertuples()):
       ax.text(i, point.Revenue, f'${point.Revenue:,.2f}',ha = 'left', va = 'top', fontsize=12)
   ax.set_ylabel("Average Revenue")
   st.pyplot(fig)

# Category vs Return Rate

   category_rr = filtered_df.groupby("Category", as_index=False).agg({
                  "Units Sold": "sum", "Units Returned": "sum"
   })
   category_rr["Return Rate (%)"] = (category_rr["Units Returned"]/category_rr["Units Sold"])*100
   fig, ax = plt.subplots(figsize = (12,6))
   st.subheader("Return Rate (%)")
   sns.barplot(data = category_rr,  x = "Return Rate (%)", y = "Category", 
               ax = ax, width = 0.4, color = 'slateblue')

   for container in ax.containers:
       ax.bar_label(container,fmt="{:,.2f}%")
   st.pyplot(fig)
   
# Product-wise Analysis

with tab3:
   st.header("Product-wise Analysis")

# Total Revenue for Product
   product_rev = filtered_df.groupby("Product Name", as_index=False)\
                 ["Revenue"].sum().sort_values(by = "Product Name")

   fig, ax = plt.subplots(figsize = (15,6))
   st.subheader("Total Revenue")
   sns.barplot(data = product_rev, x = "Product Name", y = "Revenue",ax = ax,
         palette='Paired')

   for container in ax.containers:
      ax.bar_label(container,fmt="{:,.0f}")
   plt.yscale("log")
   plt.ylabel("Revenue ($)")
   plt.xticks(rotation = 90)
   st.pyplot(fig)

# Total Units Sold based on Country
   prod_loc = filtered_df.groupby(["Product Name", "Location"],as_index=False)["Units Sold"].sum()

   fig, ax = plt.subplots(figsize = (15,6))
   st.subheader("Total Units Sold based on Country")
   sns.barplot(data = prod_loc, x = "Product Name", y = "Units Sold", hue = "Location", ax = ax,
          palette='gist_earth')
   ax.legend(loc = "upper right",bbox_to_anchor=[1.1,1])
   plt.xticks(rotation = 90)
   st.pyplot(fig)

# Units Returned
   st.subheader("Units Returned")
   
   fig, ax = plt.subplots(figsize=(15,6))
   sns.barplot(data = product_df, x = "Product Name", y = "Units Returned", palette = "crest", ax = ax)
   for container in ax.containers:
      ax.bar_label(container,fmt="{:,.0f}")
   plt.xticks(rotation=90)
   st.pyplot(fig)

# Revenue vs Units Sold
   st.subheader("Revenue vs Units Sold")
   prod_UR = filtered_df.groupby(["Product Name"],as_index=False).agg({"Units Sold":"sum",
                             "Revenue": "sum"})

   fig, ax = plt.subplots(figsize=(15, 6))
   sns.barplot(data = prod_UR, x = "Product Name", y = "Units Sold",ax=ax, label = "Units Sold", color='c')
   ax1 = ax.twinx()
   sns.lineplot(data = prod_UR,x="Product Name",y="Revenue",ax = ax1,label = "Revenue",
               marker = 'o', color='purple')
   ax.legend(loc = "upper right", bbox_to_anchor=(1.13,1))
   ax1.legend(loc = "upper right", bbox_to_anchor=(1.12,1.07))
   
   for container in ax.containers:
       ax.bar_label(container, fmt="{:,.0f}")
   ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
   st.pyplot(fig)

## Return Rate % for Product

   product_rr = filtered_df.groupby("Product Name", as_index=False).agg({
                "Units Sold": "sum", "Units Returned": "sum"
            })
   product_rr["Return Rate (%)"] = (product_rr["Units Returned"]/product_rr["Units Sold"])*100

   fig, ax = plt.subplots(figsize = (15,6))
   st.subheader("Return Rate (%)")
   sns.barplot(data = product_rr,  x = "Return Rate (%)", y = "Product Name", 
                ax = ax, width = 0.5, palette = 'viridis')

   for container in ax.containers:
       ax.bar_label(container,fmt="{:,.2f}%")
   st.pyplot(fig)

## Platform-wise Analysis

with tab4:
    st.header("Platform-wise Analysis")

## Total Revenue
    platform_rev = filtered_df.groupby("Platform",as_index=False)["Revenue"].sum()

    fig, ax = plt.subplots(figsize = (15,6))
    st.subheader("Total Revenue")
    sns.barplot(data = platform_rev,  x = "Platform", y = "Revenue",
                ax = ax, width = 0.6, palette = 'pastel')
    plt.yscale('log')

    for container in ax.containers:
        ax.bar_label(container,fmt="{:,.2f}")
    st.pyplot(fig)

## Total Revenue based on Country
 
## Discount vs Unit Sold
    platform_dis = filtered_df.groupby(["Platform","Discount"],as_index=False)["Units Sold"].sum()

    fig, ax = plt.subplots(figsize = (15,6))
    st.subheader("Discount vs Unit Sold")
    sns.lineplot(data = platform_dis,  x = "Discount", y = "Units Sold", marker = "s", hue = "Platform",
                   ax = ax, palette = 'deep')
    ax.legend(loc = "upper right", bbox_to_anchor=(1.13,1))
    st.pyplot(fig)

# Units Returned vs Return Rate (%)
    platform_rr = filtered_df.groupby("Platform", as_index=False).agg({
           "Units Sold": "sum", "Units Returned": "sum"
            }).sort_values(by="Platform", ascending=True)
    platform_rr["Return Rate (%)"] = (platform_rr["Units Returned"]/platform_rr["Units Sold"])*100

    fig, ax = plt.subplots(figsize = (15,6))
    st.subheader("Units Returned vs Return Rate (%)")
    sns.barplot(data = platform_rr,  x = "Platform", y = "Units Returned", palette="muted",
                width = 0.3, ax = ax)
    ax1 = ax.twinx()
    sns.lineplot(data = platform_rr, x = "Platform", y = "Return Rate (%)", marker = 'o', 
                 ax = ax1, color = "seagreen")

    for i,j in zip(platform_rr["Platform"], platform_rr["Return Rate (%)"]):
          plt.annotate(f'({j:,.3f}%)', (i,j), textcoords="offset points", xytext=(0, -15.7),
                  ha='center')
    
    for container in ax.containers:
         ax.bar_label(container,fmt="{:,.0f}")
    st.pyplot(fig)

##  Analysis Over Time 
    
with tab5: 
## Units Sold vs Revenue
    week_df = filtered_df.groupby("Date", as_index=False)[["Units Sold", "Revenue"]].sum()
    st.header("Analysis over Time")
    st.subheader("Units Sold vs Revenue")
    fig, ax = plt.subplots(figsize=(15, 6))

    sns.lineplot(data = week_df, x = "Date", y = "Units Sold",ax=ax,label = "Units sold", color='c')
    ax1 = ax.twinx()
    sns.lineplot(data = week_df,x="Date",y="Revenue",ax = ax1,label = "Revenue", color='purple')
    ax.set_xlabel("Week")
    ax.legend(loc = "upper right", bbox_to_anchor=(1,1))
    ax1.legend(loc = "upper right", bbox_to_anchor=(1,0.94))
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    # YoY Revenue 
    yoy_df = filtered_df.groupby("Year", as_index=False)["Revenue"].sum()
    yoy_df = yoy_df[yoy_df["Year"]<2025]
    yoy_df["Year"] = yoy_df["Year"].astype(str)
    yoy_df["YoY Revenue (%)"] = yoy_df["Revenue"].pct_change() * 100

    st.subheader("Year over Year Revenue")
    fig, ax = plt.subplots(figsize=(15, 6))
    sns.lineplot(data=yoy_df, x="Year", y="YoY Revenue (%)",marker = 's', ax=ax)
    
    for i,j in zip(yoy_df["Year"], yoy_df["YoY Revenue (%)"]):
          plt.annotate(f'({j:,.2f}%)', (i,j), textcoords="offset points", xytext=(0, -12),
                  ha='center')
    st.pyplot(fig)

# Yearly revenue for platforms    
   
    st.subheader("Yearly Revenue")
    fig, ax = plt.subplots(figsize=(15, 6))
    year_revenue = filtered_df.groupby("Year",as_index=False)["Revenue"].sum()
    year_revenue = year_revenue[year_revenue["Year"]<2025]
    year_revenue["Year"] = year_revenue["Year"].astype(str)

    sns.lineplot(data = year_revenue, x = "Year",y = "Revenue", marker = 's',
                palette ='bright', ax = ax)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    ## Month over Month
    monthly_df = filtered_df.groupby("Month")["Revenue"].sum().reset_index(name="Revenue")
    month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    monthly_df["Month"] = pd.Categorical(monthly_df["Month"], categories=month_order,ordered=True)
    monthly_df_sorted = monthly_df.sort_values(by="Month", ascending = True)
    monthly_df_sorted["MoM Revenue (%)"] = monthly_df_sorted["Revenue"].pct_change()*100

    st.subheader("Month over Month Revenue")
    fig, ax = plt.subplots(figsize=(15, 6))
    sns.lineplot(data = monthly_df_sorted, x = "Month",y = "MoM Revenue (%)", ax = ax,
                 palette = 'bright')
    for i,j in zip(monthly_df_sorted["Month"], monthly_df_sorted["MoM Revenue (%)"]):
          plt.annotate(f'({j:,.2f}%)', (i,j), textcoords="offset points", xytext=(0, -15.7),
                  ha='center')
    
    st.pyplot(fig)

    
# Discount Impact

with tab6:
    st.header("Discount & Pricing Impact")
    st.subheader("Pareto Chart for Revenue by Discount")
    bins = [0, 0.05, 0.10, 0.15, 0.20, 0.25]
    labels = ['0-5%', '5-10%', '10-15%', '15-20%', '20-25%']

    filtered_df["Discount Bucket"] = pd.cut(filtered_df["Discount"], bins=bins, labels=labels,
                                         include_lowest=True)
    pareto_discount = filtered_df.groupby("Discount Bucket", as_index=False)["Revenue"].sum()
    pareto_discount = pareto_discount.sort_values(by="Revenue", ascending=False)
    pareto_discount["Cumulative %"] = pareto_discount["Revenue"].cumsum() / pareto_discount["Revenue"].sum() * 100

    fig, ax = plt.subplots(figsize = (15,6))

    ax.bar(pareto_discount["Discount Bucket"], pareto_discount["Revenue"], width = 0.3, color = 'cyan')
    ax.set_ylabel("Revenue ($)")
    ax1 = ax.twinx()

    ax1.plot(pareto_discount["Discount Bucket"], pareto_discount["Cumulative %"], marker='o', color = 'teal')
    ax1.axhline(80, linestyle='--')
    ax1.set_ylabel("Cumulative Percentage")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Discount vs Revenue and Units Sold

    disc_df = filtered_df.groupby(["Discount"], as_index=False)[["Revenue","Units Sold"]].sum()
    disc_df["Discount"] = disc_df["Discount"].astype(str)
   
    st.subheader("Revenue and Units Sold for Discount")

    fig, ax = plt.subplots(figsize = (15,6))
    sns.barplot(data = disc_df, x = "Discount", y = "Revenue", label = "Revenue", color = 'purple',
               width = 0.3, ax = ax)
    plt.ylabel("Revenue ($)")
    ax.legend(loc = 'upper right', bbox_to_anchor = [1.15,1])
    ax1 = ax.twinx()

    sns.lineplot(data = disc_df, x = "Discount", y = "Units Sold", label = "Units Sold", color = 'royalblue', 
                 marker='o', ax = ax1)
    ax1.legend(loc = 'upper right', bbox_to_anchor = [1.15,1.07])
    plt.xticks(rotation=90)
    st.pyplot(fig)

# Pricing Impact

    st.header("Pricing Impact")
    st.subheader("Price vs Units Sold")
    fig,ax = plt.subplots(figsize = (15,6))
    bin = [10,15,20,25,30,35,40,45,50,55,60]
    label = ["10-15", "15-20", "20-25", "25-30", "30-35", "35-40", "40-45", "45-50", "50-55", "55-60"]
    filtered_df["Price Bin"] = pd.cut(df["Price"], bins = bin , labels = label, include_lowest=True)
    Price_total = filtered_df.groupby("Price Bin", as_index=False)["Units Sold"].sum()

    sns.barplot(data = Price_total, x = "Price Bin", y = "Units Sold", width = 0.3, color = "mediumpurple", ax=ax)
    plt.xlabel("Price Range ($)")
    for container in ax.containers:
        ax.bar_label(container,fmt="{:,.0f}")
    st.pyplot(fig)

# Price vs Units Sold Density
    st.subheader("Price vs Units Sold Density")
    fig, ax = plt.subplots(figsize=(10,6))
    ax.hexbin(filtered_df["Price"], filtered_df["Units Sold"], cmap="Blues", gridsize=30)
    ax.set_xlabel("Price")
    ax.set_ylabel("Units Sold")
    st.pyplot(fig)
 
