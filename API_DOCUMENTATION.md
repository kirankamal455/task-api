# Task Manager API Documentation

## Base URL
Local: `http://127.0.0.1:8000`
Production: `(Your Render/Heroku URL)`
## 📬 Postman Collection

[Download Task Manager API Collection](./postman-collection/TaskManageAPi.postman_collection.json)

## Authentication
All endpoints require a `user_id` query parameter context-switching between users.
Example: `?user_id=test_user`

## Data Models

### Task Object
| Field | Type | Description | Allowed Values |
|Data Type|Type|Description|Notes|
|---|---|---|---|
| `id` | Integer | Unique ID of the task | Auto-generated |
| `title` | String | Title of the task | Required |
| `description` | String | Detailed description | Optional |
| `is_completed` | Boolean | Completion status | Default: `false` |
| `priority` | String (Enum) | Task priority | `Low`, `Medium`, `High` |
| `category` | String (Enum) | Task category | `Work`, `Personal`, `Health`, `Finance`, `Education`, `Shopping`, `Travel`, `Others` |
| `due_date` | Datetime | Due date (ISO 8601) | Optional |
| `created_at` | Datetime | Creation timestamp | Auto-generated |
| `updated_at` | Datetime | Last update timestamp | Auto-updated |

## Endpoints

### 1. Create Task
**POST** `/tasks/?user_id={user_id}`

**Request Body:**
```json
{
  "title": "Buy Groceries",
  "description": "Milk, Bread, Eggs, Vegetables",
  "is_completed": false,
  "due_date": "2026-02-15T19:00:00",
  "priority": "Medium",
  "category": "Personal"
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Task created successfully",
  "data": {
    "id": 12,
    "title": "Buy Groceries",
    "description": "Milk, Bread, Eggs, Vegetables",
    "is_completed": false,
    "due_date": "2026-02-15T19:00:00",
    "priority": "Medium",
    "category": "Personal",
    "created_at": "2026-02-12T13:25:40"
  }
}
```

### 2. List Tasks
**GET** `/tasks/?user_id={user_id}&skip=0&limit=10`

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Number of records to return (default: 100)

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Tasks retrieved successfully",
  "data": [
    { ...task_object... },
    { ...task_object... }
  ],
  "total": 15
}
```

### 3. Get Single Task
**GET** `/tasks/{task_id}?user_id={user_id}`

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Task retrieved successfully",
  "data": { ...task_object... }
}
```

### 4. Update Task
**PUT** `/tasks/{task_id}?user_id={user_id}`

**Request Body** (Any field is optional):
```json
{
  "is_completed": true,
  "priority": "Low"
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Task updated successfully",
  "data": { ...updated_task_object... }
}
```

### 5. Delete Task
**DELETE** `/tasks/{task_id}?user_id={user_id}`

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Task 123 deleted successfully",
  "data": null
}
```

## Error Handling
Errors are returned in a standard JSON format:
```json
{
  "status": "error",
  "message": "Validation Error",
  "data": null
}
```
**Common Codes:**
- `422 Unprocessable Entity`: Invalid data (e.g., wrong Enum value).
- `404 Not Found`: Task does not exist.
