import streamlit as st
from models.user_model import create_user
from utils.security import hash_password

def show_admin():

    st.title("Admin Panel")
    st.subheader("Create User")

    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password")

    # Role mapping: display text but store number
    role_options = {"User": 0, "Admin": 1}
    role_name = st.selectbox("Role", list(role_options.keys()))
    level = role_options[role_name]  # actual value to store in DB

    if st.button("Create User"):
        create_user(name, email, hash_password(password), level)
        st.success(f"User '{name}' created with role '{role_name}'!")