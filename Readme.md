# WOW Clan stats aggregator

This code is to try and get a sense of who plays what mode in the popular on-line naval wargame called *World of Warships*.

Specifically I would like some insight as to which people in the *clan* (team) I play with, spend most of their time playing a gam mode called *random* or a game mode called *coop*.

# Data Source

This data is already published via a nice Web interface at [https://na.wows-numbers.com/](https://na.wows-numbers.com/) however I am too lazy to hand tabulate the data for my clan - hence the code.


# Software required

  - Python 3.x
  - sqlite3 (This can be changed to any DB - however Python DB code needs to be updated also).
  - Python Modules
    - Pandas
    - requests
    - BeautifulSoup
    - sqlalchemy
    - sqlalchemy.orm 

    
# Db Creation

Assuming you have the correct python modules installed 

	python create_db.py 
	
You now should see a file called **rsr_stats.db**.

To see the structure of this Db use this command (sqlite3 assumed)

	echo ".schema" | sqlite3 rsr_stats.db
	
A Db schema showing two tables (person,score) are displayed like this

```sql
CREATE TABLE person (
	int_id INTEGER NOT NULL,
	pid INTEGER,
	name VARCHAR,
	PRIMARY KEY (int_id)
);
CREATE TABLE score (
	int_id INTEGER NOT NULL,
	"when" DATE,
	pid INTEGER,
	rnd_tot INTEGER,
	coop_tot INTEGER,
	PRIMARY KEY (int_id),
	FOREIGN KEY(pid) REFERENCES person (pid)
);
```

# Clan member population 

Another script **update_members.py**

	python update_members.py
	
Expect to see data like

```
id 1823920514, name ww1
id 1818680451, name Rattles
id 1816011143, name Pink_Fort
id 1822500234, name Lifeis69
```

You can see what is in the Database by

	echo 'select * from Person'|sqlite3 rsr_stats.db

the data will be displayed as 

```
1|1823920514|ww1
2|1818680451|Rattles
3|1816011143|Pink_Fort
4|1822500234|Lifeis69
```

This clearly shows 3 Columns (fields) the database creating it's own internal ID field rather than trying to rely on the one we extracted from the website.


# Update Users Co-Op and Ranked totals

Again - a python script

When this runs you will see output like

```text
Url is https://na.wows-numbers.com/player/8023920514,ww1/
Url is https://na.wows-numbers.com/player/8023920514,ww1/?type=pve
ww1  rnd: 11849 coop: 383
```

That is two URL requests per player - the 1st is the random stats, the second is the coop. These summary totals are displayed in the script output.

These data values are now added for the user **ww1** for the date/time that this script was run.

## So show me the totals for player ww1 


### Using SQL 

We want data for player **ww1** who has an pid of 8023920514.

```sql
select p.name,s."when",s.rnd_tot,s.coop_tot from person p, score s
   where s.pid=p.pid and
   p.pid=8023920514;
```

Outputs

```text
ww1|2023-04-07|500|10
ww1|2023-04-08|600|10
```

This clearly shows me player **ww1** has got 2 records (dated April 7th and April 8th 2023) - and has played 100 rounds of random, and 0 rounds of coop in this time period.


### Using Python

If you prefer the SQLALCHEMY.ORM syntax 

```python
from rsr import Person, Score, Base,use_db,engine
sess = use_db()

#With the session now available query the Db
#All People
for u in sess.query(Person):
    print(f"{u.pid,u.name}")
    
    
## Specific Person
## This assumes the record is there !!
p=sess.query(Person).filter(Person.pid == 8028590701).first()
print(str(p))
for rec in p.scored_hist:
    print(str(rec))

```

All people has been omitted for breviety.... 
Spefic Person and their data is listed only.


```text
id 8028590701, name Skippy
When: 2023-04-07,RndTot:4387,CoopTot:364
When: 2023-04-08,RndTot:4388,CoopTot:394
```