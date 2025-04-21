from fastapi import APIRouter,Depends,HTTPException,Query
from tcc_my_project.schemas import CreateNovelists,NovelistsId,Message,UpdateNovelists,ManyNovelists
from tcc_my_project.models import Novelist
from sqlalchemy import Select
from tcc_my_project.database import get_session
from tcc_my_project.security import authenticated_user
from http import HTTPStatus
from sqlalchemy.orm import Session


router=APIRouter(tags=["novelists"],prefix="/novelists")

@router.post("/",response_model=NovelistsId)
def create_novelists(
    novelists:CreateNovelists,
    session:Session = Depends(get_session),
    authenticated_user= Depends(authenticated_user)
):
    
    name=session.scalar(Select(Novelist).where(Novelist.name == novelists.name))

    if name:
        raise HTTPException(
            detail="This name already exists in novelists!",
            status_code=HTTPStatus.CONFLICT
        )

    novelist=Novelist(
        name=" ".join(novelists.name.split()).lower()

    )

    session.add(novelist)
    session.commit()
    session.refresh(novelist)

    return novelist


@router.delete("/{id}",response_model=Message)
def delete_novelist(
   id:int,
   session:Session = Depends(get_session),
   authenticated_user= Depends(authenticated_user)
):
   novelist=session.scalar(Select(Novelist).where(id == Novelist.id))

   if not novelist:
       raise HTTPException(
           detail="Novelist not listed in MADR",
           status_code=HTTPStatus.NOT_FOUND
       )
   
   session.delete(novelist)
   session.commit()
   
   return {"message":"Novelist deleted from MADR"}


@router.patch("/{id}",response_model=NovelistsId)
def update_novelist(
    id:int,novelists:UpdateNovelists,
    session:Session = Depends(get_session),
    authenticated_user= Depends(authenticated_user)
):
    novelist=session.scalar(Select(Novelist).where(id == Novelist.id))

    if not novelist:
        raise HTTPException(
            detail="Novelist not listed in MADR",
            status_code=HTTPStatus.NOT_FOUND
        )
    
    for key,value in novelists.model_dump(exclude_unset=True).items():
        if value:
            sanitized_value=" ".join(value.split()).lower()
            novelist_patch=session.scalar(Select(Novelist).where(Novelist.name == sanitized_value))
            if novelist_patch:
                raise HTTPException(
                    detail="This name already exists in novelists!",
                    status_code=HTTPStatus.CONFLICT
                )
            
            setattr(novelist,key,sanitized_value)
            session.commit()
            session.refresh(novelist)

    return novelist
   

@router.get("/{id}",response_model=NovelistsId,status_code=HTTPStatus.OK)
def get_novelist(
    id:int,
    session:Session = Depends(get_session)
):
    novelist=session.scalar(Select(Novelist).where(id == Novelist.id))

    if not novelist:
        raise HTTPException(
            detail="Novelist not listed in MADR",
            status_code=HTTPStatus.NOT_FOUND
        )

    return novelist


@router.get("/",response_model=ManyNovelists)
def get_novelist_filter(
    name:str = Query(None),
    offset:int = Query(None),
    limit:str = Query(None),
    session:Session = Depends(get_session)
):
    
    query=Select(Novelist)

    if name:
        query=query.filter(Novelist.name.contains(name))

    novelist=session.scalars(query.offset(offset).limit(limit))

    return {'novelists':novelist.all()}