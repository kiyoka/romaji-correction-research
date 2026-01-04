import Foundation

// MARK: - Foundation Models Framework Integration
// Note: This uses Apple's Foundation Models framework (announced at WWDC 2025, released September 15, 2025)
// Requirements:
// 1. macOS 26+ (current version: macOS 26.2)
// 2. Apple Intelligence enabled in System Settings
// 3. Xcode 26+
// 4. Apple Silicon (M1+) or A17 Pro+ hardware

#if canImport(FoundationModels)
import FoundationModels

/// Service for correcting typos using Apple's Foundation Models
@available(macOS 26.0, *)
actor TypoCorrectionService {
    private let promptTemplate: String
    private let isAvailable: Bool

    init(promptTemplate: String) {
        self.promptTemplate = promptTemplate
        // Check if the Foundation Models framework is available on this device
        self.isAvailable = SystemLanguageModel.default.isAvailable
    }

    /// Correct a typo using Apple's on-device Foundation Model
    /// Creates a new session for each request to avoid context accumulation
    func correctTypo(_ typo: String) async throws -> (corrected: String, responseTime: TimeInterval) {
        guard isAvailable else {
            throw TypoCorrectionError.frameworkNotAvailable
        }

        // Create a new session for each request to prevent context window overflow
        let session = LanguageModelSession()

        let startTime = Date()

        // Format the prompt with the typo
        let prompt = promptTemplate.replacingOccurrences(of: "{typo}", with: typo)

        // Use Foundation Models framework to generate response
        let response = try await session.respond(to: prompt)
        let responseTime = Date().timeIntervalSince(startTime)

        // Clean up the response (remove extra whitespace, newlines)
        let corrected = response.content.trimmingCharacters(in: .whitespacesAndNewlines)

        return (corrected, responseTime)
    }
}

#else

/// Fallback service when Foundation Models framework is not available
@available(macOS 15.0, *)
actor TypoCorrectionService {
    private let promptTemplate: String

    init(promptTemplate: String) {
        self.promptTemplate = promptTemplate
        print("⚠️  Warning: Foundation Models framework is not available.")
        print("⚠️  This requires macOS 26+ with Apple Intelligence enabled.")
    }

    func correctTypo(_ typo: String) async throws -> (corrected: String, responseTime: TimeInterval) {
        throw TypoCorrectionError.frameworkNotAvailable
    }
}

#endif

// MARK: - Errors

enum TypoCorrectionError: Error, LocalizedError {
    case frameworkNotAvailable
    case modelNotAvailable
    case generationFailed(String)

    var errorDescription: String? {
        switch self {
        case .frameworkNotAvailable:
            return """
            Foundation Models framework is not available on this system.

            Requirements:
            - macOS 26 or later (current: macOS 26.2, released December 12, 2025)
            - Apple Intelligence enabled in System Settings
            - Xcode 26+ with Foundation Models framework support
            - Apple Silicon (M1+) or A17 Pro+ hardware

            The Foundation Models framework was released on September 15, 2025.
            Check Apple Developer documentation:
            https://developer.apple.com/documentation/FoundationModels
            """
        case .modelNotAvailable:
            return "Language model is not available or not initialized."
        case .generationFailed(let reason):
            return "Text generation failed: \(reason)"
        }
    }
}
