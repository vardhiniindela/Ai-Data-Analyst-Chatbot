import pandas as pd

def process_query(df, query):
    query = query.lower()

    if "total sales" in query:
        return df["price"].sum()

    elif "average price" in query:
        return df["price"].mean()

    elif "highest product" in query:
        return df.loc[df["price"].idxmax()]

    elif "lowest product" in query:
        return df.loc[df["price"].idxmin()]

    elif "total quantity" in query:
        return df["quantity"].sum()

    else:
        return "Try: total sales, average price, highest product"