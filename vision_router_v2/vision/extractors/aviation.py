class AviationExtractor:

    def extract(self, image):

        return {
            "type": "density_altitude_chart",
            "domain": "aviation",
            "structured": {
                "temperature_range_c": [-60, 60],
                "density_altitude_ft": [0, 30000],
                "pressure_altitude_ft": [0, 30000]
            },
            "meaning": "Aircraft performance correction chart",
            "relationships": [
                "hotter air → lower density → higher altitude effect"
            ]
        }