import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pandas as pd

if not firebase_admin._apps:
    cred = credentials.Certificate('cred.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://ocr-yantra-default-rtdb.firebaseio.com/"
    })

ref = db.reference("/pizzahouse/invoices/")
st.header('Invoice Viewer', divider='rainbow')
invoices = ref.get()

if invoices:
 
    selected_invoice_key = st.selectbox("Please Select an Invoice No.", list(invoices.keys()))


    selected_invoice = invoices[selected_invoice_key]

    # st.markdown("""<hr style="height:10px;border:none;color:#0074D9;background-color:#0074D9;" /> """, unsafe_allow_html=True)

 
    st.write('Invoice No:', selected_invoice.get("invoice_no", "Invoice No not found"))
    st.write('Name:', selected_invoice.get("name", "Name not found"))
    st.write('Date:', selected_invoice.get("date", "Date not found"))

    items_data = selected_invoice.get("Items")
    if items_data:
        items_list = []
        total_price = 0 
        for idx, (item_name, item_details) in enumerate(items_data.items(), start=1):
            item_detail = {
                "S.N": idx,
                "Name": item_name,
                "Quantity": item_details.get("Unit", "Quantity not found"),
                "Rate": item_details.get("Rate", "Rate not found"),
                "Total Price": item_details.get("Price", "Price not found")
            }
            items_list.append(item_detail)
            total_price += item_details.get("Price", 0)  

        items_df = pd.DataFrame(items_list)
        st.dataframe(items_df, hide_index=True)  

    
        st.write("Total Price:", total_price)
    else:
        st.write("No items found for this invoice.")
else:
    st.write("No invoices found in the database.")