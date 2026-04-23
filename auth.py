import bcrypt
import streamlit as st
from db import get_connection

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def login(username, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result and check_password(password, result['password']):
        st.session_state['logged_in'] = True
        st.session_state['username'] = result['username']
        return True
    return False

def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    
def is_logged_in():
    return st.session_state.get('logged_in', False)