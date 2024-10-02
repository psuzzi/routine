package dev.algo.routine.backend.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import dev.algo.routine.backend.model.User;
import dev.algo.routine.backend.service.UserService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.Mockito.when;
import static org.mockito.Mockito.any;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * Test the HTTP interface.
 * Verify the user registration endpoint works correctly.
 * Check if the endpoint returns the expected status,
 * and if the response contains the correct user information
 * (excluding the password)
 */
@SpringBootTest
@AutoConfigureMockMvc
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    void testRegisterUser() throws Exception {
        String username = "testuser";
        String usermail = "testuser@example.com";

        User user = new User();
        user.setUsername(username);
        user.setPassword("testpassword");
        user.setEmail(usermail);

        User createdUser = new User();
        createdUser.setId(1L);
        createdUser.setUsername(username);
        createdUser.setEmail(usermail);

        when(userService.createUser(any(User.class))).thenReturn(createdUser);

        mockMvc.perform(post("/api/users/register")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(user)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.username").value(username))
                .andExpect(jsonPath("$.email").value(usermail))
                .andExpect(jsonPath("$.password").doesNotExist());


    }
}
