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

# Proper noun aware prompt - handles brand names and technical terms correctly
PROPER_NOUN_AWARE_PROMPT = """以下の入力を処理してください：
- 日本語のローマ字入力の場合：タイプミスを修正して日本語（漢字仮名交じり）に変換
- 企業名・ブランド名・技術用語の場合：正規の英語表記に修正（例：openai→OpenAI, github→GitHub, javascript→JavaScript）

変換結果のみを返してください。

入力: {typo}
出力:"""

# Proper noun aware prompt V2 - more explicit examples
PROPER_NOUN_AWARE_V2_PROMPT = """以下のルールで入力を処理してください：

1. 日本語のローマ字入力の場合：タイプミスを修正して日本語に変換
   例：arigatou→ありがとう、konichiwa→こんにちは

2. 固有名詞（企業名・ブランド名・技術用語）の場合：英語の正規表記に修正
   例：openai→OpenAI、github→GitHub、iphone→iPhone、javascript→JavaScript

変換結果のみを返してください。

入力: {typo}
出力:"""

# Proper noun aware prompt V3 - concise with clear distinction
PROPER_NOUN_AWARE_V3_PROMPT = """入力を以下のように処理：
・日本語ローマ字→日本語に変換（例：arigatou→ありがとう）
・固有名詞→正規の英語表記（例：openai→OpenAI、iphone→iPhone、javascript→JavaScript）

入力: {typo}
出力:"""

# Default prompt to use
DEFAULT_PROMPT = PROPER_NOUN_AWARE_V2_PROMPT

# All prompts for comparison
ALL_PROMPTS = {
    "SIMPLE": SIMPLE_PROMPT,
    "SIMPLE_V2": SIMPLE_PROMPT_V2,
    "MINIMAL": MINIMAL_PROMPT,
    "QWERTY_AWARE": QWERTY_AWARE_PROMPT,
    "QWERTY_DETAILED": QWERTY_DETAILED_PROMPT,
    "QWERTY_CONCISE": QWERTY_CONCISE_PROMPT,
    "PROPER_NOUN_AWARE": PROPER_NOUN_AWARE_PROMPT,
    "PROPER_NOUN_AWARE_V2": PROPER_NOUN_AWARE_V2_PROMPT,
    "PROPER_NOUN_AWARE_V3": PROPER_NOUN_AWARE_V3_PROMPT,
}
