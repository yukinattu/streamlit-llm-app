import streamlit as st
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# 環境変数の読み込み
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# 関数定義
def ask_llm(user_input: str, expert_type: str) -> str:
    """入力と専門家タイプに応じてLLMへ問い合わせ、回答を返す"""
    system_messages = {
        "医者": "あなたはプロの内科医です。ユーザーの健康に関する質問に対して、専門的かつ丁寧に答えてください。",
        "法律家": "あなたは熟練の弁護士です。法律に関する質問に対して、正確かつ誠実に答えてください。",
    }

    llm = ChatOpenAI(model_name="gpt-4o", temperature=0, api_key=openai_api_key)

    messages = [
        SystemMessage(content=system_messages[expert_type]),
        HumanMessage(content=user_input),
    ]

    response = llm(messages)
    return response.content

# WebアプリのUI
st.title("LLM相談アプリ")
st.write("このアプリでは、専門家（医者または法律家）に相談する形式でAIが回答を行います。")
st.write("以下の入力フォームに相談内容を入力し、相談したい専門家を選んでください。")

# 入力フォーム
expert_type = st.radio("相談したい専門家を選んでください", ["医者", "法律家"])
user_input = st.text_area("相談内容を入力してください")

# 実行ボタン
if st.button("相談する"):
    if user_input:
        try:
            answer = ask_llm(user_input, expert_type)
            st.divider()
            st.markdown("#### 回答")
            st.write(answer)
        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")
    else:
        st.warning("相談内容を入力してください。")
