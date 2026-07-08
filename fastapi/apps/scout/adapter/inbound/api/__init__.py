from scout.adapter.inbound.api.v1.game_detail_router import game_detail_router
from scout.adapter.inbound.api.v1.metroidvania_router import metroidvania_router
from scout.adapter.inbound.api.v1.openworld_router import openworld_router
from scout.adapter.inbound.api.v1.roguelike_router import roguelike_router
from scout.adapter.inbound.api.v1.scout_director_router import scout_director_router
from scout.adapter.inbound.api.v1.scout_game_router import scout_game_router
from scout.adapter.inbound.api.v1.scout_genre_router import scout_genre_router
from scout.adapter.inbound.api.v1.scout_mod_router import scout_mod_router
from scout.adapter.inbound.api.v1.scout_patch_note_router import scout_patch_note_router
from scout.adapter.inbound.api.v1.scout_related_video_router import scout_related_video_router
from scout.adapter.inbound.api.v1.soulslike_router import soulslike_router

scout_routers = [
    scout_director_router,
    game_detail_router,
    soulslike_router,
    roguelike_router,
    openworld_router,
    metroidvania_router,
    scout_game_router,
    scout_genre_router,
    scout_mod_router,
    scout_patch_note_router,
    scout_related_video_router,
]
