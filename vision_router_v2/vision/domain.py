class DomainDetector:

    def detect(self, signals):

        score = {}

        if "aviation" in signals["clip_labels"]:
            score["aviation"] = 0.9

        if signals["ocr_signal"]:
            score["document"] = 0.6

        if signals["edge_density"] > 0.6:
            score["chart"] = 0.8

        best = max(score, key=score.get)

        return best, score[best]