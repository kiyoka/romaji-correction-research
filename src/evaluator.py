"""Evaluation metrics for typo correction."""

import Levenshtein


class TypoEvaluator:
    """Evaluator for typo correction results."""

    def __init__(self):
        """Initialize the evaluator."""
        self.results = []

    def evaluate_single(self, corrected: str, expected1: str, expected2: str = "") -> dict:
        """
        Evaluate a single correction result with multiple acceptable answers.

        Args:
            corrected: The corrected text from LLM
            expected1: The first expected correct text
            expected2: The second expected correct text (optional)

        Returns:
            dict with evaluation metrics
        """
        # Check exact match against both expected values
        exact_match1 = corrected.lower() == expected1.lower() if expected1 else False
        exact_match2 = corrected.lower() == expected2.lower() if expected2 else False
        exact_match = exact_match1 or exact_match2

        # Calculate Levenshtein distance to the closest expected value
        if expected1 and expected2:
            edit_distance1 = Levenshtein.distance(corrected.lower(), expected1.lower())
            edit_distance2 = Levenshtein.distance(corrected.lower(), expected2.lower())
            edit_distance = min(edit_distance1, edit_distance2)
            matched_expected = expected1 if edit_distance1 <= edit_distance2 else expected2
        elif expected1:
            edit_distance = Levenshtein.distance(corrected.lower(), expected1.lower())
            matched_expected = expected1
        else:
            edit_distance = 0
            matched_expected = ""

        return {
            "exact_match": exact_match,
            "edit_distance": edit_distance,
            "corrected": corrected,
            "expected": matched_expected,
            "expected1": expected1,
            "expected2": expected2
        }

    def add_result(self, result: dict):
        """Add a result to the evaluator."""
        self.results.append(result)

    def calculate_statistics(self) -> dict:
        """
        Calculate overall statistics from all results.

        Returns:
            dict with overall metrics
        """
        if not self.results:
            return {
                "total_cases": 0,
                "exact_match_rate": 0.0,
                "average_edit_distance": 0.0,
                "average_response_time": 0.0
            }

        total = len(self.results)
        exact_matches = sum(1 for r in self.results if r.get("exact_match", False))
        total_edit_distance = sum(r.get("edit_distance", 0) for r in self.results)
        total_response_time = sum(r.get("response_time", 0) for r in self.results)

        return {
            "total_cases": total,
            "exact_match_rate": exact_matches / total if total > 0 else 0.0,
            "average_edit_distance": total_edit_distance / total if total > 0 else 0.0,
            "average_response_time": total_response_time / total if total > 0 else 0.0
        }

    def get_failed_cases(self):
        """Get all cases that didn't match exactly."""
        return [r for r in self.results if not r.get("exact_match", False)]
