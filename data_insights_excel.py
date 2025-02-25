import streamlit as st
import pandasai as pai
import pandas as pd
from pandasai_local import LocalLLM


# streamlit run your_script.py

# 配置本地Ollama LLM
@st.cache_resource
def load_llm():
    return LocalLLM(
        api_base="http://localhost:11434/v1",  # 默认Ollama本地地址
        model="deepseek-coder-v2"  # 可替换为你安装的模型名称
    )


# 设置PandasAI全局配置
def configure_pandas_ai():
    llm = load_llm()
    pai.config.set({"llm": llm})  # 设置本地Ollama为默认LLM


# 处理Excel文件并转换为PandasAI DataFrame
def process_excel_file(uploaded_file):
    try:
        # 读取Excel文件的所有sheets
        excel_data = pd.read_excel(uploaded_file, sheet_name=None)
        # 转换为PandasAI的DataFrame
        pai_dfs = {sheet_name: pai.DataFrame(data) for sheet_name, data in excel_data.items()}
        return pai_dfs
    except Exception as e:
        st.error(f"处理Excel文件时出错: {str(e)}")
        return None


# 主程序
def main():
    st.title("Data insights（本地Ollama版）")
    st.write("上传Excel文件并使用自然语言提出问题，系统将使用本地Ollama处理所有工作表")

    # 配置PandasAI使用本地LLM
    configure_pandas_ai()

    # 文件上传
    uploaded_file = st.file_uploader("选择Excel文件", type=['xlsx', 'xls'])

    # 初始化session state
    if 'dfs' not in st.session_state:
        st.session_state.dfs = None

    # 处理上传的文件
    if uploaded_file is not None:
        with st.spinner("正在处理Excel文件..."):
            dfs = process_excel_file(uploaded_file)
            if dfs is not None:
                st.session_state.dfs = dfs
                st.success(f"成功加载Excel文件，包含 {len(dfs)} 个工作表")

    # 显示所有工作表预览
    if st.session_state.dfs is not None:
        st.write("所有工作表预览（前5行）：")
        for sheet_name, df in st.session_state.dfs.items():
            st.write(f"**{sheet_name}**:")
            st.dataframe(df.head())

        # 自然语言查询输入
        query = st.text_input("输入您的问题（自然语言）")

        if query:
            with st.spinner("正在使用本地Ollama处理您的查询..."):
                try:
                    # 将所有Sheet的DataFrame直接传入pai.chat
                    all_dfs = list(st.session_state.dfs.values())
                    result = pai.chat(query, *all_dfs)  # 使用*解包所有DataFrame

                    # 显示结果
                    st.write("回答:")
                    if isinstance(result, pd.DataFrame) or isinstance(result, pai.DataFrame):
                        st.dataframe(result)
                    elif isinstance(result, (list, dict)):
                        st.json(result)
                    else:
                        st.write(result)

                except Exception as e:
                    st.error(f"处理查询时出错: {str(e)}")

    # 添加使用说明
    with st.expander("使用说明"):
        st.write("""
        1. 确保本地Ollama服务运行（默认端口11434）
        2. 上传包含多个工作表的Excel文件
        3. 系统会自动加载所有工作表并显示预览
        4. 在文本框中输入自然语言问题，例如：
           - "谁的薪水最高？"
           - "按部门汇总总收入"
           - "所有表中总共有多少条记录？"
           - "画一个按照部门统计薪水的饼图。"
        5. 等待本地Ollama处理并查看结果

        注意：
        - 需要本地安装Ollama并下载模型（如llama2）
        - 查询性能取决于本地硬件和模型大小
        """)


if __name__ == "__main__":
    # 配置Streamlit页面
    st.set_page_config(
        page_title="Excel QA Tool (Local Ollama)",
        layout="wide"
    )

    # 检查Ollama连接
    try:
        llm_ = load_llm()
        main()
    except Exception as e:
        st.error("无法连接到本地Ollama服务，请确保其正在运行")
        st.write(f"错误详情: {str(e)}")
