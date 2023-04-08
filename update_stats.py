from sqlalchemy import Table, select, Column,Date, String, ForeignKey, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from rsr import Person, Score, Base

from datetime import datetime
import pandas as pd
# import sys
# sys.path.append("/Users/tim/Dev/Python/wow_coop/stats.py") 
from stats import  get_clan_members,get_player_random_count,get_player_coop_count

engine=create_engine("sqlite:///rsr_stats.db")

def use_db():
    # Import the DB Models to be created.
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)  # once engine is available
    session = Session()
    return session
sess = use_db()
nw = datetime.now()

# Sanity check see what is there
for s in sess.query(Person).all():
    pid=s.pid
    name=s.name
    rnd_cur = get_player_random_count(pid,name)
    coop_cur = get_player_coop_count(pid,name)
    s.scored_hist.append(Score(nw,pid,rnd_cur,coop_cur))
    print(f"{s.name}  rnd: {rnd_cur} coop: {coop_cur}")


sess.commit()
