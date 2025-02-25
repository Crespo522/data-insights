import streamlit as st
import pandasai as pai
import pandas as pd
from pandasai_local import LocalLLM


# Run this script using: streamlit run your_script.py

# Load the local Ollama LLM (cached for performance)
@st.cache_resource
def load_llm():
    return LocalLLM(
        api_base="http://localhost:11434/v1",  # Default Ollama local API address
        model="deepseek-coder-v2"  # Replace with the installed model name
    )


# Configure PandasAI to use the local LLM
def configure_pandas_ai():
    llm = load_llm()
    pai.config.set({"llm": llm})  # Set local Ollama as the default LLM


# Process an uploaded Excel file and convert sheets into PandasAI DataFrames
def process_excel_file(uploaded_file):
    try:
        # Read all sheets from the uploaded Excel file
        excel_data = pd.read_excel(uploaded_file, sheet_name=None)
        # Convert each sheet into a PandasAI DataFrame
        pai_dfs = {sheet_name: pai.DataFrame(data) for sheet_name, data in excel_data.items()}
        return pai_dfs
    except Exception as e:
        st.error(f"Error processing the Excel file: {str(e)}")
        return None


# Main application
def main():
    st.title("Data Insights (Local Ollama Version)")
    st.write(
        "Upload an Excel file and ask questions in natural language. "
        "The system will use local Ollama to process all sheets.")

    # Configure PandasAI with the local LLM
    configure_pandas_ai()

    # File uploader for Excel files
    uploaded_file = st.file_uploader("Select an Excel file", type=['xlsx', 'xls'])

    # Initialize session state to store DataFrames
    if 'dfs' not in st.session_state:
        st.session_state.dfs = None

    # Process the uploaded file
    if uploaded_file is not None:
        with st.spinner("Processing the Excel file..."):
            dfs = process_excel_file(uploaded_file)
            if dfs is not None:
                st.session_state.dfs = dfs
                st.success(f"Successfully loaded Excel file with {len(dfs)} sheets.")

    # Display all sheet previews
    if st.session_state.dfs is not None:
        st.write("Sheet Previews (First 5 Rows):")
        for sheet_name, df in st.session_state.dfs.items():
            st.write(f"**{sheet_name}**:")
            st.dataframe(df.head())

        # Input field for natural language queries
        query = st.text_input("Enter your question (in natural language)")

        if query:
            with st.spinner("Processing your query using local Ollama..."):
                try:
                    # Pass all sheet DataFrames to PandasAI
                    all_dfs = list(st.session_state.dfs.values())
                    result = pai.chat(query, *all_dfs)  # Unpack all DataFrames

                    # Display the response
                    st.write("Answer:")
                    if isinstance(result, pd.DataFrame) or isinstance(result, pai.DataFrame):
                        st.dataframe(result)
                    elif isinstance(result, (list, dict)):
                        st.json(result)
                    else:
                        st.write(result)
                except Exception as e:
                    st.error(f"Error processing the query: {str(e)}")

    # Expandable section with usage instructions
    with st.expander("Usage Instructions"):
        st.write("""
        1. Ensure that the local Ollama service is running (default port: 11434).
        2. Upload an Excel file containing multiple sheets.
        3. The system will automatically load all sheets and display previews.
        4. Enter a natural language question in the text box, such as:
           - "Who has the highest salary?"
           - "Summarize total revenue by department."
           - "How many records are there in total across all sheets?"
           - "Generate a pie chart of salaries by department."
        5. Wait for local Ollama to process the request and view the result.

        **Note:**
        - Ollama must be installed locally with a suitable model (e.g., LLaMA2).
        - Query performance depends on local hardware and model size.
        """)


if __name__ == "__main__":
    # Configure Streamlit page settings
    st.set_page_config(
        page_title="Excel QA Tool (Local Ollama)",
        layout="wide"
    )

    # Check Ollama connection before starting
    try:
        llm_ = load_llm()
        main()
    except Exception as e:
        st.error("Unable to connect to the local Ollama service. Please ensure it is running.")
        st.write(f"Error details: {str(e)}")
