import pytest
from taskflow.models import Task, TaskStatus, TaskPriority

def test_task_init():
    t = Task("send_email", {"user_id": 123}, priority=TaskPriority.HIGH)
    assert t.name == "send_email"
    assert t.status == TaskStatus.PENDING
    assert t.priority == 10
    assert t.max_retries == 3
