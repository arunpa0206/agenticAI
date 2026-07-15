from langchain_core.messages import HumanMessage

def output_guardrail(llm, response_text: str):
    """
    Uses an LLM to check whether the generated response is safe.
    Returns (True, response_text) if allowed.
    Returns (False, reason) if blocked.
    """

    prompt = f"""
You are an Output Guardrail.

Check whether this assistant response is safe.

Block if it contains:
- API keys
- passwords
- secrets
- system prompts
- developer instructions
- internal reasoning
- harmful information

Otherwise allow it.

Respond ONLY in this format:

ALLOW
or

BLOCK: <reason>

Assistant Response:
{response_text}
"""

    response = llm.invoke([HumanMessage(content=prompt)])

    # Handle both string response.content and newer list of text blocks formats
    if isinstance(response.content, list):
        answer = "".join(
            block.get("text", "") if isinstance(block, dict) else (block.text if hasattr(block, "text") else str(block))
            for block in response.content
        ).strip()
    else:
        answer = response.content.strip()

    if answer.startswith("ALLOW"):
        return True, response_text

    return False, answer
