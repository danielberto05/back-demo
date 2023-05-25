from fastapi import FastAPI

app = FastAPI()

from api.v1.api import api_router

app = FastAPI(
    title="Back-end Demo",
    openapi_url="/api/v1/openapi.json",
)

@app.get("/")
@app.get("", include_in_schema=False)
async def health_check():
    return {"message": "service is running"}


app.include_router(api_router, prefix="/api/v1")
