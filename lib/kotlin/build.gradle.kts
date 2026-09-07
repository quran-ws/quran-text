plugins {
    kotlin("jvm") version "2.1.20"
}

group = "org.quranpedia"
version = "0.1.0"

repositories { mavenCentral() }

dependencies {
    // Android ships org.json; on the JVM it is one small dependency.
    implementation("org.json:json:20240303")
    testImplementation(kotlin("test"))
}

kotlin { jvmToolchain(17) }

tasks.test { useJUnitPlatform() }
