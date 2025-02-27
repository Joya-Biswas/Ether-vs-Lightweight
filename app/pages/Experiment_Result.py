import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

def load_experiment_file():
    """Load experiment data from the output CSV file"""
    file_path = os.path.join("results", "output.csv")
    try:
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            return df
        else:
            st.warning("No experiment data found. Please run an experiment first.")
            return None
    except Exception as e:
        st.error(f"Error loading experiment data: {e}")
        return None

def analyze_and_visualize(df):
    """Analyze and visualize experiment data"""
    if df is None or df.empty:
        st.warning("No data to analyze")
        return
    
    # Split data for each contract type
    basic_data = df[df["contract_name"] == "BasicContract"]
    light_data = df[df["contract_name"] == "LightweightContract"]
    
    if basic_data.empty or light_data.empty:
        st.warning("Missing data for one or both contract types")
        return

    # Calculate summary statistics
    basic_add_gas_avg = basic_data["add_gas_used"].mean()
    light_add_gas_avg = light_data["add_gas_used"].mean()
    add_gas_improvement = (
        (basic_add_gas_avg - light_add_gas_avg) / basic_add_gas_avg
    ) * 100

    basic_del_gas_avg = basic_data["delete_gas_used"].mean()
    light_del_gas_avg = light_data["delete_gas_used"].mean()
    del_gas_improvement = (
        (basic_del_gas_avg - light_del_gas_avg) / basic_del_gas_avg
    ) * 100

    # Time Statistics
    basic_add_time_avg = basic_data["add_time"].mean()
    light_add_time_avg = light_data["add_time"].mean()
    add_time_improvement = (
        (basic_add_time_avg - light_add_time_avg) / basic_add_time_avg
    ) * 100

    basic_del_time_avg = basic_data["delete_time"].mean()
    light_del_time_avg = light_data["delete_time"].mean()
    del_time_improvement = (
        (basic_del_time_avg - light_del_time_avg) / basic_del_time_avg
    ) * 100

    # Create summary data
    summary_data = {
        "Operation": [
            "Add Gas Used",
            "Delete Gas Used",
            "Add Time (ms)",
            "Delete Time (ms)",
        ],
        "BasicContract": [
            basic_add_gas_avg,
            basic_del_gas_avg,
            basic_add_time_avg,
            basic_del_time_avg,
        ],
        "LightweightContract": [
            light_add_gas_avg,
            light_del_gas_avg,
            light_add_time_avg,
            light_del_time_avg,
        ],
        "Improvement (%)": [
            add_gas_improvement,
            del_gas_improvement,
            add_time_improvement,
            del_time_improvement,
        ],
    }

    summary_df = pd.DataFrame(summary_data)

    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(
        ["Tabular View", "Box Plots", "Bar Charts", "Raw Data"]
    )

    with tab1:
        st.subheader("Performance Summary Table")
        st.dataframe(summary_df.round(2), use_container_width=True)

        # Add download button for the summary
        csv = summary_df.to_csv(index=False)
        st.download_button(
            label="Download Performance Summary",
            data=csv,
            file_name="blockchain_performance_summary.csv",
            mime="text/csv",
        )

    with tab2:
        st.subheader("Performance Box Plots")

        col1, col2 = st.columns(2)

        with col1:
            # 1. Gas Usage Comparison - Add Operation
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.boxplot(data=df, x="contract_name", y="add_gas_used", ax=ax)
            ax.set_title("Add Operation: Gas Usage")
            ax.set_xlabel("Contract Type")
            ax.set_ylabel("Gas Used")
            st.pyplot(fig)

            # 3. Execution Time Comparison - Add Operation
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.boxplot(data=df, x="contract_name", y="add_time", ax=ax)
            ax.set_title("Add Operation: Execution Time")
            ax.set_xlabel("Contract Type")
            ax.set_ylabel("Execution Time (ms)")
            st.pyplot(fig)

        with col2:
            # 2. Gas Usage Comparison - Delete Operation
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.boxplot(data=df, x="contract_name", y="delete_gas_used", ax=ax)
            ax.set_title("Delete Operation: Gas Usage")
            ax.set_xlabel("Contract Type")
            ax.set_ylabel("Gas Used")
            st.pyplot(fig)

            # 4. Execution Time Comparison - Delete Operation
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.boxplot(data=df, x="contract_name", y="delete_time", ax=ax)
            ax.set_title("Delete Operation: Execution Time")
            ax.set_xlabel("Contract Type")
            ax.set_ylabel("Execution Time (ms)")
            st.pyplot(fig)

    with tab3:
        st.subheader("Performance Bar Charts")

        # Gas comparison bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        bar_width = 0.35
        x = np.arange(2)

        # Plot gas usage bars
        ax.bar(
            x - bar_width / 2,
            [basic_add_gas_avg, basic_del_gas_avg],
            bar_width,
            label="BasicContract",
            color="royalblue",
        )
        ax.bar(
            x + bar_width / 2,
            [light_add_gas_avg, light_del_gas_avg],
            bar_width,
            label="LightweightContract",
            color="lightgreen",
        )

        # Add labels and annotations
        ax.set_ylabel("Gas Used")
        ax.set_title("Gas Usage Comparison")
        ax.set_xticks(x)
        ax.set_xticklabels(["Add Operation", "Delete Operation"])
        ax.legend()

        # Add improvement annotations
        ax.annotate(
            f"{add_gas_improvement:.1f}% improvement",
            xy=(x[0], min(basic_add_gas_avg, light_add_gas_avg) / 2),
            ha="center",
            va="center",
            bbox=dict(boxstyle="round", fc="yellow", alpha=0.6),
        )
        ax.annotate(
            f"{del_gas_improvement:.1f}% improvement",
            xy=(x[1], min(basic_del_gas_avg, light_del_gas_avg) / 2),
            ha="center",
            va="center",
            bbox=dict(boxstyle="round", fc="yellow", alpha=0.6),
        )

        st.pyplot(fig)

        # Time comparison bar chart
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot time usage bars
        ax.bar(
            x - bar_width / 2,
            [basic_add_time_avg, basic_del_time_avg],
            bar_width,
            label="BasicContract",
            color="royalblue",
        )
        ax.bar(
            x + bar_width / 2,
            [light_add_time_avg, light_del_time_avg],
            bar_width,
            label="LightweightContract",
            color="lightgreen",
        )

        # Add labels and annotations
        ax.set_ylabel("Execution Time (ms)")
        ax.set_title("Execution Time Comparison")
        ax.set_xticks(x)
        ax.set_xticklabels(["Add Operation", "Delete Operation"])
        ax.legend()

        # Add improvement annotations
        ax.annotate(
            f"{add_time_improvement:.1f}% improvement",
            xy=(x[0], min(basic_add_time_avg, light_add_time_avg) / 2),
            ha="center",
            va="center",
            bbox=dict(boxstyle="round", fc="yellow", alpha=0.6),
        )
        ax.annotate(
            f"{del_time_improvement:.1f}% improvement",
            xy=(x[1], min(basic_del_time_avg, light_del_time_avg) / 2),
            ha="center",
            va="center",
            bbox=dict(boxstyle="round", fc="yellow", alpha=0.6),
        )

        st.pyplot(fig)

    with tab4:
        st.subheader("Raw Experiment Data")
        st.dataframe(df, use_container_width=True)

        # Add download button for the raw data
        raw_csv = df.to_csv(index=False)
        st.download_button(
            label="Download Raw Experiment Data",
            data=raw_csv,
            file_name="blockchain_experiment_raw_data.csv",
            mime="text/csv",
        )

def main():    
    # Load and display the experiment results
    df = load_experiment_file()
    
    if df is not None:
        # Display the performance comparison header
        st.subheader("BasicContract vs LightweightContract Performance Comparison")
        
        # Analyze and visualize the data
        analyze_and_visualize(df)
    
if __name__ == "__main__":
    st.set_page_config(
        layout="wide",
        page_title="Experiment Results",
        page_icon="📊",
        initial_sidebar_state="expanded",
    )
    main()