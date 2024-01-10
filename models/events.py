from pydantic import ConfigDict
from sqlmodel import JSON, SQLModel, Field, Column
from typing import Optional, List


class Event(SQLModel, table=True):
	id: int = Field(default=None, primary_key=True)
	title: str
	image: str
	description: str
	tags: List[str] = Field(sa_column=Column(JSON))
	location: str

	model_config = ConfigDict(
		json_schema_extra={
			"example": {
				"id": 1,
				"title": "some title",
				"image": "https://somewhere.com/image.png",
				"description": "some description",
				"tags": ["FastAPI", "React"],
				"location": "somewhere"
			}
		}
	)


class UpdateEvent(SQLModel):
	title: Optional[str]
	image: Optional[str]
	description: Optional[str]
	tags: Optional[List[str]]
	location: Optional[str]

	class Config:
		schema_extra: {
			"example": {
				"title": "something",
				"image": "https://somewhere.io",
				"description": "sometext",
				"tags": ["python", "django", "fastapi", "react"],
				"location": "Nowhere"
			}
		}