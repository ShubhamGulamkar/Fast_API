from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

dburl = "mysql+pymysql://root:Shubham@localhost/product_fast_api"
engine = create_engine(dburl)
session = sessionmaker(autocommit=False,autoflush=False,bind=engine)