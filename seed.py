from app.db.session import engine
from app.models import User, Company, Contract, Rule
from sqlalchemy.orm import Session
from datetime import datetime, timezone

with Session(engine) as db:

    # guard — skip if already seeded
    if db.query(User).first():
        print("Already seeded, skipping.")
        exit()

    # seed users
    user1 = User(name="John", age=25, nationality="IN", date_of_birth=datetime(1999, 1, 1))
    user2 = User(name="Jane", age=17, nationality="US", date_of_birth=datetime(2007, 1, 1))

    # seed companies
    company1 = Company(name="Acme Corp", industry="Logistics", country="IN", bank_deposit=500000.00)

    db.add_all([user1, user2, company1])
    db.flush()  # assigns IDs without committing so we can use them below

    # seed contracts
    contract1 = Contract(
        user_id=user1.id,
        company_id=company1.id,
        start_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
        end_date=datetime(2025, 1, 1, tzinfo=timezone.utc),
        country="IN",
        is_active=True
    )
    contract2 = Contract(
        user_id=user2.id,
        company_id=company1.id,
        start_date=datetime(2024, 6, 1, tzinfo=timezone.utc),
        end_date=datetime(2025, 6, 1, tzinfo=timezone.utc),
        country="US",
        is_active=True
    )

    # seed rules
    rule1 = Rule(field_name="User.age", operator=">=", value="18")
    rule2 = Rule(field_name="Company.bank_deposit", operator=">", value="100000")
    rule3 = Rule(field_name="User.nationality", operator="==", value="IN")

    db.add_all([contract1, contract2, rule1, rule2, rule3])
    db.commit()

print("Seeded successfully!")