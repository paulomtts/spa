from faker import Faker
from .component import TableColumn, ColumnAlign


def generate_user_data(
    count: int = 10,
) -> tuple[list[dict[str, any]], list[TableColumn]]:
    """Generate sample user data using Faker."""
    fake = Faker()
    users = []
    statuses = ["active", "inactive", "pending", "suspended"]

    for i in range(count):
        user = {
            "id": i + 1,
            "name": fake.name(),
            "email": fake.email(),
            "status": fake.random_element(statuses),
            "created_at": fake.date_this_year().strftime("%Y-%m-%d"),
            "class_name": "bg-yellow-50" if (i + 1) % 3 == 0 else "",
        }
        users.append(user)

    columns = [
        TableColumn(label="Name", key="name", align=ColumnAlign.LEFT),
        TableColumn(label="Email", key="email", align=ColumnAlign.LEFT),
        TableColumn(label="Status", key="status", align=ColumnAlign.CENTER),
        TableColumn(label="Created", key="created_at", align=ColumnAlign.RIGHT),
    ]

    return users, columns
