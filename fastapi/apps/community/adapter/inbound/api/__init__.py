from fastapi import APIRouter

from community.adapter.inbound.api.v1.telegram_router import telegram_router
from community.adapter.inbound.api.v1.juso_router import juso_router
from community.adapter.inbound.api.v1.discord_router import discord_router
from community.adapter.inbound.api.v1.detective_watson_executor_router import watson_executor_router
from community.adapter.inbound.api.v1.received_email_router import received_email_router
from community.adapter.inbound.api.v1.classify_spam_router import classify_spam_router

community_router = APIRouter(prefix="/community", tags=["community"])
community_router.include_router(telegram_router)
community_router.include_router(juso_router)
community_router.include_router(discord_router)
community_router.include_router(watson_executor_router)
community_router.include_router(received_email_router)
community_router.include_router(classify_spam_router)
