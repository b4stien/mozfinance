from sqlalchemy import Column, Integer, DateTime, UnicodeText, ForeignKey
from sqlalchemy.orm import backref, relationship

from warbmodel import User, Application

from . import Base


class Action(Base):
    __tablename__ = 'actions'
    id = Column(Integer, primary_key=True)

    datetime = Column(DateTime, index=True)
    message = Column(UnicodeText)

    created_by_id = Column(Integer, ForeignKey('wb_users.id'))
    created_by = relationship(
        'User', backref=backref('actions', order_by=id))

    application_id = Column(Integer, ForeignKey('wb_applications.id'))
    application = relationship(
        'Application', backref=backref('actions', order_by=id))
