from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Annotated
from sqlmodel import Field, Session, SQLModel, create_engine, select

app = FastAPI()
connectionString = ""
engine = create_engine(connectionString)

def get_session():
    with Session(engine) as session:
        yield session

class Link(BaseModel):
    id: int
    hyperlink: str
    author: str

engine = create_engine()

SessionDep = Annotated[Session, Depends(get_session)]

@app.on_event("startup")
def setup():
    create_db_and_tables()
    

@app.get("/")
async def root():
    return {"message": "Pls use /links"}

@app.get("/links")
async def read_links(session: SessionDep):
    hyperlinks = session.exec(select(links)).all()
    return hyperlinks

@app.post("/links")
async def write_link(derDatensatz: Link, session: SessionDep) -> Link:
    try:
        session.add(derDatensatz)
        session.commit()
        session.refresh(derDatensatz)
    except:
        raise HTTPException(status_code=400, detail="data could not be written")
    else:
        return derDatensatz
    
@app.put("/links/{id}")
async def replace_link(derDatensatz: Link, session: SessionDep) -> Link:
    try:
        session.delete(derDatensatz)
        session.commit()
        session.refresh(derDatensatz)
    except:
        raise HTTPException(status_code=400, detail="data could not be deleted")
    else:
        return derDatensatz

@app.delete("/links/{id}")
async def delete_link(derDatensatz: Link, session: SessionDep) -> Link:
    try:
        session.delete(derDatensatz)
        session.commit()
        session.refresh(derDatensatz)
    except:
        raise HTTPException(status_code=400, detail="data could not be deleted")
    else:
        return derDatensatz