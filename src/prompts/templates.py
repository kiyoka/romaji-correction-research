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

# Proper noun aware prompt V4 - strict output format with few-shot examples
PROPER_NOUN_AWARE_V4_PROMPT = """入力されたテキストを処理してください。日本語のローマ字は日本語に変換し、企業名・ブランド名・製品名などの固有名詞は正規の英語表記に修正してください。

重要：結果のみを1行で出力してください。説明や追加情報は一切不要です。

例：
入力: sumimasen → 出力: すみません
入力: ohayou → 出力: おはよう
入力: gomenasai → 出力: ごめんなさい
入力: netflix → 出力: Netflix
入力: spotify → 出力: Spotify
入力: slack → 出力: Slack

入力: {typo}
出力:"""

# Proper noun aware prompt V5 - XML-like structure for clarity
PROPER_NOUN_AWARE_V5_PROMPT = """<task>
以下の入力を処理してください：
- 日本語のローマ字表記の場合：日本語（漢字仮名交じり）に変換
- 英語の固有名詞（企業名・ブランド名・製品名・サービス名など）の場合：正規の英語表記に修正
- タイポを含む場合：修正した上で適切に処理
</task>

<examples>
sumimasen → すみません
ohayou → おはよう
gomenasai → ごめんなさい
netflix → Netflix
spotify → Spotify
slack → Slack
zoom → Zoom
</examples>

<critical>
必ず結果のみを出力してください。説明や追加のテキストは絶対に含めないでください。
</critical>

<input>{typo}</input>
<output>"""

# Proper noun aware prompt V6 - Enhanced with QWERTY keyboard typo awareness
PROPER_NOUN_AWARE_V6_PROMPT = """<task>
以下の入力を処理してください：
1. 日本語のローマ字表記（タイポを含む可能性あり）：タイポを修正して日本語（漢字仮名交じり）に変換
2. 英語の固有名詞：正規の英語表記に修正
3. タイポを含む場合：QWERTYキーボード配列を考慮して修正
</task>

<qwerty_typo_patterns>
スマートフォンのQWERTYキーボードで発生しやすいタイポパターン：
- 隣接キーの置換: a↔s, e↔w, i↔o, u↔y, n↔m など
- 文字の脱落: 文字抜け (konichiwa → konnichiwa)
- 文字の挿入: 重複 (arigatouu → arigatou)
- 文字順序の入れ替え: 転置 (konniciha → konnichiwa)
</qwerty_typo_patterns>

<examples>
日本語ローマ字（タイポあり）:
sumimasen → すみません
sumimsen → すみません (a 脱落)
ohayou → おはよう
phayou → おはよう (o→p 置換)
oyasumi → おやすみ
gyasumi → おやすみ (o→g 置換)
gomenasai → ごめんなさい
gomwnasai → ごめんなさい (e→w 置換)

英語固有名詞:
netflix → Netflix
spotify → Spotify
slack → Slack
zoom → Zoom
notion → Notion
figma → Figma
</examples>

<critical>
必ず結果のみを出力してください。説明や追加のテキストは絶対に含めないでください。
常に日本語ローマ字としての解釈を優先し、ランダムな英単語への変換は避けてください。
</critical>

<input>{typo}</input>
<output>"""

# Default prompt to use (V6 with enhanced QWERTY keyboard typo awareness)
DEFAULT_PROMPT = PROPER_NOUN_AWARE_V6_PROMPT

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
    "PROPER_NOUN_AWARE_V4": PROPER_NOUN_AWARE_V4_PROMPT,
    "PROPER_NOUN_AWARE_V5": PROPER_NOUN_AWARE_V5_PROMPT,
    "PROPER_NOUN_AWARE_V6": PROPER_NOUN_AWARE_V6_PROMPT,
}
