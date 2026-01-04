# Romaji Typo Correction Benchmark - Apple Foundation Models

このSwiftアプリケーションは、AppleのFoundation Models frameworkを使用して、ローマ字タイプミス修正のベンチマークテストを実行します。

## 概要

このツールは、既存のPythonベンチマーク（`src/experiment.py`）と同じテストケースを使用して、Apple Intelligence（オンデバイスLLM）のタイプミス修正性能を評価します。

## 必要要件

### システム要件
- **macOS 26** 以降（2025年9月15日正式リリース、現在はmacOS 26.2が最新版）
- **Apple Silicon (M-series)** プロセッサ必須
- **Xcode 26+** （Swift 6.2以降）
- **Apple Intelligence** がシステム設定で有効化されていること

### Foundation Models Frameworkについて

AppleはWWDC 2025（2025年6月9日）でFoundation Models frameworkを発表し、**2025年9月15日にmacOS 26 Tahoeと共に正式リリース**されました。このframeworkは：
- オンデバイスの3Bパラメータモデルへの直接アクセスを提供
- 完全にプライバシー保護（オンデバイス処理）
- オフラインで動作
- 50ms未満のレイテンシー
- SwiftネイティブAPI
- わずか3行のコードで利用可能

**現在の最新バージョン**: macOS 26.2（2025年12月12日リリース）にて正式に利用可能です。

## プロジェクト構造

```
swift-benchmark/
├── Package.swift                          # Swift Package Manager設定
├── README.md                              # このファイル
└── Sources/
    └── RomajiCorrectionBenchmark/
        ├── RomajiCorrectionBenchmark.swift  # メインエントリポイント
        ├── Models/
        │   └── TypoTestCase.swift          # データモデル定義
        ├── Services/
        │   ├── TypoCorrectionService.swift  # Foundation Models統合
        │   └── EvaluationService.swift      # 結果評価ロジック
        └── Utils/
            ├── FileIO.swift                 # ファイル入出力
            └── PromptTemplates.swift        # プロンプトテンプレート
```

## ビルドと実行

### 1. プロジェクトのビルド

```bash
cd swift-benchmark
swift build
```

### 2. ベンチマークの実行

リポジトリのルートディレクトリから実行：

```bash
cd /path/to/romaji-correction-research
swift run --package-path swift-benchmark
```

または、swift-benchmarkディレクトリから実行：

```bash
cd swift-benchmark
swift run
```

### 3. リリースビルド（最適化あり）

```bash
swift build -c release
.build/release/RomajiCorrectionBenchmark
```

## テストデータ

このベンチマークは以下の3つのデータセットを使用します：

1. **Real Data** (`src/data/real_typos.json`) - 実際のタイプミス事例
2. **Virtual Data** (`src/data/virtual_typos.json`) - 仮想的なタイプミス事例
3. **Proper Noun Data** (`src/data/proper_noun_typos.json`) - 固有名詞の正規化テスト

各テストケースには以下の情報が含まれます：
- タイプミスの入力
- 正解の日本語（または正規表記）
- カテゴリ（substitution, deletion, insertion, transposition等）
- 説明

## 出力結果

ベンチマーク実行後、`results/`ディレクトリに以下のファイルが生成されます：

1. **CSV形式の詳細結果**: `experiment_results_apple_YYYYMMDD_HHMMSS.csv`
   - 各テストケースの詳細な結果
   - タイプミス、期待値、実際の出力、編集距離、応答時間など

2. **テキスト形式のサマリー**: `summary_apple_YYYYMMDD_HHMMSS.txt`
   - 全体の正解率
   - 平均編集距離
   - 平均応答時間

## プロンプトテンプレート

デフォルトで使用されるプロンプトは `PROPER_NOUN_AWARE_V2` です（Pythonベンチマークと同じ）。

他のプロンプトを使用する場合は、`RomajiCorrectionBenchmark.swift`の以下の行を変更してください：

```swift
let service = TypoCorrectionService(promptTemplate: PromptTemplate.default)
```

利用可能なプロンプトテンプレート：
- `PromptTemplate.simple` - シンプルなプロンプト
- `PromptTemplate.qwertyAware` - QWERTYキーボード認識プロンプト
- `PromptTemplate.properNounAwareV2` - 固有名詞対応プロンプト（デフォルト）

詳細は `Utils/PromptTemplates.swift` を参照してください。

## トラブルシューティング

### Foundation Models frameworkが見つからない

```
Error: Foundation Models framework is not available on this system.
```

**解決方法**:
1. macOS 26以降にアップデート（推奨: macOS 26.2以降）
2. システム設定 > Apple Intelligence を有効化
3. Xcode 26+ をインストール
4. Apple Silicon（M1以降）またはA17 Pro以降のチップを搭載したデバイスを使用

### ビルドエラー

```bash
# キャッシュをクリアして再ビルド
swift package clean
swift build
```

### データファイルが見つからない

ベンチマークは以下のパスからデータを読み込みます：
- `src/data/real_typos.json`
- `src/data/virtual_typos.json`
- `src/data/proper_noun_typos.json`

リポジトリのルートディレクトリから実行してください。

## Pythonベンチマークとの比較

このSwiftベンチマークは、Pythonベンチマーク（`src/experiment.py`）と同じ：
- テストデータ
- プロンプトテンプレート
- 評価指標（正解率、編集距離、応答時間）

を使用しているため、結果を直接比較できます。

**Pythonベンチマークの実行方法**:
```bash
python -m src.experiment
```

## 実装の詳細

### Foundation Models Framework統合

`Services/TypoCorrectionService.swift`では、以下のようにFoundation Models frameworkを使用します：

```swift
#if canImport(FoundationModels)
import FoundationModels

let model = LanguageModel()
let response = try await model.generate(prompt: prompt)
#endif
```

公式ドキュメントを参照してください：
- [Foundation Models Documentation](https://developer.apple.com/documentation/FoundationModels)
- [WWDC 2025 Session 286: Meet the Foundation Models framework](https://developer.apple.com/videos/play/wwdc2025/286/)

### 評価アルゴリズム

- **編集距離**: レーベンシュタイン距離アルゴリズムを使用
- **正解判定**: 複数の正解候補（correct1, correct2）に対して完全一致を確認

## 参考資料

- [Apple Foundation Models Framework](https://developer.apple.com/documentation/FoundationModels)
- [WWDC 2025: Meet the Foundation Models framework](https://developer.apple.com/videos/play/wwdc2025/286/)
- [Apple Machine Learning Research - Foundation Models 2025](https://machinelearning.apple.com/research/apple-foundation-models-2025-updates)

## ライセンス

このプロジェクトは、親リポジトリと同じライセンスに従います。

## 貢献

バグ報告や改善提案は、GitHubのIssueまたはPull Requestでお願いします。
