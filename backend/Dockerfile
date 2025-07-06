# Use the Gradle image to build the project
FROM gradle:8.14.2-jdk21-noble AS build
# Set the working directory inside the container
WORKDIR /app
# Copy the Gradle project files
COPY . .
# Build the Spring Boot app
RUN gradle clean build

# Use a lightweight JRE for running the app
FROM openjdk:25-ea-21-jdk-slim-bookworm

# install infisical cli
RUN apt-get update && apt-get install -y \
    curl \
    && curl -1sLf 'https://artifacts-cli.infisical.com/setup.deb.sh' | bash \
    && apt-get update && apt-get install -y infisical \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the jar from the build stage
COPY --from=build /app/build/libs/*.jar app.jar

# Run
CMD infisical run \
    --token="${INFISICAL_TOKEN}" \
    --env="${INFISICAL_ENVIRONMENT}" \
    --projectId="${INFISICAL_PROJECT_ID}" \
    --domain="${INFISICAL_HOST}" \
    -- \
    java -jar app.jar