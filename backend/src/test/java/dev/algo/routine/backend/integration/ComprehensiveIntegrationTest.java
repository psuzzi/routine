package dev.algo.routine.backend.integration;

import dev.algo.routine.backend.model.Task;
import dev.algo.routine.backend.model.User;
import dev.algo.routine.backend.repository.TaskRepository;
import dev.algo.routine.backend.repository.UserRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.Base64;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@Transactional
class ComprehensiveIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private TaskRepository taskRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Test
    void testCompleteWorkflow() throws Exception {
        // 1. Verify the database starts empty
        assertEquals(0, userRepository.count());
        assertEquals(0, taskRepository.count());

        // 2. Register a new user
        String username = "testuser";
        String password = "testpassword";
        String email = "testuser@test.com";

        String userJson = String.format("{ \"username\":\"%s\", \"password\":\"%s\", \"email\":\"%s\"}",
                username, password, email);

        mockMvc.perform(post("/api/users/register")
                .contentType(MediaType.APPLICATION_JSON)
                .content(userJson))
            .andExpect(status().isOk());

        // 3. Verify that the user is written to the database
        assertEquals(1, userRepository.count());
        User savedUser = userRepository.findByUsername(username);
        assertNotNull(savedUser);
        assertEquals(username, savedUser.getUsername());
        assertTrue(passwordEncoder.matches(password, savedUser.getPassword()));

        // 4. Add two tasks for the user
        String taskJson1 = "{\"title\":\"Task 1\",\"description\":\"Description 1\",\"dueDate\":\"" +
                LocalDateTime.now().plusDays(1) + "\"}";
        String taskJson2 = "{\"title\":\"Task 2\",\"description\":\"Description 2\",\"dueDate\":\"" +
                LocalDateTime.now().plusDays(2) + "\"}";

        String basicAuth = "Basic " + Base64.getEncoder().encodeToString((username + ":" + password).getBytes());

        mockMvc.perform(post("/api/tasks")
                .contentType(MediaType.APPLICATION_JSON)
                .content(taskJson1)
                .header("Authorization", basicAuth))
            .andExpect(status().isOk());

        mockMvc.perform(post("/api/tasks")
                .contentType(MediaType.APPLICATION_JSON)
                .content(taskJson2)
                .header("Authorization", basicAuth))
            .andExpect(status().isOk());

        // 5. Verify the tasks are written to the database
        assertEquals(2, taskRepository.count());

        // 6. Find all tasks associated with the user
        List<Task> userTasks = taskRepository.findByUser(savedUser);
        assertEquals(2, userTasks.size());

        // 7. Verify the contents of the tasks
        assertTrue(userTasks.stream().anyMatch(userTask -> userTask.getTitle().equals("Task 1") && userTask.getDescription().equals("Description 1")));
        assertTrue(userTasks.stream().anyMatch(userTask -> userTask.getTitle().equals("Task 2") && userTask.getDescription().equals("Description 2")));

    }
}
