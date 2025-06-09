from fastapi import APIRouter,HTTPException,Depends,Query
from http import HTTPStatus
from tcc_my_project.schemas import CreateBook,BookId,Message,UpdateBook,ListBooksId
from sqlalchemy.orm import Session
from tcc_my_project.database import get_session
from tcc_my_project.models import Books,Novelist
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select
from tcc_my_project.security import authenticated_user


router=APIRouter(tags=["books"],prefix="/books")

@router.post("/",status_code=HTTPStatus.CREATED,response_model=BookId)
async def create_book(
    book:CreateBook,
    session:AsyncSession = Depends(get_session),
    user=Depends(authenticated_user)
):
    response= await session.scalar(Select(Books).where(book.title == Books.title))
    book_with_novelist= await session.scalar(Select(Novelist).where(book.novelist_id == Novelist.id))

    if not book_with_novelist:
        raise HTTPException(
            detail="the author does not exist",
            status_code=HTTPStatus.NOT_FOUND
        )
    
    if response:
        raise HTTPException(
            detail="This title already exists!",
            status_code=HTTPStatus.CONFLICT
        )
    
    bookid=Books(
        year=book.year,
        title=" ".join(book.title.split()).lower(),
        novelist_id=book.novelist_id
    )

    session.add(bookid)
    await session.commit()
    await session.refresh(bookid)


    return bookid


@router.delete("/{id}",status_code=HTTPStatus.OK,response_model=Message)
async def delete_book(
    id:int,
    user = Depends(authenticated_user),
    session:AsyncSession = Depends(get_session)
):
    response= await session.scalar(Select(Books).where(Books.id == id))

    if not response:
        raise HTTPException(
            detail="Book not listed in MADR",
            status_code=HTTPStatus.NOT_FOUND
        )
    
    session.delete(response)
    await session.commit()

    return {"message":"Book deleted in MADR"}


@router.patch("/{id}",response_model=BookId)
async def update_book(
    id:int,
    books:UpdateBook,
    session:AsyncSession =Depends(get_session),
    user=Depends(authenticated_user)
):
    book = await session.scalar(Select(Books).where(Books.id == id))

    if not book:
        raise HTTPException(
            detail="Book not listed in MADR",
            status_code=HTTPStatus.NOT_FOUND
        )
    
    for key,value in books.model_dump(exclude_unset=True).items():
        if key == "novelist_id":
            continue
        if key =="title":
            value = str(" ".join(value.split()).lower())
            bookdb = await session.scalar(Select(Books).where(Books.title == value))
            if bookdb:
                raise HTTPException(
                    detail="This title already exists!",
                    status_code=HTTPStatus.CONFLICT
                )
            
        if value:
            setattr(book,key,value)
    
    session.add(book)
    await session.commit()
    await session.refresh(book)

    return book


@router.get("/{id}",response_model=BookId)
async def get_book(
    id:int,
    session:AsyncSession =Depends(get_session)
):
    book= await session.scalar(Select(Books).where(Books.id == id))

    if not book:
        raise HTTPException(
            detail="Book not listed in MADR",
            status_code=HTTPStatus.NOT_FOUND
        )

    return book


@router.get("/",response_model=ListBooksId)
async def get_books_with_filter(
    title: str | None = None,
    year: int | None = None,
    offset: int | None = None,
    limit: int | None = None,
    session:AsyncSession = Depends(get_session)
):
    query = Select(Books)

    if title:
        query = query.where(Books.title.contains(str(" ".join(title.split()).lower())))

    if year:
        query = query.where(Books.year == year)
        
    response= await session.scalars(query.limit(limit).offset(offset))
    
    return {"books":response.all()}
    


    