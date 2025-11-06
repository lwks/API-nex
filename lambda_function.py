"""AWS Lambda entry point wrapping the FastAPI app with Mangum."""

from mangum import Mangum

from app.src.main import app

handler = Mangum(app)
