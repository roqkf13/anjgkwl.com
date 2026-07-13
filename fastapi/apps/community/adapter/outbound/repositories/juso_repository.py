from __future__ import annotations

import uuid

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from community.adapter.outbound.orm.contact_orm import ContactOrm
from community.app.dtos.juso_dto import ContactCommand, ContactItem, ContactListResult, ContactUploadResult, JusoQuery, JusoResponse
from community.app.ports.output.juso_port import JusoPort


class JusoRepository(JusoPort):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: JusoQuery) -> JusoResponse:
        return JusoResponse(id=query.id, name=query.name)

    def _build_values(self, commands: list[ContactCommand]) -> list[dict]:
        return [
            {
                "id": str(uuid.uuid4()),
                "first_name": cmd.first_name or None,
                "middle_name": cmd.middle_name or None,
                "last_name": cmd.last_name or None,
                "phonetic_first_name": cmd.phonetic_first_name or None,
                "phonetic_middle_name": cmd.phonetic_middle_name or None,
                "phonetic_last_name": cmd.phonetic_last_name or None,
                "name_prefix": cmd.name_prefix or None,
                "name_suffix": cmd.name_suffix or None,
                "nickname": cmd.nickname or None,
                "file_as": cmd.file_as or None,
                "organization_name": cmd.organization_name or None,
                "organization_title": cmd.organization_title or None,
                "organization_department": cmd.organization_department or None,
                "birthday": cmd.birthday or None,
                "notes": cmd.notes or None,
                "photo": cmd.photo or None,
                "labels": cmd.labels or None,
                "e_mail_1_label": cmd.e_mail_1_label or None,
                "e_mail_1_value": cmd.e_mail_1_value or None,
                "e_mail_2_label": cmd.e_mail_2_label or None,
                "e_mail_2_value": cmd.e_mail_2_value or None,
                "phone_1_label": cmd.phone_1_label or None,
                "phone_1_value": cmd.phone_1_value or None,
            }
            for cmd in commands
        ]

    async def save_contacts(self, commands: list[ContactCommand]) -> ContactUploadResult:
        """A: 전체 삭제 후 재삽입"""
        if not commands:
            return ContactUploadResult(total=0, contacts=[])
        await self.session.execute(delete(ContactOrm))
        stmt = pg_insert(ContactOrm).values(self._build_values(commands))
        await self.session.execute(stmt)
        await self.session.commit()
        return ContactUploadResult(total=len(commands), contacts=list(commands))

    async def upsert_contacts(self, commands: list[ContactCommand]) -> ContactUploadResult:
        """B: 이메일 기준 upsert — 없으면 삽입, 있으면 이름/정보 업데이트"""
        if not commands:
            return ContactUploadResult(total=0, contacts=[])
        update_cols = ["first_name", "middle_name", "last_name", "nickname",
                       "organization_name", "organization_title", "phone_1_value", "labels"]
        stmt = (
            pg_insert(ContactOrm)
            .values(self._build_values(commands))
            .on_conflict_do_update(
                index_elements=["e_mail_1_value"],
                set_={col: pg_insert(ContactOrm).excluded[col] for col in update_cols},
            )
        )
        await self.session.execute(stmt)
        await self.session.commit()
        return ContactUploadResult(total=len(commands), contacts=list(commands))

    async def list_contacts(self) -> ContactListResult:
        result = await self.session.execute(select(ContactOrm).order_by(ContactOrm.first_name))
        rows = result.scalars().all()
        items = [
            ContactItem(
                first_name=r.first_name or "",
                last_name=r.last_name or "",
                nickname=r.nickname or "",
                e_mail_1_value=r.e_mail_1_value or "",
                e_mail_2_value=r.e_mail_2_value or "",
                organization_name=r.organization_name or "",
            )
            for r in rows
        ]
        return ContactListResult(total=len(items), contacts=items)
