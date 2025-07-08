plugins {
	java
	id("org.springframework.boot") version "3.3.5"
	id("io.spring.dependency-management") version "1.1.6"
}

group = "com.world-headlines"
version = "0.0.1-SNAPSHOT"

java {
	toolchain {
		languageVersion = JavaLanguageVersion.of(21)
	}
}

repositories {
	mavenCentral()
}

dependencies {
	implementation("org.springframework.boot:spring-boot-starter-data-jdbc")
	implementation("org.springframework.boot:spring-boot-starter-security")
	implementation("org.springframework.boot:spring-boot-starter-web")
	implementation("org.postgresql:postgresql:42.5.0")
	implementation("org.springdoc:springdoc-openapi-starter-webmvc-ui:2.6.0")

	testImplementation("com.h2database:h2")
	testImplementation("org.springframework.boot:spring-boot-starter-test")
	testImplementation("org.springframework.security:spring-security-test")
	testRuntimeOnly("org.junit.platform:junit-platform-launcher")

	compileOnly("org.projectlombok:lombok:1.18.30")
	developmentOnly("org.springframework.boot:spring-boot-devtools")
	annotationProcessor("org.projectlombok:lombok:1.18.30")
}

tasks.withType<Test> {
	useJUnitPlatform()
}

tasks.named<Jar>("jar") {
	enabled = false
}


tasks.named<org.springframework.boot.gradle.tasks.run.BootRun>("bootRun") {
    environment("WORLD_HEADLINES_DB_HOST", "database")
    environment("WORLD_HEADLINES_DB_PORT", "5432")
	environment("WORLD_HEADLINES_DB_NAME", "world_headlines")
    environment("WORLD_HEADLINES_DB_USER", "airflow")
    environment("WORLD_HEADLINES_DB_PASSWORD", "airflow")
}