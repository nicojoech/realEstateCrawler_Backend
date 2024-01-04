from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.database import SessionLocal
from app.services.agentService import crudAgent

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/agents/", response_model=schemas.CrawlerAgentResponse)
def create_agent(agent: schemas.CrawlerAgent, db: Session = Depends(get_db)):
    return crudAgent.create_crawler_agent(db=db, agent=agent)


@router.delete("/agents/{agent_id}", response_model=schemas.CrawlerAgentResponse)
def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    return crudAgent.delete_crawler_agent(db=db, agent_id=agent_id)


@router.post("/agents/{agent_id}")
def start_agent(agent_id: int, db: Session = Depends(get_db)):
    return crudAgent.start_crawler_agent(db=db, agent_id=agent_id)

