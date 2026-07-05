FROM maven:3.9.6-eclipse-temurin-17 AS build
WORKDIR /app

COPY pom.xml .
COPY src ./src

RUN mvn clean package

FROM eclipse-temurin:17-jre-alpine
WORKDIR /app

COPY --from=build /app/target/jb-hello-world-maven-0.2.0.jar ./app.jar

CMD ["java", "-jar", "app.jar"]