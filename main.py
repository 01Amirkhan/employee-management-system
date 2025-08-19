import streamlit as st
import mysql.connector
import pandas as pd

st.title("EMPLOYEE MANAGEMENT SYSTEM")

choice = st.sidebar.selectbox("My Menu", ("Home", "Student", "User", "Admin"))

if "login" not in st.session_state:
    st.session_state["login"] = False
if "userid" not in st.session_state:
    st.session_state["userid"] = None

if choice == "Home":
    st.image("https://media.istockphoto.com/id/517188688/photo/mountain-landscape.jpg?s=1024x1024&w=0&k=20&c=z8_rWaI8x4zApNEEG9DnWlGXyDIXe-OmsAyQ5fGPVV8=")
    st.markdown("<centre><h1>WELCOME</h1><centre>",unsafe_allow_html=True)
elif choice == "Student":
    st.write("This is an application developed as part of training")

elif choice == "User":
    uid = st.text_input("Enter Username")
    upwd = st.text_input("Enter Password", type="password")
    btn = st.button("Login")

    if btn:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Amir@9434",
            database="EmployeeManagement"
        )
        c = mydb.cursor()
        c.execute("SELECT user_id FROM Users WHERE username=%s AND user_pwd=%s", (uid, upwd))
        row = c.fetchone()
        mydb.close()

        if row:
            st.session_state['login'] = True
            st.session_state['userid'] = row[0]
            st.success("Login Successful")
        else:
            st.session_state['login'] = False
            st.error("Incorrect Username or Password")

    if st.session_state['login']:
        feature = st.selectbox(
            "Features",
            ("None", "View Profile", "Change Password", "See Attendance", "Delete Account")
        )

        if feature == "View Profile":
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Amir@9434",
                database="EmployeeManagement"
            )
            c = mydb.cursor()
            c.execute("SELECT user_id, username, role, emp_id FROM Users WHERE user_id=%s",
                      (st.session_state['userid'],))
            user_data = c.fetchone()
            mydb.close()

            if user_data:
                st.write(f"**User ID:** {user_data[0]}")
                st.write(f"**Username:** {user_data[1]}")
                st.write(f"**Role:** {user_data[2]}")
                st.write(f"**Employee ID:** {user_data[3]}")

        elif feature == "Change Password":
            new_pwd = st.text_input("Enter New Password", type="password")
            confirm_pwd = st.text_input("Confirm New Password", type="password")
            if st.button("Update Password"):
                if new_pwd.strip() == "" or confirm_pwd.strip() == "":
                    st.error("Password cannot be empty.")
                elif new_pwd != confirm_pwd:
                    st.error("Passwords do not match. Please try again.")
                else:
                    mydb = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="Amir@9434",
                        database="EmployeeManagement"
                    )
                    c = mydb.cursor()
                    c.execute("UPDATE Users SET user_pwd=%s WHERE user_id=%s",
                              (new_pwd, st.session_state['userid']))
                    mydb.commit()
                    mydb.close()
                    st.success("Password updated successfully!")

        elif feature == "See Attendance":
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Amir@9434",
                database="EmployeeManagement"
            )
            c = mydb.cursor(dictionary=True)
            query = """
                SELECT a.* 
                FROM attendance a
                JOIN Users u ON a.emp_id = u.emp_id
                WHERE u.user_id = %s
            """
            c.execute(query, (st.session_state['userid'],))
            rows = c.fetchall()
            mydb.close()

            df = pd.DataFrame(rows)
            if df.empty:
                st.info("No attendance records found.")
            else:
                st.subheader("Your Attendance Records")
                st.dataframe(df)

        elif feature == "Delete Account":
            st.warning("Deleting your account is permanent and cannot be undone.")
            confirm = st.checkbox("I confirm I want to delete my account")
            if st.button("Delete My Account") and confirm:
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Amir@9434",
                    database="EmployeeManagement"
                )
                c = mydb.cursor()
                c.execute("DELETE FROM Users WHERE user_id=%s", (st.session_state['userid'],))
                mydb.commit()
                mydb.close()

                st.success("Your account has been deleted successfully!")
                st.session_state['login'] = False
                st.session_state['userid'] = None

elif choice == "Admin":
    st.video("https://www.youtube.com/watch?v=TgvFm9zamIw")
    st.subheader("Admin Panel - Add New User")

    new_username = st.text_input("Enter New Username")
    new_password = st.text_input("Enter Password", type="password")
    new_role = st.selectbox("Select Role", ["Admin", "Employee"])

    new_empid = None
    if new_role == "Employee":
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Amir@9434",
            database="EmployeeManagement"
        )
        c = mydb.cursor()
        c.execute("SELECT emp_id, emp_name FROM Employee")
        employees = c.fetchall()
        mydb.close()

        emp_options = {f"{e[1]} (ID: {e[0]})": e[0] for e in employees}
        if emp_options:
            selected_emp = st.selectbox("Select Employee", list(emp_options.keys()))
            new_empid = emp_options[selected_emp]
        else:
            st.warning("No employees found. Please add employees first.")

    if st.button("Add User"):
        if new_username.strip() == "" or new_password.strip() == "":
            st.error("Username and Password cannot be empty.")
        elif new_role == "Employee" and new_empid is None:
            st.error("You must select a valid employee for Employee role.")
        else:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Amir@9434",
                database="EmployeeManagement"
            )
            c = mydb.cursor()
            if new_role == "Admin":
                c.execute(
                    "INSERT INTO Users (username, user_pwd, role, emp_id) VALUES (%s, %s, %s, NULL)",
                    (new_username, new_password, new_role)
                )
            else:
                c.execute(
                    "INSERT INTO Users (username, user_pwd, role, emp_id) VALUES (%s, %s, %s, %s)",
                    (new_username, new_password, new_role, new_empid)
                )
            mydb.commit()
            mydb.close()
            st.success(f"User '{new_username}' added successfully!")


    




