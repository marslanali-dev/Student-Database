# Student Results API

A FastAPI application for managing student results stored in a Neon PostgreSQL database.

## Setup

1. **Clone or download this project**

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   - Windows: `.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up Neon Database:**
   - Create a Neon account at https://neon.tech
   - Create a new project
   - Copy the connection string from the Neon dashboard

6. **Create environment file:**
   - Copy `.env.example` to `.env`
   - Replace the DATABASE_URL with your actual Neon connection string
   - The connection string should look like: `postgresql://username:password@hostname/database_name`

7. **Run the application:**
   ```bash
   uvicorn main:app --reload
   ```

8. **Access the API:**
   - Open http://localhost:8000 in your browser
   - API documentation: http://localhost:8000/docs

## API Endpoints

- `GET /` - Welcome message
- `POST /results/` - Create a new student result
- `GET /results/` - Get all student results (with pagination)
- `GET /results/{result_id}` - Get a specific student result
- `PUT /results/{result_id}` - Update a student result
- `DELETE /results/{result_id}` - Delete a student result

## Student Result Model

```json
{
  "student_name": "string",
  "subject": "string",
  "score": "float",
  "grade": "string"
}
```

## Example Usage

Create a student result:
```bash
curl -X POST "http://localhost:8000/results/" \
     -H "Content-Type: application/json" \
     -d '{
       "student_name": "John Doe",
       "subject": "Mathematics",
       "score": 95.5,
       "grade": "A"
     }'
```

Get all results:
```bash
curl -X GET "http://localhost:8000/results/"
```