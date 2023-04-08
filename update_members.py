from sqlalchemy import Table, select, Column,Date, String, ForeignKey, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from rsr import Person, Score, Base
from stats import  get_clan_members
import pandas as pd


engine=create_engine("sqlite:///rsr_stats.db")

def use_db():
    # Import the DB Models to be created.
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)  # once engine is available
    session = Session()
    return session
sess = use_db()

rsr_clan = get_clan_members()

for p in rsr_clan[['pid','Player']].values.tolist():
    q = sess.query(Person).filter(Person.pid == p[0])
    if len(q.all())==0:
        #Record does not exist
        sess.add(Person(p[0],p[1]))
        print(f"Adding {p}")
sess.commit()

# Sanity check see what is there
for s in sess.query(Person).all():
    print(str(s))
