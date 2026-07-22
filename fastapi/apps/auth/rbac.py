"""Role 자체는 core.security에 있다. 다른 앱들이 RoleChecker(core.dependencies)를 쓰려면
Role을 참조해야 하는데, auth-isolation 계약상 apps.auth는 다른 앱이 import할 수 없기
때문에 core로 옮겨뒀다. 이 모듈은 auth 게이트웨이 내부에서만 쓰는 세부 권한(Permission)을 담당한다.
"""

from __future__ import annotations

from enum import Enum

from core.security import Role

__all__ = ["Role", "Permission", "ROLE_PERMISSIONS", "has_permission"]


class Permission(str, Enum):
    """세부 권한. Role보다 더 촘촘한 단위가 필요할 때 쓴다."""

    VIEW_ADMIN_DASHBOARD = "view_admin_dashboard"
    MANAGE_USERS = "manage_users"


ROLE_PERMISSIONS: dict[Role, set[Permission]] = {
    Role.USER: set(),
    Role.ADMIN: {Permission.VIEW_ADMIN_DASHBOARD, Permission.MANAGE_USERS},
}


def has_permission(roles: list[str], permission: Permission) -> bool:
    for role_value in roles:
        try:
            role = Role(role_value)
        except ValueError:
            continue
        if permission in ROLE_PERMISSIONS.get(role, set()):
            return True
    return False
