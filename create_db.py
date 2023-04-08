import os
def create_db():
    from sqlalchemy import (
        Table,
        select,
        Column,
        Date,
        String,
        ForeignKey,
        Integer,
        create_engine,
    )
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.orm import declarative_base

    # Need to model to be understood
    from rsr import Person, Score, Base, engine

    # engine = create_engine('sqlite:///:memory:', echo=True)
    #engine = create_engine("sqlite:///rsr_stats.db",echo=True)
    
    # Create db now
    Base.metadata.create_all(engine)
    smsession = sessionmaker(bind=engine)
    smsession.configure(bind=engine)  # once engine is available
    session = smsession()

    session.commit()
    print("Db File has been created")

if os.path.isfile("rsr_stats.db"):
    print("###################################")
    print("Database already exists.")
    print("If you want a new DB - manually remove the rsr_stats.db file")
    print("###################################")
else:
    create_db()

