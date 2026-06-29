from config.settings import ReadinessThresholdsConfig


class HiringReadinessMapper:
    def __init__(self, thresholds: ReadinessThresholdsConfig, critical_risk_cap: str):
        self.thresholds = thresholds
        self.critical_risk_cap = critical_risk_cap

        self.band_rank = {"Highly Ready": 4, "Ready": 3, "Passive": 2, "Unlikely": 1}

    def map_readiness(self, score: float, is_critical_risk: bool) -> str:
        if score >= self.thresholds.highly_ready:
            band = "Highly Ready"
        elif score >= self.thresholds.ready:
            band = "Ready"
        elif score >= self.thresholds.passive:
            band = "Passive"
        else:
            band = "Unlikely"

        if is_critical_risk:
            # Cap the band
            cap_rank = self.band_rank.get(self.critical_risk_cap, 3)
            current_rank = self.band_rank.get(band, 1)

            if current_rank > cap_rank:
                band = self.critical_risk_cap

        return band
