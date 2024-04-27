from shos.home_assistant.light.light import Light

__lights: dict[str, Light] = {}


def register_light(light_type: str):
    def decorator(fn):
        __lights[light_type] = fn
        return fn

    return decorator


def get_light(light_type: str):
    if light_type not in __lights:
        raise RuntimeError("No such a light type")
    return __lights[light_type]
