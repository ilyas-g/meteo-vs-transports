import pandas as pd

def load_to_postgres(df: pd.DataFrame, table_name: str, engine):
    """
    Charge un DataFrame Pandas dans une table PostgreSQL via SQLAlchemy.
    """
    if df.empty:
        print("Aucune donnée à charger")
        return

    df.to_sql(table_name, con=engine, if_exists='append', index=False)