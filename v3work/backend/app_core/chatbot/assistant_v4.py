from chatbot.gemini_chat_v4 import ask_gemini
from chatbot.tools import SIF_TOOLS
import traceback


def answer_question(question, chat=None, language="English"):

    if not question or not question.strip():
        return "Please enter a question.", chat

    try:
        answer, chat = ask_gemini(
            question,
            SIF_TOOLS,
            chat,
            language=language
        )

        return answer, chat

    except Exception as e:

        print("\n========== GEMINI ERROR ==========")
        print(repr(e))
        traceback.print_exc()
        print("==================================\n")

        return (
            "I’m temporarily unable to process that request. "
            "Check the terminal for the actual error."
        ), chat