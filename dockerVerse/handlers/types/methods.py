"""
Methods to pass as callback data
"""

"""
Could be anything distinct
"""

class ContainerMethod:
    start = 'START'
    stop = 'STOP'
    restart = 'RESTART'
    view = 'VIEW'
    detailed_view = 'DETAILEDVIEW'
    logs = 'LOGS'


class LogsMethod:
    time_logs = 'GET:TIME'
    line_logs = 'GET:LINE'
    update_time = 'UPDATE:TIME'
    update_line = 'UPDATE:LINE'


class SimpleButtonFormat:
    container_list = 'CONTAINER-LIST'