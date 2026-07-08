from __future__ import annotations

import asyncio

from sherlock_homes.app.ports.output.classify_spam_llm_port import ClassifySpamLlmPort


class ExaoneClassifySpamRepository(ClassifySpamLlmPort):

    async def classify_raw(self, *, message: str, system: str) -> str:
        from core.lol.t1_mid_faker_orchestrator import generate_reply_exaone

        return await asyncio.to_thread(generate_reply_exaone, message=message, system=system)
