from sqlalchemy import create_engine, text
import streamlit as st
import pandas as pd
import time

# db connection function:
    # engine
def get_engine():
    try:
        db_user = st.secrets["user"]
        db_password = st.secrets["password"]
        db_host = st.secrets["host"]
        db_port = st.secrets["port"]
        db_name = st.secrets["database"]

        connection_str = (
            f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )

        engine = create_engine(connection_str)
        return engine

    except Exception as e:
        st.error(f"Something went wrong: {e}")
        return None


    # query
def query(query):
    engine = get_engine()
    if engine is not None:
        try:
            with engine.connect() as connection:
                df = pd.read_sql(text(query), connection)
                return df
        except Exception as e:
            st.error(f"{e}")
            return None
    else:
        st.error("No Engine Available")
        return None

@st.cache_data(ttl=5)
def load(file_path):
    return pd.read_parquet(file_path)
