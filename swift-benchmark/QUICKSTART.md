# クイックスタートガイド

## 概要

このSwiftベンチマークツールは、AppleのFoundation Models framework（Apple Intelligence）を使用して、ローマ字タイプミス修正の性能を評価します。

Foundation Models frameworkは2025年9月15日にmacOS 26 Tahoeと共に正式リリースされ、現在はmacOS 26.2（2025年12月12日リリース）で利用可能です。

## 前提条件の確認

### 1. システム要件

```bash
# macOSバージョンを確認
sw_vers

# 必要: macOS 26以降（現在の最新版: macOS 26.2）
# Apple Silicon (M-series)チップが必須
```

### 2. Xcodeとツールのインストール

```bash
# Xcodeがインストールされているか確認
xcode-select -p

# Swiftバージョンを確認
swift --version
# 必要: Swift 6.2以降
```

### 3. Apple Intelligenceの有効化

1. システム設定 > Apple Intelligence を開く
2. Apple Intelligenceを有効にする
3. オンデバイスモデルのダウンロードを確認

## ビルドと実行

### 方法1: リポジトリのルートから実行（推奨）

```bash
# リポジトリのルートディレクトリに移動
cd /path/to/romaji-correction-research

# ビルドと実行
swift run --package-path swift-benchmark
```

### 方法2: swift-benchmarkディレクトリから実行

```bash
# swift-benchmarkディレクトリに移動
cd /path/to/romaji-correction-research/swift-benchmark

# ビルドと実行
swift run
```

### 方法3: リリースビルド（最速）

```bash
cd swift-benchmark
swift build -c release
.build/release/RomajiCorrectionBenchmark
```

## 出力の確認

ベンチマーク実行後、以下のファイルが生成されます：

```bash
# 結果ディレクトリを確認
ls -l results/

# CSV形式の詳細結果
cat results/experiment_results_apple_YYYYMMDD_HHMMSS.csv

# テキスト形式のサマリー
cat results/summary_apple_YYYYMMDD_HHMMSS.txt
```

## トラブルシューティング

### Foundation Models frameworkが見つからない

**エラーメッセージ:**
```
Foundation Models framework is not available on this system.
```

**解決方法:**
1. macOS 26以降にアップデート（推奨: macOS 26.2以降）
2. システム設定でApple Intelligenceを有効化
3. Xcode 26以降をインストール
4. Apple Silicon（M1以降）またはA17 Pro以降のチップを搭載したデバイスを使用

### ビルドエラー

```bash
# クリーンビルド
cd swift-benchmark
swift package clean
swift build
```

### テストデータが見つからない

**エラーメッセージ:**
```
File not found: src/data/real_typos.json
```

**解決方法:**
リポジトリのルートディレクトリから実行してください：
```bash
cd /path/to/romaji-correction-research
swift run --package-path swift-benchmark
```

## Pythonベンチマークとの比較

### Pythonベンチマークの実行

```bash
# Pythonベンチマーク（OpenAI APIを使用）
cd /path/to/romaji-correction-research
python -m src.experiment
```

### 結果の比較

両方のベンチマークは同じテストデータとプロンプトを使用するため、結果を直接比較できます：

| 指標 | Swift (Apple) | Python (OpenAI) |
|------|---------------|-----------------|
| 正解率 | ? | ? |
| 平均応答時間 | ? | ? |
| 編集距離 | ? | ? |
| コスト | 無料（オンデバイス） | API課金 |
| プライバシー | 完全オンデバイス | クラウド送信 |
| オフライン動作 | ✓ | ✗ |

## カスタマイズ

### プロンプトの変更

`Sources/RomajiCorrectionBenchmark/RomajiCorrectionBenchmark.swift`の41行目を編集：

```swift
// デフォルト（固有名詞対応）
let service = TypoCorrectionService(promptTemplate: PromptTemplate.default)

// シンプルなプロンプト
let service = TypoCorrectionService(promptTemplate: PromptTemplate.simple)

// QWERTYキーボード認識プロンプト
let service = TypoCorrectionService(promptTemplate: PromptTemplate.qwertyAware)
```

利用可能なプロンプトは `Utils/PromptTemplates.swift` を参照してください。

### テストデータの追加

新しいテストケースを追加する場合：

1. `src/data/` に新しいJSONファイルを作成
2. `RomajiCorrectionBenchmark.swift` にデータセットの読み込みコードを追加

## 次のステップ

1. ベンチマークを実行して結果を確認
2. PythonベンチマークとSwiftベンチマークの結果を比較
3. 異なるプロンプトテンプレートで実験
4. 結果を`RESULT.md`に追記

## 参考資料

- [Foundation Models Documentation](https://developer.apple.com/documentation/FoundationModels)
- [WWDC 2025 Session 286](https://developer.apple.com/videos/play/wwdc2025/286/)
- [プロジェクトREADME](README.md)
