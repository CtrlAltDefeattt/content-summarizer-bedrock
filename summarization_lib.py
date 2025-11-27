import os
import boto3
from dotenv import load_dotenv
from typing import Literal, Optional

load_dotenv()  # loads .env if present

# You can override region via .env (BEDROCK_REGION),
# otherwise it will use AWS default (from aws configure)
BEDROCK_REGION = os.getenv("BEDROCK_REGION", "us-east-1")

# Use the correct modelId that you have access to in your region.
# Example for Claude 3 Sonnet (update to 3.7 if your account has that id).
DEFAULT_MODEL_ID = os.getenv(
    "BEDROCK_MODEL_ID",
    "anthropic.claude-3-sonnet-20240229-v1:0"  # change to 3.7 ID if needed
)

SummaryStyle = Literal["brief", "detailed", "bullet_points", "executive"]


def get_bedrock_client():
    """
    Returns a Bedrock Runtime client using default AWS credentials.
    """
    session = boto3.Session(region_name=BEDROCK_REGION)
    return session.client(service_name="bedrock-runtime")


def build_prompt(raw_text: str, style: SummaryStyle) -> str:
    """
    Builds an adaptive prompt based on the requested summary style.
    """
    style_instructions = {
        "brief": (
            "Summarize the following content in 3-4 concise sentences. "
            "Focus only on the key ideas."
        ),
        "detailed": (
            "Create a detailed summary (200-300 words). "
            "Capture main arguments, key details, and conclusions."
        ),
        "bullet_points": (
            "Summarize the following content as 5-7 bullet points. "
            "Each bullet should be short and informative."
        ),
        "executive": (
            "Write an executive summary for busy decision-makers. "
            "Highlight key insights, risks, opportunities, and recommendations."
        )
    }

    instruction = style_instructions.get(style, style_instructions["brief"])

    prompt = f"""{instruction}

Content to summarize:
\"\"\"{raw_text}\"\"\""""

    return prompt


def _call_bedrock_converse(message):
    """
    Low-level function: calls Bedrock Converse API with a single message.
    """
    bedrock = get_bedrock_client()

    response = bedrock.converse(
        modelId=DEFAULT_MODEL_ID,
        messages=[message],
        inferenceConfig={
            "maxTokens": 2000,
            "temperature": 0.0
        }
    )

    # Claude 3 response structure: output -> message -> content[0]['text'] :contentReference[oaicite:2]{index=2}
    return response["output"]["message"]["content"][0]["text"]


def summarize_text(
    text: str,
    style: SummaryStyle = "brief"
) -> str:
    """
    Summarize plain text using Claude via Bedrock.
    """
    prompt = build_prompt(text, style)

    message = {
        "role": "user",
        "content": [
            {"text": prompt}
        ]
    }

    return _call_bedrock_converse(message)


def summarize_pdf(
    file_path: str,
    style: SummaryStyle = "brief",
    user_hint: Optional[str] = None
) -> str:
    """
    Summarize a PDF by sending it as a document to Claude.
    Uses Bedrock's document modality.
    """
    with open(file_path, "rb") as f:
        pdf_bytes = f.read()

    base_text = (
        "You are a helpful assistant that summarizes PDF documents.\n"
        "Read the attached PDF and generate a summary in the requested style.\n"
    )

    if user_hint:
        base_text += f"\nUser hint / context: {user_hint}\n"

    prompt = build_prompt("The content is in the attached PDF document.", style)
    full_text = base_text + "\n" + prompt

    message = {
        "role": "user",
        "content": [
            {
                "document": {
                    "name": "uploaded.pdf",
                    "format": "pdf",
                    "source": {"bytes": pdf_bytes}
                }
            },
            {"text": full_text}
        ]
    }

    return _call_bedrock_converse(message)
