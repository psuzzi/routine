package dev.algo.routine.backend.service;

import dev.algo.routine.backend.model.User;
import dev.algo.routine.backend.repository.UserRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.password.PasswordEncoder;

import static org.mockito.Mockito.when;
import static org.mockito.Mockito.verify;
import static org.junit.jupiter.api.Assertions.assertEquals;

/**
 * Test the service layer (business logic)
 */
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private PasswordEncoder passwordEncoder;

    @InjectMocks
    // Service under test
    private UserService userService;

    @Test
    void createUser_shouldEncodePasswordAndSaveUser() {
        // Arrange
        User user = new User();
        user.setUsername("testuser");
        user.setPassword("testpassword");

        when(passwordEncoder.encode("testpassword")).thenReturn("encodedPassword");
        when(userRepository.save(user)).thenReturn(user);

        // Act
        User createdUser = userService.createUser(user);

        // Assert
        verify(passwordEncoder).encode("testpassword");
        verify(userRepository).save(user);
        assertEquals("encodedPassword", createdUser.getPassword());

    }
}
