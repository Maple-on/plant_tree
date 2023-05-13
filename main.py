from fastapi import FastAPI
from database.database import Base, engine, create_unique_id_sequence
from routes import user_routes, auth_routes, tree_type_routes, tree_order_routes
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(engine)

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    with engine.connect() as conn:
        conn.execute(create_unique_id_sequence)


app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(tree_type_routes.router)
app.include_router(tree_order_routes.router)
