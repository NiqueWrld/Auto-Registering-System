import firebase_admin
from firebase_admin import credentials, db
import datetime

# Initialize Firebase Admin SDK
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://auto-register---arm-lab-default-rtdb.firebaseio.com/'  # Replace with your Realtime Database URL
})
# Reference to Realtime Database
ref = db.reference('students')

while True:
    studentNo = input("Enter student number: ")

    # Check if the student number is valid
    if len(studentNo) == 8 and studentNo.startswith('2'):
        print(f"Valid student number: {studentNo}")
        
        # Get today's date to use as the key
        today_date = datetime.datetime.now().strftime('%Y-%m-%d')  # Format as YYYY-MM-DD
        
        # Create a reference for today's date
        student_ref = ref.child(today_date)

        # Get the existing data for today's date (if any)
        existing_students = student_ref.get()

        # Check if the student number is already checked in for today
        if existing_students:
            # Filter out null values and check if the student number is already checked in
            student_numbers = [entry.get('student_number') for entry in existing_students if entry]
            if studentNo in student_numbers:
                print(f"Student number {studentNo} has already checked in today.")
            else:
                # Find the next available index (after filtering out nulls)
                next_index = len([entry for entry in existing_students if entry]) + 1

                # Push the student number to Firebase Realtime Database with a sequential index
                student_ref.child(str(next_index)).set({
                    'student_number': studentNo
                })
                print(f"Student number {studentNo} added to Firebase Realtime Database under the key {today_date}/{next_index}")
        else:
            # If no existing students, add as the first entry
            student_ref.child('1').set({
                'student_number': studentNo
            })
            print(f"Student number {studentNo} added to Firebase Realtime Database under the key {today_date}/1")
        
    else:
        print("Invalid student number")
