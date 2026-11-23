import streamlit as st
import plotly.express as px
def render(data,model):
    st.header("Monitoring Dashboard")
    a,b,c=st.columns(3)
    a.metric("Total requests",len(data))
    b.metric("Pending",int(data.Status.astype(str).str.lower().eq("pending").sum()))
    c.metric("Completed",int(data.Status.astype(str).str.lower().eq("completed").sum()))
    counts=data.Status.value_counts().rename_axis("Status").reset_index(name="Count")
    st.plotly_chart(px.pie(counts,names="Status",values="Count"),use_container_width=True)
    pending=data[data.Status.astype(str).str.lower().eq("pending")]
    st.subheader("Pending requests for staff review")
    st.dataframe(pending[["Request_ID","Service_Type","Priority","Assigned_Office","Queue_Length"]].sort_values("Queue_Length",ascending=False),use_container_width=True)
