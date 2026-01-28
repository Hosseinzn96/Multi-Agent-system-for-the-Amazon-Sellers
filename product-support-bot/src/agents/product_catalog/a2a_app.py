from google.adk.a2a.utils.agent_to_a2a import to_a2a

from .agent import create_product_catalog_agent

def create_a2a_app(port: int = 8001):
    agent = create_product_catalog_agent()
    return to_a2a(agent, port=port)


#from fastapi import FastAPI
#from google.adk.a2a.utils.agent_to_a2a import to_a2a
#from .agent import create_product_catalog_agent

#def create_a2a_app():
    #app = FastAPI()

    #agent = create_product_catalog_agent()
    #a2a_asgi_app = to_a2a(agent)

    # A2A endpoints live under /a2a
    #app.mount("/a2a", a2a_asgi_app)

    #@app.get("/health")
    #def health():
        #return {"status": "ok"}

    #return app