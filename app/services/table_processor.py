import pandas as pd
from app.services.rag_service import RAGService


class TableProcessor:

    def __init__(self):

        self.rag = RAGService()

        print("[TABLE PROCESSOR READY]")


    # =========================
    # MAIN ENTRY
    # =========================
    def process(self, path: str):

        if path.endswith(".csv"):
            df = pd.read_csv(path)
        else:
            df = pd.read_excel(path)

        # 1. Convert to semantic text
        semantic_text = self._convert_to_semantic_text(df)

        # 2. Store in RAG
        self.rag.add_text(
            text=semantic_text,
            source=path,
            doc_type="table"
        )

        return {
            "status": "ingested",
            "rows": len(df),
            "columns": list(df.columns),
            "preview": semantic_text[:500]
        }


    # =========================
    # CORE IMPROVEMENT: SEMANTIC CONVERSION
    # =========================
    def _convert_to_semantic_text(self, df: pd.DataFrame):

        sentences = []

        columns = list(df.columns)

        # Try to detect meaningful row structure
        for _, row in df.iterrows():

            row_sentences = []

            for col in columns:

                value = row[col]

                if pd.isna(value):
                    continue

                # Clean value
                value = str(value).strip()

                if value == "":
                    continue

                # Build natural language sentence
                row_sentences.append(f"{col} is {value}")

            if row_sentences:
                sentences.append(". ".join(row_sentences) + ".")

        return "\n".join(sentences)