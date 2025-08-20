from docker import DockerClient
from docker.errors import DockerException
from docker.models.containers import Container
from threading import Thread
from datetime import datetime, timedelta
from typing import Callable
import asyncio

from dockerVerse import errors
from dockerVerse.utils import error_handler
from .types import DvContainer, DvEvent
from .utils import ContainerLog
from dockerVerse.config import (
    is_accessible_container,
    is_protected_container,
    DOCKER_SOCKET
)


class DvDockerClient:
    _docker_client: DockerClient

    def __init__(self):
        try:
            self._docker_client = DockerClient(base_url=DOCKER_SOCKET)
        except DockerException:
            raise errors.DockerDaemonConnectionError()
    
    def get_container(self, container_id: str) -> DvContainer:
        container = self._docker_client.containers.get(container_id)
        
        if not is_accessible_container(container.short_id):
            raise errors.ContainerAccessProhibitedError(container_id)

        return DvContainer(container)
    
    def get_all_containers(self) -> list[DvContainer]:
        containers: list[Container] = self._docker_client.containers.list(all=True)
        dvContainers = [
            DvContainer(c)
            for c in containers
            if is_accessible_container(c.short_id)
        ]
        dvContainers.sort(key=lambda c: c.name)  # sorting by name
        return dvContainers
    
    def start_container(self, container_id: str):
        container = self._docker_client.containers.get(container_id)

        if is_protected_container(container.short_id):
            raise errors.ContainerProtectedError(container_id)
        
        container.start()
    
    def stop_container(self, container_id: str):
        container = self._docker_client.containers.get(container_id)

        if is_protected_container(container.short_id):
            raise errors.ContainerProtectedError(container_id)
        
        container.stop()
    
    def restart_container(self, container_id: str):
        container = self._docker_client.containers.get(container_id)

        if is_protected_container(container.short_id):
            raise errors.ContainerProtectedError(container_id)
        
        container.restart()
    
    def start_event_observer(self, event_handler: Callable[[DvEvent], None]):
        self._docker_event_stream = self._docker_client.api.events(decode=True)

        @error_handler
        async def event_observer():
            for event in self._docker_event_stream:
                await event_handler(DvEvent(event))

        Thread(target=lambda: asyncio.run(event_observer())).start()
    
    def stop_event_observer(self):
        self._docker_event_stream.close()

    def get_logs_by_time(self, container_id: str, minutes: int):
        from_datetime = datetime.now() - timedelta(minutes=minutes)
        
        logs = self._docker_client.api.logs(container_id, since=from_datetime).decode()
        return ContainerLog(container_id, logs)

    def get_logs_by_line(self, container_id: str, lines: int):
        logs = self._docker_client.api.logs(container_id, tail=lines).decode()
        return ContainerLog(container_id, logs)

