import sqlalchemy as db;
import fetch_weather_data as fwd;
# from sqlalchemy import create_engine

# def get_engine():
#     return create_engine(
#         "postgresql+psycopg2://mvst:password@localhost:5432/mvst"
#     )

username = "mvst"      # default user
password = "tablat1938"              # the password you set during installation
host = "localhost"         # if running locally
port = "5432"              # default PostgreSQL port
database = "mvst"    # the database you created earlier
DATABASE_URL = (f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

engine = db.create_engine(DATABASE_URL)

with engine.connect() as connection:
    # Create a Metadata Object
    metadata = db.MetaData()
    # Load the tables
    metadata.reflect(bind=engine)


    # albums = db.Table('albums', metadata, autoload_with=engine)
    # artists = db.Table('artists', metadata, autoload_with=engine)
print(engine)