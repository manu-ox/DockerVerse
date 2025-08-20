from datetime import datetime

from dockerVerse.utils import format_time
from .typing import DockerEvent as _DockerEvent


class _DockerRawEventStatus:
    START = 'start'  # Event when container start
    DIE = 'die'  # Event when container terminates
    DESTROY = 'destroy'  # Event when a container is destoryed

    # Event after succefully restarting a container
    # Before `restart` event, there will be `die` and `start` event
    RESTART = 'restart'

    STOP = 'stop'
    KILL = 'kill'

    CREATE = 'create'
    ATTACH = 'attach'
    RESIZE = 'resize'


class DvEventStatus:
    STARTED = _DockerRawEventStatus.START
    STOPPED = _DockerRawEventStatus.DIE
    DESTROYED = _DockerRawEventStatus.DESTROY
    RESTARTED = _DockerRawEventStatus.RESTART


class DockerEventType:
    CONTAINER = 'container'
    NETWORK = 'network'


class DvEvent:
    status: str | None
    type: str
    time: datetime
    time_string: str

    container_id: str
    container_long_id: str
    container_image: str | None
    container_name: str | None

    def __init__(self, event: _DockerEvent):
        self.status = event.get('status')  # None for network events
        self.type = event['Type']
        self.time = datetime.fromtimestamp(event['time'])
        self.time_string = f'"{format_time(self.time)}"'

        self.container_long_id = event['Actor']['ID']
        self.container_id = self.container_long_id[:12]
        self.container_image = event['Actor']['Attributes'].get('image')
        self.container_name = event['Actor']['Attributes'].get('name')