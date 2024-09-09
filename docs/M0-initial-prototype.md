# M0 Initial Prototype

## Milestone 0: Initial Prototype (Monolithic)

### Backend Setup
1. Set up a new Spring Boot project using Spring Initializr (https://start.spring.io/).
    - Include dependencies: Spring Web, Spring Data JPA, PostgreSQL Driver, Spring Security
2. Configure PostgreSQL database connection in `application.properties`.
3. Create JPA entities for tasks and user data.
4. Implement repositories for data access.
5. Create REST controllers for CRUD operations on tasks.
6. Implement basic Spring Security configuration for authentication.

### Frontend Setup
1. Create a new React project using Create React App.
2. Set up basic routing using React Router.
3. Implement components for task list, task creation, and user authentication.
4. Use React Context or Redux for state management.
5. Create API service to communicate with the backend.

### CI/CD Setup
1. Create a `.github/workflows` directory in your project.
2. Add a YAML file for GitHub Actions to build and test the application.
3. Set up a Heroku account and create a new app.
4. Configure GitHub Actions to deploy to Heroku after successful builds.