class OutputValidator:

    def validate(self, output, domain, confidence):

        if confidence < 0.55:
            return {
                "type": "uncertain",
                "message": "low confidence detection"
            }

        if domain == "aviation" and "weather" in str(output):
            return {
                "error": "cross_domain_blocked"
            }

        output["validated"] = True
        output["confidence"] = confidence

        return output