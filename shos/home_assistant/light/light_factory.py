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
        Takes a light type as input and assigns it the value of `fn`. The function
        then returns the same value passed to it without modification.

        Args:
            fn (function.): function that is being documented, and it is used to
                generate high-quality documentation for that function.
                
                		- `light_type`: The type of light being decorated (string)
                		- `fn`: The function to be decorated (function)

        Returns:
            fn: a lighting fixture of the specified type.
            
            		- `light_type`: This is an attribute of the returned object that
            indicates the type of light it represents, with values specified in
            the `lights` dictionary.

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
