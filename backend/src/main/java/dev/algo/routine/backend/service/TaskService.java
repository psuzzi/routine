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
//        TODO: a deeper check might be needed
//        if (task.getUser() == null){
//            throw new IllegalArgumentException("Task must be associated with a user");
//        }
//        if (task.getDeadline()==null){
//            task.setDeadline(LocalDateTime.now().plusDays(1));//default due date tomorrow
//        }
        return taskRepository.save(task);
    }

    public List<Task> getTaskForUser(User user){
        return taskRepository.findByUser(user);
    }

    public Task updateTask(Task task) {
        return taskRepository.save(task);
    }

    public void deleteTask(Long taskId) {
        taskRepository.deleteById(taskId);
    }
}
