from app.services.session_store import SessionStore
from app.services.llm_service import LLMService
from app.main import rag_service
from app.services.ollama_provider import clean_markdown
import json



class ChatService:


    def __init__(self):

        print("CHAT SERVICE START")

        self.memory = SessionStore()

        print("MEMORY OK")

        self.llm = LLMService()

        print("LLM OK")

        print("RAG OK")



    # =====================================
    # PROMPT BUILDER
    # =====================================

    def build_prompt(
        self,
        document,
        vision,
        knowledge,
        conversation,
        message
    ):


        # IMAGE MODE
        if vision:


            return f"""

You are a professional technical image analysis assistant.


CURRENT IMAGE ANALYSIS:

{vision}


USER QUESTION:

{message}


IMPORTANT RULES:

- Answer only from the current image analysis.
- Do not use previous documents.
- Do not use previous uploaded files.
- Do not mention RAG or context.
- Do not invent values.
- If numbers are unclear say unclear.
- Use bullet points.
- Give technical explanation.


FINAL ANSWER:

"""



        # NORMAL DOCUMENT MODE


        return f"""

CURRENT DOCUMENT:

{document}


KNOWLEDGE BASE:

{knowledge}


CONVERSATION:

{conversation}


USER QUESTION:

{message}


RULES:

- Give professional technical answer.
- Use Markdown.
- Use bullet points.
- Do not hallucinate.


FINAL ANSWER:

"""





    # =====================================
    # DOCUMENT CONTEXT
    # =====================================

    def build_documents_context(
        self,
        session_id
    ):


        files = self.memory.get_uploaded_files(
            session_id
        )


        if not files:

            return ""


        context=""


        for f in files:


            context += f"""

Filename:
{f['filename']}


Content:

{f.get('content','')}


-------------------------

"""


        return context





    # =====================================
    # VISION CONTEXT
    # =====================================

    def build_vision_context(
        self,
        session_id
    ):


        files = self.memory.get_vision_files(
            session_id
        )


        if not files:

            return ""


        latest = files[-1]


        raw = latest.get(
            "content",
            "{}"
        )


        try:

            data = (

                json.loads(raw)

                if isinstance(raw,str)

                else raw

            )


        except:

            data={}



        return f"""

Filename:
{latest.get('filename')}


Image Type:
{data.get('type','unknown')}


Analysis:

{data.get('analysis','')}


"""





    # =====================================
    # CONVERSATION
    # =====================================

    def build_conversation(
        self,
        session_id
    ):


        history = self.memory.get_history(
            session_id
        )


        conversation=""


        for msg in history[-3:]:


            conversation += (

                f"{msg['role']}: "

                f"{msg['message']}\n"

            )


        return conversation





    # =====================================
    # NORMAL PROCESS
    # =====================================

    def process(
        self,
        session_id:str,
        message:str
    ):


        self.memory.add_message(
            session_id,
            "user",
            message
        )


        vision = self.build_vision_context(
            session_id
        )



        if vision:


            knowledge=""

            sources=[]

            document=""


        else:


            rag_result = rag_service.get_context(

                message,

                session_id=session_id

            )


            knowledge = rag_result["context"]

            sources = rag_result["sources"]


            document = self.build_documents_context(
                session_id
            )



        conversation = self.build_conversation(
            session_id
        )



        prompt = self.build_prompt(

            document,

            vision,

            knowledge,

            conversation,

            message

        )



        response = self.llm.generate(
            prompt
        )


        response = clean_markdown(
            response
        )



        self.memory.add_message(

            session_id,

            "assistant",

            response

        )


        return {


            "response":response,


            "sources":sources,


            "vision_context":vision

        }





    # =====================================
    # STREAM PROCESS
    # =====================================

    def stream_process(
        self,
        session_id:str,
        message:str
    ):


        self.memory.add_message(

            session_id,

            "user",

            message

        )


        vision = self.build_vision_context(
            session_id
        )



        if vision:


            knowledge=""

            sources=[]

            document=""


        else:


            rag_result = rag_service.get_context(

                message,

                session_id=session_id

            )


            knowledge = rag_result["context"]

            sources = rag_result["sources"]


            document = self.build_documents_context(
                session_id
            )



        conversation = self.build_conversation(
            session_id
        )



        print("\nVISION CONTEXT:")
        print(vision)



        prompt = self.build_prompt(

            document,

            vision,

            knowledge,

            conversation,

            message

        )



        full_response=""


        for token in self.llm.stream_generate(prompt):


            full_response += token


            yield token



        full_response = clean_markdown(
            full_response
        )


        self.memory.add_message(

            session_id,

            "assistant",

            full_response

        )