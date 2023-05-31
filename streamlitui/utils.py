import streamlit as st
import base64
from pdf2image import convert_from_bytes
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, ColumnsAutoSizeMode

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

def confidence_format(df, scale_mode, key, edit_cols=None):
    if scale_mode == "fit_contents":
        autosize_option = ColumnsAutoSizeMode.FIT_CONTENTS
    elif scale_mode == "fit_view":
        autosize_option = ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW
    else:
        autosize_option = ColumnsAutoSizeMode.NO_AUTOSIZE

    gb = GridOptionsBuilder.from_dataframe(df)

    jscode = JsCode("""
    function(params) {
        var positive_color = '#40BF60'; //'#009E73';
        var negative_color = '#9A0E2A'; //'#D55E00';

        function hasAlphaNum (str) {
            var code, i, len;
            if (!str) {
                return false;
            };
            
            for (i = 0, len = str.length; i < len; i++) {
                code = str.charCodeAt(i);
                if ((code > 47 && code < 58) || (code > 64 && code < 91) || (code > 96 && code < 123)) {
                    return true;
                }
            };
            return false;
        };

        if (params.data.Conf >= 0.5 && hasAlphaNum(params.data.Value)) {
            return {
                'fontWeight': 'bold',
                'backgroundColor': positive_color,
            };
        } else {
            return {
                'fontWeight': 'bold',
                'backgroundColor': negative_color
            };
        };
    };
    """)

    if edit_cols:
        gb.configure_columns(edit_cols, editable=True)

    grid_options = gb.build()
    grid_options['getRowStyle'] = jscode
    return_grid = AgGrid(
        df, 
        gridOptions=grid_options,
        fit_columns_on_grid_load=True,
        columns_auto_size_mode=autosize_option, 
        allow_unsafe_jscode=True,
        theme="streamlit",
        key=key
    )
    return return_grid["data"]

@st.cache_data(ttl=60*60)
def df_to_csv(df):
    return df.to_csv().encode("utf-8")