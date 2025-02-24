import streamlit as st
import pandas as pd
import os

if "run_experiment" not in st.session_state:
    st.session_state.run_experiment = False


def run_experiment():
    st.session_state.run_experiment = True


def reset_experiment():
    st.session_state.run_experiment = False


def save_uploaded_file(uploaded_file):
    try:
        if not os.path.exists("datasets"):
            os.makedirs("datasets")  # Create the directory if it doesn't exist

        file_path = os.path.join("datasets", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File saved to: {file_path}")
        st.session_state.file_path = file_path  # Store the file path in session state.
    except Exception as e:
        st.error(f"Error saving file: {e}")


def main():
    st.header(
        "A Study of Variation of Blockchain to address the issue of Verification and Validation"
    )
    st.write("")

    if not st.session_state.get("run_experiment"):
        uploaded_file = st.file_uploader(
            "Open a Dataset", type=["csv"], accept_multiple_files=False
        )
        if uploaded_file is not None:
            save_uploaded_file(uploaded_file)
            dataframe = pd.read_csv(uploaded_file)
            columns_sub_analyze = st.columns(4)

            with columns_sub_analyze[0]:
                st.subheader(uploaded_file.name)
            with columns_sub_analyze[-1]:
                st.button("Run Experiment", type="primary", on_click=run_experiment)

            st.write(dataframe)
    else:
        st.button("Reset", type="primary", on_click=reset_experiment)
        dataframe = pd.read_csv(st.session_state.file_path)
        st.write(dataframe)


if __name__ == "__main__":
    st.set_page_config(
        page_title="A Study of Variation of Blockchain to address the issue of Verification and Validation",
        page_icon=":chart_with_upwards_trend:",
        layout="centered",
    )
    main()
