"""Prompt comparison experiment script."""

import json
from datetime import datetime
from pathlib import Path
import csv

from src.config import REAL_TYPOS_FILE, VIRTUAL_TYPOS_FILE, RESULTS_DIR
from src.llm_client import TypoCorrectionClient
from src.evaluator import TypoEvaluator
from src.prompts.templates import ALL_PROMPTS


def load_typo_data(file_path: Path) -> list:
    """Load typo data from JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def test_single_case(client: TypoCorrectionClient, case: dict, prompt_template: str):
    """Test a single case with a given prompt."""
    typo = case['typo']
    correct1 = case.get('correct1', case.get('correct', ''))
    correct2 = case.get('correct2', '')

    # Correct the typo using LLM
    response = client.correct_typo(typo, prompt_template)

    if response['error']:
        return None

    return {
        'typo': typo,
        'corrected': response['corrected'],
        'correct1': correct1,
        'correct2': correct2,
        'response_time': response['response_time'],
        'japanese': case['japanese'],
        'category': case.get('category', '')
    }


def run_prompt_experiment(prompt_name: str, prompt_template: str, data: list, client: TypoCorrectionClient):
    """Run experiment with a specific prompt."""
    print(f"\n{'='*60}")
    print(f"Testing prompt: {prompt_name}")
    print(f"{'='*60}")

    evaluator = TypoEvaluator()
    results = []

    for i, case in enumerate(data, 1):
        typo = case['typo']
        correct1 = case.get('correct1', case.get('correct', ''))
        correct2 = case.get('correct2', '')

        # Display expected values
        if correct2:
            expected_display = f"{correct1} or {correct2}"
        else:
            expected_display = correct1

        print(f"[{i}/{len(data)}] {typo} → {expected_display}")

        result = test_single_case(client, case, prompt_template)

        if result is None:
            print(f"  ✗ Error occurred")
            continue

        # Evaluate
        eval_result = evaluator.evaluate_single(
            result['corrected'],
            result['correct1'],
            result['correct2']
        )
        eval_result.update(result)
        eval_result['prompt'] = prompt_name

        evaluator.add_result(eval_result)
        results.append(eval_result)

        # Display result
        if eval_result['exact_match']:
            print(f"  ✓ Correct: {result['corrected']} ({result['response_time']:.2f}s)")
        else:
            print(f"  ✗ Wrong: {result['corrected']} (expected: {expected_display}, dist: {eval_result['edit_distance']}, {result['response_time']:.2f}s)")

    # Calculate statistics
    stats = evaluator.calculate_statistics()
    stats['prompt'] = prompt_name

    print(f"\n{prompt_name} Results:")
    print(f"  Exact match rate: {stats['exact_match_rate']:.2%}")
    print(f"  Average edit distance: {stats['average_edit_distance']:.2f}")
    print(f"  Average response time: {stats['average_response_time']:.2f}s")

    return results, stats


def main():
    """Main function to run prompt comparison."""
    print("\n" + "="*60)
    print("Prompt Comparison Experiment")
    print("="*60)

    # Load datasets
    print("\nLoading datasets...")
    real_data = load_typo_data(REAL_TYPOS_FILE)
    virtual_data = load_typo_data(VIRTUAL_TYPOS_FILE)
    all_data = real_data + virtual_data
    print(f"✓ Loaded {len(real_data)} real cases")
    print(f"✓ Loaded {len(virtual_data)} virtual cases")
    print(f"Total: {len(all_data)} cases")

    # Initialize client
    client = TypoCorrectionClient()

    # Run experiments for each prompt
    all_results = []
    all_stats = []

    for prompt_name, prompt_template in ALL_PROMPTS.items():
        results, stats = run_prompt_experiment(prompt_name, prompt_template, all_data, client)
        all_results.extend(results)
        all_stats.append(stats)

    # Save comparison results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save detailed results
    csv_file = RESULTS_DIR / f"prompt_comparison_{timestamp}.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['prompt', 'typo', 'expected', 'expected1', 'expected2',
                      'correct1', 'correct2', 'corrected', 'japanese', 'category',
                      'exact_match', 'edit_distance', 'response_time']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_results)

    print(f"\n✓ Detailed results saved to: {csv_file}")

    # Save summary comparison
    summary_file = RESULTS_DIR / f"prompt_comparison_summary_{timestamp}.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("Prompt Comparison Summary\n")
        f.write("="*60 + "\n\n")
        f.write(f"Total test cases: {len(all_data)}\n\n")

        # Sort by accuracy (descending)
        all_stats.sort(key=lambda x: x['exact_match_rate'], reverse=True)

        f.write("Results (sorted by accuracy):\n")
        f.write("-" * 60 + "\n")
        for stats in all_stats:
            f.write(f"\nPrompt: {stats['prompt']}\n")
            f.write(f"  Accuracy: {stats['exact_match_rate']:.2%} ({stats['total_cases']} cases)\n")
            f.write(f"  Avg edit distance: {stats['average_edit_distance']:.2f}\n")
            f.write(f"  Avg response time: {stats['average_response_time']:.2f}s\n")

    print(f"✓ Summary saved to: {summary_file}")

    # Display final comparison
    print("\n" + "="*60)
    print("Final Comparison (sorted by accuracy)")
    print("="*60)

    for i, stats in enumerate(all_stats, 1):
        print(f"\n{i}. {stats['prompt']}")
        print(f"   Accuracy: {stats['exact_match_rate']:.2%}")
        print(f"   Avg edit distance: {stats['average_edit_distance']:.2f}")
        print(f"   Avg response time: {stats['average_response_time']:.2f}s")

    print("\n" + "="*60)
    print("Experiment completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
