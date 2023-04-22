from bson import ObjectId as BsonObjectId
from pydantic import BaseModel
from typing import Optional

class ObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not BsonObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return BsonObjectId(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


# anything loaded from DB should use this model so _id works
class MongoBaseModel(BaseModel):
    id: Optional[ObjectId]
    # Fix To Allow ID being loaded
    class Config:
        allow_population_by_field_name = True
        json_encoders = {BsonObjectId: str}
        fields = {"id": {"alias": "_id"}}  