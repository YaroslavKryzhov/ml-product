from pydantic import BaseModel


class TaskJwtResponse(BaseModel):
    task_id: str
    jwt_token: str
