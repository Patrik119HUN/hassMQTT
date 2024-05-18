from threading import Lock, Thread


class SingletonMeta(type):
    _instances: dict = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        """
        Generates high-quality documentation for code given to it, creates an
        instance of a class if no existing instance exists for that class, and
        returns the instance.

        Args:
            cls (instance of the class (i.e., any user-defined or built-in classes).):
                class for which an instance is being created.
                
                		- `cls_lock`: A dictionary that maintains a reference count for
                each instance of the class. If the instance is already created,
                this value will be true (set to 1).
                		- `instances`: A dictionary that maps the class name to its
                instances. This is where the new instance created by `__call__`
                is stored.

        Returns:
            instance of the class for which it was defined, according to the given
            code segment: an instance of a class.
            
            		- `cls`: This is the class that defined the `__call__` method.
            		- `instance`: This is the instance created and returned by the
            `__call__` method.
            		- `args`: This is an optional argument passed to the `__call__`
            method, representing a tuple of positional arguments.
            		- `kwargs`: This is an optional argument passed to the `__call__`
            method, representing a dictionary of keyword arguments.

        """
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
