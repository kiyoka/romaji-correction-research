import Foundation

enum FileIOError: Error {
    case fileNotFound(String)
    case decodingFailed(String)
    case writeFailed(String)
}

/// Utility for file input/output operations
struct FileIO {
    /// Load typo test cases from a JSON file
    static func loadTestCases(from path: String) throws -> [TypoTestCase] {
        let url = URL(fileURLWithPath: path)

        guard FileManager.default.fileExists(atPath: path) else {
            throw FileIOError.fileNotFound("File not found: \(path)")
        }

        let data = try Data(contentsOf: url)
        let decoder = JSONDecoder()

        do {
            let dataset = try decoder.decode(TypoDataset.self, from: data)
            return dataset.cases
        } catch {
            throw FileIOError.decodingFailed("Failed to decode JSON: \(error.localizedDescription)")
        }
    }

    /// Save benchmark results to CSV file
    static func saveResultsToCSV(results: [TestResult], to path: String) throws {
        var csvLines = ["dataset,typo,expected,expected1,expected2,corrected,japanese,category,exact_match,edit_distance,response_time"]

        for result in results {
            let expected1 = result.testCase.correct1
            let expected2 = result.testCase.correct2 ?? ""
            let expected = result.testCase.correctAnswers.joined(separator: " or ")

            let line = [
                result.dataset,
                result.testCase.typo,
                expected,
                expected1,
                expected2,
                result.corrected,
                result.testCase.japanese,
                result.testCase.category,
                result.isCorrect ? "True" : "False",
                "\(result.editDistance)",
                String(format: "%.2f", result.responseTime)
            ].joined(separator: ",")

            csvLines.append(line)
        }

        let csvContent = csvLines.joined(separator: "\n")

        do {
            try csvContent.write(toFile: path, atomically: true, encoding: .utf8)
        } catch {
            throw FileIOError.writeFailed("Failed to write CSV: \(error.localizedDescription)")
        }
    }

    /// Save benchmark summary to text file
    static func saveSummary(stats: BenchmarkStatistics, to path: String) throws {
        let summary = """
        ============================================================
        Typo Correction Experiment Summary (Apple Foundation Models)
        ============================================================

        Total cases: \(stats.totalCases)
        Exact match rate: \(String(format: "%.2f%%", stats.accuracy * 100))
        Average edit distance: \(String(format: "%.2f", stats.averageEditDistance))
        Average response time: \(String(format: "%.2f", stats.averageResponseTime))s
        """

        do {
            try summary.write(toFile: path, atomically: true, encoding: .utf8)
        } catch {
            throw FileIOError.writeFailed("Failed to write summary: \(error.localizedDescription)")
        }
    }
}
