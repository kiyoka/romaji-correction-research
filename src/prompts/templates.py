"""Prompt templates for typo correction."""

# Simple prompt template - optimized for speed and accuracy
SIMPLE_PROMPT = """次のローマ字入力（タイプミスを含む可能性あり）を日本語に変換してください。変換結果のみを返してください。

入力: {typo}
日本語:"""

# Alternative simple prompt with more context
SIMPLE_PROMPT_V2 = """以下はタイプミスを含む可能性があるローマ字入力です。正しい日本語（漢字仮名交じり）に変換してください。
変換結果のみを出力し、説明は不要です。

{typo}"""

# Minimal prompt for maximum speed
MINIMAL_PROMPT = """Convert this romaji (may contain typos) to Japanese: {typo}"""

# Default prompt to use
DEFAULT_PROMPT = SIMPLE_PROMPT
