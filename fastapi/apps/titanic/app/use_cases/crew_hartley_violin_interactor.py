from __future__ import annotations

import io

import matplotlib
matplotlib.use("Agg")  # GUI 팝업 방지 — pyplot import 전에 설정해야 한다
import matplotlib.pyplot as plt
import seaborn as sns
from pandas import DataFrame

from titanic.adapter.inbound.api.schemas.crew_hartley_violin_schema import HartleyViolinSchema
from titanic.app.dtos.crew_hartley_violin_dto import HartleyViolinQuery, HartleyViolinResponse
from titanic.app.ports.input.crew_hartley_violin_use_case import HartleyViolinUseCase
from titanic.app.ports.output.crew_hartley_violin_port import HartleyViolinPort


def _fig_to_png(fig: plt.Figure) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    data = buf.getvalue()
    plt.close(fig)
    return data


class HartleyViolinInteractor(HartleyViolinUseCase):

    def __init__(self, repository: HartleyViolinPort):
        self.repository = repository

    def generate_correlation_heatmap(self, df: DataFrame) -> bytes:
        """수치형 피처 간 상관관계 히트맵을 PNG 바이트로 반환한다."""
        numeric_df = df.select_dtypes(include=["number"])
        corr = numeric_df.corr()

        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
        ax.set_title("Titanic Feature Correlation")
        return _fig_to_png(fig)

    def _encode_all_vos(self, df: DataFrame) -> DataFrame:
        """상관관계 기반으로 선별된 5개 VO를 수치 인코딩한다."""
        import pandas as pd
        from titanic.domain.value_objects.cabin_vo import CabinAssigned
        from titanic.domain.value_objects.embarked_vo import Embarked, PortType
        from titanic.domain.value_objects.passenger_identity_vo import PassengerIdentity
        from titanic.domain.value_objects.socioeconomic_vo import SocioeconomicStatus

        _port_ord = {
            PortType.CHERBOURG: 1, PortType.QUEENSTOWN: 2, PortType.SOUTHAMPTON: 3,
        }

        def _embarked(v):
            try:
                return _port_ord[Embarked.from_raw(str(v)).value] if v and str(v).strip() else None
            except ValueError:
                return None

        enc = pd.DataFrame()
        enc["survived"] = pd.to_numeric(df["survived"], errors="coerce")                 # survived_vo

        # PassengerIdentity (Embedded: Gender + Title)
        identity = df.apply(
            lambda r: PassengerIdentity.from_raw(str(r["name"]), str(r["gender"])), axis=1
        )
        enc["gender"] = identity.map(lambda i: i.gender_encoded)
        enc["title"]  = identity.map(lambda i: i.title_ordinal)

        # SocioeconomicStatus (Embedded: PClass + Fare)
        def _socioeconomic(r):
            try:
                return SocioeconomicStatus.from_raw(int(r["pclass"]), float(r["fare"]))
            except (ValueError, TypeError):
                return None
        socio = df.apply(_socioeconomic, axis=1)
        enc["pclass"] = socio.map(lambda s: s.pclass_encoded if s else None)
        enc["fare"]   = socio.map(lambda s: s.fare_value if s else None)

        # CabinAssigned  (cabin_vo)
        enc["cabin_assigned"] = df["cabin"].apply(
            lambda v: CabinAssigned.from_cabin(v).as_feature
        )

        # Embarked  (embarked_vo)
        enc["embarked"] = df["embarked"].apply(_embarked)

        return enc

    def generate_survival_charts(self, df: DataFrame) -> bytes:
        """11개 VO 인코딩 후 survived와의 상관계수를 높은 순으로 정렬하여 반환한다."""
        import pandas as pd

        enc = self._encode_all_vos(df)

        if enc["survived"].isna().all():
            raise ValueError("DataFrame에 유효한 'survived' 값이 없습니다.")

        corr: pd.Series = (
            enc.corr()["survived"]
            .drop("survived")
            .dropna()
            .sort_values(key=abs, ascending=True)   # barh 는 아래→위 순서
        )

        colors = ["#e74c3c" if v > 0 else "#4a90d9" for v in corr.values]

        fig, ax = plt.subplots(figsize=(11, max(5, len(corr) * 0.52)))
        bars = ax.barh(corr.index, corr.values, color=colors, edgecolor="white", height=0.6)

        for bar, val in zip(bars, corr.values):
            offset = 0.013 if val >= 0 else -0.013
            ha = "left" if val >= 0 else "right"
            ax.text(val + offset, bar.get_y() + bar.get_height() / 2,
                    f"{val:+.3f}", va="center", ha=ha, fontsize=9, fontweight="bold")

        ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
        ax.set_xlim(-1.15, 1.15)
        ax.set_xlabel("Correlation Coefficient with Survived", fontsize=11)
        ax.set_title(
            "Feature Correlation with Survived  (5 Value Objects, ranked by |r|)",
            fontsize=12, pad=14,
        )
        ax.tick_params(axis="y", labelsize=10)

        from matplotlib.patches import Patch
        ax.legend(
            handles=[Patch(color="#e74c3c", label="positive (+)"),
                     Patch(color="#4a90d9", label="negative (−)")],
            loc="lower right", fontsize=9,
        )

        plt.tight_layout()
        return _fig_to_png(fig)

    def generate_fare_distribution(self, df: DataFrame) -> bytes:
        """운임 분포 히스토그램 + FareBin 경계선을 PNG 바이트로 반환한다."""
        import pandas as pd
        from titanic.domain.value_objects.socioeconomic_vo import FareBinType

        fare = pd.to_numeric(df["fare"], errors="coerce").dropna()

        _cutpoints = [7.91, 14.45, 31.0]
        _labels = ["VERY_LOW\n(< 7.91)", "LOW\n(7.91–14.45)", "MEDIUM\n(14.45–31.0)", "HIGH\n(≥ 31.0)"]
        _colors = ["#4a90d9", "#5dade2", "#f39c12", "#e74c3c"]

        fig, ax = plt.subplots(figsize=(11, 5))

        ax.hist(fare, bins=60, color="#95a5a6", edgecolor="white", alpha=0.8)

        boundaries = [0.0] + _cutpoints + [fare.max()]
        for i, (lo, hi) in enumerate(zip(boundaries, boundaries[1:])):
            ax.axvspan(lo, hi, alpha=0.08, color=_colors[i])
            mid = (lo + hi) / 2
            ax.text(mid, ax.get_ylim()[1] * 0.92, _labels[i],
                    ha="center", va="top", fontsize=8, color=_colors[i], fontweight="bold")

        for cut in _cutpoints:
            ax.axvline(cut, color="black", linewidth=1.2, linestyle="--", alpha=0.7)
            ax.text(cut + 0.4, ax.get_ylim()[1] * 0.98, f"{cut}", fontsize=8, va="top", alpha=0.8)

        ax.set_xlim(0, fare.quantile(0.99))
        ax.set_xlabel("Fare", fontsize=11)
        ax.set_ylabel("Count", fontsize=11)
        ax.set_title("Fare Distribution  (FareBin cutpoints: Kaggle quartiles)", fontsize=12, pad=14)

        plt.tight_layout()
        return _fig_to_png(fig)

    async def introduce_myself(self, schema: HartleyViolinSchema) -> HartleyViolinResponse:
        '''하틀리 바이올린의 자기소개 인터렉트'''
        return await self.repository.introduce_myself(HartleyViolinQuery(
            id=schema.id,
            name=schema.name,
        ))
