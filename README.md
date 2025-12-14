研究用のプロジェクトです。

## ローマ字タイプミス自動修正実験

### セットアップ

#### 方法1: Makefileを使う（推奨）

1. 環境変数の設定
```bash
cp .env.example .env
# .envファイルにOpenAI API Keyを設定してください
```

2. 仮想環境のセットアップと依存関係のインストール
```bash
make setup
```

#### 方法2: virtualenvを手動で作成

1. virtualenvのインストール（未インストールの場合）
```bash
# Python 3の場合、venvモジュールは標準で含まれています
# virtualenvを使いたい場合は以下でインストール
pip install virtualenv
```

2. 仮想環境の作成
```bash
# venvモジュールを使う場合（Python 3標準）
python3 -m venv venv

# または virtualenv を使う場合
virtualenv venv
```

3. 仮想環境の有効化
```bash
# Linux/macOS の場合
source venv/bin/activate

# Windows の場合
venv\Scripts\activate
```

4. 依存関係のインストール
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

5. 環境変数の設定
```bash
cp .env.example .env
# .envファイルを編集してOPENAI_API_KEYを設定してください
```

6. 仮想環境の無効化（作業終了時）
```bash
deactivate
```

### 実験の実行

#### Makefileを使う場合
```bash
make run
```

#### 手動で実行する場合
```bash
# 仮想環境を有効化（まだの場合）
source venv/bin/activate  # Linux/macOS
# または
venv\Scripts\activate     # Windows

# 実験を実行
python src/experiment.py
```

実験結果は`results/`ディレクトリに保存されます。

### クリーンアップ

```bash
make clean
```

### プロジェクト構造

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
├── requirements.txt               # Python依存関係
├── Makefile                       # ビルドスクリプト
└── .env                           # 環境変数（要作成）
```
