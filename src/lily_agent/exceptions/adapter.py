class AdapterError(Exception):
    def __init__(self, message: str):
        super().__init__(f"An adapter error occurred: '{message}'")