"""API の入出力スキーマ（Pydantic モデル）。

- TaskCreate: POST /tasks の入力
- TaskUpdate: PUT /tasks/{id} の入力（部分更新。未指定フィールドは変更しない）
- Task: レスポンスとして返す完全なタスク
"""

from datetime import datetime

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)
    done: bool = False


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    done: bool | None = None


class Task(BaseModel):
    id: str
    title: str
    description: str
    done: bool
    created_at: datetime
