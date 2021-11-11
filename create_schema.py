import argparse
import uuid

from dotenv import load_dotenv

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mock", dest="requested_mock_data", action="store_true")
args = parser.parse_args()

success = load_dotenv(".env.development")

if success:
    from app import db

    db.create_all()

    if args.requested_mock_data:

        def add_commit_rows(*rows):
            for row in rows:
                db.session.add(row)
            db.session.commit()

        from app import User, Upload, Feedback
        from psycopg2.extras import NumericRange

        user1 = User(
            first_name="Jadon",
            last_name="Fan",
            email="j53fan@uwaterloo.ca",
            firebase_token=uuid.uuid4(),
            is_admin=True,
        )
        user2 = User(
            first_name="Chandler",
            last_name="Lei",
            email="q4lei@uwaterloo.ca",
            firebase_token=uuid.uuid4(),
            is_admin=True,
        )
        add_commit_rows(user1, user2)

        upload1 = Upload(category=Upload.Category.INTERVIEW, user_id=user1.id)
        upload2 = Upload(category=Upload.Category.PRESENTATION, user_id=user1.id)
        upload3 = Upload(category=Upload.Category.INTERVIEW, user_id=user1.id)
        add_commit_rows(upload1, upload2, upload3)

        feedback1 = Feedback(
            type=Feedback.Type.SENTIMENT,
            text="testing...",
            score=2.5,
            time_range=NumericRange(1, 10),
            user_report="is this working?",
            upload_id=upload1.id,
        )
        add_commit_rows(feedback1)
