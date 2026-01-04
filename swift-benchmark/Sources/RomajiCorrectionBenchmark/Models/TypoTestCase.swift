import Foundation

/// Represents a single typo test case
struct TypoTestCase: Codable {
    let id: Int
    let typo: String
    let correct1: String
    let correct2: String?
    let japanese: String
    let category: String
    let description: String
    let source: String
    let subcategory: String?

    /// Returns all acceptable correct answers
    var correctAnswers: [String] {
        var answers = [correct1]
        if let correct2 = correct2, !correct2.isEmpty {
            answers.append(correct2)
        }
        return answers
    }
}

/// Dataset containing multiple test cases
struct TypoDataset: Codable {
    let cases: [TypoTestCase]

    init(from decoder: Decoder) throws {
        let container = try decoder.singleValueContainer()
        cases = try container.decode([TypoTestCase].self)
    }
}

/// Result of a single test case evaluation
struct TestResult {
    let testCase: TypoTestCase
    let corrected: String
    let isCorrect: Bool
    let editDistance: Int
    let responseTime: TimeInterval
    let dataset: String
}

/// Summary statistics for all test results
struct BenchmarkStatistics {
    let totalCases: Int
    let correctCases: Int
    let averageEditDistance: Double
    let averageResponseTime: Double

    var accuracy: Double {
        guard totalCases > 0 else { return 0.0 }
        return Double(correctCases) / Double(totalCases)
    }
}
