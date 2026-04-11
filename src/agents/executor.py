from src.agents.router import route_query


def run_agent(user_query: str):
    return route_query(user_query)