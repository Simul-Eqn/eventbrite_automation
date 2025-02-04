from send_verification_message import load_from_csv, send_verify_attendance_message_to_all 

import streamlit as st 
import pandas as pd 
import io 


st.title("csv app")

csv_file = st.file_uploader("Upload your CSV file here") 
if csv_file is not None: 
    df = pd.read_csv(csv_file) 
    st.write("Preview of Uploaded Data:")
    st.write(df.head())

    # Column Selection
    st.write("### Select Columns")
    phone_col = st.selectbox("Select Phone Number Column", df.columns)
    name_col = st.selectbox("Select Name Column", df.columns)
    email_col = st.selectbox("Select Email Column", df.columns) 

    # Event Details Input
    st.write("### Enter Event Details")
    event_name = st.text_input("Event Name", placeholder="Event name")
    event_details = st.text_input("Event Details", placeholder="Enter one-line event details") 

    if st.button("Preview message"): 
        st.write('Registration for {}'.format(event_name)) 
        st.write('Hello [name], our records indicate that you have registered for {}. The details of the registration are as follows:'.format(event_name)) 
        st.write(event_details) 
        st.write('\n')
        st.write('To acknowledge that these details are correct, please reply "Yes". Otherwise, please respond with relevant corrections.')
        st.write('\n') 

    if st.button("SEND MESSAGE"): 
        st.write("Sending...")
        load_from_csv(df, phone_col_name=phone_col, name_col_name=name_col, email_col_name=email_col, in_additional_event_details=event_details) 
        send_verify_attendance_message_to_all(event_name)
        st.write("SENT SUCCESSFULLY!")
    

    if st.button("Download cleaned CSV for mailchimp"): 
        #a = 
        st.write("not implemented yet")


