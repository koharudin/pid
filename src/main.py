from __future__ import annotations

from typing import List

from pydantic import BaseModel

from dynaconf import Dynaconf
from starlette.middleware.cors import CORSMiddleware

settings = Dynaconf(settings_files=["settings.toml"])
import uvicorn

print(settings.EKO)

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
import starlette.status as status
import uuid

app = FastAPI(title="Packaging Service", description="desc",
              version="v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/test")
def test_endpoint(request: Request):
    return request.json()

@app.post("/persid")
async def test_endpoint(req: Request):
    # if desc != 'dans':
    #     raise HTTPException(401, detail="desc not valide")
    json_data = await req.json()
    p = PidModel(**json_data)
    ptitle = p.title
    prefix = p.identifier.prefix

    print(json_data)
    myuuid = uuid.uuid4()
    x = str(myuuid)
    print(f'Your UUID is: {x}')
    return {"title": p.title, "prefix": prefix}


@app.get("/id")
def get_id():
    return {"id": "123"}


# @app.get('/')
# def info():
#     return {"name": "My teste", "version": "v.1.0"}


@app.get("/{pid}")
async def resolve(pid: str):
    # Redirect to an absolute URL
    if pid == 'urn:nbn:id:pp-11-uuid123':
        return RedirectResponse(
            url="https://www.tokopedia.com", status_code=status.HTTP_302_FOUND
        )
    else:
        return RedirectResponse(
            url="https://shopee.co.id", status_code=status.HTTP_302_FOUND
        )


class Identifier(BaseModel):
    prefix: str = None
    id: str


class Location(BaseModel):
    url: str
    priority: int


class PidModel(BaseModel):
    identifier: Identifier
    locations: List[Location]
    title: str
    description: str
    authors: List[str]
    year: int


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=2004, reload=False)
