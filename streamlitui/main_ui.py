from fr_ui import (
    sidebar,
    main_page
)

def main():
    uploaded_pdf = sidebar()
    if uploaded_pdf:
        main_page()

if __name__ == "__main__":
    main()