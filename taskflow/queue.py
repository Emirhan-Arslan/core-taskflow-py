from abc import ABC, abstractmethod
from typing import Optional, Tuple
import asyncio
from taskflow.models import Task, TaskStatus

class BaseQueue(ABC):
    @abstractmethod
    async def push(self, task: Task) -> None:
        pass

    @abstractmethod
    async def pop(self, timeout: Optional[float] = None) -> Optional[Task]:
        pass

    @abstractmethod
    async def size(self) -> int:
        pass

class MemoryQueue(BaseQueue):
    def __init__(self) -> None:
        self._queue: asyncio.PriorityQueue[Tuple[int, float, Task]] = asyncio.PriorityQueue()

    async def push(self, task: Task) -> None:
        task.status = TaskStatus.QUEUED
        priority_key = -int(task.priority)
        await self._queue.put((priority_key, task.created_at.timestamp(), task))

    async def pop(self, timeout: Optional[float] = None) -> Optional[Task]:
        try:
            if timeout:
                _, _, task = await asyncio.wait_for(self._queue.get(), timeout=timeout)
            else:
                _, _, task = await self._queue.get()
            return task
        except (asyncio.TimeoutError, asyncio.QueueEmpty):
            return None

    async def size(self) -> int:
        return self._queue.qsize()
