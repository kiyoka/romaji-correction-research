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

# QWERTY keyboard aware prompt - mentions keyboard layout
QWERTY_AWARE_PROMPT = """次のローマ字入力はスマートフォンのQWERTYキーボードで入力されたもので、隣接するキーの誤タップによるタイプミスを含む可能性があります。
正しい日本語に変換してください。変換結果のみを返してください。

入力: {typo}
日本語:"""

# QWERTY keyboard aware prompt V2 - more detailed explanation
QWERTY_DETAILED_PROMPT = """以下はスマートフォンのQWERTYキーボードで入力されたローマ字です。
小さい画面での入力のため、以下のようなタイプミスが含まれる可能性があります：
- 隣接キーの誤タップ（例: a→s, e→w, i→o）
- 文字の脱落や重複
- 文字順序の入れ替え

タイプミスを修正して、正しい日本語（漢字仮名交じり）に変換してください。変換結果のみを返してください。

入力: {typo}
日本語:"""

# QWERTY keyboard aware prompt V3 - concise with keyboard context
QWERTY_CONCISE_PROMPT = """スマートフォンQWERTYキーボードでの誤入力を含む可能性があるローマ字を、正しい日本語に変換してください。
変換結果のみを返してください。

入力: {typo}
日本語:"""

# Default prompt to use
DEFAULT_PROMPT = SIMPLE_V2

# All prompts for comparison
ALL_PROMPTS = {
    "SIMPLE": SIMPLE_PROMPT,
    "SIMPLE_V2": SIMPLE_PROMPT_V2,
    "MINIMAL": MINIMAL_PROMPT,
    "QWERTY_AWARE": QWERTY_AWARE_PROMPT,
    "QWERTY_DETAILED": QWERTY_DETAILED_PROMPT,
    "QWERTY_CONCISE": QWERTY_CONCISE_PROMPT,
}
