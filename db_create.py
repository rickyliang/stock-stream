#!/usr/bin/env python

from sqlalchemy import create_engine
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_ECHO
from stream import models

def main():
    db_engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=SQLALCHEMY_ECHO)
    Base = models.Base
    Base.metadata.create_all(db_engine)
    
if __name__ == '__main__':
    main()