# Assignment 2 Grading: zhanghungyuli

**Final Score: 79/100 (C+)**

## Summary
- Database Models: 16/20
- Task Endpoints: 27/30
- Category Endpoints: 13/15
- Background Tasks: 7/15
- Docker Compose: 16/20

## Detailed Results

### Database Models (16/20)

❌ **DB-01**: Task model has all required fields
   - Score: 4/8
   - Deduction: Missing required fields: ['created_at', 'updated_at'] (-4 pts, major)

✅ **DB-02**: Category model with unique name constraint
   - Score: 6/6
   - Correctly rejects duplicate category name (status 400)

✅ **DB-03**: Task-Category relationship (task belongs to category)
   - Score: 6/6
   - Task includes nested category object

### Task Endpoints with Validation (27/30)

✅ **TASK-01**: GET /tasks returns list of all tasks
   - Score: 4/4
   - Returns list of 2 tasks

✅ **TASK-02**: GET /tasks?completed=false filters by completion status
   - Score: 4/4
   - Filter returns 4 incomplete tasks

✅ **TASK-03**: GET /tasks/:id returns single task with category info
   - Score: 3/3
   - Returns single task object

✅ **TASK-04**: GET /tasks/:id returns 404 when not found
   - Score: 2/2
   - Correctly returns 404

✅ **TASK-05**: POST /tasks creates task, returns 201
   - Score: 4/4
   - Creates task and returns 201 with task object

✅ **TASK-06**: POST /tasks validates input (title required, length limits)
   - Score: 4/4
   - Validation working: 4/4 tests passed

✅ **TASK-07**: Validation errors include structured messages
   - Score: 2/2
   - Structured error response: {"code": 422, "errors": {"json": {"title": ["Missing data for required field."]}}, "status": "Unprocessable Entity"}

❌ **TASK-08**: PUT /tasks/:id updates task, returns 200
   - Score: 0/3
   - Deduction: Returns 422 for PUT update (-3 pts, major)

✅ **TASK-09**: PUT /tasks/:id returns 404 when not found
   - Score: 1/1
   - Correctly returns 404

✅ **TASK-10**: DELETE /tasks/:id deletes task, returns 200 with message
   - Score: 2/2
   - Returns success for DELETE

✅ **TASK-11**: DELETE /tasks/:id returns 404 when not found
   - Score: 1/1
   - Correctly returns 404

### Category Endpoints (13/15)

❌ **CAT-01**: GET /categories returns categories with task_count
   - Score: 3/5
   - Returns 2 categories but missing task_count
   - Deduction: Categories missing task_count field (-2 pts, minor)

✅ **CAT-02**: GET /categories/:id returns category with its tasks
   - Score: 3/3
   - Returns category with tasks array (0 tasks)

✅ **CAT-03**: POST /categories validates unique name and hex color
   - Score: 4/4
   - Category validation working: 4/4 tests passed

✅ **CAT-04**: DELETE /categories/:id prevents deletion with existing tasks
   - Score: 3/3
   - Correctly prevents deletion of category with tasks (400)

### Background Task Processing (7/15)

✅ **BG-01**: Redis and rq worker properly configured
   - Score: 4/4
   - Redis and worker services defined in docker-compose.yml

❌ **BG-02**: notification_queued: true when due_date within 24h
   - Score: 0/5
   - Deduction: POST not responding (-5 pts, critical)

❌ **BG-03**: notification_queued: false when no due_date or > 24h
   - Score: 2/3
   - Deduction: Partial: one of two false-notification tests passed (-1 pts, minor)

❌ **BG-04**: Background job executes (worker logs show reminder)
   - Score: 1/3
   - Worker logs present but no 'Reminder' message found
   - Deduction: Worker running but no reminder message in logs (-2 pts, minor)

### Docker Compose (16/20)

❌ **DOCK-01**: docker-compose.yml defines all 4 services (app, db, redis, worker)
   - Score: 3/5
   - Found services: ['api', 'redis', 'worker']
   - Deduction: Missing services: ['db'] (-2 pts, major)

❌ **DOCK-02**: docker-compose up --build runs without errors
   - Score: 6/8
   - docker-compose up --build succeeded, all containers running
   - Deduction: Code/config issue fixed for grading (broken migration/missing migrations/circular import) (-2 pts, minor)

✅ **DOCK-03**: All services connect properly (app to db+redis, worker to redis)
   - Score: 4/4
   - Connectivity verified through functional endpoint tests

✅ **DOCK-04**: API is accessible and functional on configured port
   - Score: 3/3
   - API accessible at http://127.0.0.1:5050 (port 5050)

## Strengths
- Redis and rq worker properly configured
- All services connect properly (app to db+redis, worker to redis)
- API is accessible and functional on configured port
- Category model with unique name constraint
- Task-Category relationship (task belongs to category)

## Areas for Improvement
- docker-compose.yml defines all 4 services (app, db, redis, worker): Missing services: ['db']
- docker-compose up --build runs without errors: Code/config issue fixed for grading (broken migration/missing migrations/circular import)
- Task model has all required fields: Missing required fields: ['created_at', 'updated_at']
- PUT /tasks/:id updates task, returns 200: Returns 422 for PUT update
- GET /categories returns categories with task_count: Categories missing task_count field
- notification_queued: true when due_date within 24h: POST not responding
- notification_queued: false when no due_date or > 24h: Partial: one of two false-notification tests passed
- Background job executes (worker logs show reminder): Worker running but no reminder message in logs
