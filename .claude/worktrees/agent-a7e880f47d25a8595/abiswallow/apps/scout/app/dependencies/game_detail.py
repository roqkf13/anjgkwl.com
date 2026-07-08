"""Game detail — composition root (DIP)."""

from scout.adapter.outbound.file.patch_translation_file_repository import (
    PatchTranslationFileRepository,
)
from scout.adapter.outbound.gemini.gemini_patch_note_translator import (
    GeminiPatchNoteTranslator,
)
from scout.adapter.outbound.http.composite_mod_http_repository import (
    CompositeModHttpRepository,
)
from scout.adapter.outbound.http.steam_news_http_repository import (
    SteamNewsHttpRepository,
)
from scout.adapter.outbound.static.game_detail_static_repository import (
    GameDetailStaticRepository,
)
from scout.app.ports.input.game_detail_use_case import GameDetailUseCase
from scout.app.ports.output.game_detail_repository import GameDetailRepository
from scout.app.ports.output.mod_repository import ModRepository
from scout.app.ports.output.patch_note_translator import PatchNoteTranslator
from scout.app.ports.output.patch_translation_repository import (
    PatchTranslationRepository,
)
from scout.app.ports.output.steam_news_repository import SteamNewsRepository
from scout.app.use_cases.game_detail_interactor import GameDetailInteractor


def get_game_detail_use_case() -> GameDetailUseCase:
    repository: GameDetailRepository = GameDetailStaticRepository()
    steam_news: SteamNewsRepository = SteamNewsHttpRepository()
    translation_store: PatchTranslationRepository = PatchTranslationFileRepository()
    patch_translator: PatchNoteTranslator = GeminiPatchNoteTranslator(
        translation_store
    )
    mod_repository: ModRepository = CompositeModHttpRepository()
    return GameDetailInteractor(
        repository,
        steam_news,
        patch_translator,
        translation_store,
        mod_repository,
    )
