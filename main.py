from fastapi import FastAPI, HTTPException
import pyodbc


# Database configuration
DB_CONFIG = {
    "DRIVER": "{SQL Server}",
    "SERVER": "26.67.197.81",
    "DATABASE": "Accounting",
    "UID": "sa",
    "PWD": "123456",
}

# FastAPI app instance
app = FastAPI()

# Function to create a database connection
def get_db_connection():
    try:
        conn = pyodbc.connect(
            f"DRIVER={DB_CONFIG['DRIVER']};"
            f"SERVER={DB_CONFIG['SERVER']};"
            f"DATABASE={DB_CONFIG['DATABASE']};"
            f"UID={DB_CONFIG['UID']};"
            f"PWD={DB_CONFIG['PWD']}"
        )
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")


# Endpoint to fetch student details by CardId
@app.get("/students/{card_id}")
def get_student(card_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT [StudentId], [UniversityId], [CardId], [StudentName], 
                   [Money], [Phone], [FacultyId], [DepartId], [YearId], [date]
            FROM [dbo].[Students] 
            WHERE [CardId] = ?
        """, (card_id,))

        student = cursor.fetchone()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        return {
            "StudentId": student[0],
            "UniversityId": student[1],
            "CardId": student[2],
            "StudentName": student[3],
            "Money": student[4],
            "Phone": student[5],
            "FacultyId": student[6],
            "DepartId": student[7],
            "YearId": student[8],
            "date": student[9]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()

