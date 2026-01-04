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

    /// Default prompt to use (matches Python implementation)
    static let `default` = properNounAwareV2

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
        "PROPER_NOUN_AWARE_V3": properNounAwareV3
    ]
}
