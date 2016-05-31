from __future__ import absolute_import

__author__ = 'patrizio'

from testagent.services.rest import events, tasks

handlers = [
    (r"/tasks", tasks.ListTasks),
    (r"/task/info/(.*)", tasks.TaskInfo),
    (r"/task/result/(.+)", tasks.TaskResult),
    (r"/task/events/task-sent/(.*)", events.TaskSent),
    (r"/task/events/task-received/(.*)", events.TaskReceived),
    (r"/task/events/task-started/(.*)", events.TaskStarted),
    (r"/task/events/task-succeeded/(.*)", events.TaskSucceeded),
    (r"/task/events/task-failed/(.*)", events.TaskFailed),
    (r"/task/events/task-revoked/(.*)", events.TaskRevoked),
    (r"/task/events/task-retried/(.*)", events.TaskRetried),
]