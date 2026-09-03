"""ヘルスチェック。将来 ALB / ECS のヘルスチェック先に使う想定なので、
外部依存を持たない軽量なレスポンスにしている。
"""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
