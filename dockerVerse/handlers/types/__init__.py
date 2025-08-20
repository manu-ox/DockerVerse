from .command import (
    StartCommand,
    ListCommand
)


from .query import (
    ContainerStartButton,
    ContainerStopButton,
    ContainerRestartButton,
    ContainerCompactViewButton,
    ContainerDetailedViewButton,
    ContainerListButton,
    ContainerLogsOptionButton,
    TimeLogsButton,
    LineLogsButton,
    UpdateLogsLineButton,
    UpdateLogsTimeButton
)


class Commands:
    start = StartCommand()  # Used as default command
    list = ListCommand()

    ENABLED_COMMANDS = [
        list
    ]


class Buttons:
    container_start = ContainerStartButton()
    container_stop = ContainerStopButton()
    container_restart = ContainerRestartButton()

    container_compact_view = ContainerCompactViewButton()
    container_detailed_view = ContainerDetailedViewButton()

    container_logs_option = ContainerLogsOptionButton()
    container_list = ContainerListButton()

    time_logs = TimeLogsButton()
    line_logs = LineLogsButton()

    update_logs_time = UpdateLogsTimeButton()
    update_logs_line = UpdateLogsLineButton()

    ENABLED_BUTTONS = [
        container_start,
        container_stop,
        container_restart,
        container_compact_view,
        container_detailed_view,
        container_logs_option,
        container_list,
        time_logs,
        line_logs,
        update_logs_time,
        update_logs_line,
    ]

