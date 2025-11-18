from . import models, hashing
from .database import MY_SESSION_MAKER


def create_or_update_admin():
    db = MY_SESSION_MAKER()

    admin_username = "admin"
    admin_email = "admin@example.com"
    admin_password = "Admin@123"

    existing_admin = (
        db.query(models.Users)
        .filter(models.Users.username == admin_username)
        .first()
    )

    if existing_admin:
        # UPDATE existing admin
        existing_admin.email = admin_email
        existing_admin.password = hashing.Hash.argon2(admin_password)
        existing_admin.role = "admin"

        db.commit()
        db.close()
        print("Admin user updated successfully!")
        return

    # CREATE a new admin
    new_admin = models.Users(
        username=admin_username,
        email=admin_email,
        password=hashing.Hash.argon2(admin_password),
        role="admin"
    )

    db.add(new_admin)
    db.commit()
    db.close()

    print("Admin user created successfully!")


create_or_update_admin()
