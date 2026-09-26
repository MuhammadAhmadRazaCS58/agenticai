# import os
# import requests
# import pandas as pd

# class ETLTools:

#     def __init__(self):
#         pass

#     def extract_load(self,url:str, output_folder:str, format:str):
#         """
#         This tool extracts the data from the API (url) and loads it into the
#         the desired location (output_folder).

#         Args:
#             url (str): The API endpoint from which to extract data.
#             output_folder (str): The folder where the extracted data will be saved.
        
#         Returns:
#             str: A message indicating the success or failure of the operation.

#         """

#         project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
#         output_folder = os.path.join(project_root, output_folder)      

#         try:
#             response = requests.get(url)
#             response.raise_for_status()
#             data  = response.json()

#             filename = os.path.join(output_folder, f"extracted_data.{format}")
#             os.makedirs(output_folder, exist_ok=True)

#             df = pd.json_normalize(data['results'])
#             if format == "csv":
#                 df.to_csv(filename, index=False)
#             elif format == "json":
#                 df.to_json(filename, orient="records", lines=True)
#             elif format == "parquet":
#                 df.to_parquet(filename, index=False)
#             else:
#                 return f"Unsupported format: {format}"

#             return f"Data successfully extracted and saved to {filename}"
#         except requests.exceptions.RequestException as e:
#             return f"Failed to extract data: {e}"





#     def transform_load_context(self, file_path:str):
#         """
#         This tool transforms the data from the specified file and loads it into the
#         desired location (output_folder).

#         Args:
#             file_path (str): The path to the file containing the data to be transformed.
#             output_folder (str): The folder where the transformed data will be saved.
#             output_format (str): The format in which to save the transformed data (csv, json, parquet).
#         Returns:
#             str: A message indicating the success or failure of the operation.
#         """

#         file_extension = os.path.splitext(file_path)[1].lower()
#         if file_extension == ".csv":
#             df = pd.read_csv(file_path)
#         elif file_extension == ".json":
#             df = pd.read_json(file_path, lines=True)
#         elif file_extension == ".parquet":
#             df = pd.read_parquet(file_path)
#         else:
#             return f"Unsupported file format: {file_extension}"

#         top_3_rows = str(df.head(3))

#         return top_3_rows
# #     def execute_code(self,code:str):
# #         """
# #         This tool executes the provided code and returns the output.

# #         Args:
# #             code (str): The code to be executed.
# #         Returns:
# #             str: The output of the executed code or an error message if execution fails.
# #         """

# #         try:
# #             exec(code)
# #             return "Code executed successfully."
# #         except Exception as e:
# #             return f"Failed to execute code: {e}"
    
  
# # if __name__ == "__main__":
# #     obj = ETLTools()
# #     path = "C:\\Users\\DELL\\Downloads\\agenticai\\data\\extract\\extracted_data.csv"
# #     print(obj.transform_load_context(path))
          
# def execute_code(self, code:str, extra_globals: dict = None):
#         """
#         This tool executes the provided code and returns the output.

#         Args:
#             code (str): The code to be executed.
#             extra_globals (dict): Optional extra variables (e.g. a pre-loaded
#                 DataFrame) to make available to the executed code.
#         Returns:
#             str: The captured stdout / result of the executed code, or an
#             error message if execution fails.
#         """
#         import io
#         import contextlib

#         exec_globals = {"pd": pd, "os": os, "requests": requests}
#         if extra_globals:
#             exec_globals.update(extra_globals)

#         local_vars = {}
#         buffer = io.StringIO()

#         try:
#             with contextlib.redirect_stdout(buffer):
#                 exec(code, exec_globals, local_vars)

#             output = buffer.getvalue().strip()

#             if not output and "result" in local_vars:
#                 output = str(local_vars["result"])

#             return output if output else "Code executed successfully, but produced no output."
#         except Exception as e:
#             return f"Failed to execute code: {e}"

# def answer_question_about_file(self, file_path: str, question: str) -> str:
#         """
#         Loads the file at file_path into a pandas DataFrame and uses an LLM to
#         write and run pandas code that answers the question using ONLY that
#         file's data.

#         Args:
#             file_path (str): Path to the uploaded file (csv, json, xlsx, parquet).
#             question (str): The user's question about the file.
#         Returns:
#             str: The answer, followed by the pandas code that produced it.
#         """
#         from utils.llm_pick import pick_llm

#         file_extension = os.path.splitext(file_path)[1].lower()

#         try:
#             if file_extension == ".csv":
#                 df = pd.read_csv(file_path)
#             elif file_extension == ".json":
#                 df = pd.read_json(file_path)
#             elif file_extension in (".xlsx", ".xls"):
#                 df = pd.read_excel(file_path)
#             elif file_extension == ".parquet":
#                 df = pd.read_parquet(file_path)
#             else:
#                 return f"Unsupported file format: {file_extension}"
#         except Exception as e:
#             return f"Failed to read the uploaded file: {e}"

#         preview = df.head(5).to_string()
#         columns_info = ", ".join(f"{c} ({df[c].dtype})" for c in df.columns)

#         llm = pick_llm("medium")

#         prompt = f"""
#             You are a Python data analyst. Write ONLY pandas code (no explanation,
#             no markdown fences, no imports) that answers the user's question using
#             a DataFrame called `df` that is ALREADY loaded in memory. Do not read
#             the file again and do not save/write any file.

#             The DataFrame has these columns: {columns_info}
#             Preview of the data:
#             {preview}

#             Store your final answer in a variable called `result` and also
#             print(result) at the end.

#             User's question: {question}
#         """

#         code = llm.invoke(prompt).content
#         code = code.strip().strip("```").strip()
#         if code.lower().startswith("python"):
#             code = code[len("python"):].strip()

#         output = self.execute_code(code, extra_globals={"df": df})

#         return f"{output}\n\n---\nPandas code used:\n{code}"


# if __name__ == "__main__":
#   obj = ETLTools()
#   path = "C:\\Users\\DELL\\Downloads\\agenticai\\data\\extract\\extracted_data.csv"
#   print(obj.transform_load_context(path))
        


import os
import requests
import pandas as pd

class ETLTools:

    def __init__(self):
        pass

    def extract_load(self,url:str, output_folder:str, format:str):
        """
        This tool extracts the data from the API (url) and loads it into the
        the desired location (output_folder).

        Args:
            url (str): The API endpoint from which to extract data.
            output_folder (str): The folder where the extracted data will be saved.
        
        Returns:
            str: A message indicating the success or failure of the operation.

        """

        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        output_folder = os.path.join(project_root, output_folder)      

        try:
            response = requests.get(url)
            response.raise_for_status()
            data  = response.json()

            filename = os.path.join(output_folder, f"extracted_data.{format}")
            os.makedirs(output_folder, exist_ok=True)

            df = pd.json_normalize(data['results'])
            if format == "csv":
                df.to_csv(filename, index=False)
            elif format == "json":
                df.to_json(filename, orient="records", lines=True)
            elif format == "parquet":
                df.to_parquet(filename, index=False)
            else:
                return f"Unsupported format: {format}"

            return f"Data successfully extracted and saved to {filename}"
        except requests.exceptions.RequestException as e:
            return f"Failed to extract data: {e}"


    def transform_load_context(self, file_path:str):
        """
        This tool transforms the data from the specified file and loads it into the
        desired location (output_folder).

        Args:
            file_path (str): The path to the file containing the data to be transformed.
            output_folder (str): The folder where the transformed data will be saved.
            output_format (str): The format in which to save the transformed data (csv, json, parquet).
        Returns:
            str: A message indicating the success or failure of the operation.
        """

        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == ".csv":
            df = pd.read_csv(file_path)
        elif file_extension == ".json":
            df = pd.read_json(file_path, lines=True)
        elif file_extension == ".parquet":
            df = pd.read_parquet(file_path)
        else:
            return f"Unsupported file format: {file_extension}"

        top_3_rows = str(df.head(3))

        return top_3_rows

    def execute_code(self, code:str, extra_globals: dict = None):
        """
        This tool executes the provided code and returns the output.

        Args:
            code (str): The code to be executed.
            extra_globals (dict): Optional extra variables (e.g. a pre-loaded
                DataFrame) to make available to the executed code.
        Returns:
            str: The captured stdout / result of the executed code, or an
            error message if execution fails.
        """
        import io
        import contextlib

        exec_globals = {"pd": pd, "os": os, "requests": requests}
        if extra_globals:
            exec_globals.update(extra_globals)

        local_vars = {}
        buffer = io.StringIO()

        try:
            with contextlib.redirect_stdout(buffer):
                exec(code, exec_globals, local_vars)

            output = buffer.getvalue().strip()

            if not output and "result" in local_vars:
                output = str(local_vars["result"])

            return output if output else "Code executed successfully, but produced no output."
        except Exception as e:
            return f"Failed to execute code: {e}"

    def answer_question_about_file(self, file_path: str, question: str) -> str:
        """
        Loads the file at file_path into a pandas DataFrame and uses an LLM to
        write and run pandas code that answers the question using ONLY that
        file's data.

        Args:
            file_path (str): Path to the uploaded file (csv, json, xlsx, parquet).
            question (str): The user's question about the file.
        Returns:
            str: The answer, followed by the pandas code that produced it.
        """
        from utils.llm_pick import pick_llm

        file_extension = os.path.splitext(file_path)[1].lower()

        try:
            if file_extension == ".csv":
                df = pd.read_csv(file_path)
            elif file_extension == ".json":
                df = pd.read_json(file_path)
            elif file_extension in (".xlsx", ".xls"):
                df = pd.read_excel(file_path)
            elif file_extension == ".parquet":
                df = pd.read_parquet(file_path)
            else:
                return f"Unsupported file format: {file_extension}"
        except Exception as e:
            return f"Failed to read the uploaded file: {e}"

        preview = df.head(5).to_string()
        columns_info = ", ".join(f"{c} ({df[c].dtype})" for c in df.columns)

        llm = pick_llm("medium")

        prompt = f"""
            You are a Python data analyst. Write ONLY pandas code (no explanation,
            no markdown fences, no imports) that answers the user's question using
            a DataFrame called `df` that is ALREADY loaded in memory. Do not read
            the file again and do not save/write any file.

            The DataFrame has these columns: {columns_info}
            Preview of the data:
            {preview}

            Store your final answer in a variable called `result` and also
            print(result) at the end.

            User's question: {question}
        """

        code = llm.invoke(prompt).content
        code = code.strip().strip("```").strip()
        if code.lower().startswith("python"):
            code = code[len("python"):].strip()

        output = self.execute_code(code, extra_globals={"df": df})

        return f"{output}\n\n---\nPandas code used:\n{code}"


if __name__ == "__main__":
    obj = ETLTools()
    path = "C:\\Users\\DELL\\Downloads\\agenticai\\data\\extract\\extracted_data.csv"
    print(obj.transform_load_context(path))