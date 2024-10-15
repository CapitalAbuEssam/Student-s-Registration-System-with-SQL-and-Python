# All import packages
import pymysql
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ttkthemes as ttkth
from ttkthemes import ThemedTk
from collections import Counter

# Connection for Database
def connection():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='password',
        db='students_db',
    )
    return conn

def classify_gender(gender_code):
    # Map the gender code to the actual gender
    if gender_code == 'Male':
        return 'Male'
    elif gender_code == 'Female':
        return 'Female'
    else:
        return 'Other'  # You can handle other cases as needed

def show_gender_distribution():
    # Retrieve data from the database
    with connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT GENDER FROM students")
        results = cursor.fetchall()

    # Print the raw results for debugging
    raw_data_message = "Raw gender data from database:\n" + str(results)
    messagebox.showinfo("Debug Information", raw_data_message)

    # Classify each student's gender
    classified_genders = [classify_gender(gender[0]) for gender in results]

    # Print the classified genders for debugging
    classified_data_message = "Classified genders:\n" + str(classified_genders)
    messagebox.showinfo("Debug Information", classified_data_message)

    # Count the occurrences of each gender
    gender_counts = Counter(classified_genders)

    # Print the gender counts for debugging
    gender_counts_message = "Gender counts:\n" + str(gender_counts)
    messagebox.showinfo("Debug Information", gender_counts_message)

    # Plot the bar graph
    fig, ax = plt.subplots()
    genders = gender_counts.keys()
    counts = gender_counts.values()
    ax.bar(genders, counts, color=['pink', 'blue'])

    # Add labels and title
    plt.xlabel('Gender')
    plt.ylabel('Number of Students')
    plt.title('Gender Distribution Among Students')

    # Display the plot in a new window
    plt.show()



def show_graph():
    # Retrieve data from the database
    with connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COURSEID FROM students")
        results = cursor.fetchall()

    # Extract course IDs
    course_ids = [result[0] for result in results]

    # Count the occurrences of each course ID
    course_counts = Counter(course_ids)

    # Plot the pie chart
    fig, ax = plt.subplots()
    ax.pie(course_counts.values(), labels=course_counts.keys(), autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.

    # Display the plot in a new window
    plt.title('Distribution of Courses Among Students')
    plt.show()


def generate_verification_code():
    # Implement a secure way to generate a verification code
    # For simplicity, I'll use a basic hash of the current time
    import time
    return hashlib.sha256(str(time.time()).encode()).hexdigest()[:6]

def send_verification_email(email, verification_code):
    # Update with your email credentials
    sender_email = "databasetestingsender@gmail.com"  # Replace with your email
    sender_password = "rrcv egna qmja qjui"  # Replace with your email password

    subject = "Account Verification Code"
    body = f"Your verification code is: {verification_code}"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, message.as_string())
        messagebox.showinfo("Email Sent", "Email sent successfully. Please check your email for the verification code.")
    except Exception as e:
        messagebox.showinfo("Error", f"Email sending failed: {e}")

def create_account_window():
    global email_entry
    global password_entry
    global user_type_var  # Declare user_type_var as global


    def create_account():
        email = email_entry.get()
        password = password_entry.get()
        user_type = user_type_var.get()

        # Check if email and password are provided
        if not email or not password:
            messagebox.showinfo("Error", "Please provide both email and password.")
            return

        # Send verification email
        verification_code = generate_verification_code()
        send_verification_email(email, verification_code)
        messagebox.showinfo("Debug", "Verification email sent. Waiting for user input.")

        # Admin verifies and generates a verification code
        user_input_verification_code = simpledialog.askstring("Verification Code", "Enter the verification code sent to your email:")

        # Check if the entered code matches the generated code
        if user_input_verification_code == verification_code:
            messagebox.showinfo("Success", "Account created successfully!")

            # Insert the user details into the database, including the user_type
            with connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO administrators (EMAIL, PASSWORD, USER_TYPE) VALUES (%s, %s, %s)",
                            (email, password, user_type))
                conn.commit()
            messagebox.showinfo("Debug", "Data inserted into the database.")

            create_account_window.destroy()  # Close the create account window
            open_student_registration_gui(email, user_type, root)
        else:
            messagebox.showinfo("Error", "Invalid verification code. Please try again.")

    create_account_window = Toplevel(root)
    create_account_window.title("Create Account")
    create_account_window.geometry("400x300")


    email_label = Label(create_account_window, text="Email", font=('Arial', 15))
    email_entry = Entry(create_account_window, width=30, bd=5, font=('Arial', 15))
    password_label = Label(create_account_window, text="Create password", font=('Arial', 15))
    password_entry = Entry(create_account_window, width=30, bd=5, font=('Arial', 15), show="*")

    user_type_label = Label(create_account_window, text="User Type", font=('Arial', 15))
    user_type_var = StringVar()
    user_type_var.set("user")  # Default to user type
    user_type_radio_user = Radiobutton(create_account_window, text="User", variable=user_type_var, value="user", font=('Arial', 12))
    user_type_radio_admin = Radiobutton(create_account_window, text="Admin", variable=user_type_var, value="admin", font=('Arial', 12))

    create_account_btn = Button(create_account_window, text="Create Account", padx=20, pady=10, width=15, bd=5, font=('Arial', 15), command=create_account)

    email_label.pack(pady=10)
    email_entry.pack(pady=10)
    password_label.pack(pady=5)
    password_entry.pack(pady=10)

    user_type_label.pack(pady=5)
    user_type_radio_user.pack(pady=5)
    user_type_radio_admin.pack(pady=5)

    create_account_btn.pack(pady=20)




def debug_popup(message):
    messagebox.showinfo("Debug Info", message)

def validate_login(email, password):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM administrators WHERE email=%s AND password=%s", (email, password))
    result = cursor.fetchone()
    conn.close()

    # Display debug information in a pop-up window
    debug_message = f"Email: {email}\nPassword: {password}\nQuery result: {result}"
    messagebox.showinfo("Debug Info", debug_message)

    if result:
        # Check the length of the result tuple
        if len(result) >= 4:  # Check the length against the number of columns in your table
            _, email, password, user_type = result[:4]  # Take only the first four values
            debug_message = f"Login successful.\nEmail: {email}\nUser Type: {user_type}"
            messagebox.showinfo("Debug Info", debug_message)
            return True, user_type
        else:
            debug_message = "Invalid database result format."
            messagebox.showinfo("Error", "Invalid database result format.")
    else:
        debug_message = "Invalid username or password."
        messagebox.showinfo("Error", "Invalid username or password.")
        return False, None


def login():
    email = usernameEntry.get()
    password = passwordEntry.get()

    # Validate the login
    success, user_type = validate_login(email, password)

    if success:
        # Show message based on user type
        if user_type == "admin":
            messagebox.showinfo("Login Successful", "Admin login successful!")
        elif user_type == "user":
            messagebox.showinfo("Login Successful", "User login successful!")

        # Open the student registration GUI
        open_student_registration_gui(email, user_type, root)
        
        # Hide the login window
        root.withdraw()
    else:
        messagebox.showinfo("Login Failed", "Invalid username or password")



def open_student_registration_gui(email, user_type, parent_window):
    student_registration_root = ThemedTk(theme="equilux")  # Setting the theme to equilux
    student_registration_root.title("Student Registration System")
    student_registration_root.geometry("1080x720")
    style = ttk.Style()

    # Configure Treeview style
    style.configure("mystyle.Treeview", font=('Arial', 12), rowheight=25)
    my_tree = ttk.Treeview(student_registration_root, style="mystyle.Treeview")     
    style.configure("TButton", font=('Arial', 12))
    

    # Declare my_tree as a local variable
    my_tree = ttk.Treeview(student_registration_root)

    # Set columns and their headings
    my_tree["columns"] = ("Student ID", "First Name", "Last Name", "Address", "Phone", "Gender", "Course ID")
    for col in my_tree["columns"]:
        my_tree.column(col, anchor="w", width=120)
        my_tree.heading(col, text=col, anchor='w')

    my_tree.grid(row=8, column=0, columnspan=5, rowspan=11, padx=10, pady=20, sticky="nsew")


    def refreshTable():
        my_tree.delete(*my_tree.get_children())  # Clear existing data

        # Retrieve all records from the database
        with connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students")
            results = cursor.fetchall()

        # Populate the Treeview with new data
        for array in results:
            my_tree.insert(parent='', index='end', iid=array, text="", values=(array), tag="orow")

        my_tree.tag_configure('orow', background='#EEEEEE', font=('Arial', 12))


    def setph(word, num):
        ph[num - 1].set(word)

    ph1 = tk.StringVar()
    ph2 = tk.StringVar()
    ph3 = tk.StringVar()
    ph4 = tk.StringVar()
    ph5 = tk.StringVar()
    ph6 = tk.StringVar()
    ph7 = tk.StringVar()

    # Labels for the text entry fields
    labels = ["Student ID", "First Name", "Last Name", "Address", "Phone", "Gender", "CourseID"]
    for i, label_text in enumerate(labels):
        label = tk.Label(student_registration_root, text=label_text, font=('Arial', 15))
        label.grid(row=i, column=0, padx=20, pady=(10, 0))

    
    studidEntry = Entry(student_registration_root, width=30, bd=5, font=('Arial', 15), textvariable=ph1)
    fnameEntry = Entry(student_registration_root, width=30, bd=5, font=('Arial', 15), textvariable=ph2)
    lnameEntry = Entry(student_registration_root, width=30, bd=5, font=('Arial', 15), textvariable=ph3)
    addressEntry = Entry(student_registration_root, width=30, bd=5, font=('Arial', 15), textvariable=ph4)
    phoneEntry = Entry(student_registration_root, width=30, bd=5, font=('Arial', 15), textvariable=ph5)
    courseidEntry = Entry(student_registration_root, width=30, bd=5, font=('Arial', 15), textvariable=ph6)
    genderEntry = Entry(student_registration_root, width=30, bd=5, font=('Arial', 15), textvariable=ph7)

    ph = [tk.StringVar() for _ in range(7)]

    def set_placeholder(word, num):
        ph[num - 1].set(word)

    def read():
        with connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students")
            results = cursor.fetchall()
        return results


    def add():
        studid = str(studidEntry.get())
        fname = str(fnameEntry.get())
        lname = str(lnameEntry.get())
        address = str(addressEntry.get())
        phone = str(phoneEntry.get())
        courseid = str(courseidEntry.get())
        gender = str(genderEntry.get())

        try:
            with connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO students VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (studid, fname, lname, address, phone, gender, courseid))
                conn.commit()
        except Exception as e:
            messagebox.showinfo("Error", f"An error occurred while adding data: {e}")
            return

        refreshTable()

    def reset():
        # First warning pop-up
        messagebox.showwarning("Warning", "Resetting will delete all data from the student's table. This action cannot be undone!")

        # Second warning pop-up with a verification step
        verification_sentence = "I understand the consequences of resetting the student's table."
        user_input = simpledialog.askstring("Verification", f"Please type the following sentence:\n\n'{verification_sentence}'\n\nThis is to verify that you understand the consequences.")

        if user_input is None or user_input.strip().lower() != verification_sentence.lower():
            messagebox.showinfo("Verification Failed", "Reset operation canceled. You did not enter the correct verification sentence.")
            return

        # Final confirmation before proceeding with deletion
        decision = messagebox.askquestion("Warning", "Are you sure you want to delete all data? This action cannot be undone.")
        if decision != "yes":
            messagebox.showinfo("Operation Canceled", "Reset operation canceled. No data has been deleted.")
            return
        else:
            try:
                # Perform database reset
                with connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM students")
                    conn.commit()
            except Exception as e:
                messagebox.showinfo("Error", f"Sorry, an error occurred: {e}")
                return

            # Revert button colors and refresh the table
            messagebox.showinfo("Reset Successful", "All data deleted successfully.")
            refreshTable()

    def delete():
        decision = messagebox.askquestion("Warning!!", "Delete the selected data?")
        if decision != "yes":
            return
        else:
            selected_item = my_tree.selection()[0]
            delete_data = str(my_tree.item(selected_item)['values'][0])

            try:
                with connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM students WHERE STUDID=%s", (delete_data,))
                    conn.commit()
            except Exception as e:
                messagebox.showinfo("Error", f"An error occurred while deleting data: {e}")
                return

            refreshTable()

    def select():
        try:
            selected_item = my_tree.selection()[0]
            item_values = my_tree.item(selected_item, 'values')

            if item_values and len(item_values) == 7:
                # Display information about the selected item
                messagebox.showinfo("Selected Item", f"Selected Item ID: {selected_item}\n\nSelected Item Values:\n{item_values}")

                # Update the Entry widgets directly
                studidEntry.delete(0, 'end')
                studidEntry.insert(0, item_values[0])
                
                fnameEntry.delete(0, 'end')
                fnameEntry.insert(0, item_values[1])
                
                lnameEntry.delete(0, 'end')
                lnameEntry.insert(0, item_values[2])
                
                addressEntry.delete(0, 'end')
                addressEntry.insert(0, item_values[3])
                
                phoneEntry.delete(0, 'end')
                phoneEntry.insert(0, item_values[4])

                genderEntry.delete(0, 'end')
                genderEntry.insert(0, item_values[5])

                courseidEntry.delete(0, 'end')
                courseidEntry.insert(0, item_values[6])

                # Display information about the values to be inserted
                messagebox.showinfo("Values to Insert", f"Values to be Inserted:\n"
                                                        f"Student ID: {item_values[0]}\n"
                                                        f"First Name: {item_values[1]}\n"
                                                        f"Last Name: {item_values[2]}\n"
                                                        f"Address: {item_values[3]}\n"
                                                        f"Phone: {item_values[4]}\n"
                                                        f"Gender: {item_values[5]}\n"
                                                        f"Course ID: {item_values[6]}")
            else:
                messagebox.showinfo("Info", "No data found for the selected row or unexpected data format")
        except IndexError:
            messagebox.showinfo("Info", "Please select a data row")
        except Exception as e:
            messagebox.showinfo("Error", f"An error occurred in the select function: {e}")



    def search():
        studid = str(studidEntry.get())
        fname = str(fnameEntry.get())
        lname = str(lnameEntry.get())
        address = str(addressEntry.get())
        phone = str(phoneEntry.get())
        gender = str(genderEntry.get())
        courseid = str(courseidEntry.get())

        with connection() as conn:
            cursor = conn.cursor()

            # Construct the query based on non-empty search parameters
            query = "SELECT * FROM students WHERE"
            conditions = []

            if studid:
                conditions.append("STUDID=%s")
            if fname:
                conditions.append("FNAME LIKE %s")
            if lname:
                conditions.append("LNAME LIKE %s")
            if address:
                conditions.append("ADDRESS LIKE %s")
            if phone:
                conditions.append("PHONE LIKE %s")
            if gender:
                conditions.append("GENDER LIKE %s")
            if courseid:
                conditions.append("COURSEID LIKE %s")

            full_query = query + " " + "OR".join(conditions)

            # Show the query in a message box
            messagebox.showinfo("Executing query", full_query)

            # Construct the values tuple for the parameters
            values = tuple(f"%{param}%" for param in [studid, fname, lname, address, phone, gender, courseid] if param)

            try:
                cursor.execute(full_query, values)
                conn.commit()
                result = cursor.fetchall()

                # Show the result in a message box
                messagebox.showinfo("Query Result", result)

                # Clear existing data in Treeview
                my_tree.delete(*my_tree.get_children())

                # Populate the Treeview with new search result
                for array in result:
                    my_tree.insert(parent='', index='end', iid=array, text="", values=(array), tag="orow")
                    my_tree.tag_configure('orow', background='#EEEEEE', font=('Arial', 12))
            except Exception as e:
                # Show any exceptions in a message box
                messagebox.showinfo("Error", f"An error occurred: {e}")
                messagebox.showinfo("Error", "An error occurred while executing the search")


    def update():
        selected_studid = ""

        try:
            selected_item = my_tree.selection()[0]
            selected_studid = str(my_tree.item(selected_item)['values'][0])
        except IndexError:
            messagebox.showinfo("Error", "Please select a data row")

        studid = str(studidEntry.get())
        fname = str(fnameEntry.get())
        lname = str(lnameEntry.get())
        address = str(addressEntry.get())
        phone = str(phoneEntry.get())
        gender = str(genderEntry.get())
        courseid = str(courseidEntry.get())

        if all(value.strip() == '' for value in [studid, fname, lname, address, phone, gender, courseid]):
            messagebox.showinfo("Error", "Please fill up the blank entry")
            return
        else:
            try:
                with connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE students SET STUDID=%s, FNAME=%s, LNAME=%s, ADDRESS=%s, PHONE=%s, GENDER=%s, COURSEID=%s WHERE STUDID=%s",
                        (studid, fname, lname, address, phone, gender, courseid, selected_studid))
                    conn.commit()
            except pymysql.IntegrityError:
                messagebox.showinfo("Error", "Stud ID already exists")
                return

        refreshTable()

    def resetFields():
        for entry in [studidEntry, fnameEntry, lnameEntry, addressEntry, phoneEntry, genderEntry, courseidEntry]:
            entry.delete(0, END)

    def show_course_info():
        selected_item = my_tree.selection()[0]
        studid = str(my_tree.item(selected_item)['values'][0])

        # Perform the join operation to retrieve course information
        with connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT students.STUDID, students.FNAME, students.LNAME, courses.COURSE_NAME FROM students LEFT JOIN courses ON students.COURSEID = courses.COURSEID WHERE students.STUDID = %s", (studid,))
            result = cursor.fetchall()

        # Display the joined information in a new window or messagebox
        if result:
            course_info_window = Toplevel(root)
            course_info_window.title("Course Information")
            course_info_window.geometry("400x300")

            course_tree = ttk.Treeview(course_info_window, columns=("Course Name",))
            course_tree.heading("Course Name", text="Course Name")
            course_tree.column("Course Name", width=150)

            for row in result:
                course_tree.insert("", "end", values=(row[3],))  # Use row[3] for course name

            course_tree.pack(padx=20, pady=20)
        else:
            messagebox.showinfo("Error", "No course information found for the selected student.")

    def logout():
        student_registration_root.destroy()
        login()  # Replace this with the actual function to open the login GUI


    logoutBtn = Button(student_registration_root, text="Logout", padx=20, pady=10, bd=5, font=('Arial', 12), command=student_registration_root.destroy)
    logoutBtn.grid(row=7, column=5, padx=20, pady=(0, 10))
    
    # Add the new button to the student_registration_root window
    showGenderDistributionBtn = Button(student_registration_root, text="Show Gender Distribution", padx=10, pady=5, bd=5, font=('Arial', 12), command=show_gender_distribution)
    showGenderDistributionBtn.grid(row=7, column=2, padx=10, pady=(0, 10))

    courseidLabel = Label(student_registration_root, text="Course ID", font=('Arial', 15))
    courseidLabel.grid(row=0, column=2, padx=20, pady=(0, 10))

    courseidEntry = Entry(student_registration_root, width=30, bd=5, font=('Arial', 15), textvariable=ph6)
    courseidEntry.grid(row=0, column=3, padx=20, pady=(0, 10))

    genderLabel = Label(student_registration_root, text="Gender", font=('Arial', 15))
    genderLabel.grid(row=1, column=2, padx=20, pady=(0, 10))

    genderEntry = Entry(student_registration_root, width=30, bd=5, font=('Arial', 15), textvariable=ph7)
    genderEntry.grid(row=1, column=3, padx=20, pady=(0, 10))

    studidEntry.grid(row=0, column=1, padx=20, pady=(10, 0))
    fnameEntry.grid(row=1, column=1, padx=20, pady=(0, 10))
    lnameEntry.grid(row=2, column=1, padx=20, pady=(0, 10))
    addressEntry.grid(row=3, column=1, padx=20, pady=(0, 10))
    phoneEntry.grid(row=4, column=1, padx=20, pady=(0, 10))
    
    
    addBtn = Button(student_registration_root, text="Add", padx=20, pady=10, bd=5, font=('Arial', 12), command=add, bg="green", fg="green")
    resetBtn = Button(student_registration_root, text="Reset", padx=20, pady=10, bd=5, font=('Arial', 12), command=reset, bg="red", fg="red")
    deleteBtn = Button(student_registration_root, text="Delete", padx=20, pady=10, bd=5, font=('Arial', 12), command=delete, bg="red", fg="red")
    selectBtn = Button(student_registration_root, text="Select", padx=20, pady=10, bd=5, font=('Arial', 12), command=select, bg="green", fg="green")
    searchBtn = Button(student_registration_root, text="Search", padx=20, pady=10, bd=5, font=('Arial', 12), command=search, bg="green", fg="green")
    updateBtn = Button(student_registration_root, text="Update", padx=20, pady=10, bd=5, font=('Arial', 12), command=update, bg="orange", fg="orange")

    addBtn.grid(row=5, column=0, padx=20, pady=(0, 10))
    resetBtn.grid(row=5, column=1, padx=20, pady=(0, 10), sticky="ew")
    deleteBtn.grid(row=5, column=2, padx=20, pady=(0, 10))
    selectBtn.grid(row=5, column=3, padx=20, pady=(0, 10))
    searchBtn.grid(row=5, column=4, padx=20, pady=(0, 10))
    updateBtn.grid(row=6, column=0, padx=20, pady=(0, 10))

    viewAllBtn = Button(student_registration_root, text="View All", padx=20, pady=10, bd=5, font=('Arial', 12), command=refreshTable)
    viewAllBtn.grid(row=5, column=5, padx=20, pady=(0, 10))

    showGraphBtn = Button(student_registration_root, text="Show Graph", padx=20, pady=10, bd=5, font=('Arial', 12), command=show_graph)
    showGraphBtn.grid(row=7, column=3, padx=10, pady=(0, 10))

    resetFieldsBtn = Button(student_registration_root, text="Reset Fields", padx=20, pady=10, bd=5, font=('Arial', 12), command=resetFields)
    resetFieldsBtn.grid(row=6, column=5, padx=20, pady=(0, 10))

    logoutBtn = Button(student_registration_root, text="Logout", padx=20, pady=10, bd=5, font=('Arial', 12), command=logout)
    logoutBtn.grid(row=7, column=5, padx=20, pady=(0, 10))

    # Add a new button for displaying course information
    courseInfoBtn = Button(student_registration_root, text="Course Info", padx=20, pady=10, bd=5, font=('Arial', 12), command=show_course_info)
    courseInfoBtn.grid(row=7, column=4, padx=10, pady=(0, 10))

    # Place button configurations here (after buttons and functions are defined)
    if user_type == "admin":
        # Enable admin buttons
        addBtn.grid(row=5, column=0, padx=10, pady=(0, 10), sticky="ew")
        resetBtn.grid(row=5, column=2, padx=10, pady=(0, 10), sticky="ew", bg="red", fg="white")
        deleteBtn.grid(row=5, column=1, padx=10, pady=(0, 10), sticky="ew")
        selectBtn.grid(row=5, column=3, padx=10, pady=(0, 10), sticky="ew")
        searchBtn.grid(row=5, column=4, padx=10, pady=(0, 10), sticky="ew")
        updateBtn.grid(row=6, column=0, padx=10, pady=(0, 10), sticky="ew")
        viewAllBtn.grid(row=6, column=0, padx=10, pady=(0, 10), sticky="ew")
        logoutBtn.grid(row=5, column=5, padx=10, pady=(0, 10), sticky="ew")
    else:

        # Disable admin buttons
        addBtn.grid_forget()
        resetBtn.grid_forget()
        deleteBtn.grid_forget()
        selectBtn.grid_forget()
        updateBtn.grid_forget()
        showGraphBtn.grid_forget()
        showGenderDistributionBtn.grid_forget()

        # Enable user buttons
        viewAllBtn.grid(row=5, column=0, padx=10, pady=(0, 10), sticky="ew")
        resetFieldsBtn.grid(row=6, column=0, padx=10, pady=(0, 10), sticky="ew")
        searchBtn.grid(row=5, column=4, padx=10, pady=(0, 10), sticky="ew")
       

    my_tree = ttk.Treeview(student_registration_root)
    my_tree["columns"] = ("Student ID", "First Name", "Last Name", "Address", "Phone", "Gender",  "Course ID")

    for col in my_tree["columns"]:
        my_tree.column(col, anchor="w", width=200)
        my_tree.heading(col, text=col, anchor='w')

    my_tree.grid(row=8, column=0, columnspan=5, rowspan=11, padx=10, pady=20)

    def resize_columns(event):
        for col in my_tree["columns"]:
            my_tree.column(col, width=int(student_registration_root.winfo_width() / 6))

    # Bind the resize_columns function to the <Configure> event of the window
    student_registration_root.bind("<Configure>", resize_columns)

    # Center the window on the screen
    student_registration_root.update_idletasks()
    width = student_registration_root.winfo_width()
    height = student_registration_root.winfo_height()
    x = (student_registration_root.winfo_screenwidth() // 2) - (width // 2)
    y = (student_registration_root.winfo_screenheight() // 2) - (height // 2)
    student_registration_root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    # Set a fixed size for the Treeview widget
    my_tree.grid(row=8, column=0, columnspan=5, rowspan=11, padx=10, pady=20, sticky="nsew")
    student_registration_root.grid_rowconfigure(8, weight=1)
    student_registration_root.grid_columnconfigure(0, weight=1)

    # Initial population of the Treeview
    refreshTable()

    student_registration_root.mainloop()




# Login Page
root = ThemedTk(theme="equilux")  # Setting the theme to equilux
root.title("Login")
root.geometry("400x300")

style = ttk.Style()
style.configure("TButton", font=('Arial', 15))

label = Label(root, text="Login", font=('Arial Bold', 20))
label.pack(pady=20)

usernameLabel = Label(root, text="Username", font=('Arial', 15))
passwordLabel = Label(root, text="Password", font=('Arial', 15))
usernameLabel.pack(pady=5)
passwordLabel.pack(pady=5)

usernameEntry = Entry(root, width=30, bd=5, font=('Arial', 15))
passwordEntry = Entry(root, width=30, bd=5, font=('Arial', 15), show="*")
usernameEntry.pack(pady=5)
passwordEntry.pack(pady=5)

loginBtn = Button(root, text="Login", padx=20, pady=10, width=10, bd=5, font=('Arial', 15), command=login)
loginBtn.pack(pady=20)


createAccountBtn = Button(root, text="Create Account", padx=10, pady=5, bd=5, font=('Arial', 12), command=create_account_window)
createAccountBtn.pack(pady=10)

root.mainloop()
