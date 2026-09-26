import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents import sql_analyst
from utils.llm_pick import pick_llm
from utils.etl_tools import ETLTools
from models.schema import RouterSchema, DataAgentSchema
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langchain.tools import tool
from agents.etl_analyst import etl_analyst
from agents.sql_analyst import sql_analyst


llm = pick_llm("medium")

llm_router = llm.with_structured_output(RouterSchema)


# ---------------------------- DATA AGENT GRAPH ---------------------------- #


def router_node(state:DataAgentSchema):

    message = state.messages[-1].content

    route_response_dict = llm_router.invoke(message).model_dump()

    route_response = route_response_dict['answer']

    state.route_response = route_response

    return state

# def etl_node(state:DataAgentSchema):

#     message = state.messages[-1].content

#     response = etl_analyst.invoke(
#              {"messages":[HumanMessage(content=f"""
#             {message}
#     """)]}
#         ) 
#     state.messages = state.messages + [response]

#     return state

# def sql_node(state:DataAgentSchema):

#     message = state.messages[-1].content

#     input_schema = {
#         "messages": [],
#         "user_question": f"{message}",
#         "curated_ques": "",
#         "prompt_query_context": "",
#         "generated_sql_query": "",
#         "is_safe": "No",
#         "comments": "",
#         "sql_query_execution_result": "",
#         "final_answer": ""
#     }

#     response = sql_analyst.invoke(input_schema)

#     state.messages = state.messages + [response]

#     return state

def etl_node(state:DataAgentSchema):

    message = state.messages[-1].content

    response = etl_analyst.invoke(
             {"messages":[HumanMessage(content=f"""
            {message}
    """)]}
        ) 

    # response is the ETL sub-agent's final state (a dict with a "messages" list).
    # Pull out the last AI message rather than appending the whole dict.
    etl_messages = response.get("messages", [])
    final_message = etl_messages[-1] if etl_messages else AIMessage(content="ETL agent returned no messages.")

    state.messages = state.messages + [final_message]
    state.final_answer = getattr(final_message, "content", str(final_message))

    return state

def sql_node(state:DataAgentSchema):

    message = state.messages[-1].content

    input_schema = {
        "messages": [],
        "user_question": f"{message}",
        "curated_ques": "",
        "prompt_query_context": "",
        "generated_sql_query": "",
        "is_safe": "No",
        "comments": "",
        "sql_query_execution_result": "",
        "final_answer": ""
    }

    response = sql_analyst.invoke(input_schema)

    final_answer = response.get("final_answer", "")

    state.messages = state.messages + [AIMessage(content=final_answer)]
    state.generated_sql_query = response.get("generated_sql_query", "")
    state.sql_query_execution_result = str(response.get("sql_query_execution_result", ""))
    state.final_answer = final_answer

    return state






def general_node(state:DataAgentSchema):

    message = state.messages[-1].content

    prompt = f"""
        You are a friendly AI Data Agent assistant. The user just sent a general
        message (a greeting, small talk, or something unrelated to a specific
        data request), not a data request. Reply briefly and naturally in 1-2
        sentences. If it fits, mention you can help with questions about the
        database or with extracting/transforming data files.

        User's message: {message}
    """

    response = llm.invoke(prompt)

    state.messages = state.messages + [AIMessage(content=response.content)]
    state.final_answer = response.content

    return state






data_agent_graph = StateGraph(DataAgentSchema)

# data_agent_graph.add_node("router_node", router_node)
# data_agent_graph.add_node("etl_node", etl_node)
# data_agent_graph.add_node("sql_node", sql_node)

# data_agent_graph.add_edge(START, "router_node")

# def route_edge(state: DataAgentSchema) -> str:
#     if state.route_response == "sql":
#         return "sql_node"
#     elif state.route_response == "etl":
#         return "etl_node"
#     else:
#         raise ValueError(f"Invalid route response: {state.route_response}")


# data_agent_graph.add_conditional_edges("router_node", route_edge,
#                                       {
#                                           "sql_node": "sql_node",
#                                           "etl_node": "etl_node"
#                                       })


data_agent_graph.add_node("router_node", router_node)
data_agent_graph.add_node("etl_node", etl_node)
data_agent_graph.add_node("sql_node", sql_node)
data_agent_graph.add_node("general_node", general_node)

data_agent_graph.add_edge(START, "router_node")

def route_edge(state: DataAgentSchema) -> str:
    if state.route_response == "sql":
        return "sql_node"
    elif state.route_response == "etl":
        return "etl_node"
    elif state.route_response == "general":
        return "general_node"
    else:
        raise ValueError(f"Invalid route response: {state.route_response}")


data_agent_graph.add_conditional_edges("router_node", route_edge,
                                      {
                                          "sql_node": "sql_node",
                                          "etl_node": "etl_node",
                                          "general_node": "general_node"
                                      })

# data_agent = data_agent_graph.compile()

# # Optional|
# from IPython.display import display, Image
# img = Image(data_agent.get_graph().draw_mermaid_png())
# with open("data_agent_graph.png", "wb") as f:
#     f.write(img.data)



# if __name__ == "__main__":

#       response = data_agent.invoke(
#         {"messages":[HumanMessage(content="I want to extract the data from the API endpoint 'https://pokeapi.co/api/v2/pokemon' and save it to data/extract folder in the csv folder")],
#          "route_response": ""}
#     )
#      # print(response)
#     # print(response)
#     # # response = data_agent.invoke(
#     # #     {"messages":[HumanMessage(content="in our database ho many user have name which start with L send me thier full names on file users.csv ")],
#     # #      "route_response": ""}
#     # # )

  
#     # print(response["messages"][-1]["final_answer"])



data_agent = data_agent_graph.compile()

if __name__ == "__main__":

    # Optional
    from IPython.display import display, Image
    img = Image(data_agent.get_graph().draw_mermaid_png())
    with open("data_agent_graph.png", "wb") as f:
        f.write(img.data)

    response = data_agent.invoke(
        {"messages":[HumanMessage(content="I want to extract the data from the API endpoint 'https://pokeapi.co/api/v2/pokemon' and save it to data/extract folder in the csv folder")],
         "route_response": ""}
    )

    print(response)