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

# Set the working directory inside the container
WORKDIR /app

# Copy the jar from the build stage
COPY --from=build /app/build/libs/*.jar app.jar

# # Expose the port Spring Boot will run on
# EXPOSE 3017

# Command to run the Spring Boot app
ENTRYPOINT ["java", "-jar", "app.jar"]