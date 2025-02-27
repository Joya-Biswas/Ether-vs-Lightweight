import time
import streamlit as st
import pandas as pd
import os
from connection import w3, lightweight_contract, basic_contract
from utils.ipfs_utils import upload_to_ipfs
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

if "run_experiment" not in st.session_state:
    st.session_state.run_experiment = False


def run_experiment():
    st.session_state.run_experiment = True


def reset_experiment():
    st.session_state.run_experiment = False


def save_uploaded_file(uploaded_file):
    try:
        if not os.path.exists("datasets"):
            os.makedirs("datasets")
        file_path = os.path.join("datasets", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.session_state.file_path = file_path
    except Exception as e:
        st.error(f"Error saving file: {e}")


def save_experiment_results(experiment_data):
    """Save experiment results to a CSV file in the results directory"""
    try:
        # Create results directory if it doesn't exist
        if not os.path.exists("results"):
            os.makedirs("results")
        
        # Save the data to a fixed CSV file
        file_path = os.path.join("results", "output.csv")
        
        # Save the data to CSV
        df = pd.DataFrame(experiment_data)
        df.to_csv(file_path, index=False)
        
        st.success(f"Experiment results saved successfully!")
        return file_path
    except Exception as e:
        st.error(f"Error saving experiment results: {e}")
        return None


def main():
    st.header(
        "A Study of Variation of Blockchain to address the issue of Verification and Validation"
    )

    if not st.session_state.get("run_experiment"):
        st.markdown("#### Upload a Dataset:")
        uploaded_file = st.file_uploader("", type=["csv"], accept_multiple_files=False)
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

        st.write("Processing Dataset...")
        progress_bar = st.progress(0)
        input_data, output_measures = st.columns(2)
        with input_data:
            row_placeholder = st.empty()
        with output_measures:
            output_placeholder = st.empty()
        account = w3.eth.accounts[0]

        experiment_data = []
        for index, row in dataframe.iterrows():
            progress = (index + 1) / len(dataframe)
            progress_bar.progress(progress)

            row_output = f"**Row Index:** {index} \n"
            for col_name, value in row.items():
                row_output += f"- **{col_name}:** {value}\n"
            row_placeholder.markdown(row_output)

            for name, contract in zip(
                ["BasicContract", "LightweightContract"],
                [basic_contract, lightweight_contract],
            ):
                # ipfs_hash = upload_to_ipfs(str(index), row.to_csv())
                ipfs_hash = "gg"
                start_time = time.time()
                if contract is basic_contract:
                    tx_receipt = contract.functions.addRecord(
                        index, [str(ele) for ele in row.to_list()]
                    ).transact({"from": account})
                else:
                    tx_receipt = contract.functions.addRecord(
                        index, [str(ele) for ele in row.to_list()], ipfs_hash
                    ).transact({"from": account})
                end_time = time.time()
                add_time = end_time - start_time

                add_receipt = w3.eth.get_transaction_receipt(tx_receipt)

                start_time = time.time()
                tx_receipt = contract.functions.deleteRecord(index).transact(
                    {"from": account}
                )
                end_time = time.time()
                delete_time = end_time - start_time

                delete_receipt = w3.eth.get_transaction_receipt(tx_receipt)

                output_placeholder.markdown(
                    f"**{name}** \n `addRecord Transaction for id: {index} - Gas Used: {add_receipt['gasUsed']}, Time: {add_time:.4f} seconds` \n `deleteRecord Transaction for id: {index} - Gas Used: {delete_receipt['gasUsed']}, Time: {delete_time:.4f} seconds`"
                )

                experiment_data.append(
                    {
                        "contract_name": name,
                        "index": index,
                        "add_gas_used": add_receipt["gasUsed"],
                        "add_time": add_time * 1000,
                        "delete_gas_used": delete_receipt["gasUsed"],
                        "delete_time": delete_time * 1000,
                    }
                )

        row_placeholder.markdown("Processing complete!")
        output_placeholder.markdown("")

        # Save experiment data to CSV file
        save_experiment_results(experiment_data)
        
        # Display completion message and link to results page
        st.success("Experiment completed successfully!")
        st.info("View the detailed results in the 'Experiment Results' page.")
        
        # Add a button to navigate to the Results page
        st.markdown("[Go to Experiment Results Page](/Experiment_Result)")


if __name__ == "__main__":
    st.set_page_config(
        layout="centered",
        page_title="Experiment",
        page_icon="🧪",
        initial_sidebar_state="expanded",
    )
    main()