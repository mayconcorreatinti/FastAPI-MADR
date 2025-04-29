from fastapi import APIRouter,HTTPException,Depends,Query
from http import HTTPStatus
from tcc_my_project.schemas import CreateBook,BookId,Message,UpdateBook,ListBooksId
from sqlalchemy.orm import Session
from tcc_my_project.database import get_session
from tcc_my_project.models import Books
from sqlalchemy import Select
from tcc_my_project.security import authenticated_user


router=APIRouter(tags=["books"],prefix="/books")

@router.post("/",status_code=HTTPStatus.OK,response_model=BookId)
def create_book(
    book:CreateBook,
    session:Session = Depends(get_session),
    user=Depends(authenticated_user)
):
    response=session.scalar(Select(Books).where(book.title == Books.title))

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
    session.commit()
    session.refresh(bookid)


    return bookid


@router.delete("/{id}",status_code=HTTPStatus.OK,response_model=Message)
def delete_book(
    id:int,
    user = Depends(authenticated_user),
    session:Session = Depends(get_session)
):
    response=session.scalar(Select(Books).where(Books.id == id))

    if not response:
        raise HTTPException(
            detail="Book not listed in MADR",
            status_code=HTTPStatus.NOT_FOUND
        )
    
    session.delete(response)
    session.commit()

    return {"message":"Book deleted in MADR"}


@router.patch("/{id}",response_model=BookId)
def update_book(
    id:int,
    books:UpdateBook,
    session:Session =Depends(get_session),
    user=Depends(authenticated_user)
):
    book = session.scalar(Select(Books).where(Books.id == id))

    if not book:
        raise HTTPException(
            detail="Book not listed in MADR",
            status_code=HTTPStatus.NOT_FOUND
        )
    
    for key,value in books.model_dump(exclude_unset=True).items():
        if key =='title':
            value = str(" ".join(value.split()).lower())
            bookdb = session.scalar(Select(Books).where(Books.title == value))
            if bookdb:
                raise HTTPException(
                    detail="This title already exists!",
                    status_code=HTTPStatus.CONFLICT
                )
            
        if value:
            setattr(book,key,value)
    
    session.add(book)
    session.commit()
    session.refresh(book)

    return book


@router.get("/{id}",response_model=BookId)
def get_book(
    id:int,
    session:Session =Depends(get_session)
):
    book=session.scalar(Select(Books).where(Books.id == id))

    if not book:
        raise HTTPException(
            detail="Book not listed in MADR",
            status_code=HTTPStatus.NOT_FOUND
        )

    return book


@router.get("/",response_model=ListBooksId)
def get_books_with_filter(
    title: str | None = None,
    year: int | None = None,
    offset: int | None = None,
    limit: int | None = None,
    session:Session = Depends(get_session)
):
    query = Select(Books)

    if title:
        query = query.filter(Books.title.contains(title))

    if year:
        query = query.filter(
            Books.year.contains(year)
        )
    
    response=session.scalars(query.limit(limit).offset(offset))
    
    return {"livros":response.all()}
    


    