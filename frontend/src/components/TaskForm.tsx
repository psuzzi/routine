import React, { useState } from 'react'
import api from '../services/api';
import { useNavigate } from 'react-router-dom'

const TaskForm: React.FC = () => {
    const [title, setTitle] = useState<string>('')
    const [description, setDescription] = useState<string>('')
    const [dueDate, setDueDate] = useState<string>('')
    const navigate = useNavigate()

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        try {
            // Note: With OAuth, we will need to pass token Bearer
            await api.post("/tasks", {
                title,
                description,
                dueDate
            });
            navigate("/tasks");
        } catch (error) {
            console.log('Error creating task', error);
        }
    }

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                placeholder="Title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
            />
            <input
                type="text"
                placeholder="Description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
            />
            <input
                type="date"
                placeholder="Due Date"
                value={dueDate}
                onChange={(e) => setDueDate(e.target.value)}
            />
            <button type="submit">Create Task</button>
        </form>
    )
}

export default TaskForm;