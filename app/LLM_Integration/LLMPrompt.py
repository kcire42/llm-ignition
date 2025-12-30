import requests
from LLM_Integration.config import OLLAMA_API_URL, MODEL_NAME , REQUEST_TIMEOUT_SECONDS
from LLMGetInfo.doc.getLLMContext import getdocContext

def getLLMResponse(prompt: str) -> str:
    answer = routeAnswerToLLM(prompt)
    return answer

def routeQuestionToLLM(prompt: str) -> str:
    ROUTER_PROMPT = """
    You are a request router.

    Decide which data source is required to answer the question.

    Allowed routes:
    - RAG_ONLY
    - SQL_ONLY
    - HYBRID

    Rules:
    - Choose ONLY one route
    - Respond ONLY with the route name
    - Do NOT explain anything

    Question:
    {prompt}
    """
    response = callLLM(ROUTER_PROMPT.format(prompt=prompt))
    return response

def routeAnswerToLLM(prompt: str) -> str:
    route = routeQuestionToLLM(prompt)
    if route == "RAG_ONLY":
        return ragAnswerToLLM(prompt)
    elif route == "SQL_ONLY":
        return sqlAnswerToLLM(prompt)
    elif route == "HYBRID":
        return hybridAnswerToLLM(prompt)
    raise ValueError(f"Unknown route: {route}")


def ragAnswerToLLM(prompt: str) -> str:
    docContext = getdocContext(prompt)
    RAGPrompt = f"""
                You are a technical documentation assistant for Ignition Smart Factory.

                STRICT RULES:
                - Answer ONLY with concrete, actionable steps.
                - Use short, clear bullet points.
                - Do NOT explain sections, guides, or assumptions.
                - Do NOT mention document sections or numbers.
                - Do NOT add commentary or meta explanations.
                - Do NOT repeat the question.
                - Do NOT include information not present in the context.

                FORMAT:
                - Start directly with the steps.
                - Maximum 7 steps.
                - Each step must start with an action verb.

                Question:
                {prompt}

                Context:
                {docContext}
                """
    return callLLM(RAGPrompt)

def sqlAnswerToLLM(prompt: str) -> str:
    sqlResults = "Sample SQL data results relevant to the question."
    SQLPrompt = f"""
    You are an industrial data analyst.
    Rules:
    - Use ONLY the provided data
    - Do NOT assume missing values
    - Identify anomalies
    - Suggest corrective actions
    - Be concise and technical

    Measured data:
    {sqlResults}

    User question:
    {prompt}
    """
    return callLLM(SQLPrompt)

def hybridAnswerToLLM(prompt: str) -> str:
    docContext = getdocContext(prompt)
    sqlResults = "Sample SQL data results relevant to the question."
    hybridPrompt = f"""
    You are an industrial data analyst.
    Rules:
    - Use ONLY the provided data
    - Do NOT assume missing values
    - Identify anomalies
    - Suggest corrective actions
    - Be concise and technical

    Operational documentation:
    {docContext}

    Measured data:
    {sqlResults}

    User question:
    {prompt}
    """
    return callLLM(hybridPrompt)


def callLLM(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 250
        }
    }

    response = requests.post(OLLAMA_API_URL, json=payload, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()
    answer = response.json()["response"]
    return answer
