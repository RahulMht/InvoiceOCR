
import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

if not firebase_admin._apps:
    cred = credentials.Certificate('cred.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://ocr-yantra-default-rtdb.firebaseio.com/"
    })

ref = db.reference("/pizzahouse/invoices/")

json_data ={
  "invoice_no": "0064",
  "name": "Shyam Bhandari",
  "date": "15/01/24",
  "items": [
    {
      "S.N": 1,
      "Item": "Chips",
      "Rate": 130,
      "Unit": 5,
      "Price": 650
    },
    {
      "S.N": 2,
      "Item": "Chicken wings",
      "Rate": 120,
      "Unit": 3,
      "Price": 360
    },
    {
      "S.N": 3,
      "Item": "Chicken drumstick",
      "Rate": 160,
      "Unit": 2,
      "Price": 320
    },
    {
      "S.N": 4,
      "Item": "Coke",
      "Rate": 80,
      "Unit": 5,
      "Price": 400
    }
  ],
  "total": 1730
}

# Create a dataframe from the JSON data
df = pd.DataFrame(json_data["items"])
st.header('Edit Section', divider='rainbow')
col1, col2 = st.columns([1, 1])
with col1:
    Invoice_no = st.text_input( 'Invoice_no', value = json_data["invoice_no"])
with col2:
    Date = st.text_input( 'Date', value = json_data["date"])
Name = st.text_input( 'Name', value = json_data["name"])

# Make the dataframe editable
df.drop('Price', axis=1, inplace=True)
edited_df = st.data_editor(df)
edited_df['price'] = edited_df['Rate'] * edited_df['Unit']
total_price = edited_df['price'].sum()


# Preview and upload buttons
preview = st.button('Preview Final Output')


# Preview
if preview:
    st.header('Preview Section', divider='rainbow')
    st.write('Name:', Name)
    st.write('Invoice No:', Invoice_no)
    st.write('Date:', Date)
    # Show dataframe and total price without redundant calculations
    st.dataframe(edited_df)
    st.write('Total Price:', total_price)
st.header('', divider='rainbow')
upload = st.button('Upload to database')

# Upload
if upload:
    json_data.update({
        "date": Date,
        "name": Name,
        "invoice_no": Invoice_no,
        "items": edited_df.to_dict(orient="records"),
        "total": int(total_price),
    })

    items = json_data.pop('items')
    ref.child(Invoice_no).set(json_data)
    for item in items:
        item_ref = ref.child(Invoice_no).child("Items").child(item['Item'])
        item_ref.set({
            "Rate": item["Rate"],
            "Unit": item["Unit"],
            "Price": item["Rate"]*item["Unit"],  
        })
    st.success('Data uploaded successfully!')