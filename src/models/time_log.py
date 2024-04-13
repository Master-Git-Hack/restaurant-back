from datetime import datetime

from mongoengine import DateTimeField, Document, ReferenceField

from .restaurant import Model as Restaurant
from .user import Model as User


# Define EmployeeTimeLog document
class Model(Document):
    meta = dict(
        collection="time_log",
        strict=False,
    )
    employee = ReferenceField(User, required=True)
    restaurant = ReferenceField(Restaurant, required=True)
    check_in_time = DateTimeField(required=True, default=datetime.now)
    check_out_time = DateTimeField()

    def calculate_work_hours(self):
        """
        Calculate the duration of work hours based on check-in and check-out times.
        Returns the duration in hours (float).
        """
        if self.check_out_time and self.check_in_time:
            work_duration = self.check_out_time - self.check_in_time
            work_hours = work_duration.total_seconds() / 3600.0
            return work_hours
        else:
            return None


from ..middlewares.db import Template


class TimeLog(Template):
    def __init__(self):
        super().__init__(Model)
