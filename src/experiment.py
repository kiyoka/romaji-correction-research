"""Main experiment script for typo correction."""

import json
import csv
from datetime import datetime
from pathlib import Path

from src.config import REAL_TYPOS_FILE, VIRTUAL_TYPOS_FILE, RESULTS_DIR
from src.llm_client import TypoCorrectionClient
from src.evaluator import TypoEvaluator
from src.prompts.templates import DEFAULT_PROMPT


def load_typo_data(file_path: Path) -> list:
    """Load typo data from JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def run_experiment(data: list, dataset_name: str, client: TypoCorrectionClient, evaluator: TypoEvaluator):
    """
    Run the typo correction experiment on a dataset.

    Args:
        data: List of typo cases
        dataset_name: Name of the dataset (for display)
        client: LLM client for correction
        evaluator: Evaluator for metrics
    """
    print(f"\n{'='*60}")
    print(f"Testing on {dataset_name}")
    print(f"{'='*60}")

    results = []

    for i, case in enumerate(data, 1):
        typo = case['typo']
        correct = case['correct']
        japanese = case['japanese']

        print(f"\n[{i}/{len(data)}] Testing: {typo} → {correct} ({japanese})")

        # Correct the typo using LLM
        response = client.correct_typo(typo, DEFAULT_PROMPT)

        if response['error']:
            print(f"  ✗ Error: {response['error']}")
            continue

        corrected = response['corrected']
        response_time = response['response_time']

        # Evaluate the result
        eval_result = evaluator.evaluate_single(corrected, correct)
        eval_result['response_time'] = response_time
        eval_result['typo'] = typo
        eval_result['japanese'] = japanese
        eval_result['category'] = case.get('category', '')
        eval_result['dataset'] = dataset_name

        evaluator.add_result(eval_result)
        results.append(eval_result)

        # Display result
        if eval_result['exact_match']:
            print(f"  ✓ Correct: {corrected} (time: {response_time:.2f}s)")
        else:
            print(f"  ✗ Wrong: {corrected} (expected: {correct}, edit_distance: {eval_result['edit_distance']}, time: {response_time:.2f}s)")

    return results


def save_results(all_results: list, stats: dict):
    """Save results to CSV file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = RESULTS_DIR / f"experiment_results_{timestamp}.csv"

    # Write detailed results
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['dataset', 'typo', 'expected', 'corrected', 'japanese', 'category',
                      'exact_match', 'edit_distance', 'response_time']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_results)

    print(f"\n✓ Results saved to: {csv_file}")

    # Write summary statistics
    summary_file = RESULTS_DIR / f"summary_{timestamp}.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("Typo Correction Experiment Summary\n")
        f.write("="*60 + "\n\n")
        f.write(f"Total cases: {stats['total_cases']}\n")
        f.write(f"Exact match rate: {stats['exact_match_rate']:.2%}\n")
        f.write(f"Average edit distance: {stats['average_edit_distance']:.2f}\n")
        f.write(f"Average response time: {stats['average_response_time']:.2f}s\n")

    print(f"✓ Summary saved to: {summary_file}")


def main():
    """Main function to run the experiment."""
    print("\n" + "="*60)
    print("Typo Correction Experiment")
    print("="*60)

    # Initialize client and evaluator
    client = TypoCorrectionClient()
    evaluator = TypoEvaluator()

    # Load datasets
    print("\nLoading datasets...")
    real_data = load_typo_data(REAL_TYPOS_FILE)
    virtual_data = load_typo_data(VIRTUAL_TYPOS_FILE)
    print(f"✓ Loaded {len(real_data)} real cases")
    print(f"✓ Loaded {len(virtual_data)} virtual cases")

    # Run experiments
    all_results = []
    all_results.extend(run_experiment(real_data, "Real Data", client, evaluator))
    all_results.extend(run_experiment(virtual_data, "Virtual Data", client, evaluator))

    # Calculate and display statistics
    stats = evaluator.calculate_statistics()

    print("\n" + "="*60)
    print("Overall Results")
    print("="*60)
    print(f"Total cases: {stats['total_cases']}")
    print(f"Exact match rate: {stats['exact_match_rate']:.2%}")
    print(f"Average edit distance: {stats['average_edit_distance']:.2f}")
    print(f"Average response time: {stats['average_response_time']:.2f}s")

    # Show failed cases
    failed_cases = evaluator.get_failed_cases()
    if failed_cases:
        print(f"\n{'='*60}")
        print(f"Failed Cases ({len(failed_cases)}):")
        print(f"{'='*60}")
        for fc in failed_cases:
            print(f"  {fc['typo']} → {fc['corrected']} (expected: {fc['expected']}, distance: {fc['edit_distance']})")

    # Save results
    save_results(all_results, stats)

    print("\n" + "="*60)
    print("Experiment completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
