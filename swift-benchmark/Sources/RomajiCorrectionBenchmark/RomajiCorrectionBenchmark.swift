import Foundation

#if canImport(FoundationModels)
import FoundationModels
#endif

@main
@available(macOS 26.0, *)
struct RomajiCorrectionBenchmark {
    static func main() async {
        print("============================================================")
        print("Romaji Typo Correction Benchmark - Apple Foundation Models")
        print("============================================================\n")

        // Check if Foundation Models framework is available
        #if canImport(FoundationModels)
        if !SystemLanguageModel.default.isAvailable {
            print("❌ Error: Foundation Models framework is not available on this device.")
            print("   Requirements:")
            print("   - macOS 26+ with Apple Intelligence enabled")
            print("   - Apple Silicon (M1+) or A17 Pro+ chip")
            print("\n   Please check System Settings > Apple Intelligence\n")
            return
        }
        print("✓ Foundation Models framework is available\n")
        #else
        print("⚠️  Warning: Foundation Models framework is not imported.")
        print("   This benchmark requires macOS 26+ and Xcode 26+\n")
        #endif

        // Get the current working directory
        let currentPath = FileManager.default.currentDirectoryPath
        print("Current directory: \(currentPath)\n")

        // Define paths to test data files (relative to repository root)
        let basePath = currentPath.hasSuffix("swift-benchmark")
            ? "\(currentPath)/../src/data"
            : "\(currentPath)/src/data"

        let realDataPath = "\(basePath)/real_typos.json"
        let virtualDataPath = "\(basePath)/virtual_typos.json"
        let properNounDataPath = "\(basePath)/proper_noun_typos.json"

        // Results directory
        let resultsPath = currentPath.hasSuffix("swift-benchmark")
            ? "\(currentPath)/../results"
            : "\(currentPath)/results"

        do {
            // Load test datasets
            print("Loading test datasets...")
            let realData = try FileIO.loadTestCases(from: realDataPath)
            let virtualData = try FileIO.loadTestCases(from: virtualDataPath)
            let properNounData = try FileIO.loadTestCases(from: properNounDataPath)

            print("✓ Loaded \(realData.count) real cases")
            print("✓ Loaded \(virtualData.count) virtual cases")
            print("✓ Loaded \(properNounData.count) proper noun cases\n")

            // Initialize the typo correction service with the default prompt
            let service = TypoCorrectionService(promptTemplate: PromptTemplate.default)

            // Run experiments
            var allResults: [TestResult] = []

            allResults += await runExperiment(
                data: realData,
                datasetName: "Real Data",
                service: service
            )

            allResults += await runExperiment(
                data: virtualData,
                datasetName: "Virtual Data",
                service: service
            )

            allResults += await runExperiment(
                data: properNounData,
                datasetName: "Proper Noun Data",
                service: service
            )

            // Calculate statistics
            let stats = EvaluationService.calculateStatistics(from: allResults)

            // Display overall results
            print("\n============================================================")
            print("Overall Results")
            print("============================================================")
            print("Total cases: \(stats.totalCases)")
            print(String(format: "Exact match rate: %.2f%%", stats.accuracy * 100))
            print(String(format: "Average edit distance: %.2f", stats.averageEditDistance))
            print(String(format: "Average response time: %.2fs", stats.averageResponseTime))

            // Show failed cases
            let failedCases = EvaluationService.getFailedCases(from: allResults)
            if !failedCases.isEmpty {
                print("\n============================================================")
                print("Failed Cases (\(failedCases.count)):")
                print("============================================================")
                for fc in failedCases {
                    let expected = fc.testCase.correctAnswers.joined(separator: " or ")
                    print("  \(fc.testCase.typo) → \(fc.corrected) (expected: \(expected), distance: \(fc.editDistance))")
                }
            }

            // Save results
            let timestamp = DateFormatter.timestamp
            let csvPath = "\(resultsPath)/experiment_results_apple_\(timestamp).csv"
            let summaryPath = "\(resultsPath)/summary_apple_\(timestamp).txt"

            try FileIO.saveResultsToCSV(results: allResults, to: csvPath)
            try FileIO.saveSummary(stats: stats, to: summaryPath)

            print("\n✓ Results saved to: \(csvPath)")
            print("✓ Summary saved to: \(summaryPath)")

            print("\n============================================================")
            print("Experiment completed!")
            print("============================================================\n")

        } catch let error as TypoCorrectionError {
            print("\n❌ Error: \(error.localizedDescription)\n")
            exit(1)
        } catch {
            print("\n❌ Unexpected error: \(error.localizedDescription)\n")
            exit(1)
        }
    }

    /// Run experiment on a single dataset
    static func runExperiment(
        data: [TypoTestCase],
        datasetName: String,
        service: TypoCorrectionService
    ) async -> [TestResult] {
        print("\n============================================================")
        print("Testing on \(datasetName)")
        print("============================================================")

        var results: [TestResult] = []

        for (index, testCase) in data.enumerated() {
            let expectedDisplay = testCase.correctAnswers.joined(separator: " or ")

            print("\n[\(index + 1)/\(data.count)] Testing: \(testCase.typo) → \(expectedDisplay) (\(testCase.japanese))")

            do {
                // Correct the typo using Foundation Models
                let (corrected, responseTime) = try await service.correctTypo(testCase.typo)

                // Evaluate the result
                let result = EvaluationService.evaluate(
                    testCase: testCase,
                    corrected: corrected,
                    responseTime: responseTime,
                    dataset: datasetName
                )

                results.append(result)

                // Display result
                if result.isCorrect {
                    print(String(format: "  ✓ Correct: %@ (time: %.2fs)", corrected, responseTime))
                } else {
                    print(String(format: "  ✗ Wrong: %@ (expected: %@, edit_distance: %d, time: %.2fs)",
                                 corrected, expectedDisplay, result.editDistance, responseTime))
                }
            } catch {
                print("  ✗ Error: \(error.localizedDescription)")
            }
        }

        return results
    }
}

// MARK: - Extensions

extension DateFormatter {
    static var timestamp: String {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyyMMdd_HHmmss"
        return formatter.string(from: Date())
    }
}
