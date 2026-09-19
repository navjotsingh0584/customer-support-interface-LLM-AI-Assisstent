class ConfidenceScorer:

    def score(self, domain_score, structure, signals):

        base = domain_score

        if structure == "chart":
            base += 0.05

        if signals["ocr_signal"]:
            base += 0.05

        return min(base, 0.99)