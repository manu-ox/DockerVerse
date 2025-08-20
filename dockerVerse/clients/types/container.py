from docker.models.containers import Container
from docker.models.containers import Container
from datetime import datetime, timezone
from dateutil import parser
from datetime import datetime

from dockerVerse.config import is_protected_container
from .typing import ContainerType
from dockerVerse.utils import (
    get_duration_from_seconds,
    get_status_tag,
    format_time
)


class ContainerStatus:
    RUNNING = 'running'
    EXITED = 'exited'
    RESTARTING = 'restarting'
    PAUSED = 'paused'


class ContainerUtils:
    _container: Container | ContainerType

    def __init__(self, container: Container | ContainerType):
        self._container = container


    def get_state_time(self, *, start: bool=False, exit: bool=False, created: bool=False):
        if start:
            time = self._container.attrs['State']['StartedAt']
        elif exit:
            time = self._container.attrs['State']['FinishedAt']
        elif created:
            time = self._container.attrs['Created']
        else:
            raise ValueError(f"Invalid Params: 'start', 'exit' or 'create' param is needed")
        
        return parser.isoparse(time)
    

    def get_created_time(self):
        created_time = self.get_state_time(created=True)
        return format_time(created_time)


    def get_restart_policy(self):
        return self._container.attrs['HostConfig']['RestartPolicy']['Name']


    def get_image_name(self):
        return self._container.attrs['Config']['Image']
    

    def get_networks(self) -> list[str]:
        networks: dict =  self._container.attrs['NetworkSettings']['Networks']
        return list(networks.keys())


    def get_uptime(self):
        uptime = datetime.now(timezone.utc) - self.get_state_time(start=True)
        return get_duration_from_seconds(uptime.seconds)


    def get_time_ran(self):
        time_ran = self.get_state_time(exit=True) - self.get_state_time(start=True)
        return get_duration_from_seconds(time_ran.seconds)


    def get_exit_time(self):
        exit_time = self.get_state_time(exit=True)
        return format_time(exit_time)


    def get_port_mappings(self) -> list[str]:
        ports = self._container.ports

        port_mappings = []
        for container_port, host_port_maps in ports.items():
            if host_port_maps:
                for hm in host_port_maps:
                    # Ignoring IPv6
                    if hm['HostIp'] == '::': continue

                    port_mappings.append(f"{hm['HostIp']}:{hm['HostPort']} => {container_port}")

        return port_mappings


class DvContainer:
    id: str
    long_id: str
    name: str
    image: str
    status: str
    uptime: str | None
    created_time: str
    exit_time: str | None
    time_ran: str | None
    restart_policy: str
    port_maps: list[str]
    networks: list[str]
    is_running: bool
    is_protected: bool

    def __init__(self, container: Container):
        self.id = container.short_id
        self.long_id = container.id
        self.name = container.name
        self.status = container.status

        container_utils = ContainerUtils(container)

        self.image = container_utils.get_image_name()
        self.restart_policy = container_utils.get_restart_policy()
        self.is_protected = is_protected_container(self.id)
        self.networks = container_utils.get_networks()
        self.created_time = container_utils.get_created_time()

        if container.status == ContainerStatus.RUNNING:
            self.is_running = True
            self.uptime = container_utils.get_uptime()
            self.port_maps = container_utils.get_port_mappings()
            self.exit_time = None
            self.time_ran = None
        else:
            self.is_running = False
            self.uptime = None
            self.port_maps = []
            self.exit_time = container_utils.get_exit_time()
            self.time_ran = container_utils.get_time_ran()


    def to_string(self, detailed=False):
        compact = (
            f"CONTAINER-ID: `{self.id}`",
            f"STATUS: `{self.status.title()}` {get_status_tag(self.is_running)}",
            f"CONTAINER: `{self.name}`",
            f"UPTIME: `{self.uptime}`" if self.is_running else "",
            f"STOPPED: `{self.exit_time}`" if not self.is_running else "",
            f"EXECUTED: `{self.time_ran}`" if not self.is_running else "",
        )

        if not detailed:
            return '\n'.join(filter(None, compact))
        
        if len(self.networks) == 1:
            network_details = f"NETWORK: `{self.networks[0]}`"
        else:
            network_details = f"NETWORKS: {'\n - `' + '`\n - `'.join(self.networks)}`"
        
        complete = (
            *compact,
            f"\nCREATED: `{self.created_time}`",
            f"IMAGE: `{self.image}`",
            f"RESTART-POLICY: `{self.restart_policy}`" if self.restart_policy else "",
            f"PORT-MAPS: {'\n - `' + '`\n - `'.join(self.port_maps)}`" if self.port_maps else "",
            network_details,
        )
        
        return '\n'.join(filter(None, complete))

