"""
* sahab tts wrapper REST service
* author: @alisharify7
* © under GPL-3.0 license.
* email: alisharifyofficial@gmail.com
* https://github.com/alisharify7/RESTful-tts-wrapper
"""

import uuid
import datetime
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from flask import current_app
from src.extensions import db


class BaseModel(db.Model):
    """
    Base Parent Abstract Model.
    all models inheritance from this model.
    """

    __abstract__ = True
    # __table_args__ = {
    #     # 'mysql_engine': 'InnoDB',
    #     # 'mysql_charset': 'utf8',
    #     # 'mysql_collate': 'utf8_persian_ci'
    # }

    id: so.Mapped[int] = so.mapped_column(sa.INTEGER, primary_key=True)

    @staticmethod
    def set_table_nae(name: str) -> str:
        """
        this static method concat table prefix names and table names
        for all models.

        :param name: name of the table
        :type name: str
        :return: name of the table
        :rtype: str

        """
        name = name.replace("-", "_").replace(" ", "")
        return f"{BaseModel.DATABASE_TABLE_PREFIX_NAME}{name}".lower()

    def set_public_key(self):
        """This Method Set a Unique PublicKey of each record"""
        while True:
            token = uuid.uuid4().hex
            if self.query.filter_by(public_key=token).first():
                continue

            self.public_key = token
            break

    def save(self, show_traceback: bool = True) -> bool:
        """
        combination of two steps, add and commit session

        :param show_traceback: flag to show traceback of exception into stdout or not
        :type show_traceback: bool
        :return: True or False
        :rtype: bool
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:  # pylint: disable=W0718
            db.session.rollback()
            if show_traceback:
                current_app.logger.exception(exc_info=e, msg=e)
            return False

        return True

    public_key: so.Mapped[str] = so.mapped_column(
        sa.String(36), nullable=False, unique=True, index=True
    )  # unique key for each element <usually used in frontend>
    created_time: so.Mapped[Optional[datetime.datetime]] = so.mapped_column(
        sa.DateTime, default=datetime.datetime.now
    )
    modified_time: so.Mapped[Optional[datetime.datetime]] = so.mapped_column(
        sa.DateTime,
        onupdate=datetime.datetime.now,
        default=datetime.datetime.now,
    )
