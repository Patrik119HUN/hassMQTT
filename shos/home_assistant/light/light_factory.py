from shos.home_assistant.device import Entity

__lights: dict[str, Entity] = {}


def register_light(light_type: str):
    """
    Defines a decorator that registers a lighting function (`fn`) with a given
    name and type for later use.

    Args:
        light_type (str): type of light to be decorated, which is stored in the
            `__lights` cache for later use by the `decorator` function.

    Returns:
        instance of the function object type, as indicated by the return keyword
        `return: a light function with a name and type.
        
        	1/ `decorator`: This is the return value of the function, which is an
        instance of the `decorator` class.
        	2/ `__lights`: A dictionary containing the light types and their corresponding
        functions.
        	3/ `light_type`: The type of light for which the function was registered.

    """
    def decorator(fn):
        """
        Takes a light type and returns a function that is assigned to the specified
        light type.

        Args:
            fn (function.): function to generate high-quality documentation for.
                
                		- `light_type`: The type of light to be generated, which is a string.
                		- `return`: The function value returned by `fn`.

        Returns:
            fn: a function that takes no arguments and returns another function
            without any explicit implementation.
            
            		- `light_type`: The type of light, specified as a string.
            		- `fn`: The function to be decorated, which is assigned to the
            `lights` variable.

        """
        __lights[light_type] = fn
        return fn

    return decorator


def get_light(light_type: str):
    """
    Verifies if the given `light_type` exists in the internal light types dictionary
    `__lights`. If it does not, it raises a `RuntimeError`. Otherwise, it returns
    the corresponding value from the dictionary.

    Args:
        light_type (str): specific type of light for which the function is retrieving
            documentation.

    Returns:
        Light` object, as denoted by the colon (:) after `light_type` in the
        function definition: the value of the specified light type from the list
        `__lights`.
        
        		- `__lights`: A dictionary that contains the light types and their
        corresponding lights.
        		- `light_type`: The type of light being retrieved, which is obtained
        from the input parameter.
        		- `raise RuntimeError`: Raises a `RuntimeError` exception if the input
        `light_type` is not found in the `__lights` dictionary.

    """
    if light_type not in __lights:
        raise RuntimeError("No such a light type")
    return __lights[light_type]
