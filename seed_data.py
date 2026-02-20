# Script to be run to import 10 users and 10 opportunities into the app
from app import app
from models import db, User, Opportunity
from datetime import datetime

def seed_users():
    users_data = [
        {"name": "Scott McLaughlin",      "email": "scott.mclaughlin@royalmail.com",       "role": "admin"},
        {"name": "Promise Akwaowo",       "email": "promise.akwaowo@royalmail.com",        "role": "admin"},
        {"name": "Olivia Mendel-Portnoy", "email": "olivia.mendel-portnoy@royalmail.com",  "role": "admin"},
        {"name": "Samuel May",            "email": "samuel.may@royalmail.com",             "role": "regular"},
        {"name": "Tom Mosforth-Hunt",     "email": "tom.mosforth-hunt@royalmail.com",      "role": "regular"},
        {"name": "Priya Udhayabhanu",     "email": "priya.udhayabhanu@royalmail.com",      "role": "regular"},
        {"name": "Andrew Cannon",         "email": "andrew.cannon@royalmail.com",          "role": "regular"},
        {"name": "Daniel Cross",          "email": "daniel.cross@royalmail.com",           "role": "regular"},
        {"name": "Neale Jarrett",         "email": "neale.jarrett@royalmail.com",          "role": "regular"},
        {"name": "Agata Lee",             "email": "agata.lee@royalmail.com",              "role": "regular"},
    ]
    created_count = 0

    for udata in users_data:
        existing = User.query.filter_by(email=udata["email"]).first()
        if existing:
            print(f"User already exists, skipping: {udata['email']}")
            continue

        user = User(
            name=udata["name"],
            email=udata["email"],
            role=udata["role"],
        )

        if udata["role"] == "admin":
            user.set_password("Admin!")
        else:
            user.set_password("Password!")
        db.session.add(user)
        created_count += 1
    db.session.commit()
    print(f"Users seeding complete. New users created: {created_count}")


def seed_opportunities():
    opportunities_data = [
        {
            "title": "Automated Linehaul Allocation",
            "description": "Automate allocation of linehaul routes based on volumetrics and depot capacity.",
            "business_unit": "Logistics",
            "predicted_benefits": "Reduced manual planning and improved delivery reliability.",
            "business_criticality": "High",
            "status": "Qualified",
            "value_score": 82,
            "effort_score": 55,
            "submitter_email": "scott.mclaughlin@royalmail.com",
        },
        {
            "title": "OCR-Based Address Validation",
            "description": "Use OCR and machine learning to validate handwritten addresses before sorting.",
            "business_unit": "Processing",
            "predicted_benefits": "Higher sorting accuracy and reduced manual keying effort.",
            "business_criticality": "Critical",
            "status": "In Discovery",
            "value_score": 90,
            "effort_score": 70,
            "submitter_email": "promise.akwaowo@royalmail.com",
        },
        {
            "title": "Automated Demand Intake Reporting",
            "description": "Generate daily dashboards showing intake levels, prioritisation scores and triage bottlenecks.",
            "business_unit": "RAD Team",
            "predicted_benefits": "Improved transparency of the triage process across the organisation.",
            "business_criticality": "Medium",
            "status": "Under Review",
            "value_score": 75,
            "effort_score": 40,
            "submitter_email": "olivia.mendel-portnoy@royalmail.com",
        },
        {
            "title": "Delivery Route Compliance Checker",
            "description": "Automate validation of delivery route completion against planned time windows.",
            "business_unit": "Delivery Operations",
            "predicted_benefits": "Increased SLA compliance and reduced manual audit effort.",
            "business_criticality": "Medium",
            "status": "New",
            "value_score": None,
            "effort_score": None,
            "submitter_email": "samuel.may@royalmail.com",
        },
        {
            "title": "Vehicle Maintenance Reminder Automation",
            "description": "Automatically track vehicle mileage and generate maintenance reminders.",
            "business_unit": "Fleet",
            "predicted_benefits": "Reduced downtime through preventative maintenance.",
            "business_criticality": "Low",
            "status": "New",
            "value_score": None,
            "effort_score": None,
            "submitter_email": "tom.mosforth-hunt@royalmail.com",
        },
        {
            "title": "Parcel Reconciliation Automation",
            "description": "Automate reconciliation of mismatched parcel records between depots and delivery units.",
            "business_unit": "Parcels",
            "predicted_benefits": "Fewer lost parcels and improved auditability.",
            "business_criticality": "High",
            "status": "New",
            "value_score": None,
            "effort_score": None,
            "submitter_email": "priya.udhayabhanu@royalmail.com",
        },
        {
            "title": "Staff Roster Auto-Generation",
            "description": "Automatically generate weekly rosters based on availability, skills and business rules.",
            "business_unit": "HR / Operations",
            "predicted_benefits": "Saves planners time each week and improves fairness of allocation.",
            "business_criticality": "Medium",
            "status": "Under Review",
            "value_score": None,
            "effort_score": None,
            "submitter_email": "andrew.cannon@royalmail.com",
        },
        {
            "title": "Customer Refund Automation",
            "description": "Automate refund processing for delayed tracked items using scan data.",
            "business_unit": "Customer Services",
            "predicted_benefits": "Faster refunds for customers and reduced manual back-office effort.",
            "business_criticality": "High",
            "status": "New",
            "value_score": None,
            "effort_score": None,
            "submitter_email": "daniel.cross@royalmail.com",
        },
        {
            "title": "Depot Stock Level Alerts",
            "description": "Automatically alert managers when packaging materials fall below threshold levels.",
            "business_unit": "Supplies",
            "predicted_benefits": "Prevents stock-outs and operational disruption.",
            "business_criticality": "Low",
            "status": "New",
            "value_score": None,
            "effort_score": None,
            "submitter_email": "neale.jarrett@royalmail.com",
        },
        {
            "title": "International Package Manifest Checker",
            "description": "Validate export declarations and customs data before international dispatch.",
            "business_unit": "International Mail",
            "predicted_benefits": "Reduces customs delays and compliance issues.",
            "business_criticality": "High",
            "status": "New",
            "value_score": None,
            "effort_score": None,
            "submitter_email": "agata.lee@royalmail.com",
        },
    ]

    emails = [o["submitter_email"] for o in opportunities_data]
    users = User.query.filter(User.email.in_(emails)).all()
    user_by_email = {u.email: u for u in users}

    created_count = 0

    for odata in opportunities_data:
        existing = Opportunity.query.filter_by(title=odata["title"]).first()
        if existing:
            print(f"Opportunity already exists, skipping: {odata['title']}")
            continue

        submitter_email = odata["submitter_email"]
        submitter = user_by_email.get(submitter_email)

        if not submitter:
            print(f"Submitter not found for email {submitter_email}, skipping opportunity {odata['title']}")
            continue

        opp = Opportunity(
            title=odata["title"],
            description=odata["description"],
            business_unit=odata["business_unit"],
            predicted_benefits=odata["predicted_benefits"],
            business_criticality=odata["business_criticality"],
            status=odata["status"],
            submitted_by=submitter.user_id,
            date_submitted=datetime.now(),
        )

        if odata.get("value_score") is not None:
            opp.value_score = odata["value_score"]
        if odata.get("effort_score") is not None:
            opp.effort_score = odata["effort_score"]

        db.session.add(opp)
        created_count += 1

    db.session.commit()
    print(f"Opportunities seeding complete. New opportunities created: {created_count}")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        seed_users()
        seed_opportunities()

        print("Seeding finished.")