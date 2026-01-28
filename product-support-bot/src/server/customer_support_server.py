from fastapi import FastAPI
from google.adk.a2a.utils.agent_to_a2a import to_a2a

from src.agents.customer_support.agent import customer_support_agent

app = FastAPI()

# Turn the agent into an A2A ASGI app and expose its routes
a2a_app = to_a2a(customer_support_agent)
app.router.routes.extend(a2a_app.router.routes)

@app.get("/health")
def health():
    return {"status": "ok"}
