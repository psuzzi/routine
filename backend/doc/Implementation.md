# Backend - Spring Boot Application

This document outlines the structure and implementation of the dev.algo.routine.backend application using Spring Boot.

## 1. Project Configuration

### 1.1 Set up Spring Boot project

1. web https://start.spring.io/
2. Configure: [link](https://start.spring.io/#!type=maven-project&language=java&platformVersion=3.3.3&packaging=jar&jvmVersion=17&groupId=dev.algo.routine&artifactId=backend&name=backend&description=Routine%20App%20Backend&packageName=dev.algo.routine.backend&dependencies=web,data-jpa,postgresql,security,lombok)
3. Unzip, unpack, import in your IDE

### 1.2 Configure PostgreSQL database

Setting up a robust database is crucial for our application. We'll use PostgreSQL, a powerful open-source relational database system.

1. Install PostgreSQL if not already installed
2. Create a new database named `routine_app`
3. Open `src/main/resources/application.properties` and add:

```properties
spring.datasource.url=jdbc:postgresql://localhost:5432/routine_app
spring.jpa.hibernate.ddl-auto=update
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.PostgreSQLDialect
```

As you don't want to push remotely your user and pass, add an `application-local.properties`.
Also, make sure you gitignore that file
```properties
spring.datasource.username=your_username
spring.datasource.password=your_password
```

Note: In a production environment, consider using environment variables or a secure vault for sensitive information.

### 1.3 Create JPA entities

Entities are the backbone of our data model. They represent the structure of our database tables in Java objects.

1. Create a new package `dev.algo.routine.backend.model`
2. Create `User.java`:

```java
package dev.algo.routine.backend.model;

import lombok.Data;
import javax.persistence.*;

@Data
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String username;

    @Column(nullable = false)
    private String password;

    @Column(nullable = false, unique = true)
    private String email;
}
```

3. Create `Task.java`:

```java
package dev.algo.routine.backend.model;

import lombok.Data;
import javax.persistence.*;
import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "tasks")
public class Task {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String title;

    private String description;

    @Column(nullable = false)
    private LocalDateTime dueDate;

    @ManyToOne
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    private boolean completed;
}
```

Note: Consider adding additional fields like `createdAt` and `updatedAt` for better tracking of records.

### 1.4 Implement repositories

Repositories provide an abstraction layer for database operations, allowing us to interact with our entities easily.

1. Create a new package `dev.algo.routine.backend.repository`
2. Create `UserRepository.java`:

```java
package dev.algo.routine.backend.repository;

import dev.algo.routine.backend.model.User;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRepository extends JpaRepository<User, Long> {
    User findByUsername(String username);
}
```

3. Create `TaskRepository.java`:

```java
package dev.algo.routine.backend.repository;

import dev.algo.routine.backend.model.Task;
import dev.algo.routine.backend.model.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface TaskRepository extends JpaRepository<Task, Long> {
    List<Task> findByUser(User user);
}
```

Note: For more complex queries, consider using `@Query` annotations or QueryDSL for type-safe queries.

### 1.5 Create services

Services encapsulate our business logic, providing a clean separation between the web layer and data access layer.

1. Create a new package `dev.algo.routine.backend.service`
2. Create `UserService.java`:

```java
package dev.algo.routine.backend.service;

import dev.algo.routine.backend.model.User;
import dev.algo.routine.backend.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    public User createUser(User user) {
        // Encode the password before saving
        user.setPassword(passwordEncoder.encode(user.getPassword()));
        return userRepository.save(user);
    }

    public User findByUsername(String username) {
        return userRepository.findByUsername(username);
    }
}
```

3. Create `TaskService.java`:

```java
package dev.algo.routine.backend.service;

import dev.algo.routine.backend.model.Task;
import dev.algo.routine.backend.model.User;
import dev.algo.routine.backend.repository.TaskRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class TaskService {
    @Autowired
    private TaskRepository taskRepository;

    public Task createTask(Task task) {
        return taskRepository.save(task);
    }

    public List<Task> getTasksForUser(User user) {
        return taskRepository.findByUser(user);
    }

    public Task updateTask(Task task) {
        return taskRepository.save(task);
    }

    public void deleteTask(Long taskId) {
        taskRepository.deleteById(taskId);
    }
}
```

Note: Consider adding validation logic and error handling in these service methods for robustness.

### 1.6 Implement REST controllers

Controllers handle HTTP requests and responses, defining the API endpoints for our application.

1. Create a new package `dev.algo.routine.backend.controller`
2. Create `UserController.java`:

```java
package dev.algo.routine.backend.controller;

import dev.algo.routine.backend.model.User;
import dev.algo.routine.backend.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/users")
public class UserController {
    @Autowired
    private UserService userService;

    @PostMapping("/register")
    public ResponseEntity<User> registerUser(@RequestBody User user) {
        User createdUser = userService.createUser(user);
        return ResponseEntity.ok(createdUser);
    }
}
```

3. Create `TaskController.java`:

```java
package dev.algo.routine.backend.controller;

import dev.algo.routine.backend.model.Task;
import dev.algo.routine.backend.model.User;
import dev.algo.routine.backend.service.TaskService;
import dev.algo.routine.backend.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/tasks")
public class TaskController {
    @Autowired
    private TaskService taskService;

    @Autowired
    private UserService userService;

    @PostMapping
    public ResponseEntity<Task> createTask(@RequestBody Task task, Authentication authentication) {
        // Get the authenticated user
        User user = userService.findByUsername(authentication.getName());
        task.setUser(user);
        Task createdTask = taskService.createTask(task);
        return ResponseEntity.ok(createdTask);
    }

    @GetMapping
    public ResponseEntity<List<Task>> getTasks(Authentication authentication) {
        User user = userService.findByUsername(authentication.getName());
        List<Task> tasks = taskService.getTasksForUser(user);
        return ResponseEntity.ok(tasks);
    }

    @PutMapping("/{taskId}")
    public ResponseEntity<Task> updateTask(@PathVariable Long taskId, @RequestBody Task task, Authentication authentication) {
        User user = userService.findByUsername(authentication.getName());
        task.setId(taskId);
        task.setUser(user);
        Task updatedTask = taskService.updateTask(task);
        return ResponseEntity.ok(updatedTask);
    }

    @DeleteMapping("/{taskId}")
    public ResponseEntity<Void> deleteTask(@PathVariable Long taskId) {
        taskService.deleteTask(taskId);
        return ResponseEntity.ok().build();
    }
}
```

Note: Consider implementing pagination for the `getTasks` endpoint to handle large numbers of tasks efficiently.

### 1.7 Implement basic Spring Security configuration

Security is crucial for any application. Here, we set up basic authentication and authorization rules.

1. Create a new package `dev.algo.routine.backend.config`
2. Create `SecurityConfig.java`:

```java
package dev.algo.routine.backend.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

   @Bean
   public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
      http
              .csrf(AbstractHttpConfigurer::disable)  // Disable CSRF for simplicity. Enable in production.
              .authorizeHttpRequests(auth -> auth
                      .requestMatchers("/api/users/register").permitAll()
                      .anyRequest().authenticated()
              )
              .httpBasic( httpBasic -> {});  // Use HTTP Basic Authentication
      return http.build();
   }

   @Bean
   public PasswordEncoder passwordEncoder() {
      return new BCryptPasswordEncoder();
   }
}
```

3. Create `CustomUserDetailsService.java`:

```java
package dev.algo.routine.backend.config;

import dev.algo.routine.backend.model.User;
import dev.algo.routine.backend.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

@Service
public class CustomUserDetailsService implements UserDetailsService {

    @Autowired
    private UserService userService;

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        User user = userService.findByUsername(username);
        if (user == null) {
            throw new UsernameNotFoundException("User not found");
        }
        // Convert our custom User to Spring's UserDetails
        return org.springframework.security.core.userdetails.User
                .withUsername(user.getUsername())
                .password(user.getPassword())
                .roles("USER")
                .build();
    }
}
```

Note: For production, consider implementing JWT (JSON Web Tokens) for stateless authentication and more granular authorization rules.

## 3. Running the Application

To run the application:

1. Ensure PostgreSQL is running and the database is created
2. Run the Spring Boot application
3. The API will be available at `http://localhost:8080`

## 4. API Endpoints

- POST `/api/users/register`: Register a new user
- POST `/api/{{ project.entity.name|lower }}s`: Create a new {{ project.entity.name|lower }}
- GET `/api/{{ project.entity.name|lower }}s`: Get all {{ project.entity.name|lower }}s for the authenticated user
- PUT `/api/{{ project.entity.name|lower }}s/{id}`: Update a {{ project.entity.name|lower }}
- DELETE `/api/{{ project.entity.name|lower }}s/{id}`: Delete a {{ project.entity.name|lower }}

Remember to implement proper error handling, validation, and testing for a production-ready application.