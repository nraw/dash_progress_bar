#  broker_url = "pyamqp://"
broker_url = "pyamqp://guest@localhost//"
result_backend = "rpc://"

task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
task_track_started = True
timezone = "Europe/Prague"
enable_utc = True
