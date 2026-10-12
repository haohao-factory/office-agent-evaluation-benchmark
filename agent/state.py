from typing import TypedDict, Any
class AgentState(TypedDict, total=False):
 messages:list; task_id:str; run_id:str; tool_calls:list; tool_results:list; error_log:list; step_count:int; final_response:str
