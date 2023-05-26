from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

from api.v1.api import api_router

app = FastAPI(
    title="Back-end Demo",
    openapi_url="/api/v1/openapi.json",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
@app.get("", include_in_schema=False)
async def health_check():
    return {"message": "service is running"}


app.include_router(api_router, prefix="/api/v1")
