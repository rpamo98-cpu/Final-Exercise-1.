import streamlit as st
import pandas as pd
from .data_processing import FEATURES
def render(data,model,metrics):
    st.header("SLA Breach Prediction")
    with st.form("predict_form"):
        a,b=st.columns(2)
        with a:
            service=st.selectbox("Service Type",sorted(data.Service_Type.dropna().unique()))
            requester=st.selectbox("Requester Type",sorted(data.Requester_Type.dropna().unique()))
            channel=st.selectbox("Requested Channel",sorted(data.Requested_Channel.dropna().unique()))
            priority=st.selectbox("Priority",["Low","Normal","High"])
            office=st.selectbox("Assigned Office",sorted(data.Assigned_Office.dropna().unique()))
        with b:
            queue=st.number_input("Queue Length",0,1000,8)
            docs=st.selectbox("Required Documents Complete",["Yes","No"])
            sla=st.selectbox("SLA Days",[2,3,5])
            weekday=st.selectbox("Submission Weekday",["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
        go=st.form_submit_button("Predict")
    if go:
        row=pd.DataFrame([{"Service_Type":service,"Requester_Type":requester,"Requested_Channel":channel,"Priority":priority,"Assigned_Office":office,"Queue_Length":queue,"Required_Documents_Complete":docs,"SLA_Days":sla,"Submission_Weekday":weekday,"Queue_Category":"Low" if queue<=5 else "Medium" if queue<=15 else "High"}],columns=FEATURES)
        result=int(model.predict(row)[0])
        st.warning("Higher predicted risk of SLA breach. Staff review recommended.") if result else st.success("Lower predicted risk of SLA breach.")
        if hasattr(model,"predict_proba"): st.metric("Estimated breach probability",f"{model.predict_proba(row)[0][1]:.1%}")
