
from fastapi import Depends,FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import session , engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)

database_models.Base.metadata.create_all(bind=engine)

# products = [
#     Product(1,"IPhone","Simple Phone",99,1123),
#     Product(2,"Macbook","Simple Laptop",999,77),
#     Product(3,"IPod","Simple Music way",50,34),
#     Product(4,"IPhone 17","Simple Phone",99,555),
#     Product(5,"IPhone 16","Simple Phone",99,666)

# ]



products = [
    Product(id=1, name="Phone", description="A smartphone", price=699.99, quantity=50),
    Product(id=2, name="Laptop", description="A powerful laptop", price=999.99, quantity=30),
    Product(id=3, name="Pen", description="A blue ink pen", price=1.99, quantity=100),
    Product(id=4, name="Table", description="A wooden table", price=199.99, quantity=20),
]


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db =session()

    count = db.query(database_models.Product).count

    if count == 0 :
        for product in products:
            db.add(database_models.Product(**product.model_dump()))

        db.commit()

init_db()



@app.get("/")
def greet():
    return "Hi welcome to first Python project"
    # print("Hi welcome to first Python project")

@app.get("/products")
def get_all_products(db:Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products

@app.get("/products/{id}")
def get_product_by_id(id : int,db:Session = Depends(get_db)):
    db_products = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_products:
        return db_products
    
    return "Product Not Found"


@app.post("/product")
def add_product(product : Product,db:Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product


@app.put("/product/{id}")
def update_product(id:int ,product:Product,db:Session = Depends(get_db)):
    db_products = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_products:
        db_products.name = product.name
        db_products.description = product.description
        db_products.price = product.price
        db_products.quantity = product.quantity
        db.commit()
        return 'Product Updated successfully'
    
    return "No Product found"


@app.delete("/product/{id}")
def delete_product(id:int,db:Session = Depends(get_db)):
    db_products = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_products:
        db.delete(db_products)
        db.commit()
        return "product deleted successfully"
        
    return "No Product found"

# greet()