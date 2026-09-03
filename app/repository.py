"""タスクの永続化層。

TaskRepository はインターフェース（抽象基底クラス）。
InMemoryTaskRepository はプロセスのメモリ上に保持する実装。

将来 DB を使う場合は、同じインターフェースを実装した
SqlTaskRepository などを追加し、dependencies.py の注入先を差し替えるだけでよい。
"""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from uuid import uuid4

from app.schemas import Task, TaskCreate, TaskUpdate


class TaskRepository(ABC):
    @abstractmethod
    def list(self) -> list[Task]: ...

    @abstractmethod
    def get(self, task_id: str) -> Task | None: ...

    @abstractmethod
    def create(self, data: TaskCreate) -> Task: ...

    @abstractmethod
    def update(self, task_id: str, data: TaskUpdate) -> Task | None: ...

    @abstractmethod
    def delete(self, task_id: str) -> bool: ...


class InMemoryTaskRepository(TaskRepository):
    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}

    def list(self) -> list[Task]:
        return sorted(self._tasks.values(), key=lambda t: t.created_at)

    def get(self, task_id: str) -> Task | None:
        return self._tasks.get(task_id)

    def create(self, data: TaskCreate) -> Task:
        task = Task(
            id=str(uuid4()),
            title=data.title,
            description=data.description,
            done=data.done,
            created_at=datetime.now(timezone.utc),
        )
        self._tasks[task.id] = task
        return task

    def update(self, task_id: str, data: TaskUpdate) -> Task | None:
        task = self._tasks.get(task_id)
        if task is None:
            return None
        updated = task.model_copy(update=data.model_dump(exclude_unset=True))
        self._tasks[task_id] = updated
        return updated

    def delete(self, task_id: str) -> bool:
        return self._tasks.pop(task_id, None) is not None
