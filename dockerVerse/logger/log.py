import logging


dv_log = logging.getLogger("dockerVerse")
dv_log.setLevel(logging.INFO)

log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

dv_log_file_handler = logging.FileHandler("dockerVerse.log")
dv_log_file_handler.setFormatter(log_format)

console_log_handler = logging.StreamHandler()
console_log_handler.setFormatter(log_format)

dv_log.addHandler(dv_log_file_handler)
dv_log.addHandler(console_log_handler)


event_log = logging.getLogger("event")
event_log.setLevel(logging.INFO)

event_log_file_handler = logging.FileHandler("event.log")
event_log_file_handler.setFormatter(log_format)

event_log.addHandler(event_log_file_handler)
event_log.addHandler(dv_log_file_handler)
event_log.addHandler(console_log_handler)

