#this file is for the observability app
# support_app/agent.py
# This file exposes existing customer support agent
# as the ADK root agent so the Web UI can run and debug it

from src.agents.customer_support.agent import customer_support_agent

# ADK Web UI expects a variable named root_agent
root_agent = customer_support_agent
