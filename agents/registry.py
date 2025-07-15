AGENT_REGISTRY = {}

def register_agent(name):
    def decorator(cls):
        AGENT_REGISTRY[name] = cls
        return cls
    return decorator

def get_agent(name, **kwargs):
    agent_class = AGENT_REGISTRY.get(name)
    if not agent_class:
        raise ValueError(f"Agent {name} not found")
    return agent_class(**kwargs)
