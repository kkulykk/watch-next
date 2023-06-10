from pydantic import BaseModel, Field


class UserActivityTrailLog(BaseModel):
    user_id: str
    action: str
    data: dict
    timestamp: int = Field(description="Time of last edit in the UNIX format "
                                       "(number of seconds since Epoch)")
