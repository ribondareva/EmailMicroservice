from fastapi import FastAPI
from app.api.v1.endpoints import router as email_router


app = FastAPI(
    title="Email Microservice",
    description="Сервис для отправки и получения писем",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
)

app.include_router(email_router, prefix="/api/v1/emails")


