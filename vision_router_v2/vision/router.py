from .classifier import VisionClassifier
from .domain import DomainDetector
from .structure import StructureDetector
from .core.confidence import ConfidenceScorer
from .extractors.aviation import AviationExtractor
from .extractors.chart import ChartExtractor
from .extractors.document import DocumentExtractor

class VisionRouterV2:

    def __init__(self):
        self.cls = VisionClassifier()
        self.domain = DomainDetector()
        self.structure = StructureDetector()
        self.conf = ConfidenceScorer()

        self.aviation = AviationExtractor()
        self.chart = ChartExtractor()
        self.document = DocumentExtractor()

    def process(self, image):

        signals = self.cls.predict(image)

        domain, dscore = self.domain.detect(signals)

        structure = self.structure.detect(signals)

        confidence = self.conf.score(dscore, structure, signals)

        result = self.route(domain, structure, image)

        return {
            "domain": domain,
            "structure": structure,
            "confidence": confidence,
            "data": result
        }

    def route(self, domain, structure, image):

        if domain == "aviation":
            return self.aviation.extract(image)

        if structure == "chart":
            return self.chart.extract(image)

        return self.document.extract(image)