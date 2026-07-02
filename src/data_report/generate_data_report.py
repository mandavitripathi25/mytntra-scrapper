import streamlit as st
import pandas as pd
import plotly.express as px
import os, sys
from src.exception import CustomException


class DashboardGenerator:
    def __init__(self, data):
        self.data = data

    def display_general_info(self):
        st.header('General Information')
        self.data['Over_All_Rating'] = pd.to_numeric(self.data['Over_All_Rating'], errors='coerce')
        self.data['Price'] = pd.to_numeric(
            self.data['Price'].apply(lambda x: x.replace("₹", "")), errors='coerce'
        )
        self.data["Rating"] = pd.to_numeric(self.data['Rating'], errors='coerce')

        product_ratings = self.data.groupby('Product Name', as_index=False)['Over_All_Rating'].mean().dropna()
        fig_pie = px.pie(product_ratings, values='Over_All_Rating', names='Product Name',
                         title='Average Ratings by Product')
        st.plotly_chart(fig_pie)

        avg_prices = self.data.groupby('Product Name', as_index=False)['Price'].mean().dropna()
        fig_bar = px.bar(avg_prices, x='Product Name', y='Price', color='Product Name',
                         title='Average Price Comparison Between Products')
        st.plotly_chart(fig_bar)

    def display_product_sections(self):
        st.header('Product Sections')
        product_names = self.data['Product Name'].unique()
        for product_name in product_names:
            product_data = self.data[self.data['Product Name'] == product_name]
            with st.container():
                st.subheader(product_name)
                if "Product Link" in product_data.columns:
                    st.markdown(f"[🔗 View Product](<{product_data['Product Link'].iloc[0]}>)")
                st.markdown(f"💰 Average Price: ₹{product_data['Price'].mean():.2f}")
                st.markdown(f"⭐ Average Rating: {product_data['Over_All_Rating'].mean():.2f}")

                st.markdown("#### Positive Reviews")
                for _, row in product_data[product_data['Rating'] >= 4.5].nlargest(5, 'Rating').iterrows():
                    st.markdown(f"✨ Rating: {row['Rating']} - {row['Comment']}")

                st.markdown("#### Negative Reviews")
                for _, row in product_data[product_data['Rating'] <= 2].nsmallest(5, 'Rating').iterrows():
                    st.markdown(f"💢 Rating: {row['Rating']} - {row['Comment']}")

                st.markdown("#### Rating Counts")
                for rating, count in product_data['Rating'].value_counts().sort_index(ascending=False).items():
                    st.write(f"🔹 Rating {rating} count: {count}")
                st.divider()