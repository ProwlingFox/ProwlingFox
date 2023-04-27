# Testing Embeddings As Classification Of Job Titles

from numpy import dot
from numpy.linalg import norm
from time import sleep
from typing import List
import components.secrets as secrets
secrets.init()

import components.db as db
db.init()
jobaiDB = db.jobaiDB

from pydantic import BaseModel
import openai
# from openai.embeddings_utils import get_embedding
openai.api_key = secrets.secrets["OpenAISecret"]

class Role(BaseModel):
    role: str
    embedding: List[float]

class Sector(BaseModel):
    sector: str
    roles: List[Role]
    embedding: List[float]


# Warning, This will remove all existing embeds
def fillRoleEmbeddings():
    jobaiDB.roles.delete_many({})

    with open("roleslist.md") as roles_list:
        current_sector = ""
        
        while True:
            sector = False
            line = roles_list.readline().removesuffix('\n')
            if not line:
                break

            if line.startswith("#"):
                current_sector = line.removeprefix("# ")
                continue

            while True:
                try:
                    resp = openai.Embedding.create(
                        input=current_sector + " " + line,
                        model="text-embedding-ada-002"
                    )
                    break
                except openai.OpenAIError as e:
                    print("Rate Limited")
                    sleep(2)
            
            role = Role(
                role=line,
                sector=current_sector,
                embedding=resp["data"][0]["embedding"]
            )

            jobaiDB.roles.insert_one(role.dict())
            print("inserted", line)

def getRoleEmbeddings() -> List[Role]:
    rolesEmbeddings = list(map(lambda x: Role.parse_obj(x),  jobaiDB.roles.find({}) ))

    return rolesEmbeddings
# fillRoleEmbeddings()
roleEmbedings = getRoleEmbeddings()

testRoleTitle = "Swim Teacher - Casual - King Alfred Leisure Centre"
testRoleEmbedding = openai.Embedding.create(input=testRoleTitle, model="text-embedding-ada-002")["data"][0]["embedding"]

cos_sims = []

for role in roleEmbedings:
    cos_sim = dot(role.embedding, testRoleEmbedding)/(norm(role.embedding)*norm(testRoleEmbedding))
    cos_sims.append((role.role, cos_sim))

cos_sims.sort(key=lambda x: x[1], reverse=False)

for cos_sim in cos_sims:
    print("Closeness to role,", cos_sim[0], ":", cos_sim[1])
