# 引き継ぎ: macOS 27 での Foundation Models 再測定

> **実施済み（2026-09-19）:** macOS 27.0で同条件の46件を2回測定し、いずれも31/46（67.39%）だった。結果ファイルと比較・注意点は [RESULT.md の追加計測](RESULT.md#macos-270での追加計測2026-09-19) を参照。この記事は現在 `japanese-input-method-sumibi-25.md` で、未公開のまま。以下には測定前に作成した手順も残している。

作成日: 2026-09-16 / 作成環境: Windows(WSL)側のセッション
実行担当: macOS 27 にアップデート済みの MacBook Air (M4, 24GB)

## 目的

Zenn記事 `japanese-input-method-sumibi-25.md`（iOS 27 の Foundation Models を扱う回、
`published: false` で保留中）を公開するために、**オンデバイス3Bモデルのローマ字タイプミス
修正性能を macOS 27 世代で測り直す**。

記事の核心は「オンデバイスモデルの変換品質は実用に届くか」で、macOS 26 世代では 46.67% と
GPT-5.2 の 97.62% に遠く及ばなかった。iOS/macOS 27 でオンデバイスモデルが作り直されたため、
再測定しないと現在値が分からない。

## 過去の測定値（比較対象）

| モデル | 完全一致率 | 平均編集距離 | 平均応答時間 | 測定日 |
|---|---|---|---|---|
| GPT-5.2 (OpenAI Responses API) | 97.62% (41/42) | - | 1.45秒 | 2025-12-30 |
| Apple Foundation Models オンデバイス (macOS 26世代) | 46.67% (45件) | 1.98 | 0.70秒 | 2026-01-12 |

結果ファイルは `results/` にある:
- `summary_apple_20260112_221331.txt` / `experiment_results_apple_20260112_221331.csv`
- `summary_20251230_001143.txt` / `experiment_results_20251230_001143.csv`（GPT-5.2側）

## 手順

```bash
cd <romaji-correction-research のルート>

# 1. まずビルドが通るか確認する
swift build --package-path swift-benchmark

# 2. 通ったら本番実行（リポジトリのルートから実行すること。src/data/ を相対パスで読む）
swift run --package-path swift-benchmark
```

実行条件（前回と揃えるため**変更しないこと**）:
- テストデータ: `src/data/` の3セット計46件（real_typos 8 / virtual_typos 10 / proper_noun_typos 28）
- プロンプト: `PROPER_NOUN_AWARE_V6_ENGLISH`（`Utils/PromptTemplates.swift` の `default`。前回のmacOS 26.2と同じ）
- 指標: 完全一致率 / 平均編集距離 / 平均応答時間

出力:
- `results/experiment_results_apple_<YYYYMMDD_HHMMSS>.csv`
- `results/summary_apple_<YYYYMMDD_HHMMSS>.txt`

## ビルドが落ちた場合に見るところ

macOS 27 で Foundation Models の API が変わっている。落ちるとしたらこの2箇所が候補:

1. **`Sources/RomajiCorrectionBenchmark/Services/TypoCorrectionService.swift:22`**
   ```swift
   self.isAvailable = SystemLanguageModel.default.isAvailable
   ```
   これは旧 API。27 では `SystemLanguageModel.default.availability` が
   `.available` / `.deviceNotEligible` などを返す形になっている。
   非推奨または削除されていればここで止まる。

2. **`swift-benchmark/Package.swift` の `platforms: [.macOS(.v15)]`**
   `@available(macOS 26.0, *)` で切っているので動きはするが、27 世代の API を使うなら上げる。

`LanguageModelSession().respond(to:)` の呼び出し自体は 27 でも残っている見込みなので、
修正は1〜2行で済むはず。判断に迷ったらエラー出力を Windows 側のセッションに貼る。

## 測定後に報告してほしいもの

- `results/summary_apple_<日付>.txt` の中身
- `results/experiment_results_apple_<日付>.csv`（データセット別に分解して見るため）

見たいのは全体の一致率だけではない。**データセット別の内訳**（real / virtual / 固有名詞）で、
46.67% からどこが動いたかを確認する。macOS 26 世代の落ち方が固有名詞（46件中28件と比重が大きい）
に偏っていたのか、素のタイプミス修正から崩れていたのかで記事の結論が変わる。

## 注意点

- **比較対象のケース集合が厳密に揃っていない**。過去の2回は GPT側42件 / Apple側45件でずれがある
  （Apple側のみ `apple intelligence` `apple intelligenceban` `chatgpt` `claude` の4件、
  GPT側のみ `srigtou` の1件）。Apple 同士の比較（46.67% → X%）は成立するが、
  GPT-5.2 と厳密に並べるなら同じ46件で両方を測り直す必要がある。
- **データリークに注意**。過去に、プロンプトの examples にテストデータと同じ内容を含めてしまい
  結果が過剰に良く出た事例がある（64.44% → 修正後 46.67%）。プロンプトを触る場合は必ず確認する。

## やらないこと

- **AJIMEE-Bench の測定はしない**（2026-09-15 にユーザーが決定）。
  `Sumibi/benchmark/` にある CER ベースのかな漢字変換ベンチ（JWTD v2 由来200件）は
  part24 では使わない。
- **App Extension のレートリミット検証は不可能**。手元の最新 iPhone が iPhone 14 Plus (A15) で
  Apple Intelligence 非対応。PCC だけを使う抜け道もない（PCC は対応端末のあふれを受ける仕組みで、
  非対応端末では `availability` が `.deviceNotEligible` を返すだけ）。

## 測定後の作業（当初の想定）

1. 数値を `articles/japanese-input-method-sumibi-25.md` に反映
2. 「これから確かめること」「検証できるもの、できないもの」の2節を実測値ベースに書き直す
3. 実機未検証の範囲を明記して公開可否を判断する（現時点では `published: false`）

## 関連リポジトリ

- 記事: `zenn-content` (`articles/japanese-input-method-sumibi-25.md`)
- 実装: `kiyoka/Sumibi-iOS`
- 本ベンチ: `kiyoka/romaji-correction-research`
