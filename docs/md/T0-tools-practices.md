# Tools and Best Practices
Collection of tools and best practices for development

## IntelliJ IDEA
Dev backend Java-SpringBoot
- plugins: 
  - SonarLint: code quality
  - Maven Helper: easier dep management
  - Spring Boot Extension Pack
  - Lombok : if needed, and enable annotation processing for easier coding

## Maven
Dep management and build
- build: `mvn clean install`
- test: `mvn test`
- run psringboot: `mvn spring-boot: run`

### VSCode 
Dev Frontend, Mobile
- plugins:
  - ESLint: JS/TS linting to avoid common errors
  - Prettier: code formatting
  - Live Server: quickly serve a frontend
  - React/Redux Snippets: speed up development
  - Integrated terminal for NPM commands

## GIT
Version Control System
- ignore all build files, and local properties, e.g. src/main/resources/application-local.properties

## Spring Boot Actuator
Monitoring and managing Spring Boot application 
- web: https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html
- how to
  - add actuator dep to the project
  - configure endpoints in application.properties
  - Access health and metrics invormation via REST eps

## Docker
containerization
- write dockerfiles for SpringBoot and React applications
- build images, e.g. 
  ```bash
  docker build -t routine-backend .
  docker build -t routine-frontend .
  docker run -p 8080:8080 routine-backend
  docker run -p 3000:3000 routine-frontend
  ```
- use docker-compose to orchestrate containers:
  ```yaml
  version: '3'
  services:
    backend:
      image: routine-backend
      ports:
        - "8080:8080"
    frontend:
      image: routine-frontend
      ports:
        - "3000:3000"
  ```

## PostgreSQL 
- get PostgreSQL: https://www.postgresql.org/download/
- add DB: `createdb routine_db`
- tools
  - [pgAdmin](https://www.pgadmin.org/): to visualize and manage the DB
    - connect to server, e.g. PostgreSQL 16
    - menu: Tools > Query Tool.
      - e.g. `CREATE DATABASE routine_db`
  - DBeaver: alternative cross-platform db tool 

## Swagger UI
Interactive API documentation
- https://swagger.io/tools/swagger-ui/
- howto:
  - add swagger dependencies to the SpringBoot app
  - Configure Swagger in app
  - Access UI at /swagger-ui.html when the app is running

## Postman
API Testing
- add collections for REST API endpoints: GET, POST, PUT, DELETE tasks
- setup env variables for different environments: local, staging, prod
- save request examples
- use Postman to validate responses (e.g. check for 200 status codes)
- write tests for api responses

## Node
- get node, npm, nvm
  - init: `npm init`
  - install dep: `npm install <pkg-name>`
  - run defined script: `npm run <script-name>`

## Create React App
Setup new react project with good default config
- web: https://create-react-app.dev/
- new: `npx create-react-app routine-app-frontend --template typescript`
- start dev: `npm start`
- build for prod: `npm run build`

## React dev tools
- install chrome ext: https://chrome.google.com/webstore/detail/react-developer-tools/fmkadmapgofadopljbjfkapdkoienihi
- open react app in browser
- open Developer Tools and navigate to the Components tab

## GitHub Actions
Automation and CI/CD
- docs: https://docs.github.com/en/actions
- Actions for this project https://github.com/psuzzi/routine/actions
- Workflows in `.github/workflows/ci.yml`
  - e.g. GitHub action for Java backend: 
    ```yaml
    name: Java CI
    on:
      push:
        branches:
          - "main"
          - "issue/*"
    jobs:
      build:
        runs-on: ubuntu-latest
        steps:
          - name: Code Checkout 
            uses: actions/checkout@v4
          - name: Set up JDK 17
            uses: actions/setup-java@v4
            with:
              java-version: '17'
              distribution: 'temurin'
              cache: maven
          - name: Build with Maven
            run: mvn -B package --file pom.xml
          - name: Test with Maven
            run: mvn test

      ```


## GitHub Project
- Routine: https://github.com/users/psuzzi/projects/2/
- Backlog: https://github.com/users/psuzzi/projects/2/views/1

## Cypress
E2E Testing
- install: `npm install cypress --save-dev`
- run test: `npx cypress open`

## Kubernetes
Container orchestration
- install minikube for local K8S cluster testing
- install kubectl to interact with K8S clusters
Setup:
- create deployment and service yaml files for microservices
- deploy to K8S locally with `kubectl apply -f deployment.yaml`

## ELK Elasticsearch, Logstash, Kibana
Optional, for production monitoring
- web: https://www.elastic.co/elastic-stack
- howto
  - setup ELK
  - configure app to send logs to logstash
  - use kibana visualization

## Prometheus and Grafana
Optional, for production monitoring
- use docker to run Prometheus and Grafana
- setup pPrometheus to scrape metrics from your SpringBoot application
- visualize metrics on Grafana dashboards.

## Heroky CLI
Deploy and manage Heroku apps from CLI
- web: https://devcenter.heroku.com/articles/heroku-cli
- howto
  - `heroku login` 
  - `heroku create` to create a new app
  - `git push heroku main` deploy app
  - `heroku logs --tail` view logs


## AIMS: Am I missing something? 
- Sure, let's fix it