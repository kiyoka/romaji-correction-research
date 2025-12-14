

本リポジトリはLLMを使って、iPhoneなどの小さいデバイス上のQWERTYキーボードでタイプミスしがちなケースを自動修正するにはどのようなプロンプトが適切かを調べるためのものです。
実際に発生しそうなタイプミスの事例を集めて、それを修正するためのプロンプトを最適化していきます。

---

## ローマ字タイプミス自動修正プロンプト最適化 計画案

### フェーズ1: タイプミスパターンの収集と分類

**1.1 QWERTYキーボードの特性分析**
- 隣接キーの誤入力パターンの特定（例: `a` → `s`, `o` → `p`）
- 小さい画面での親指タイピング特有のミス（例: スペースキー周辺の誤タップ）
- 日本語ローマ字入力に特化したミスパターン

#### ネットから収集した情報

**QWERTYキーボードの隣接キーエラーパターン**
- 最もミスしやすい文字: S, D, R, E, I（キーボード中央に位置し隣接キーが多い）
- 最もミスしにくい文字: Q, Z, J, X, Y, V（角やキーボード端に位置）
- 中央のキー（例: D）は8つの隣接キーがあり、角のキー（例: Q）は3つしかない

**タイプミスの4分類（学術的分類）**
- Insertion（挿入）: 余分な文字が入る
- Deletion（削除）: 文字が抜ける
- Substitution（置換）: 隣接キーを誤って押す
- Transposition（転置）: 文字の順序が入れ替わる（例: `teh` → `the`）

**スマートフォン特有の問題**
- 小さい画面では親指で正確にキーを押すのが難しい
- 予測変換・自動修正が補完している（例: `thwre` → `there`）
- タイピング速度が速いほどミスが増える傾向

**日本語フリック入力の特性**
- 「あ行」と「ら行」は離れているため混同しにくい
- キーボードサイズや感度調整でミスを軽減可能

**参考資料:**
- [Sloppy Typing - DataGenetics](http://datagenetics.com/blog/november42012/index.html)
- [From QWERTY to Oops: Common Keyboard Typing Errors Explained](https://fastercapital.com/content/From-QWERTY-to-Oops--Common-Keyboard-Typing-Errors-Explained.html)
- [KEYBOARD PATTERNS FOR SPELLING DETECTION (PDF)](https://portal.scitech.au.edu/kwankamol/wp-content/uploads/2017/07/Keyboard-Patterns-Maria.pdf)
- [A Study of Variations of Qwerty Soft Keyboards for Mobile Phones](https://www.yorku.ca/mack/mhci2013g.html)
- [フリック入力 - Wikipedia](https://ja.wikipedia.org/wiki/フリック入力)

**1.2 タイプミス事例データベースの作成**
- 一般的なタイプミス事例を収集（手動・調査ベース）
- カテゴリ分け：
  - 隣接キー入力ミス
  - 文字の重複・脱落
  - 順序入れ替え（`teh` → `the` 的なもの）
  - 長音・促音の入力ミス

#### タイプミス具体例データ(実データ)

| タイプミス     | 正解の入力      | 正解日本語       | azookeyの結果(修正機能なし) | 説明         |
|----------------|-----------------|------------------|-----------------------------|--------------|
| kanselshimazu  | kyanserushimasu | キャンセルします | カンセル島ず                | s→z,y抜け    |
| sousimazu      | sousimasu       | そうします       | 創始まず                    | s→z          |
| roukaidesu     | ryoukaidesu     | 了解です         | ろうかいです                | y抜け        |
| okdesu         | okkeidesu       | OKです           | おkです                     | 省略した入力 |
| daijyobudesu   | daijyoubudesu   | 大丈夫です       | だいじょぶです              | u抜け        |
| gwnnki         | genki           | 元気             | gwんき                      | e→w          |
| mattetekudadai | mattetekudasai  | 待っててください | 待っててくだだい            | s→d          |
| shinkanswn     | shinkansen      | 新幹線           | 新刊swn                     | s→d          |

#### タイプミス具体例データ(仮想データ、下のOpus 4.5によるものから作成)

| タイプミス    | 正解の入力    | 正解日本語   | azookeyの結果(修正機能無し) | 説明           |
|---------------|---------------|--------------|---------------------------|----------------|
| srigatou      | arigatou      | ありがとう   | サリが当                    | a→s            |
| arigatoi      | arigatou      | ありがとう   | ありがとい                  | u→i            |
| kawsii        | kawaii        | かわいい     | かwしい                     | a→s            |
| onegiashimasu | onegaishimasu | お願いします | おねぎあします              | 文字順入れ替え |
| konichiwa     | konnichiwa    | こんにちは   | こにちわ                    | n脱落          |
| arigatouu     | arigatou      | ありがとう   | ありがとうう                | u重複          |
| konniciha     | konnichiwa    | こんにちは   | 今イチは                  | h-i入れ替え    |
| srigtou       | arigatou      | ありがとう   | sリg等                     | a→s + a脱落    |
| tanoshu       | tanoshii      | たのしい     | たのしゅ                    | i→u            |
| gwnki         | genki         | げんき       | gwんき                      | e→w            |

上記の表をタイプミス仮想データ(Claude Opus 4.5による)からいくつかサンプルを取得して追記してください。

#### タイプミス仮想データ(Claude Opus 4.5による生成)

**カテゴリ1: Substitution（置換）- 隣接キー誤入力**

| タイプミス | 正解 | 日本語 | 誤入力キー | 説明 |
|-----------|------|--------|-----------|------|
| srigatou | arigatou | ありがとう | a→s | A-S隣接 |
| arigatoi | arigatou | ありがとう | u→i | U-I隣接 |
| konnichiwq | konnichiwa | こんにちは | a→q | A-Q隣接 |
| ohaypi | ohayou | おはよう | o→p | O-P隣接 |
| tanoshu | tanoshii | たのしい | i→u | I-U隣接 |
| sugpi | sugoi | すごい | o→p | O-P隣接 |
| kawsii | kawaii | かわいい | a→s | A-S隣接 |
| oishoo | oishii | おいしい | i→o | I-O隣接 |
| genki desu | genki desu | 元気です | (正解例) | - |
| gwnki | genki | げんき | e→w | E-W隣接 |
| samio | samui | さむい | u→o | U-O隣接 |
| atsuo | atsui | あつい | i→o | I-O隣接 |
| hayso | hayai | はやい | a→s | A-S隣接 |
| ospo | osoi | おそい | i→p | I-P隣接 (やや遠い) |
| tsukqrete | tsukarete | つかれて | a→q | A-Q隣接 |
| nemio | nemui | ねむい | u→o | U-O隣接 |

**カテゴリ2: Deletion（削除）- 文字脱落**

| タイプミス | 正解 | 日本語 | 説明 |
|-----------|------|--------|------|
| arigtou | arigatou | ありがとう | a脱落 |
| konichiwa | konnichiwa | こんにちは | n脱落 |
| tanshii | tanoshii | たのしい | o脱落 |
| kawai | kawaii | かわいい | i脱落 |
| oishi | oishii | おいしい | i脱落 |
| geki | genki | げんき | n脱落 |
| tsukaete | tsukarete | つかれて | r脱落 |
| wakarimshta | wakarimashita | わかりました | a脱落 |
| yorshiku | yoroshiku | よろしく | o脱落 |
| omedetou | omedetou | おめでとう | (正解例) |
| omedtou | omedetou | おめでとう | e脱落 |

**カテゴリ3: Insertion（挿入）- 余分な文字**

| タイプミス | 正解 | 日本語 | 説明 |
|-----------|------|--------|------|
| arigatouu | arigatou | ありがとう | u重複 |
| konnnichiwa | konnichiwa | こんにちは | n重複 |
| tanoshiii | tanoshii | たのしい | i重複 |
| kawaiii | kawaii | かわいい | i重複 |
| oiishii | oishii | おいしい | i重複 |
| genkii | genki | げんき | i追加 |
| hayaai | hayai | はやい | a重複 |
| sugooi | sugoi | すごい | o重複 |
| samuui | samui | さむい | u重複 |
| atsuui | atsui | あつい | u重複 |

**カテゴリ4: Transposition（転置）- 文字順序入れ替え**

| タイプミス | 正解 | 日本語 | 説明 |
|-----------|------|--------|------|
| arigatuo | arigatou | ありがとう | o-u入れ替え |
| konniciha | konnichiwa | こんにちは | h-i入れ替え |
| taonshii | tanoshii | たのしい | n-o入れ替え |
| kaawii | kawaii | かわいい | w-a入れ替え |
| oihsii | oishii | おいしい | s-h入れ替え |
| geinki | genki | げんき | n-e入れ替え |
| hayia | hayai | はやい | a-i入れ替え |
| sugoi | sugoi | すごい | (正解例) |
| sugio | sugoi | すごい | o-i入れ替え |
| samiu | samui | さむい | u-i入れ替え |

**カテゴリ5: 複合エラー**

| タイプミス | 正解 | 日本語 | 説明 |
|-----------|------|--------|------|
| srigtou | arigatou | ありがとう | a→s + a脱落 |
| konnichiwq | konnichiwa | こんにちは | a→q |
| tanosgii | tanoshii | たのしい | h→g + 順序 |
| wakarimshta | wakarimashita | わかりました | a脱落 |
| yoroshikuu | yoroshiku | よろしく | u重複 |

> **注意: 上記のタイプミス具体例は論文から引用したものではありません。**
>
> Claude（AI）が以下の原則に基づいて生成した**仮想データ**です：
> 1. QWERTYキーボードの物理的配列に基づく隣接キーの関係
> 2. 収集した学術的分類（Insertion, Deletion, Substitution, Transposition）
> 3. 一般的な日本語表現のローマ字表記
>
> **実際の研究で使用する場合は、以下のアプローチを検討してください：**
> - 実際のユーザー入力ログから収集したデータを使用
> - 既存の研究論文からのデータセット引用
> - クラウドソーシングによるタイプミスデータ収集
> - 公開されているタイプミスコーパスの活用

#### 公開されている実際のタイプミスデータセット

**大規模・多言語データセット**

| データセット | 規模 | 特徴 | リンク |
|-------------|------|------|--------|
| GitHub Typo Corpus | 350k+ 編集、65M文字、15言語以上 | 最大規模のタイプミスデータセット。GitHubのコミットから収集 | [GitHub](https://github.com/mhagiwara/github-typo-corpus) / [論文](https://aclanthology.org/2020.lrec-1.835/) |
| Google TSI Dataset | 43,735例 | モバイルタッチスクリーンのタップデータ。挿入・省略・置換・転置エラーを含む | [GitHub](https://github.com/google-research-datasets/tap-typing-with-touch-sensing-images) |
| 136 Million Keystrokes | 1.36億キーストローク | 大規模キーストロークデータ（Aalto大学） | [データ](http://userinterfaces.aalto.fi/136Mkeystrokes) |

**ベンチマークデータセット**

| データセット | 規模 | 用途 | リンク |
|-------------|------|------|--------|
| TOEFL-Spell | 6,121スペルエラー | 英語学習者のエッセイから収集した実際のミススペル | [論文](https://aclanthology.org/W19-4407/) |
| CoNLL-2014 | 1,312文 | 文法エラー訂正の標準ベンチマーク | [NLP-progress](http://nlpprogress.com/english/grammatical_error_correction.html) |
| BEA 2019 | 4,477文 | 非ネイティブ英語学習者の作文 | [NLP-progress](http://nlpprogress.com/english/grammatical_error_correction.html) |
| Kaggle Spelling | 多数 | スペル訂正用データ | [Kaggle](https://www.kaggle.com/datasets/bittlingmayer/spelling) |

**ツールキット・リソース**

| リソース | 説明 | リンク |
|---------|------|--------|
| NeuSpell | 10種類のスペル訂正モデルとベンチマーク | [GitHub](https://github.com/neuspell/neuspell) |
| Papers with Code | スペル訂正タスクのまとめ | [リンク](https://paperswithcode.com/task/spelling-correction) |

**日本語関連リソース**

| リソース | 説明 | リンク |
|---------|------|--------|
| 国立国語研究所 | 各種日本語コーパス | [リンク](https://www.ninjal.ac.jp/resources/) |
| BCCWJ | 現代日本語書き言葉均衡コーパス（1億430万語） | [リンク](https://clrd.ninjal.ac.jp/bccwj/) |

#### GitHub Typo Corpus 分析結果

GitHub Typo Corpusをダウンロードして分析した結果：

**言語別データ件数（上位10言語）**

| 言語 | 件数 |
|------|------|
| 英語 (eng) | 678,860 |
| 簡体中国語 (cmn-hans) | 7,982 |
| **日本語 (jpn)** | **3,432** |
| ロシア語 (rus) | 3,200 |
| フランス語 (fra) | 2,260 |
| ドイツ語 (deu) | 1,400 |
| ポルトガル語 (por) | 1,280 |
| スペイン語 (spa) | 1,156 |
| 韓国語 (kor) | 884 |
| ポーランド語 (pol) | 464 |

**日本語タイプミスの具体例**

| 誤 | 正 | エラータイプ |
|----|----|----|
| デフォルトととして | デフォルトとして | 文字重複 |
| ヒーロを | ヒーローを | 長音脱落 |
| 適応する | 適用する | 漢字間違い |
| 絶体URL | 絶対URL | 漢字間違い |
| レクエスト | リクエスト | カタカナ誤り |
| formGroup 使って | formGroup を使って | 助詞脱落 |
| `undfinede` | `undefined` | 英単語スペルミス |
| `touthed` | `touched` | 英単語スペルミス |
| `text.ts` | `test.ts` | 英単語スペルミス |

> **重要な発見**: GitHub Typo Corpusの日本語データは「変換後の日本語テキスト」のタイプミスであり、**ローマ字入力時のタイプミスではない**。本研究の目的（ローマ字入力のタイプミス修正）には直接使用できないが、参考にはなる。

> **結論**: 日本語ローマ字入力に特化したタイプミスデータセットは現時点で公開されているものが見つかりませんでした。本研究で独自に収集・構築する価値があります。

### フェーズ2: ベースラインプロンプトの設計

**2.1 基本プロンプト作成**
- シンプルな修正指示プロンプト
- コンテキスト情報を含むプロンプト
- few-shot例を含むプロンプト

**2.2 評価指標の定義**
- 正解率（Accuracy）
- 過修正率（Over-correction rate）
- 処理速度・コスト

### フェーズ3: プロンプト最適化実験

**3.1 実験設計**
- テストデータセットの作成（正解ペア付き）
- 複数LLMでの比較（Claude, GPT-4, Gemini等）
- プロンプトバリエーションの体系的テスト

**3.2 反復改善**
- 失敗ケースの分析
- プロンプトの調整と再テスト

### フェーズ4: 成果物のまとめ

- 最適化されたプロンプトテンプレート
- タイプミスパターンデータベース
- 実験結果レポート
