# # """
# # Streamlit web UI for the AI Data Agent.

# # Run with:
# #     streamlit run app.py
# # """

# # import os
# # import traceback

# # import streamlit as st
# # from dotenv import load_dotenv
# # from langchain_core.messages import AIMessage, HumanMessage

# # load_dotenv()

# # from agents.data_agent import data_agent  # noqa: E402  (import after load_dotenv on purpose)


# # # --------------------------------------------------------------------------- #
# # # Page setup
# # # --------------------------------------------------------------------------- #

# # st.set_page_config(
# #     page_title="AI Data Agent",
# #     page_icon="🤖",
# #     layout="wide",
# # )

# # REQUIRED_DB_VARS = ["host", "port", "user", "password", "database"]
# # REQUIRED_LLM_VARS = ["ANTHROPIC_API_KEY", "OPENAI_API_KEY"]


# # def env_status(var_names):
# #     return {name: bool(os.environ.get(name)) for name in var_names}


# # # --------------------------------------------------------------------------- #
# # # Sidebar
# # # --------------------------------------------------------------------------- #

# # with st.sidebar:
# #     st.title("🤖 AI Data Agent")
# #     st.caption("Ask questions in plain English. The router sends SQL questions "
# #                "to the SQL analyst and data-pipeline requests to the ETL analyst.")

# #     st.divider()
# #     st.subheader("Environment check")

# #     db_status = env_status(REQUIRED_DB_VARS)
# #     llm_status = env_status(REQUIRED_LLM_VARS)

# #     for name, ok in {**llm_status, **db_status}.items():
# #         st.write(("✅ " if ok else "❌ ") + name)

# #     if not all(db_status.values()):
# #         st.warning("Missing DB env vars — SQL questions will fail. Set them in a `.env` file "
# #                     "(see `.env.example`).")
# #     if not any(llm_status.values()):
# #         st.warning("No LLM API key found. Set ANTHROPIC_API_KEY and/or OPENAI_API_KEY in `.env`.")

# #     st.divider()
# #     if st.button("🗑️ Clear conversation", use_container_width=True):
# #         st.session_state.lc_messages = []
# #         st.session_state.display_messages = []
# #         st.rerun()

# #     st.divider()
# #     with st.expander("Example questions"):
# #         st.markdown(
# #             "- What are the different payment methods in the database?\n"
# #             "- Show me the 10 most recent rides.\n"
# #             "- Extract data from `https://pokeapi.co/api/v2/pokemon` and save it "
# #             "to `data/extract` as csv.\n"
# #         )


# # # --------------------------------------------------------------------------- #
# # # Session state
# # # --------------------------------------------------------------------------- #

# # if "lc_messages" not in st.session_state:
# #     st.session_state.lc_messages = []          # LangChain message objects fed to the agent
# # if "display_messages" not in st.session_state:
# #     st.session_state.display_messages = []     # dicts used to render the chat


# # # --------------------------------------------------------------------------- #
# # # Render existing history
# # # --------------------------------------------------------------------------- #

# # st.header("Chat with your data")

# # for msg in st.session_state.display_messages:
# #     with st.chat_message(msg["role"]):
# #         if msg["role"] == "assistant" and msg.get("route"):
# #             st.caption(f"routed to **{msg['route']}** agent")
# #         st.markdown(msg["content"])
# #         if msg.get("sql_query"):
# #             with st.expander("Generated SQL query"):
# #                 st.code(msg["sql_query"], language="sql")
# #         if msg.get("sql_result"):
# #             with st.expander("Raw query result"):
# #                 st.code(msg["sql_result"])


# # # --------------------------------------------------------------------------- #
# # # Handle new input
# # # --------------------------------------------------------------------------- #

# # user_input = st.chat_input("Ask about your data, or ask the agent to extract/transform a dataset...")

# # if user_input:
# #     st.session_state.display_messages.append({"role": "user", "content": user_input})
# #     st.session_state.lc_messages.append(HumanMessage(content=user_input))

# #     with st.chat_message("user"):
# #         st.markdown(user_input)

# #     with st.chat_message("assistant"):
# #         with st.spinner("Thinking..."):
# #             try:
# #                 response = data_agent.invoke(
# #                     {"messages": st.session_state.lc_messages, "route_response": ""}
# #                 )

# #                 route = response.get("route_response", "")
# #                 final_answer = response.get("final_answer") or "The agent finished but returned no text answer."
# #                 sql_query = response.get("generated_sql_query", "")
# #                 sql_result = response.get("sql_query_execution_result", "")

# #                 st.session_state.lc_messages = response.get("messages", st.session_state.lc_messages)

# #                 if route:
# #                     st.caption(f"routed to **{route}** agent")
# #                 st.markdown(final_answer)

# #                 if sql_query:
# #                     with st.expander("Generated SQL query"):
# #                         st.code(sql_query, language="sql")
# #                 if sql_result:
# #                     with st.expander("Raw query result"):
# #                         st.code(sql_result)

# #                 st.session_state.display_messages.append({
# #                     "role": "assistant",
# #                     "content": final_answer,
# #                     "route": route,
# #                     "sql_query": sql_query,
# #                     "sql_result": sql_result,
# #                 })

# #             except Exception as e:
# #                 error_text = f"Something went wrong: {e}"
# #                 st.error(error_text)
# #                 with st.expander("Details"):
# #                     st.code(traceback.format_exc())
# #                 st.session_state.display_messages.append({
# #                     "role": "assistant",
# #                     "content": error_text,
# #                 })
# #                 if st.session_state.lc_messages and isinstance(st.session_state.lc_messages[-1], HumanMessage):
# #                     st.session_state.lc_messages.pop()

# """
# Streamlit web UI for the AI Data Agent.

# Run with:

#     streamlit run app.py
# """

# import os
# import traceback

# import streamlit as st
# from dotenv import load_dotenv
# # from langchain_core.messages import HumanMessage

# # load_dotenv()

# # from agents.data_agent import data_agent
# from langchain_core.messages import AIMessage, HumanMessage

# load_dotenv()

# from agents.data_agent import data_agent
# from utils.etl_tools import ETLTools

# etl_tools = ETLTools()

# GREETINGS = {
#     "hi", "hello", "hey", "hii", "hiya", "yo", "sup",
#     "good morning", "good afternoon", "good evening",
#     "how are you", "whats up", "what's up", "thanks", "thank you", "bye"
# }


# def is_greeting(text: str) -> bool:
#     cleaned = text.strip().lower().rstrip("!?. ")
#     return cleaned in GREETINGS


# # ---------------------------------------------------------------------------
# # Page setup
# # ---------------------------------------------------------------------------

# st.set_page_config(
#     page_title="AI Data Agent",
#     page_icon="🤖",
#     layout="wide",
# )


# # ---------------------------------------------------------------------------
# # Environment variables
# # ---------------------------------------------------------------------------

# REQUIRED_DB_VARS = [
#     "host",
#     "port",
#     "user",
#     "password",
#     "database"
# ]

# REQUIRED_LLM_VARS = [
#     "MISTRAL_API_KEY"
# ]


# def env_status(var_names):
#     return {
#         name: bool(os.environ.get(name))
#         for name in var_names
#     }


# # ---------------------------------------------------------------------------
# # Sidebar
# # ---------------------------------------------------------------------------

# with st.sidebar:

#     st.title("🤖 AI Data Agent")

#     st.caption(
#         "Ask questions in plain English. "
#         "The router sends SQL questions to the SQL analyst "
#         "and data-pipeline requests to the ETL analyst."
#     )

#     st.divider()

#     st.subheader("Environment check")

#     db_status = env_status(REQUIRED_DB_VARS)
#     llm_status = env_status(REQUIRED_LLM_VARS)

#     for name, ok in {
#         **llm_status,
#         **db_status
#     }.items():

#         st.write(
#             ("✅ " if ok else "❌ ") + name
#         )

#     if not all(db_status.values()):

#         st.warning(
#             "Missing DB environment variables. "
#             "SQL questions may fail. "
#             "Set them in your .env file."
#         )

#     if not all(llm_status.values()):

#         st.warning(
#             "Mistral API key not found. "
#             "Set MISTRAL_API_KEY in your .env file."
#         )

#     st.divider()

#     if st.button(
#         "🗑️ Clear conversation",
#         use_container_width=True
#     ):

#     #     st.session_state.lc_messages = []
#     #     st.session_state.display_messages = []

#     #     st.rerun()

#     # st.divider()

#     # with st.expander("Example questions"):
#      st.session_state.lc_messages = []
#     st.session_state.display_messages = []

#     st.rerun()

#     st.divider()

#     st.subheader("📁 Ask about your own file")

#     uploaded_file = st.file_uploader(
#         "Upload a CSV, JSON, Excel, or Parquet file",
#         type=["csv", "json", "xlsx", "xls", "parquet"]
#     )

#     if uploaded_file is not None:

#         upload_dir = os.path.join(
#             os.path.dirname(os.path.abspath(__file__)), "data", "uploads"
#         )
#         os.makedirs(upload_dir, exist_ok=True)

#         saved_path = os.path.join(upload_dir, uploaded_file.name)

#         with open(saved_path, "wb") as f:
#             f.write(uploaded_file.getbuffer())

#         st.session_state.uploaded_file_path = saved_path
#         st.success(f"Now answering questions from: {uploaded_file.name}")

#     if st.session_state.get("uploaded_file_path"):

#         st.caption(
#             f"Active file: **{os.path.basename(st.session_state.uploaded_file_path)}**. "
#             "Questions will be answered from this file only."
#         )

#         if st.button("❌ Clear uploaded file", use_container_width=True):
#             st.session_state.uploaded_file_path = None
#             st.rerun()

#     st.divider()

#     with st.expander("Example questions"):

#         st.markdown(
#             "- What are the different payment methods in the database?\n"
#             "- Show me the 10 most recent rides.\n"
#             "- Extract data from https://pokeapi.co/api/v2/pokemon "
#             "and save it to `data/extract` as csv."
#         )


# # ---------------------------------------------------------------------------
# # Session state
# # ---------------------------------------------------------------------------

# if "lc_messages" not in st.session_state:

#     st.session_state.lc_messages = []


# # if "display_messages" not in st.session_state:

# #     st.session_state.display_messages = []
# if "display_messages" not in st.session_state:

#     st.session_state.display_messages = []

# if "uploaded_file_path" not in st.session_state:

#     st.session_state.uploaded_file_path = None

# # ---------------------------------------------------------------------------
# # Render existing chat history
# # ---------------------------------------------------------------------------

# st.header("💬 Chat with your data")

# for msg in st.session_state.display_messages:

#     with st.chat_message(msg["role"]):

#         if msg["role"] == "assistant" and msg.get("route"):

#             st.caption(
#                 f"Routed to **{msg['route']}** agent"
#             )

#         st.markdown(msg["content"])

#         if msg.get("sql_query"):

#             with st.expander("Generated SQL query"):

#                 st.code(
#                     msg["sql_query"],
#                     language="sql"
#                 )

#         if msg.get("sql_result"):

#             with st.expander("Raw query result"):

#                 st.code(msg["sql_result"])


# # ---------------------------------------------------------------------------
# # Handle new user input
# # ---------------------------------------------------------------------------

# user_input = st.chat_input(
#     "Ask about your data, or ask the agent to extract/transform a dataset..."
# )


# if user_input:

#     # Save user message
#     st.session_state.display_messages.append(
#         {
#             "role": "user",
#             "content": user_input
#         }
#     )

#     st.session_state.lc_messages.append(
#         HumanMessage(content=user_input)
#     )

#     # Display user message
#     with st.chat_message("user"):

#         st.markdown(user_input)

#     # Generate AI response
#     with st.chat_message("assistant"):

#         with st.spinner("🤔 Thinking..."):

#             # try:

#             #     response = data_agent.invoke(
#             #         {
#             #             "messages": st.session_state.lc_messages,
#             #             "route_response": ""
#             #         }
#             #     )

#             #     # Get response information
#             #     route = response.get(
#             #         "route_response",
#             #         ""
#             #     )

#             #     final_answer = response.get(
#             #         "final_answer"
#             #     ) or "The agent finished but returned no text answer."

#             #     sql_query = response.get(
#             #         "generated_sql_query",
#             #         ""
#             #     )

#             #     sql_result = response.get(
#             #         "sql_query_execution_result",
#             #         ""
#             #     )

#             #     # Update conversation
#             #     st.session_state.lc_messages = response.get(
#             #         "messages",
#             #         st.session_state.lc_messages
#             #     )

#             #     # Show route
#             #     if route:

#             #         st.caption(
#             #             f"Routed to **{route}** agent"
#             #         )

#             #     # Show final answer
#             #     st.markdown(final_answer)
#             try:

#                 route = ""
#                 sql_query = ""
#                 sql_result = ""

#                 if is_greeting(user_input):
#                     # Fast path: no LLM/agent call needed for plain greetings.
#                     route = "general"
#                     final_answer = (
#                         "Hey there! 👋 Ask me a question about your database, "
#                         "upload a file in the sidebar to search through it, "
#                         "or ask me to extract/transform some data."
#                     )
#                     st.session_state.lc_messages.append(AIMessage(content=final_answer))

#                 elif st.session_state.get("uploaded_file_path"):
#                     # A file is active: answer strictly from that file, not
#                     # the database or anything else.
#                     route = "uploaded file"
#                     final_answer = etl_tools.answer_question_about_file(
#                         st.session_state.uploaded_file_path,
#                         user_input
#                     )
#                     st.session_state.lc_messages.append(AIMessage(content=final_answer))

#                 else:
#                     response = data_agent.invoke(
#                         {
#                             "messages": st.session_state.lc_messages,
#                             "route_response": ""
#                         }
#                     )

#                     route = response.get("route_response", "")

#                     final_answer = response.get(
#                         "final_answer"
#                     ) or "The agent finished but returned no text answer."

#                     sql_query = response.get("generated_sql_query", "")
#                     sql_result = response.get("sql_query_execution_result", "")

#                     # Update conversation history only for the graph path -
#                     # greeting/file answers aren't part of the graph's own memory.
#                     st.session_state.lc_messages = response.get(
#                         "messages",
#                         st.session_state.lc_messages
#                     )

#                 # Show route
#                 if route:

#                     st.caption(
#                         f"Routed to **{route}**"
#                     )

#                 # Show final answer
#                 st.markdown(final_answer)

#                 # Show SQL
#                 if sql_query:

#                     with st.expander("Generated SQL query"):

#                         st.code(
#                             sql_query,
#                             language="sql"
#                         )

#                 # Show SQL result
#                 if sql_result:

#                     with st.expander("Raw query result"):

#                         st.code(sql_result)

#                 # Save assistant message
#                 st.session_state.display_messages.append(
#                     {
#                         "role": "assistant",
#                         "content": final_answer,
#                         "route": route,
#                         "sql_query": sql_query,
#                         "sql_result": sql_result,
#                     }
#                 )

#             except Exception as e:

#                 error_text = f"Something went wrong: {e}"

#                 st.error(error_text)

#                 with st.expander("Details"):

#                     st.code(
#                         traceback.format_exc()
#                     )

#                 st.session_state.display_messages.append(
#                     {
#                         "role": "assistant",
#                         "content": error_text,
#                     }
#                 )

#                 # Remove failed user message
#                 if (
#                     st.session_state.lc_messages
#                     and isinstance(
#                         st.session_state.lc_messages[-1],
#                         HumanMessage
#                     )
#                 ):

#                     st.session_state.lc_messages.pop()


"""
Streamlit web UI for the AI Data Agent.

Run with:

    streamlit run app.py
"""

import os
import traceback

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage

load_dotenv()

from agents.data_agent import data_agent
from utils.etl_tools import ETLTools

etl_tools = ETLTools()

GREETINGS = {
    "hi", "hello", "hey", "hii", "hiya", "yo", "sup",
    "good morning", "good afternoon", "good evening",
    "how are you", "whats up", "what's up", "thanks", "thank you", "bye"
}


def is_greeting(text: str) -> bool:
    cleaned = text.strip().lower().rstrip("!?. ")
    return cleaned in GREETINGS


# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="AI Data Agent",
    page_icon="🤖",
    layout="wide",
)


# ---------------------------------------------------------------------------
# Environment variables
# ---------------------------------------------------------------------------

REQUIRED_DB_VARS = [
    "host",
    "port",
    "user",
    "password",
    "database"
]

REQUIRED_LLM_VARS = [
    "MISTRAL_API_KEY"
]


def env_status(var_names):
    return {
        name: bool(os.environ.get(name))
        for name in var_names
    }


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:

    st.title("🤖 AI Data Agent")

    st.caption(
        "Ask questions in plain English. "
        "The router sends SQL questions to the SQL analyst "
        "and data-pipeline requests to the ETL analyst."
    )

    st.divider()

    st.subheader("Environment check")

    db_status = env_status(REQUIRED_DB_VARS)
    llm_status = env_status(REQUIRED_LLM_VARS)

    for name, ok in {
        **llm_status,
        **db_status
    }.items():

        st.write(
            ("✅ " if ok else "❌ ") + name
        )

    if not all(db_status.values()):

        st.warning(
            "Missing DB environment variables. "
            "SQL questions may fail. "
            "Set them in your .env file."
        )

    if not all(llm_status.values()):

        st.warning(
            "Mistral API key not found. "
            "Set MISTRAL_API_KEY in your .env file."
        )

    st.divider()

    if st.button(
        "🗑️ Clear conversation",
        use_container_width=True
    ):
        st.session_state.lc_messages = []
        st.session_state.display_messages = []
        st.rerun()

    st.divider()

    st.subheader("📁 Ask about your own file")

    uploaded_file = st.file_uploader(
        "Upload a CSV, JSON, Excel, or Parquet file",
        type=["csv", "json", "xlsx", "xls", "parquet"]
    )

    if uploaded_file is not None:

        upload_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "data", "uploads"
        )
        os.makedirs(upload_dir, exist_ok=True)

        saved_path = os.path.join(upload_dir, uploaded_file.name)

        with open(saved_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.session_state.uploaded_file_path = saved_path
        st.success(f"Now answering questions from: {uploaded_file.name}")

    if st.session_state.get("uploaded_file_path"):

        st.caption(
            f"Active file: **{os.path.basename(st.session_state.uploaded_file_path)}**. "
            "Questions will be answered from this file only."
        )

        if st.button("❌ Clear uploaded file", use_container_width=True):
            st.session_state.uploaded_file_path = None
            st.rerun()

    st.divider()

    with st.expander("Example questions"):

        st.markdown(
            "- What are the different payment methods in the database?\n"
            "- Show me the 10 most recent rides.\n"
            "- Extract data from https://pokeapi.co/api/v2/pokemon "
            "and save it to `data/extract` as csv."
        )


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

if "lc_messages" not in st.session_state:

    st.session_state.lc_messages = []

if "display_messages" not in st.session_state:

    st.session_state.display_messages = []

if "uploaded_file_path" not in st.session_state:

    st.session_state.uploaded_file_path = None


# ---------------------------------------------------------------------------
# Render existing chat history
# ---------------------------------------------------------------------------

st.header("💬 Chat with your data")

for msg in st.session_state.display_messages:

    with st.chat_message(msg["role"]):

        if msg["role"] == "assistant" and msg.get("route"):

            st.caption(
                f"Routed to **{msg['route']}** agent"
            )

        st.markdown(msg["content"])

        if msg.get("sql_query"):

            with st.expander("Generated SQL query"):

                st.code(
                    msg["sql_query"],
                    language="sql"
                )

        if msg.get("sql_result"):

            with st.expander("Raw query result"):

                st.code(msg["sql_result"])


# ---------------------------------------------------------------------------
# Handle new user input
# ---------------------------------------------------------------------------

user_input = st.chat_input(
    "Ask about your data, or ask the agent to extract/transform a dataset..."
)


if user_input:

    # Save user message
    st.session_state.display_messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    st.session_state.lc_messages.append(
        HumanMessage(content=user_input)
    )

    # Display user message
    with st.chat_message("user"):

        st.markdown(user_input)

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("🤔 Thinking..."):

            try:

                route = ""
                sql_query = ""
                sql_result = ""

                if is_greeting(user_input):
                    # Fast path: no LLM/agent call needed for plain greetings.
                    route = "general"
                    final_answer = (
                        "Hey there! 👋 Ask me a question about your database, "
                        "upload a file in the sidebar to search through it, "
                        "or ask me to extract/transform some data."
                    )
                    st.session_state.lc_messages.append(AIMessage(content=final_answer))

                elif st.session_state.get("uploaded_file_path"):
                    # A file is active: answer strictly from that file, not
                    # the database or anything else.
                    route = "uploaded file"
                    final_answer = etl_tools.answer_question_about_file(
                        st.session_state.uploaded_file_path,
                        user_input
                    )
                    st.session_state.lc_messages.append(AIMessage(content=final_answer))

                else:
                    response = data_agent.invoke(
                        {
                            "messages": st.session_state.lc_messages,
                            "route_response": ""
                        }
                    )

                    route = response.get("route_response", "")

                    final_answer = response.get(
                        "final_answer"
                    ) or "The agent finished but returned no text answer."

                    sql_query = response.get("generated_sql_query", "")
                    sql_result = response.get("sql_query_execution_result", "")

                    # Update conversation history only for the graph path -
                    # greeting/file answers aren't part of the graph's own memory.
                    st.session_state.lc_messages = response.get(
                        "messages",
                        st.session_state.lc_messages
                    )

                # Show route
                if route:

                    st.caption(
                        f"Routed to **{route}**"
                    )

                # Show final answer
                st.markdown(final_answer)

                # Show SQL
                if sql_query:

                    with st.expander("Generated SQL query"):

                        st.code(
                            sql_query,
                            language="sql"
                        )

                # Show SQL result
                if sql_result:

                    with st.expander("Raw query result"):

                        st.code(sql_result)

                # Save assistant message
                st.session_state.display_messages.append(
                    {
                        "role": "assistant",
                        "content": final_answer,
                        "route": route,
                        "sql_query": sql_query,
                        "sql_result": sql_result,
                    }
                )

            except Exception as e:

                error_text = f"Something went wrong: {e}"

                st.error(error_text)

                with st.expander("Details"):

                    st.code(
                        traceback.format_exc()
                    )

                st.session_state.display_messages.append(
                    {
                        "role": "assistant",
                        "content": error_text,
                    }
                )

                # Remove failed user message
                if (
                    st.session_state.lc_messages
                    and isinstance(
                        st.session_state.lc_messages[-1],
                        HumanMessage
                    )
                ):

                    st.session_state.lc_messages.pop()