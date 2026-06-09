from database.database import engine

try:
    from database.database import (
    DATABASE_URL
    )


    connection = engine.connect()

    print(
        "Database Connected Successfully"
    )

    connection.close()

except Exception as e:

    print(
        f"Connection Error: {e}"
    )