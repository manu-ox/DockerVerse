import os


class ContainerLog:
    def __init__(self, container_id: str, logs: str):
        self.filename = f'container_{container_id}.log'
        self.logs = logs
    
    def __enter__(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(self.logs)

        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        os.remove(self.filename)


