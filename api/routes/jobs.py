from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from components import authentication

router = APIRouter()

