from datetime import datetime

from app.resources.base_resource import BaseResource


class TimestampMixin(BaseResource):
    created_at: datetime
    updated_at: datetime
