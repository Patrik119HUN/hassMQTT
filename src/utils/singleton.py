from threading import Lock, Thread


class SingletonMeta(type):
    _instances: dict = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        """
        Creates a new instance of a class and stores it in the class's instances
        dictionary when none exist for that class.

        Args:
            cls (class object.): class to which the instance belongs, and is used
                to store the instance in a dictionary for later retrieval.
                
                	1/ `_lock`: A boolean property that indicates whether cls is in
                use or not.
                	2/ `instances`: A dictionary that maps class instances to their
                respective classes. When a class is instanciated using the `__call__`
                function, its instance is stored in this dictionary.

        Returns:
            str: an instance of a class.

        """
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
