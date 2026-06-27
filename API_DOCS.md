# API Documentation

## Endpoints

### Auth

#### `POST /auth/signup`

Signup


#### `POST /auth/login`

Login


#### `POST /auth/password-reset-request`

Password Reset Request


#### `POST /auth/password-reset`

Password Reset


### Dashboard

#### `GET /dashboard/weekly`

Get Weekly Dashboard


### Habit

#### `GET /habits`

List Habits


#### `POST /habits`

Create Habit


#### `GET /habits/{habit_id}`

Get Habit


#### `PUT /habits/{habit_id}`

Update Habit


#### `DELETE /habits/{habit_id}`

Delete Habit


#### `POST /habits/{habit_id}/log`

Create Habit Log


#### `GET /habits/{habit_id}/logs`

List Habit Logs


#### `DELETE /habits/{habit_id}/logs/{log_id}`

Delete Habit Log


### User

#### `GET /users/me`

Read Current User


#### `PUT /users/me`

Update Current User

