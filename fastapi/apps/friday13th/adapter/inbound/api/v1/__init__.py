from friday13th.adapter.inbound.api.v1.ginny_oauth_router import ginny_router
from friday13th.adapter.inbound.api.v1.jason_login_router import jason_router
from friday13th.adapter.inbound.api.v1.pamela_signup_router import pamela_router

friday13th_v1_routers = [jason_router, pamela_router, ginny_router]
