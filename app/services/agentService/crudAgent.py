from time import sleep

from sqlalchemy.orm import Session

from app import schemas, models
from app.services.schedulingService.scheduler import Scheduler


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

    crawler_filter = {
        "max_price": db_agent.max_price,
        "min_area": db_agent.min_area
    }

    service = Scheduler(
        interval_hours=1,
        duration_hours=24,
        receiver_email="wi21b032@technikum-wien.at",
        crawler_filter=crawler_filter,
        zip_code=db_agent.zip_code,
        number_of_rooms=db_agent.number_of_rooms
    )

    try:
        print("Starte das Crawling...")
        service.start_crawling()
        sleep(5 * 60)

    finally:
        print("Stoppe das Crawling...")
        service.stop_crawling()

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

