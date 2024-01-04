from time import sleep

from sqlalchemy.orm import Session

from app import schemas, models
from app.services.schedulingService.scheduler import Scheduler
from app.services.authService.auth import get_current_user


def create_crawler_agent(db: Session, agent: schemas.CrawlerAgent):
    db_agent = models.CrawlerAgent(
        name=agent.name,
        min_area=agent.min_area,
        max_price=agent.max_price,
        number_of_rooms=agent.number_of_rooms,
        zip_code=agent.zip_code,
        state=agent.state,
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


def start_crawler_agent(db: Session, agent_id: int):
    agent_to_start = db.query(models.CrawlerAgent).filter(models.CrawlerAgent.id == agent_id).first()

    crawler_filter = {
        "max_price": agent_to_start.max_price,
        "min_area": agent_to_start.min_area
    }

    service = Scheduler(
        interval_hours=1,
        duration_hours=24,
        receiver_email="wi21b032@technikum-wien.at",
        crawler_filter=crawler_filter,
        zip_code=agent_to_start.zip_code,
        number_of_rooms=agent_to_start.number_of_rooms
    )

    service.start_crawling()

