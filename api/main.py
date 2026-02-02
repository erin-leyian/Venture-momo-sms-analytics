from fastapi import FastAPI
from config import Base, engine
from routers import auth_router, users_router, transactions_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="MoMo API", version="1.0")

app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
# Transactions endpoints are available at /transactions
app.include_router(transactions_router)


@app.get("/")
async def root():
    return {"message": "MoMo API", "docs": "/docs", "transactions": "/transactions"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
