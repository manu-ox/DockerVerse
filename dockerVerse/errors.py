
class DockerDaemonConnectionError(Exception):
    def __init__(self):
        super().__init__(
            "Connection to Docker daemon failed! Is docker daemon running? "
            "If dockerVerse itself is in a docker container: is `/var/run/docker.sock` mounted?"
        )


class ContainerProtectedError(Exception):
    def __init__(self, container_id):
        super().__init__(
            f"Container {container_id} is Protected"
        )


class ContainerAccessProhibitedError(Exception):
    def __init__(self, container_id):
        super().__init__(
            f"Access to Container {container_id} is Prohibited"
        )


