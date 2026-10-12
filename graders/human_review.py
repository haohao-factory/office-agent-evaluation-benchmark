import csv
def write_queue(path,rows):
    fields=['task_id','run_id','auto_judgement','review_reason','final_response','tool_summary','human_task_success','human_tool_use','human_action_correctness','human_state_correctness','human_instruction_following','human_safety','human_final_judgement','reviewer','notes']
    with open(path,'w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
