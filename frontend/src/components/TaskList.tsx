import React, { useState, useEffect } from 'react'
import api from '../services/api';
import { Link } from 'react-router-dom'

interface Task {
    id: number;
    title: string;
    description: string;
    dueDate: string
    completed: boolean;
}

const TaskList: React.FC = () => {

    const [tasks, setTasks] = useState<Task[]>([]);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        // Fetch tasks when component mounts
        const fetchTasks = async () => {
            try {
                const response = await api.get<Task[]>('/tasks');
                // // Note: With OAuth, we will need to pass `Bearer ${token}`
                // const response = await api.get<Task[]>('/tasks', {
                //     headers: {
                //         Authorization: `Bearer ${localStorage.getItem('token')}`
                //     }
                // });
                setTasks(response.data);
                setError(null);
            }
            catch (error) {
                console.log('Error fetching tasks', error);
                setError('Error fetching tasks. Please try again.');
            }
        }

        fetchTasks()
    }, [])

    const handleComplete = async (id: number) => {
        try {
            // Note: With OAuth, we will need to pass `Bearer ${token}`
            // Update task completion status
            await api.put(`/tasks/${id}`, { completed: true });
            setTasks(tasks.map(task => {
                if (task.id === id) {
                    task.completed = !task.completed;
                }
                return task;
            }))
            setError(null);
        } catch (error) {
            console.log('Error completing task', error)
            setError('Error completing task. Please try again.');
        }
    }

    if (error) {
        return <div>Error: {error}</div>
    }

    return (
        <div>
            <h1>Tasks</h1>
            <Link to="/new-task">Add Task</Link>
            <ul>
                {tasks.map(task => (
                    <li key={task.id}>
                        {task.title} - {task.dueDate}
                        {!task.completed && <button onClick={() => handleComplete(task.id)}>Complete</button>}
                    </li>
                ))}
            </ul>
        </div>
    )
}

export default TaskList;