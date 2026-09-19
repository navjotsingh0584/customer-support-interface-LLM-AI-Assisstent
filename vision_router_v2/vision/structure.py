class StructureDetector:

    def detect(self, signals):

        if "chart" in signals["clip_labels"]:
            return "chart"

        if signals["ocr_signal"]:
            return "document"

        return "unknown"