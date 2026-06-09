from database.database import (
    engine
)

from database.model import (
    Base
)

Base.metadata.create_all(
    bind=engine
)

print(
    "Tables Created Successfully"
)