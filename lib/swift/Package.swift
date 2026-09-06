// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "QuranText",
    platforms: [.iOS(.v13), .macOS(.v10_15), .watchOS(.v6), .tvOS(.v13)],
    products: [.library(name: "QuranText", targets: ["QuranText"])],
    targets: [
        .target(name: "QuranText", resources: [.copy("Resources/hafs.json"), .copy("Resources/UthmanicHafs-v-3.0.ttf")]),
        .testTarget(name: "QuranTextTests", dependencies: ["QuranText"]),
    ]
)
