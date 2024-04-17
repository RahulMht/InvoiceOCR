import streamlit as st
from PIL import Image
import google.generativeai as genai
import pandas as pd
import ast
import os
from dotenv import load_dotenv
widget_id = (id for id in range(1, 100_00))

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


def parse_ocr_result(response):
    """Extracts dictionary of key-value pairs from OCR response, handling errors."""
    start_index = response.text.find("{")
    end_index = response.text.rfind("}")

    if start_index != -1 and end_index != -1:
        result_string = response.text[start_index: end_index + 1].strip()
        try:
            dictionary = ast.literal_eval(result_string)
            return dictionary
        except (ValueError, SyntaxError):
            st.error("Error parsing OCR result:", result_string)
            return None
    else:
        st.error("OCR result missing \"{\" or \"}\" delimiters.")
        return None


def ocr_image(image):
    st.image(image,width=400)
    response = model.generate_content(
        ['''OCR the invoice and extract the value of invoice_no, name, date, items, and total. give output in JSON format.
desired output template:
json_data ={
  "invoice_no": "",
  "name": "",
  "date": "",
  "items": [
    {
      "S.N": 1,
      "Item": "",
      "Rate": int,
      "Unit": int,
      "Price": int
    },
    {
      "S.N": 2,
      "Item": "",
      "Rate": int,
      "Unit": int
      "Price": int
    },
    ............
  ],
  "total": int
}''', image],
        stream=False,
        generation_config=genai.types.GenerationConfig(temperature=0.1),
    )
    response.resolve()
    return parse_ocr_result(response)


def process_folder(folder_path):
    """Processes images in a folder, collecting results in a DataFrame."""
    for filename in os.listdir(folder_path):
        if filename.endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(folder_path, filename)
            img = Image.open(img_path)
            try:
                with st.spinner('Performing OCR...'):
                    json_data = ocr_image(img)
                    if json_data:  # If OCR is successful, process the data
                        post_process(json_data)
            except Exception as e:
                st.error(f"Error processing image {filename}: {e}")


def post_process(json_data):
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
    edited_df = st.data_editor(df, hide_index=True)
    edited_df['price'] = edited_df['Rate'] * edited_df['Unit']
    total_price = edited_df['price'].sum()


    # Preview and upload buttons
    preview = st.button('Preview Final Output', key=next(widget_id))


    # Preview
    if preview:
        st.header('Preview Section', divider='rainbow')
        st.write('Name:', Name)
        st.write('Invoice No:', Invoice_no)
        st.write('Date:', Date)
        # Show dataframe and total price without redundant calculations
        st.dataframe(edited_df, hide_index=True)
        st.write('Total Price:', total_price)
    st.header('', divider='rainbow')

    upload = st.button('Upload to database', key=next(widget_id))

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
        st.markdown("""<hr style="height:10px;border:none;color:#0074D9;background-color:#0074D9;" /> """, unsafe_allow_html=True)
   



st.title("Invoice OCR 🔍")

# Initialize model (assuming API key is set via environment variable)
load_dotenv()
genai.configure(api_key=os.environ.get("google_api_key"))
model = genai.GenerativeModel("gemini-pro-vision")

# Radio buttons for input selection
input_type = st.radio("Choose input method:", ("Single Image","Take Image", "Image Folder",),horizontal=True)

if input_type == "Single Image":
    uploaded_file = st.file_uploader("Upload an image (.jpg)", type=["jpg" or "jpeg" or "png"])
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        with st.spinner('Performing OCR...'):
            json_data =  ocr_image(img)
            post_process(json_data)

elif input_type == "Take Image":
    img = st.camera_input("Take a picture")
    if img is not None:
        img = Image.open(img)
        with st.spinner('Performing OCR...'):
            json_data =  ocr_image(img)
            post_process(json_data)

else:
    folder_path = st.text_input("Enter the path to your image folder:")
    if folder_path and os.path.isdir(folder_path):
        process_folder(folder_path)
 




    

