"""/tasks の CRUD エンドポイント。

ビジネスロジックが薄いため service 層は挟まず、
ルーターからリポジトリを直接呼ぶ。
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_task_repository
from app.repository import TaskRepository
from app.schemas import Task, TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])

# ルーター全体で使うリポジトリ依存（FastAPI 推奨の Annotated 形式）
RepoDep = Annotated[TaskRepository, Depends(get_task_repository)]


@router.get("", response_model=list[Task])
def list_tasks(repo: RepoDep) -> list[Task]:
    return repo.list()


@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, repo: RepoDep) -> Task:
    return repo.create(payload)


@router.put("/{task_id}", response_model=Task)
def update_task(task_id: str, payload: TaskUpdate, repo: RepoDep) -> Task:
    task = repo.update(task_id, payload)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, repo: RepoDep) -> None:
    if not repo.delete(task_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
