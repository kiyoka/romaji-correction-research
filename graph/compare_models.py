#!/usr/bin/env python3
"""
データセット別の正解率比較グラフを生成するスクリプト

GPT-5.2とApple Intelligence (3B)の性能を比較する棒グラフを作成します。
"""

import matplotlib.pyplot as plt
import numpy as np

# 日本語フォント設定（macOS）
plt.rcParams['font.family'] = ['Arial Unicode MS', 'Hiragino Sans', 'DejaVu Sans']
plt.rcParams['font.size'] = 12

# データ（正解率）
datasets = ['Real Data\n(8件)', 'Virtual Data\n(10件)', 'Proper Noun\n(24件)', 'Overall\n(42件)']
gpt52_scores = [87.5, 100.0, 100.0, 97.62]
apple_ai_scores = [0.0, 60.0, 25.0, 28.57]

# グラフの位置設定
x = np.arange(len(datasets))
width = 0.35

# グラフ作成
fig, ax = plt.subplots(figsize=(12, 7))

# 棒グラフ描画（正解率）
bars1 = ax.bar(x - width/2, gpt52_scores, width, label='GPT-5.2',
               color='#4CAF50', alpha=0.8, edgecolor='black', linewidth=1.2)
bars2 = ax.bar(x + width/2, apple_ai_scores, width, label='Apple Intelligence (3B)',
               color='#2196F3', alpha=0.8, edgecolor='black', linewidth=1.2)

# ラベルとタイトル
ax.set_xlabel('データセット', fontsize=14, fontweight='bold')
ax.set_ylabel('正解率 (%)', fontsize=14, fontweight='bold')
ax.set_title('ローマ字タイプミス修正ベンチマーク: モデル別正解率比較\nGPT-5.2 vs Apple Intelligence (3B)',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(datasets)
ax.legend(fontsize=12, loc='upper left')
ax.set_ylim(0, 110)

# グリッド追加
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.set_axisbelow(True)

# 各バーに数値を表示
def add_value_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=11, fontweight='bold')

add_value_labels(bars1)
add_value_labels(bars2)

# レイアウト調整
plt.tight_layout()

# 保存（正解率版）
output_path = 'graph/model_comparison.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f'✓ 正解率グラフを保存しました: {output_path}')

# 表示（オプション）
# plt.show()
