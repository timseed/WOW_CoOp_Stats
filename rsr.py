from sqlalchemy import Table, select, Column,Date, String, ForeignKey, Integer, create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref, Query
from sqlalchemy.orm import mapped_column
from pprint import pprint
from datetime import datetime
Base = declarative_base()
engine=create_engine("sqlite:///rsr_stats.db")
########################################################################
class Person(Base):
    """"""
    __tablename__ = "person"
    int_id = Column(Integer, autoincrement=True, primary_key=True)
    pid = Column(Integer)
    name = Column(String)
    scored_hist = relationship("Score", back_populates="player_score")

    # ----------------------------------------------------------------------
    def __init__(self, pid,name):
        """"""
        self.pid=pid
        self.name = name
    
    def __str__(self):
        return f"id {self.pid}, name {self.name}"
        
class Score(Base):
    __tablename__="score"
    int_id = Column(Integer, autoincrement=True, primary_key=True)
    when = Column(Date)
    pid = mapped_column(ForeignKey("person.pid"))
    rnd_tot = Column(Integer)
    coop_tot = Column(Integer)
    player_score = relationship("Person", back_populates="scored_hist")
    
    def __init__(self, when,pid,r_tot,c_tot):
        """"""
        self.when=when
        self.pid=pid
        self.rnd_tot=r_tot
        self.coop_tot = c_tot
        
    def __str__(self):
        return f"When: {self.when.isoformat()},RndTot:{self.rnd_tot},CoopTot:{self.coop_tot}"

    
    

def use_db():
    # Import the DB Models to be created.
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)  # once engine is available
    session = Session()
    return session