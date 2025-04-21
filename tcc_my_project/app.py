from fastapi import FastAPI
from tcc_my_project.routers.accounts import router as accounts
from tcc_my_project.routers.books import router as books
from tcc_my_project.routers.novelists import router as novelists

app=FastAPI()

app.include_router(accounts)
app.include_router(books)
app.include_router(novelists)