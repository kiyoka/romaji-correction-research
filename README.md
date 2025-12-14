# ローマ字タイプミス自動修正実験

iPhoneなどの小さいデバイス上のQWERTYキーボードでのタイプミスを、LLMを使って自動修正する研究プロジェクトです。

## 最新の実験結果（GPT-5.2 + Responses API）

**実験日時**: 2024-12-14 14:33:58

### 総合結果

| 指標 | 値 |
|------|------|
| 総テストケース数 | 18件 |
| 完全一致率 | **72.22% (13/18)** |
| 平均編集距離 | 1.00 |
| 平均応答時間 | 2.58秒 |

### データセット別結果

- **実データ正解率**: 50.0% (4/8)
- **仮想データ正解率**: 90.0% (9/10)

### 使用モデル

- モデル: GPT-5.2
- API: OpenAI Responses API
- 設定: reasoning.effort = "low", reasoning.summary = "concise"

### 主な成果

- GPT-4と比較して正解率が **16.66ポイント改善** (55.56% → 72.22%)
- 実データの正解率が **倍増** (25.0% → 50.0%)
- 複雑なタイプミスへの対応力が向上

### 課題

- 応答時間が2.58秒（IME用途には改善が必要）
- 漢字変換の制御が不完全
- 同音異義語の誤変換

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
