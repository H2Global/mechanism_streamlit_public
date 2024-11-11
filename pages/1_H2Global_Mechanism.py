import streamlit as st

from utils.flow_h2global_analysis import show_evaluation_page, show_info_page


# Function to initialize session state
# The first page is used to describe the H2Global mechanism and the goal of the tool
# With this configuration the user can't go back to info page once he/she starts with the evaluation
def init_session_state():
    if 'page' not in st.session_state:
        st.session_state.page = 'Information'

def switch_to_mechanism():
    st.session_state.page = 'Analysis_Mechanism'
    
def switch_to_information():
    st.session_state.page = 'Information'


# Initialize session state
init_session_state()

# Show the page based on the current state
if st.session_state.page == 'Information':
    show_info_page()
    st.button("Start analysis", on_click=switch_to_mechanism)
    
elif st.session_state.page == 'Analysis_Mechanism':
    show_evaluation_page()
    st.button("Go back to start page", on_click=switch_to_information)
    
elif st.session_state.page == 'Analysis_Project':
    show_info_page()
    st.button("Start analysis", on_click=switch_to_mechanism)

else:
    raise AttributeError("No such session state defined.")