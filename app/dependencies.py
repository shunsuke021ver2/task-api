"""FastAPI の依存性注入（Depends）用のプロバイダ。

ルーターは get_task_repository() 経由でリポジトリを受け取るため、
「実装が何か」を知らない。テストでは app.dependency_overrides で差し替える。
"""

from app.repository import InMemoryTaskRepository, TaskRepository

# アプリ起動中は 1 つのインスタンスを共有する（メモリ実装なのでこれが保存先）
_repository: TaskRepository = InMemoryTaskRepository()


def get_task_repository() -> TaskRepository:
    return _repository
