import time
import qrcode
import cv2
import mysql.connector as connector
import tkinter as tk
from datetime import date
import pygame
from gtts import gTTS
import os
import psutil
import pyttsx3
import pandas as pd
file = pd.read_csv('attendance_sheet.csv')
#file.loc[0,"Name"] ="Ranjeet"
#print(file)



'''
pygame.mixer.init()
sound_file = "present.mp3"
def play_sound():
    pygame.mixer.music.load(sound_file)  # Load the MP3 file
    pygame.mixer.music.play()
'''
def get_music_process_id():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'your_music_player_executable.exe':
            return proc.info['pid']
    return None
# Define a list of students as required for every class
students = []

class DBhelper:
    def __init__(self):
        self.con=connector.connect(
	host = "localhost",
	user = "root",
	password = "subham",
        database="student_data" )

        query='create table if not exists student(StudentId int primary key ,StudentName varchar(200),enorll_No varchar (20))'
        
        cur=self.con.cursor()
        cur.execute(query)
        print("Created")

    #insert user
    def insert_user(self,StudentId ,StudentName, enroll_No):
        query="insert into student(StudentId,StudentName,enorll_No) values({},'{}','{}')".format(StudentId,StudentName,enroll_No)
        print(query)
        cur=self.con.cursor()
        cur.execute(query)
        self.con.commit()
        print("user saved to db")

    def fetch_all(self):
        query="select * from student"  
        cur= self.con.cursor()
        cur.execute(query)
        for row in cur:
            print(row)
            students.append(row[1])

    def add_date_col(self,date):
        
        query='ALTER TABLE student ADD '+date+' varchar(20)'
        cur=self.con.cursor()
        cur.execute(query)
        self.con.commit()

    def add_att(self,date,stat):
        query2="insert into student({}) values('{}')".format(date,stat)
        cur=self.con.cursor()
        cur.execute(query2)

    
        
    
            

helper=DBhelper()
#helper.insert_user(3,"Ranjeet","567")
helper.fetch_all()

# Generate QR code for each student

for student in students:
    
    # Create a unique code for each student
    qr_code = qrcode.make(student)
    #file.loc[i,"Name"] =student
    # Save the QR code as an image file
    qr_code.save(f"{student}.png")
    

# Initialize camera

cap = cv2.VideoCapture(0)

# Load attendance lists
attendance = {student: False for student in students}

# Capture video until 'q' key is pressed
while True:
    
    '''
    file_name = "output.mp3"
    if os.path.exists(file_name):
            # Delete the file
            os.remove(file_name)
    '''
    # Read a frame from the camera
    ret, frame = cap.read()
    
    # Display the frame
    cv2.imshow('frame', frame)
    
    # Decode QR code
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(frame)

    c=0
    # Mark student as present
    if data in students:
        
        attendance[data] = True
        '''
        for index,row in file.iterrows():
            if file.loc[index,"Name"]==data:
                file.loc[index,"Status"]="Present"
            else:
                file.loc[index,"Status"]="Absent"
        
        pygame.mixer.init()
        text=data+"Present"
        tts = gTTS(text)
        #tts.save("output"+str(a)+".mp3")
        #sound_file = "output"+str(a)+".mp3"
        tts.save("output.mp3")
        sound_file = "output.mp3"
        pygame.mixer.music.load(sound_file)  # Load the MP3 file
        pygame.mixer.music.play()
        time.sleep(5)
        '''
        # Initialize the text-to-speech engine
        engine = pyttsx3.init()

        # Set the speech rate (optional)
        engine.setProperty('rate', 150)  # You can adjust the value as needed

        # Set the speech volume (optional)
        engine.setProperty('volume', 1.0)  # You can adjust the value between 0 and 1

        # Specify the text to be spoken
        text = data+ "present"

        # Speak the text
        engine.say(text)
        engine.runAndWait()
        
    
    # Quit program when 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break

print(file)
# Release camera and close windows
cap.release()
cv2.destroyAllWindows()

today = date.today()
#d1 = today.strftime("%d/%m/%Y")
#helper.add_date_col("jeet")



# Print attendance report
print("====================================")
print("      Attendance Report:")
print("====================================")
i=0
for student, present in attendance.items():
    status = "Present" if present else "Absent"
    print(f"{student}: {status}")
    #helper.add_att("jeet",status)
    file.loc[i,"Name"]=student
    file.loc[i,"Status"]=status
    i+=1
    

print("====================================")
print(file)
file.to_csv('attendance_sheet.csv', index=False)
wait=input()
print("press q fo exit")

