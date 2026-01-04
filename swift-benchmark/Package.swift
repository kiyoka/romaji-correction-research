// swift-tools-version: 6.2
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "RomajiCorrectionBenchmark",
    platforms: [
        .macOS(.v15)  // Foundation Models framework requires macOS 26+, but we set v15 for compatibility
    ],
    targets: [
        // Targets are the basic building blocks of a package, defining a module or a test suite.
        // Targets can depend on other targets in this package and products from dependencies.
        .executableTarget(
            name: "RomajiCorrectionBenchmark"
        ),
    ]
)
