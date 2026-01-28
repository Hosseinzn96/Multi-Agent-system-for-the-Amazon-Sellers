#this file is for the observability app
# support_app/agent.py
# This file exposes existing customer support agent


from src.agents.customer_support.agent import customer_support_agent

# ADK Web UI expects a variable named root_agent
root_agent = customer_support_agent
