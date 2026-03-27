import streamlit as st
from controllers.auth_controller import login

def show_login():

    st.title("AI Audit Dashboard Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        user = login(email, password)
        if user:
                st.session_state.user = user
                st.success(f"Welcome {user['name']}! Reloading dashboard...")

                # Stop execution, dashboard will load on next render
                st.stop()
        else:
            st.error("Invalid credentials")