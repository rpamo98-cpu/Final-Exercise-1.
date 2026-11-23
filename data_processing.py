import pandas as pd
FEATURES=["Service_Type","Requester_Type","Requested_Channel","Priority","Assigned_Office","Queue_Length","Required_Documents_Complete","SLA_Days","Submission_Weekday","Queue_Category"]
CATEGORICAL=["Service_Type","Requester_Type","Requested_Channel","Priority","Assigned_Office","Required_Documents_Complete","Submission_Weekday","Queue_Category"]
NUMERIC=["Queue_Length","SLA_Days"]
REQUIRED_COLUMNS=["Request_ID","Service_Type","Requester_Type","Submission_Date","Requested_Channel","Priority","Assigned_Office","Queue_Length","Required_Documents_Complete","Processing_Days","SLA_Days","Status","Reopened","Satisfaction_Score","Submission_Weekday","Queue_Category","SLA_Breached"]
def validate(data):
    if not isinstance(data,pd.DataFrame) or data.empty: raise ValueError("CSV is empty or invalid.")
    missing=[c for c in REQUIRED_COLUMNS if c not in data.columns]
    if missing: raise ValueError("Missing required columns: "+", ".join(missing))
    data=data.copy()
    for c in ["Queue_Length","SLA_Days","Processing_Days","SLA_Breached"]:
        data[c]=pd.to_numeric(data[c],errors="coerce")
    data["Submission_Date"]=pd.to_datetime(data["Submission_Date"],errors="coerce")
    return data
