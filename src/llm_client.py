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

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0,  # Deterministic output for consistency
                max_tokens=50,  # Keep response short for speed
            )

            # Extract the corrected text
            corrected = response.choices[0].message.content.strip()

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
