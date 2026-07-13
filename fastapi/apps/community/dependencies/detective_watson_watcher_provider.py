from community.adapter.outbound.repositories.report_intent_escalation_policy import ReportIntentEscalationPolicy
from community.app.ports.input.detective_watson_watcher_use_case import WatsonWatcherUseCase
from community.app.use_cases.detective_watson_watcher_interactor import WatsonWatcherInteractor


def get_watson_watcher_interactor() -> WatsonWatcherUseCase:
    return WatsonWatcherInteractor(escalation_policies=[ReportIntentEscalationPolicy()])
