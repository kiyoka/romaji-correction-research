# ローマ字タイプミス自動修正実験

iPhoneなどの小さいデバイス上のQWERTYキーボードでのタイプミスを、LLMを使って自動修正する研究プロジェクトです。

## 最新の実験結果（GPT-5.2 + SIMPLE_V2プロンプト）

**実験日時**: 2025-12-14 16:42:04

### 総合結果

| 指標 | 値 |
|------|------|
| 総テストケース数 | 18件 |
| 完全一致率 | **100.00% (18/18)** 🎉 |
| 平均編集距離 | **0.00** |
| 平均応答時間 | **1.77秒** |

### データセット別結果

- **実データ正解率**: 100.0% (8/8) 🎉
- **仮想データ正解率**: 100.0% (10/10) 🎉

### 使用モデル・設定

- モデル: GPT-5.2
- API: OpenAI Responses API
- 設定: reasoning.effort = "low", reasoning.summary = "concise"
- プロンプト: SIMPLE_V2（6種類の比較実験で選定）
- 評価方式: 複数正解対応（correct1またはcorrect2のいずれかが一致すれば正解）

### 主な成果

- **完璧な正解率を達成**: プロンプト最適化により **100.00%** を実現 🎉
- **プロンプト比較実験**: 6種類のプロンプトを評価し、SIMPLE_V2が最優秀
- **応答時間も改善**: 2.52秒 → 1.77秒（30%短縮）
- **全種類のタイプミスに対応**: 置換、削除、挿入、転置、複合エラーすべてを完璧に修正

### 課題

- 応答時間が1.77秒（IME用途には約6倍遅い、目標0.3秒）
  - 次のステップ: reasoning.effort="none"のテスト、高速モデルの検討

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
