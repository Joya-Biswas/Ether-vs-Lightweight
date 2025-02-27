import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def theoretical_analysis_page():
    st.title("Theoretical Analysis")

    st.markdown(
        """
    ## Theoretical Comparison on Ethereum (Basic) vs. Lightweight Solidity Contract
    
    Blockchain-based smart contracts are widely used for secure and decentralized data storage and processing. 
    This paper compares two Solidity-based implementations: Ethereum (Basic) Medical Contract and Lightweight 
    Medical Contract. The comparison is made in terms of time complexity, space complexity, security, gas 
    consumption, and scalability.
    """
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Ethereum (Basic Contract)")
        st.markdown(
            """
        * **Functions**: `getPatient(uint256 patientId)`, `getDoctor(uint256 doctorId)`
        * **Time Complexity**: O(1) – Direct lookup from Solidity mapping.
        * **Space Complexity**: O(n×m) – Stores all attributes on-chain.
        * **Security**: High – Full data is immutable and stored permanently.
        * **Gas Cost**: High – Fetching large records consumes more gas.
        """
        )

    with col2:
        st.subheader("Lightweight Contract")
        st.markdown(
            """
        * **Functions**: `getPatientHash(uint256 patientId)`, `getDoctorHash(uint256 doctorId)`
        * **Time Complexity**: O(1) – Direct lookup for hash but requires off-chain retrieval.
        * **Space Complexity**: O(n) – Stores only hashes on-chain, significantly reducing storage.
        * **Security**: Medium – Relies on IPFS (off-chain storage), which may be altered.
        * **Gas Cost**: Low – Fetching a small hash is cheaper.
        """
        )

    # Deleting Data Section
    st.subheader("Deleting Patient and Doctor Data")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Ethereum (Basic Contract)")
        st.markdown(
            """
        * **Functions**: `deletePatient(uint256 patientId)`, `deleteDoctor(uint256 doctorId)`
        * **Time Complexity**: O(1) – Solidity delete operation on mapping.
        * **Space Complexity**: O(n×m) – Full records are removed, freeing storage.
        * **Security**: High – Permanent removal of data.
        * **Gas Cost**: High – Removing multiple attributes increases gas costs.
        """
        )

    with col2:
        st.subheader("Lightweight Contract")
        st.markdown(
            """
        * **Functions**: `deletePatient(uint256 patientId)`, `deleteDoctor(uint256 doctorId)`
        * **Time Complexity**: O(1) – Removing a single hash from mapping.
        * **Space Complexity**: O(n) – Only hash is removed.
        * **Security**: Medium – Data still exists off-chain unless manually deleted.
        * **Gas Cost**: Low – Only one hash is removed, reducing gas costs.
        """
        )

    # Visual Comparison Chart
    st.subheader("Visual Comparison")

    # Create comparison data for visualization
    st.subheader("Theoretical Comparison on Ethereum vs. Lightweight Solidity Contract")

    # Create data for radar chart
    categories = [
        "Time Efficiency",
        "Space Efficiency",
        "Security",
        "Gas Efficiency",
        "Scalability",
    ]
    ethereum_values = [3, 1, 5, 1, 2]  # 1-5 rating where 5 is best
    lightweight_values = [4, 4, 3, 5, 5]  # 1-5 rating where 5 is best

    # Create DataFrame for plotting
    df = pd.DataFrame(
        {
            "Category": categories,
            "Ethereum (Basic)": ethereum_values,
            "Lightweight": lightweight_values,
        }
    )

    # Plot the data
    fig, ax = plt.subplots(figsize=(8, 6))
    bar_width = 0.35
    x = range(len(categories))

    ax.bar(
        [i - bar_width / 2 for i in x],
        df["Ethereum (Basic)"],
        bar_width,
        label="Ethereum (Basic)",
        color="#3366cc",
    )
    ax.bar(
        [i + bar_width / 2 for i in x],
        df["Lightweight"],
        bar_width,
        label="Lightweight",
        color="#cc6633",
    )

    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha="right")
    ax.set_ylim(0, 6)
    ax.set_ylabel("Rating (1-5)")
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    st.pyplot(fig)

    # Final Comparison Table
    st.subheader("Final Comparison Table")

    comparison_data = {
        "Functionality": [
            "Retrieving Data",
            "Time Complexity",
            "Space Complexity",
            "Gas Cost",
            "Deleting Data",
            "Verification & Security",
            "Existence Checks",
        ],
        "Ethereum (Basic) Contract": [
            "getPatient(), getDoctor() (Full on-chain data)",
            "O(1)",
            "O(n × m) (All attributes stored)",
            "High (Full data retrieval)",
            "deletePatient(), deleteDoctor() (Full record)",
            "No explicit verification needed",
            "Not implemented",
        ],
        "Lightweight Contract": [
            "getPatientHash(), getDoctorHash() (Only hash)",
            "O(1) for hash lookup, O(k) for verification",
            "O(n) (Only hashes stored)",
            "Low (Only hash retrieval)",
            "deletePatient(), deleteDoctor() (Deletes hash only)",
            "verifyPatientData() (Ensures integrity via hashing)",
            "patientExists(), doctorExists()",
        ],
    }

    table_df = pd.DataFrame(comparison_data)
    st.table(table_df)

    # Conclusion Section
    st.subheader("Conclusion")

    st.markdown(
        """
    * **Ethereum (Basic Contract)**: More secure but costly due to on-chain data storage.
    * **Lightweight Contract**: More scalable and cost-efficient but relies on off-chain data integrity.
    * **Use Case Recommendation**: Ethereum for legal records, Lightweight for large-scale data management.
    """
    )


if __name__ == "__main__":
    theoretical_analysis_page()
