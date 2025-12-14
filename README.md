# ローマ字タイプミス自動修正実験

iPhoneなどの小さいデバイス上のQWERTYキーボードでのタイプミスを、LLMを使って自動修正する研究プロジェクトです。

## 最新の実験結果（GPT-5.2 + Responses API + 複数正解対応）

**実験日時**: 2025-12-14 15:07:09

### 総合結果

| 指標 | 値 |
|------|------|
| 総テストケース数 | 18件 |
| 完全一致率 | **88.89% (16/18)** |
| 平均編集距離 | 0.39 |
| 平均応答時間 | 2.52秒 |

### データセット別結果

- **実データ正解率**: 87.5% (7/8)
- **仮想データ正解率**: 90.0% (9/10)

### 使用モデル

- モデル: GPT-5.2
- API: OpenAI Responses API
- 設定: reasoning.effort = "low", reasoning.summary = "concise"
- 評価方式: 複数正解対応（correct1またはcorrect2のいずれかが一致すれば正解）

### 主な成果

- 複数正解対応により正解率が **16.67ポイント改善** (72.22% → 88.89%)
- 実データの正解率が **37.5ポイント向上** (50.0% → 87.5%)
- 漢字・平仮名の表記ゆれに対応し、実用性が大幅に向上
- 複雑なタイプミス（複合エラー、文字順入れ替えなど）も高精度で修正可能

### 課題

- 応答時間が2.52秒（IME用途には約8倍遅い、目標0.3秒）
- 複雑な複合エラーへの対応（kanselshimazu → キャンセルします）
- 語尾の微妙な変換ミス（tanoshu → たのしい）

詳細な実験結果は `RESULT.md` を参照してください。

---

## セットアップ

### 1. 環境変数の設定

```bash
cp .env.example .env
# .envファイルにOPENAI_API_KEYを設定してください
```

### 2. 仮想環境のセットアップと依存関係のインストール

```bash
make setup
```

または手動で：

```bash
# 仮想環境の作成
python3 -m venv venv

# 仮想環境の有効化
source venv/bin/activate  # Linux/macOS
# または
venv\Scripts\activate     # Windows

# 依存関係のインストール
pip install --upgrade pip
pip install -r requirements.txt
```

## 実験の実行

```bash
make run
```

実験結果は`results/`ディレクトリに保存されます。

## プロジェクト構造

```
.
├── src/
│   ├── data/
│   │   ├── real_typos.json       # 実データ
│   │   └── virtual_typos.json    # 仮想データ
│   ├── prompts/
│   │   └── templates.py          # プロンプトテンプレート
│   ├── config.py                 # 設定ファイル
│   ├── llm_client.py             # OpenAI APIクライアント
│   ├── evaluator.py              # 評価ロジック
│   └── experiment.py             # メインスクリプト
├── results/                       # 実験結果（自動生成）
├── RESULT.md                      # 詳細な実験結果レポート
├── requirements.txt               # Python依存関係
├── Makefile                       # ビルドスクリプト
└── .env                           # 環境変数（要作成）
```

## クリーンアップ

```bash
make clean
```
