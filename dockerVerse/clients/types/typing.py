from typing import TypedDict, Literal


class DockerEventActorAttributes(TypedDict):
    image: str
    name: str


class DockerEventActor(TypedDict):
    ID: str
    Attributes: DockerEventActorAttributes


class DockerEvent(TypedDict):
    status: str
    Type: str
    Actor: DockerEventActor
    time: int


class HostPortMapType(TypedDict):
    HostIp: str
    HostPort: str


class ContainerState(TypedDict):
    StartedAt: str
    FinishedAt: str
    ExitCode: str
    Status: Literal['exited', 'running', 'restarting', 'paused']


class RestartPolicyType(TypedDict):
    Name: Literal['no', 'always', 'on-failure', 'unless-stopped']
    MaximumRetryCount: str


class HostConfigType(TypedDict):
    AutoRemove: Literal['True', 'False']


class ConfigType(TypedDict):
    Image: str


class NetworkSettingsType(TypedDict):
    Networks: dict[str, dict]


class ContainerAttributeType(TypedDict):
    State: ContainerState
    Created: str
    HostConfig: HostConfigType
    RestartPolicy: RestartPolicyType
    Config: ConfigType
    NetworkSettings: NetworkSettingsType


class ContainerType:
    attrs: ContainerAttributeType
    ports: dict[str, list[HostPortMapType]]
