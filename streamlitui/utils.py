import streamlit as st
import base64
from pdf2image import convert_from_bytes
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

def displaypdf(file: st.runtime.uploaded_file_manager.UploadedFile):
    """
    BUG: Not working on the cloud. Bug on Streamlit side.
    
    """
    bytes_pdf = base64.b64encode(file.read()).decode("utf-8")
    pdf_display = f'<embed src="data:application/pdf;base64,{bytes_pdf}" width="600" height="400" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)

def display_pdf_to_image(file:st.runtime.uploaded_file_manager.UploadedFile):
    bytes_pdf = file.read()
    image = convert_from_bytes(bytes_pdf, 500)
    st.image(image)

@st.cache_data(ttl=60*60)
def display_image_cached(file:st.runtime.uploaded_file_manager.UploadedFile):
    images = convert_from_bytes(file.read())
    return images

def confidence_format(df):
    gb = GridOptionsBuilder.from_dataframe(df)

    cellsytle_jscode = JsCode("""
    function(params) {
        try {
            if (params.data.Conf >= 0.5) {
                return {
                    'color': '#FFFFFF',
                    'backgroundColor': '#40BF60',
                }
            } else {
                return {
                    'color': '#FFFFFF',
                    'backgroundColor': '#9A0E2A'                    
                }
            };
        } catch(err) {
            return {
                    'color': '#000000',
                    'backgroundColor': '#0000FF'                    
                }
        }

    }
    """)
    gb.configure_columns(df,cellStyle=cellsytle_jscode, editable=True)
    grid_options = gb.build()
    grid_return = AgGrid(df, gridOptions=grid_options, allow_unsafe_jscode=True)

    return grid_return

# def row_format(row):
#     value = row["Conf"]
#     try:
#         value = float(value)
#     except TypeError:
#         pass

#     if value >= 0.5:
#         color = "#40BF60"
#     else:
#         color = "#9A0E2A"
#     return [f"background-color: {color}; color: #000000" for _ in row]