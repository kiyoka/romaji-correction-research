import Foundation

/// Service for evaluating test results
struct EvaluationService {
    /// Calculate Levenshtein distance (edit distance) between two strings
    static func levenshteinDistance(_ s1: String, _ s2: String) -> Int {
        let s1Array = Array(s1)
        let s2Array = Array(s2)
        let m = s1Array.count
        let n = s2Array.count

        // Create a matrix to store distances
        var matrix = Array(repeating: Array(repeating: 0, count: n + 1), count: m + 1)

        // Initialize first row and column
        for i in 0...m {
            matrix[i][0] = i
        }
        for j in 0...n {
            matrix[0][j] = j
        }

        // Calculate distances
        for i in 1...m {
            for j in 1...n {
                let cost = s1Array[i - 1] == s2Array[j - 1] ? 0 : 1
                matrix[i][j] = min(
                    matrix[i - 1][j] + 1,      // deletion
                    matrix[i][j - 1] + 1,      // insertion
                    matrix[i - 1][j - 1] + cost // substitution
                )
            }
        }

        return matrix[m][n]
    }

    /// Evaluate a single test result
    static func evaluate(
        testCase: TypoTestCase,
        corrected: String,
        responseTime: TimeInterval,
        dataset: String
    ) -> TestResult {
        let correctAnswers = testCase.correctAnswers
        let isCorrect = correctAnswers.contains(corrected)

        // Calculate minimum edit distance from all acceptable answers
        let editDistance = correctAnswers.map { answer in
            levenshteinDistance(corrected, answer)
        }.min() ?? Int.max

        return TestResult(
            testCase: testCase,
            corrected: corrected,
            isCorrect: isCorrect,
            editDistance: editDistance,
            responseTime: responseTime,
            dataset: dataset
        )
    }

    /// Calculate overall statistics from results
    static func calculateStatistics(from results: [TestResult]) -> BenchmarkStatistics {
        let totalCases = results.count
        let correctCases = results.filter { $0.isCorrect }.count

        let totalEditDistance = results.reduce(0) { $0 + $1.editDistance }
        let averageEditDistance = totalCases > 0 ? Double(totalEditDistance) / Double(totalCases) : 0.0

        let totalResponseTime = results.reduce(0.0) { $0 + $1.responseTime }
        let averageResponseTime = totalCases > 0 ? totalResponseTime / Double(totalCases) : 0.0

        return BenchmarkStatistics(
            totalCases: totalCases,
            correctCases: correctCases,
            averageEditDistance: averageEditDistance,
            averageResponseTime: averageResponseTime
        )
    }

    /// Get failed test cases from results
    static func getFailedCases(from results: [TestResult]) -> [TestResult] {
        return results.filter { !$0.isCorrect }
    }
}
