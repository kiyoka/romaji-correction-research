# グラフ生成スクリプト

このディレクトリには、ベンチマーク結果を可視化するためのPythonスクリプトが含まれています。

## 必要なパッケージ

```bash
pip install matplotlib numpy
```

## 使用方法

### モデル比較グラフの生成

GPT-5.2とApple Intelligence (3B)のデータセット別正解率を比較する棒グラフを生成します。

```bash
# リポジトリのルートディレクトリから実行
python graph/compare_models.py
```

生成されるファイル:
- `graph/model_comparison.png` - 比較棒グラフ（300dpi PNG）

## グラフの内容

**データセット別正解率比較:**
- Real Data (8件)
- Virtual Data (10件)
- Proper Noun Data (24件)
- Overall (42件)

**比較モデル:**
- GPT-5.2: クラウドベースのフロンティアモデル
- Apple Intelligence (3B): オンデバイスの3Bパラメータモデル

## カスタマイズ

グラフのスタイルや色を変更したい場合は、`compare_models.py`を編集してください。

主要な設定:
- `figsize`: グラフのサイズ
- `color`: バーの色
- `dpi`: 出力解像度（デフォルト: 300dpi）
