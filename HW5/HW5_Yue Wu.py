
# Using SQLAlchemy to Talk to a Database
# =====================
# SqlAlchemy helps you use a database to store and retrieve information from python.  It abstracts the specific storage engine from te way you use it - so it doesn't care if you end up using MySQL, SQLite, or whatever else. In addition, you can use core and the object-relational mapper (ORM) to avoid writing any SQL at all.  The [SQLAlchemy homepage](http://www.sqlalchemy.org/) has lots of good examples and full documentation.

# In[ ]:

from sqlalchemy import *
import datetime

# add `echo=True` to see log statements of all the SQL that is generated
engine = create_engine('sqlite:///:memory:',echo=True) # just save the db in memory for now (ie. not on disk)
metadata = MetaData()
# define a table to use
queries = Table('queries', metadata,
    Column('id', Integer, primary_key=True),
    Column('keywords', String(400), nullable=False),
    Column('count', Integer, default=0),
)
metadata.create_all(engine) # and create the tables in the database


# In[ ]:

import mediacloud, datetime


# In[ ]:

mc = mediacloud.api.MediaCloud('4923e5782ddbc72d23d4a57cfcf2176efbaef3b18677b4ae7eb7581e8356e924')
trump_count = mc.sentenceCount('( Trump )', solr_filter=[mc.publish_date_query( datetime.date( 2016, 9, 1), datetime.date( 2016, 9, 30) ), 'tags_id_media:1' ])
print("Trump count:", trump_count['count']) # prints the number of sentences found
clinton_count = mc.sentenceCount('( Clinton )', solr_filter=[mc.publish_date_query( datetime.date( 2016, 9, 1), datetime.date( 2016, 9, 30) ), 'tags_id_media:1' ])
print("Clinton count:", clinton_count['count']) # prints the number of sentences found


# In[ ]:

trump_count


# In[ ]:



insert_stmt = queries.insert()
str(insert_stmt) # see an example of what this will do
insert_stmt = queries.insert().values(keywords="Trump", count = trump_count['count'])
db_conn = engine.connect()
result = db_conn.execute(insert_stmt)
result.inserted_primary_key # print out


# In[ ]:

insert_stmt = queries.insert().values(keywords="Clinton", count = clinton_count['count'])
result = db_conn.execute(insert_stmt)
result.inserted_primary_key # print out


# ### Retrieving Data
# Read more about using [SQL select statments](http://docs.sqlalchemy.org/en/rel_1_0/core/tutorial.html#selecting).

# In[ ]:

from sqlalchemy.sql import select
select_stmt = select([queries])
results = db_conn.execute(select_stmt)
for row in results:
    print(row)


# In[ ]:

queries.c.id


# In[ ]:

select_stmt = select([queries]).where(queries.c.id.in_([1,2]))
for row in db_conn.execute(select_stmt):
    print(row)


# In[ ]:

select_stmt = select([queries]).where(queries.c.keywords.like('t%'))
for row in db_conn.execute(select_stmt):
    print(row)


# ## ORM
# You can use their ORM library to handle the translation into full-fledged python objects.  This can help you build the Model for you [MVC](https://en.wikipedia.org/wiki/Model–view–controller) solution.

# In[1]:

import datetime
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
Base = declarative_base()


# ### Creating a class mapping
# Read more about [creating a mapping](http://docs.sqlalchemy.org/en/rel_1_0/orm/tutorial.html#declare-a-mapping).

# In[2]:

class Query(Base):
    __tablename__ = 'queries'
    id = Column(Integer, primary_key=True)
    keywords = Column(String(400))
    count = Column(Integer,default=0)
    def __repr__(self):
        return "<Query(keywords='%s',count='%s')>" % (self.keywords, self.count)
Query.__table__


# In[3]:

import mediacloud, datetime


# In[4]:

mc = mediacloud.api.MediaCloud('4923e5782ddbc72d23d4a57cfcf2176efbaef3b18677b4ae7eb7581e8356e924')
trump_count = mc.sentenceCount('( Trump )', solr_filter=[mc.publish_date_query( datetime.date( 2016, 9, 1), datetime.date( 2016, 9, 30) ), 'tags_id_media:1' ])
print("Trump count:", trump_count['count']) # prints the number of sentences found
clinton_count = mc.sentenceCount('( Clinton )', solr_filter=[mc.publish_date_query( datetime.date( 2016, 9, 1), datetime.date( 2016, 9, 30) ), 'tags_id_media:1' ])
print("Clinton count:", clinton_count['count']) # prints the number of sentences found


# ### Creating a connection and session
# Read more about [creating this stuff](http://docs.sqlalchemy.org/en/rel_1_0/orm/tutorial.html#creating-a-session).

# In[5]:

engine = create_engine('sqlite:///:memory:') # just save the db in memory for now (ie. not on disk)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
my_session = Session()


# ### Inserting Data
# Read more about [inserting data with an ORM](http://docs.sqlalchemy.org/en/rel_1_0/orm/tutorial.html#adding-new-objects).

# In[6]:

query = Query(keywords="Trump", count = trump_count['count'])
query.keywords


# In[7]:

my_session.add(query)
my_session.commit()
query.id


# ### Retrieving Data
# Read more about [retrieving data from the db](http://docs.sqlalchemy.org/en/rel_1_0/orm/tutorial.html#querying) via an ORM class.

# In[8]:

for q in my_session.query(Query):
    print(q)


# In[9]:

query1 = Query(keywords="robot")
query2 = Query(keywords="puppy")
my_session.add_all([query1,query2])
my_session.commit()


# In[11]:

for q in my_session.query(Query):
    print(q)


# In[12]:

for q in my_session.query(Query).filter(Query.keywords.like('r%')):
    print(q)

