# import streamlit as st
# from views.login_view import show_login
# from views.dashboard_view import show_dashboard
# from views.admin_view import show_admin
# from controllers.auth_controller import validate_session, logout


# st.set_page_config(page_title="Audit Dashboard", layout="wide")

# if "user" not in st.session_state:
#     show_login()

# else:

#     user = st.session_state.user

#     menu = ["Dashboard"]

#     if user["level"] == 1:
#         menu.append("Admin")

#     choice = st.sidebar.selectbox("Menu", menu)

#     if choice == "Dashboard":
#         show_dashboard()

#     elif choice == "Admin":
#         show_admin()

# def load_css():
#     with open("assets/style.css") as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# load_css()

import streamlit as st
from views.login_view import show_login
from views.dashboard_view import show_dashboard
from views.admin_view import show_admin
from controllers.auth_controller import validate_session, logout

st.set_page_config(page_title="Audit Dashboard", layout="wide")

# -----------------------------
# LOGOUT BUTTON
# -----------------------------
if "user" in st.session_state:
    if st.sidebar.button("Logout"):
        logout(st.session_state.user)
        del st.session_state.user
        st.experimental_rerun = lambda: st.stop()  # safe fallback
        st.stop()

# -----------------------------
# LOGIN CHECK
# -----------------------------
if "user" not in st.session_state:
    show_login()
else:
    user = st.session_state.user
    # Optionally validate session in DB
    # valid = validate_session(user["session_id"], user["session_token"])
    # if not valid:
    #     st.warning("Session expired. Please login again.")
    #     del st.session_state.user
    #     st.stop()

    menu = ["Dashboard"]
    if user["level"] == 1:
        menu.append("Admin")

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Dashboard":
        show_dashboard()
    elif choice == "Admin":
        show_admin()

# -----------------------------
# CSS
# -----------------------------
def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css()