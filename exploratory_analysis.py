import streamlit as st
import plotly.express as px
def render(data):
    st.header("Exploratory Data Analysis")
    a,b,c=st.columns(3); a.metric("Total requests",len(data)); b.metric("Service types",data.Service_Type.nunique()); c.metric("Offices",data.Assigned_Office.nunique())
    counts=data.Service_Type.value_counts().rename_axis("Service Type").reset_index(name="Requests")
    st.plotly_chart(px.bar(counts,x="Service Type",y="Requests"),use_container_width=True)
    labeled=data[data.SLA_Breached.isin([0,1])]
    if not labeled.empty:
        rates=labeled.groupby("Assigned_Office",as_index=False).SLA_Breached.mean()
        rates["Breach Rate (%)"]=rates.SLA_Breached*100
        st.plotly_chart(px.bar(rates,x="Assigned_Office",y="Breach Rate (%)"),use_container_width=True)
