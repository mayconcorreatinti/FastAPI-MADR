from fastapi import APIRouter,Depends,HTTPException,Query
from tcc_my_project.schemas import CreateNovelists,NovelistsId,Message,UpdateNovelists,ManyNovelists
from tcc_my_project.models import Novelist
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from tcc_my_project.database import get_session
from tcc_my_project.security import authenticated_user
from http import HTTPStatus
from sqlalchemy.orm import Session


router=APIRouter(tags=["novelists"],prefix="/novelists")

@router.post("/",response_model=NovelistsId,status_code=HTTPStatus.CREATED)
async def create_novelists(
    novelists:CreateNovelists,
    session:AsyncSession = Depends(get_session),
    authenticated_user= Depends(authenticated_user)
):
    
    name= await session.scalar(Select(Novelist).where(Novelist.name == novelists.name))

    if name:
        raise HTTPException(
            detail="This name already exists in novelists!",
            status_code=HTTPStatus.CONFLICT
        )

    novelist=Novelist(
        name=" ".join(novelists.name.split()).lower()

    )

    session.add(novelist)
    await session.commit()
    await session.refresh(novelist)

    return novelist


@router.delete("/{id}",response_model=Message)
async def delete_novelist(
   id:int,
   session:AsyncSession = Depends(get_session),
   authenticated_user= Depends(authenticated_user)
):
   novelist= await session.scalar(Select(Novelist).where(id == Novelist.id))

   if not novelist:
       raise HTTPException(
           detail="Novelist not listed in MADR",
           status_code=HTTPStatus.NOT_FOUND
       )
   
   session.delete(novelist)
   await session.commit()
   
   return {"message":"Novelist deleted from MADR"}


@router.patch("/{id}",response_model=NovelistsId)
async def update_novelist(
    id:int,
    novelists:UpdateNovelists,
    session:AsyncSession = Depends(get_session),
    authenticated_user= Depends(authenticated_user)
):
    novelist= await session.scalar(Select(Novelist).where(id == Novelist.id))

    if not novelist:
        raise HTTPException(
            detail="Novelist not listed in MADR",
            status_code=HTTPStatus.NOT_FOUND
        )
    
    for key,value in novelists.model_dump(exclude_unset=True).items():
        if value:
            sanitized_value=" ".join(value.split()).lower()
            novelist_patch= await session.scalar(Select(Novelist).where(Novelist.name == sanitized_value))
            if novelist_patch:
                raise HTTPException(
                    detail="This name already exists in novelists!",
                    status_code=HTTPStatus.CONFLICT
                )
            
            setattr(novelist,key,sanitized_value)
            await session.commit()
            await session.refresh(novelist)

    return novelist
   

@router.get("/{id}",response_model=NovelistsId,status_code=HTTPStatus.OK)
async def get_novelist(
    id:int,
    session:AsyncSession = Depends(get_session)
):
    novelist= await session.scalar(Select(Novelist).where(id == Novelist.id))

    if not novelist:
        raise HTTPException(
            detail="Novelist not listed in MADR",
            status_code=HTTPStatus.NOT_FOUND
        )

    return novelist


@router.get("/",response_model=ManyNovelists)
async def get_novelist_filter(
    name:str = Query(None),
    offset:int = Query(None),
    limit:str = Query(None),
    session:AsyncSession = Depends(get_session)
):
    
    query=Select(Novelist)

    if name:
        query=query.filter(Novelist.name.contains(name))

    novelist= await session.scalars(query.offset(offset).limit(limit))

    return {'novelists':novelist.all()}