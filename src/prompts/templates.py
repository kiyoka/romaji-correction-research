"""Prompt templates for typo correction."""

# Simple prompt template - optimized for speed and accuracy
SIMPLE_PROMPT = """次のローマ字入力のタイプミスを修正してください。修正結果のみを返してください。

入力: {typo}
修正:"""

# Alternative simple prompt with more context
SIMPLE_PROMPT_V2 = """以下は日本語ローマ字入力時のタイプミスです。正しいローマ字に修正してください。
修正結果のみを出力し、説明は不要です。

{typo}"""

# Minimal prompt for maximum speed
MINIMAL_PROMPT = """Correct this Japanese romaji typo: {typo}"""

# Default prompt to use
DEFAULT_PROMPT = SIMPLE_PROMPT
