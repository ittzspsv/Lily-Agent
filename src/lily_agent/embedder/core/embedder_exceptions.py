class EmbedderError(Exception):
    def __init__(self, message: str):
        super().__init__(f"An Embedder error occurred: '{message}'")