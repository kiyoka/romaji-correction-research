import Foundation

/// Prompt templates for typo correction
/// These templates are based on the Python implementation in src/prompts/templates.py
enum PromptTemplate {
    /// Simple prompt template - optimized for speed and accuracy
    static let simple = """
    次のローマ字入力（タイプミスを含む可能性あり）を日本語に変換してください。変換結果のみを返してください。

    入力: {typo}
    日本語:
    """

    /// Alternative simple prompt with more context
    static let simpleV2 = """
    以下はタイプミスを含む可能性があるローマ字入力です。正しい日本語（漢字仮名交じり）に変換してください。
    変換結果のみを出力し、説明は不要です。

    {typo}
    """

    /// Minimal prompt for maximum speed
    static let minimal = "Convert this romaji (may contain typos) to Japanese: {typo}"

    /// QWERTY keyboard aware prompt - mentions keyboard layout
    static let qwertyAware = """
    次のローマ字入力はスマートフォンのQWERTYキーボードで入力されたもので、隣接するキーの誤タップによるタイプミスを含む可能性があります。
    正しい日本語に変換してください。変換結果のみを返してください。

    入力: {typo}
    日本語:
    """

    /// QWERTY keyboard aware prompt V2 - more detailed explanation
    static let qwertyDetailed = """
    以下はスマートフォンのQWERTYキーボードで入力されたローマ字です。
    小さい画面での入力のため、以下のようなタイプミスが含まれる可能性があります：
    - 隣接キーの誤タップ（例: a→s, e→w, i→o）
    - 文字の脱落や重複
    - 文字順序の入れ替え

    タイプミスを修正して、正しい日本語（漢字仮名交じり）に変換してください。変換結果のみを返してください。

    入力: {typo}
    日本語:
    """

    /// QWERTY keyboard aware prompt V3 - concise with keyboard context
    static let qwertyConcise = """
    スマートフォンQWERTYキーボードでの誤入力を含む可能性があるローマ字を、正しい日本語に変換してください。
    変換結果のみを返してください。

    入力: {typo}
    日本語:
    """

    /// Proper noun aware prompt - handles brand names and technical terms correctly
    static let properNounAware = """
    以下の入力を処理してください：
    - 日本語のローマ字入力の場合：タイプミスを修正して日本語（漢字仮名交じり）に変換
    - 企業名・ブランド名・技術用語の場合：正規の英語表記に修正（例：openai→OpenAI, github→GitHub, javascript→JavaScript）

    変換結果のみを返してください。

    入力: {typo}
    出力:
    """

    /// Proper noun aware prompt V2 - more explicit examples
    static let properNounAwareV2 = """
    以下のルールで入力を処理してください：

    1. 日本語のローマ字入力の場合：タイプミスを修正して日本語に変換
       例：arigatou→ありがとう、konichiwa→こんにちは

    2. 固有名詞（企業名・ブランド名・技術用語）の場合：英語の正規表記に修正
       例：openai→OpenAI、github→GitHub、iphone→iPhone、javascript→JavaScript

    変換結果のみを返してください。

    入力: {typo}
    出力:
    """

    /// Proper noun aware prompt V3 - concise with clear distinction
    static let properNounAwareV3 = """
    入力を以下のように処理：
    ・日本語ローマ字→日本語に変換（例：arigatou→ありがとう）
    ・固有名詞→正規の英語表記（例：openai→OpenAI、iphone→iPhone、javascript→JavaScript）

    入力: {typo}
    出力:
    """

    /// Proper noun aware prompt V4 - strict output format with few-shot examples
    static let properNounAwareV4 = """
    入力されたテキストを処理してください。日本語のローマ字は日本語に変換し、企業名・ブランド名・製品名などの固有名詞は正規の英語表記に修正してください。

    重要：結果のみを1行で出力してください。説明や追加情報は一切不要です。

    例：
    入力: sumimasen → 出力: すみません
    入力: ohayou → 出力: おはよう
    入力: gomenasai → 出力: ごめんなさい
    入力: netflix → 出力: Netflix
    入力: spotify → 出力: Spotify
    入力: slack → 出力: Slack

    入力: {typo}
    出力:
    """

    /// Proper noun aware prompt V5 - XML-like structure for clarity (Japanese)
    static let properNounAwareV5 = """
    <task>
    以下の入力を処理してください：
    - 日本語のローマ字表記の場合：日本語（漢字仮名交じり）に変換
    - 英語の固有名詞（企業名・ブランド名・製品名・サービス名など）の場合：正規の英語表記に修正
    - タイポを含む場合：修正した上で適切に処理
    </task>

    <examples>
    arigatou → ありがとう
    openai → OpenAI
    iphone → iPhone
    apple intelligence → Apple Intelligence
    apple intelligenceban → Apple Intelligence
    github → GitHub
    chatgpt → ChatGPT
    </examples>

    <critical>
    必ず結果のみを出力してください。説明や追加のテキストは絶対に含めないでください。
    </critical>

    <input>{typo}</input>
    <output>
    """

    /// Proper noun aware prompt V5 (English) - XML-like structure for clarity
    static let properNounAwareV5English = """
    <task>
    Process the input according to these rules:
    - If it's Japanese romaji: Convert to Japanese (kanji/kana mixed)
    - If it's an English proper noun (company, brand, product, service names): Fix to proper English notation
    - If it contains typos: Fix them and process appropriately
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
    Output ONLY the result. Do NOT include any explanations or additional text.
    </critical>

    <input>{typo}</input>
    <output>
    """

    /// Proper noun aware prompt V6 (English) - Enhanced with QWERTY keyboard typo awareness
    static let properNounAwareV6English = """
    <task>
    Process the input according to these rules:
    1. If it's Japanese romaji (may contain typos): Fix typos and convert to Japanese (kanji/kana mixed)
    2. If it's an English proper noun: Fix to proper English notation
    3. If it contains typos: Fix them considering QWERTY keyboard layout
    </task>

    <qwerty_typo_patterns>
    Common QWERTY keyboard typos on smartphones:
    - Adjacent key substitutions: a↔s, e↔w, i↔o, u↔y, n↔m, etc.
    - Character deletions: missing letters (konichiwa → konnichiwa)
    - Character insertions: doubled letters (arigatouu → arigatou)
    - Transpositions: swapped order (konniciha → konnichiwa)
    </qwerty_typo_patterns>

    <examples>
    Japanese romaji with typos:
    sumimasen → すみません
    sumimsen → すみません (missing a)
    ohayou → おはよう
    phayou → おはよう (o→p substitution)
    oyasumi → おやすみ
    gyasumi → おやすみ (o→g substitution)
    gomenasai → ごめんなさい
    gomwnasai → ごめんなさい (e→w substitution)

    English proper nouns:
    netflix → Netflix
    spotify → Spotify
    slack → Slack
    zoom → Zoom
    notion → Notion
    figma → Figma
    </examples>

    <critical>
    Output ONLY the result. Do NOT include any explanations or additional text.
    Always prioritize Japanese romaji interpretation over random English words.
    </critical>

    <input>{typo}</input>
    <output>
    """

    /// Default prompt to use (V6 with enhanced QWERTY keyboard typo awareness)
    static let `default` = properNounAwareV6English

    /// All available prompts
    static let all: [String: String] = [
        "SIMPLE": simple,
        "SIMPLE_V2": simpleV2,
        "MINIMAL": minimal,
        "QWERTY_AWARE": qwertyAware,
        "QWERTY_DETAILED": qwertyDetailed,
        "QWERTY_CONCISE": qwertyConcise,
        "PROPER_NOUN_AWARE": properNounAware,
        "PROPER_NOUN_AWARE_V2": properNounAwareV2,
        "PROPER_NOUN_AWARE_V3": properNounAwareV3,
        "PROPER_NOUN_AWARE_V4": properNounAwareV4,
        "PROPER_NOUN_AWARE_V5": properNounAwareV5,
        "PROPER_NOUN_AWARE_V5_ENGLISH": properNounAwareV5English,
        "PROPER_NOUN_AWARE_V6_ENGLISH": properNounAwareV6English
    ]
}
