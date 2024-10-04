from datetime import datetime

import pandas as pd
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

# JSON path
df = pd.read_json("/home/owari/Documents/projects/Etl_mercadolivre/data/data.json")

# add _source column
df["_source"] = "https://lista.mercadolivre.com.br/tenis-corrida-masculino"

# add _collect_date column
df["_collect_date"] = datetime.now()

# show all pandas columns
pd.options.display.max_columns = None

# Convert new_price_reais to string type, handling NaN values
df["new_price_reais"] = df["new_price_reais"].astype(str).fillna("")


# handle null values
df["new_price_reais"] = df["new_price_reais"].fillna(0).astype(float)
df["new_price_centavos"] = df["new_price_centavos"].fillna(0).astype(float)
df["old_price_reais"] = df["old_price_reais"].fillna(0).astype(float)
df["old_price_centavos"] = df["old_price_centavos"].fillna(0).astype(float)
df["reviews_rating_number"] = df["reviews_rating_number"].fillna(0).astype(float)

# removing parentheses from the column reviews_amount and handle null values
df["reviews_amount"] = df["reviews_amount"].str.replace(r"[\(\)]", "", regex=True)
df["reviews_amount"] = df["reviews_amount"].fillna(0).astype(int)

# handle dots from values
df["new_price_reais"] = df["new_price_reais"].apply(
    lambda x: x * 1000 if isinstance(x, float) and (x < 1 or (x >= 1 and x < 10)) else x
)

df["old_price_reais"] = df["old_price_reais"].apply(
    lambda x: x * 1000 if isinstance(x, float) and (x < 1 or (x >= 1 and x < 10)) else x
)

# calculate total values
df["new_price"] = df["new_price_reais"] + df["new_price_centavos"] / 100
df["old_price"] = df["old_price_reais"] + df["old_price_centavos"] / 100

# drop old columns
df.drop(
    columns=[
        "new_price_reais",
        "new_price_centavos",
        "old_price_reais",
        "old_price_centavos",
    ],
    axis=1,
    inplace=True,
)

# save df on postgresSQL
df.to_sql(
    "mercadolivre_items", con=engine, if_exists="replace", index=False, chunksize=50
)

print(df.head())
