# {{ app.title }}

This is the monorepo for the {{ app.title }}, containing backend, frontend, and mobile applications.

## Project Structure

- `backend/`: Spring Boot backend application
- `frontend/`: React frontend application
- `mobile/`: React Native mobile application
- `docs/`: Project documentation

## Setup Instructions

1. Backend Setup
   - Navigate to the `backend` directory
   - Run `mvn install` to install dependencies
   - Run `mvn spring-boot:run` to start the backend server

2. Frontend Setup
   - Navigate to the `frontend` directory
   - Run `npm install` to install dependencies
   - Run `npm start` to start the development server

3. Mobile Setup
   - Navigate to the `mobile` directory
   - Run `npm install` to install dependencies
   - Run `npx react-native run-android` or `npx react-native run-ios` to start the mobile app

For more detailed instructions, refer to the README files in each component's directory.