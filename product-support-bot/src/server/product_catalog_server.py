from src.config import GOOGLE_API_KEY
from src.agents.product_catalog.a2a_app import create_a2a_app
import uvicorn

# Create the A2A FastAPI app
app = create_a2a_app(port=8001)


if __name__ == "__main__":
    uvicorn.run(
        "src.server.product_catalog_server:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
    )


