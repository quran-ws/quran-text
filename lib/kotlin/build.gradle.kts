plugins {
    kotlin("jvm") version "2.1.20"
    `maven-publish`
    signing
}

group = "ws.quran"
version = "0.1.0"

repositories { mavenCentral() }

dependencies {
    // Android ships org.json; on the JVM it is one small dependency.
    implementation("org.json:json:20240303")
    testImplementation(kotlin("test"))
}

kotlin { jvmToolchain(17) }

// Maven Central requires sources and javadoc jars alongside the binary.
java { withSourcesJar(); withJavadocJar() }

publishing {
    publications {
        create<MavenPublication>("maven") {
            from(components["java"])
            artifactId = "quran-text"
            pom {
                name.set("quran-text")
                description.set("Read the quran-text dataset: the Qurʾān in seven riwāyāt with pages, lines, āyāt, pause marks and one shared word numbering. Ḥafṣ bundled.")
                url.set("https://quran.ws")
                licenses {
                    license {
                        name.set("MIT License")
                        url.set("https://github.com/quran-ws/quran-text/blob/main/lib/kotlin/LICENSE")
                    }
                }
                developers {
                    developer { id.set("quran-ws"); name.set("quran-ws"); email.set("service@quran.ws") }
                }
                scm {
                    url.set("https://github.com/quran-ws/quran-text")
                    connection.set("scm:git:https://github.com/quran-ws/quran-text.git")
                    developerConnection.set("scm:git:ssh://git@github.com/quran-ws/quran-text.git")
                }
            }
        }
    }
    repositories {
        maven {
            name = "central"
            url = uri("https://ossrh-staging-api.central.sonatype.com/service/local/staging/deploy/maven2/")
            credentials {
                username = findProperty("centralUsername") as String?
                password = findProperty("centralPassword") as String?
            }
        }
    }
}

// Central rejects unsigned artifacts. Keys come from ~/.gradle/gradle.properties.
signing {
    setRequired({ gradle.taskGraph.hasTask("publish") })
    sign(publishing.publications["maven"])
}

tasks.test { useJUnitPlatform() }
