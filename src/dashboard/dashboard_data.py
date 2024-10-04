import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

# Database connection
DATABASE_TYPE = "postgresql"
DBAPI = "psycopg2"
HOST = "localhost"
USER = "postgres"
PASSWORD = "postgres"
DATABASE = "dbshoes"
PORT = "5432"

connection_string = (
    f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)
engine = create_engine(connection_string)

# load data
df = pd.read_sql_query("SELECT * FROM mercadolivre_items", engine)

# title
st.title("Serach Market - sport shoes on Mercado Livre")

# title KPIs
st.subheader("main KPIs")
col1, col2, col3 = st.columns(3)

# KPI 1: total of itens
total_itens = df.shape[0]
col1.metric(label="Total of itens", value=total_itens)

# KPI 2: Number of unique brands
unique_brands = df["brand"].nunique()
col2.metric("Number of unique brands", value=unique_brands)

# KPI 3: Average price (REAIS)
average_new_price = df["new_price"].mean()
col3.metric("Average new price (R$)", value=f"{average_new_price:.2f}")

# most finded brand until page 10
st.subheader("Most finded brand until page 10")
col1, col2 = st.columns([4, 2])
top_10_pages_brands = df["brand"].value_counts().sort_values(ascending=False)
col1.bar_chart(top_10_pages_brands)
col2.write(top_10_pages_brands)

# Average price per brand
st.subheader("Average price per brand")
col1, col2 = st.columns([4, 2])
average_price_by_brand = (
    df.groupby("brand")["new_price"].mean().round(2).sort_values(ascending=False)
)
col1.bar_chart(average_price_by_brand)
col2.write(average_price_by_brand)

# Total satisfaction per Brand
st.subheader("Total satisfaction per Brand")
col1, col2 = st.columns([4, 2])
df_non_zero_reviews = df[df["reviews_rating_number"] > 0]
satisfaction_by_brand = (
    df_non_zero_reviews.groupby("brand")["reviews_rating_number"]
    .mean()
    .sort_values(ascending=False)
)
col1.bar_chart(satisfaction_by_brand)
col2.write(satisfaction_by_brand)
