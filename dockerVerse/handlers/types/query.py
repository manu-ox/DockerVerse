from . import base
from .methods import SimpleButtonFormat, ContainerMethod, LogsMethod


class ContainerListButton(base.ButtonHandler):
    """Button to list all containers"""
    _data_format = SimpleButtonFormat.container_list


class ContainerStartButton(base.ContainerControlButtonHandler):
    """Button to start container"""
    _method = ContainerMethod.start


class ContainerStopButton(base.ContainerControlButtonHandler):
    """Button to stop container"""
    _method = ContainerMethod.stop


class ContainerRestartButton(base.ContainerControlButtonHandler):
    """Button to restart container"""
    _method = ContainerMethod.restart


class ContainerCompactViewButton(base.ContainerControlButtonHandler):
    """Button to view basic details of container"""
    _method = ContainerMethod.view


class ContainerDetailedViewButton(base.ContainerControlButtonHandler):
    """Button to view full details of container"""
    _method = ContainerMethod.detailed_view


class ContainerLogsOptionButton(base.ContainerControlButtonHandler):
    """Button to list all options to retrive logs"""
    _method = ContainerMethod.logs


class TimeLogsButton(base.LogsButtonHandler):
    """Button to get logs by time"""
    _method = LogsMethod.time_logs


class LineLogsButton(base.LogsButtonHandler):
    """Button to get logs by number of lines"""
    _method = LogsMethod.line_logs


class UpdateLogsTimeButton(base.LogsButtonHandler):
    """Button to update time for time based logs"""
    _method = LogsMethod.update_time


class UpdateLogsLineButton(base.LogsButtonHandler):
    """Button to update lines for line based logs"""
    _method = LogsMethod.update_line

