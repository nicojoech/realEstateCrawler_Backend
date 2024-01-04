from sqlalchemy.orm import Session

from app import schemas, models


def create_crawler_agent(db: Session, agent: schemas.CrawlerAgent):
    db_agent = models.CrawlerAgent(
        name=agent.name,
        min_area=agent.min_area,
        max_price=agent.max_price,
        number_of_rooms=agent.number_of_rooms,
        zip_code=agent.zip_code,
        state=agent.state,
        rent=agent.rent,
        type=agent.type
    )
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent


def get_crawler_agent(db: Session, agent_id: int):
    return db.query(models.CrawlerAgent).filter(models.CrawlerAgent.id == agent_id).first()


def update_crawler_agent(db: Session, agent_id: int, new_data: schemas.CrawlerAgent):
    db_agent = db.query(models.CrawlerAgent).filter(models.CrawlerAgent.id == agent_id).first()
    if db_agent:
        for key, value in new_data.model_dump().items():
            setattr(db_agent, key, value)
        db.commit()
        db.refresh(db_agent)
    return db_agent


def delete_crawler_agent(db: Session, agent_id: int):
    db_agent = db.query(models.CrawlerAgent).filter(models.CrawlerAgent.id == agent_id).first()
    if db_agent:
        db.delete(db_agent)
        db.commit()
    return db_agent

