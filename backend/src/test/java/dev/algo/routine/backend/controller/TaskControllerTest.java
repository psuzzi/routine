package dev.algo.routine.backend.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import dev.algo.routine.backend.model.Task;
import dev.algo.routine.backend.model.User;
import dev.algo.routine.backend.service.TaskService;
import dev.algo.routine.backend.service.UserService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.web.servlet.MockMvc;

import java.time.LocalDateTime;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/**
 * Test the HTTP interface.
 * Verify the task creation endpoint works correctly.
 * Check if the endpoint returns the expected status,
 * and if the response contains the correct task information
 * (including the associated user)
 */
@SpringBootTest
@AutoConfigureMockMvc
class TaskControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private TaskService taskService;

    @MockBean
    private UserService userService;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    @WithMockUser(username = "testuser")
    void testCreateTask() throws Exception {

        long userId = 1L;
        String username = "testuser";

        User user = new User();
        user.setId(userId);
        user.setUsername(username);

        long taskId = 1L;
        String taskTitle = "Test Task";
        String taskDescription = "This is a test Task";

        Task task = new Task();
        task.setTitle(taskTitle);
        task.setDescription(taskDescription);
        task.setDueDate(LocalDateTime.now().plusDays(1));


        Task createdTask = new Task();
        createdTask.setId(taskId);
        createdTask.setTitle(taskTitle);
        createdTask.setDescription(taskDescription);
        createdTask.setDueDate(task.getDueDate());
        createdTask.setUser(user);

        when(userService.findByUsername(username)).thenReturn(user);
        when(taskService.createTask(any(Task.class))).thenReturn(createdTask);

        mockMvc.perform(post("/api/tasks")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(task)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(userId))
                .andExpect(jsonPath("$.title").value(taskTitle))
                .andExpect(jsonPath("$.description").value(taskDescription))
                .andExpect(jsonPath("$.user.id").value(userId))
                .andExpect(jsonPath("$.user.username").value(user.getUsername()));
    }


}
