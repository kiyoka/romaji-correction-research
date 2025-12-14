"""OpenAI API client for typo correction."""

import time
from openai import OpenAI
from src.config import OPENAI_API_KEY, OPENAI_MODEL


class TypoCorrectionClient:
    """Client for correcting typos using OpenAI API."""

    def __init__(self, model=OPENAI_MODEL):
        """Initialize the client with API key and model."""
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = model

    def correct_typo(self, typo_text: str, prompt_template: str) -> dict:
        """
        Correct a typo using the LLM.

        Args:
            typo_text: The text with typo
            prompt_template: The prompt template to use

        Returns:
            dict with keys: 'corrected', 'response_time', 'error'
        """
        start_time = time.time()

        try:
            # Format the prompt with the typo text
            prompt = prompt_template.format(typo=typo_text)

            # Call OpenAI Responses API with GPT-5.2
            response = self.client.responses.create(
                model=self.model,
                input=[
                    {"role": "user", "content": prompt}
                ],
                reasoning={
                    "effort": "low",      # Match azooKey settings
                    "summary": "concise"  # Match azooKey settings
                }
            )

            # Extract the corrected text from response output
            corrected = ""
            if response.output is not None:
                for item in response.output:
                    # Skip reasoning items (they have content=None)
                    if hasattr(item, "content") and item.content is not None:
                        for content in item.content:
                            if hasattr(content, "text"):
                                corrected += content.text

            corrected = corrected.strip()

            # If no text was extracted, raise an error with response details
            if not corrected:
                error_msg = f"No text extracted from response. Response output: {response.output}"
                raise ValueError(error_msg)

            # Calculate response time
            response_time = time.time() - start_time

            return {
                "corrected": corrected,
                "response_time": response_time,
                "error": None
            }

        except Exception as e:
            response_time = time.time() - start_time
            return {
                "corrected": None,
                "response_time": response_time,
                "error": str(e)
            }
