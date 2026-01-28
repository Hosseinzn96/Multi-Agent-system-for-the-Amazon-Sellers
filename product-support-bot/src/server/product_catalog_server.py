from src.config import GOOGLE_API_KEY
from src.agents.product_catalog.a2a_app import create_a2a_app
import uvicorn
import os

# Create the A2A FastAPI app
app = create_a2a_app(port=8001)


if __name__ == "__main__":
    uvicorn.run(
        "src.server.product_catalog_server:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
    )



'''import os
from src.agents.product_catalog.a2a_app import create_a2a_app

app = create_a2a_app()

if os.getenv("DEBUG_ROUTES") == "1":
    for r in app.routes:
        print("ROUTE:", getattr(r, "path", r), "METHODS:", getattr(r, "methods", None))'''
