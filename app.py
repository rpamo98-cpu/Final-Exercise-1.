from pathlib import Path
import json,joblib,pandas as pd,streamlit as st
from modules.data_processing import validate
from modules.exploratory_analysis import render as eda
from modules.prediction import render as prediction
from modules.dashboard import render as dashboard
st.set_page_config(page_title="Student Service SLA Monitor",page_icon="📋",layout="wide")
root=Path(__file__).resolve().parent
@st.cache_resource
def load_model(): return joblib.load(root/"models/student_model.pkl")
@st.cache_data
def default_data(): return pd.read_csv(root/"data/student_data.csv")
st.sidebar.title("Student Service Monitor")
menu=st.sidebar.selectbox("Module",["Home","Dataset","Data Analysis","Prediction","Dashboard","System Design"])
uploaded=st.sidebar.file_uploader("Upload a CSV (optional)",type=["csv"])
try:
    data=validate(pd.read_csv(uploaded) if uploaded else default_data())
    model=load_model()
    metrics=json.loads((root/"models/metrics.json").read_text())
except Exception as exc:
    st.error(f"App setup or dataset validation failed: {exc}"); st.stop()
if menu=="Home":
    st.title("Student Service Request Monitoring")
    st.write("SLA breach prediction and staff decision support.")
    st.warning("This uses a reconstructed Decision Tree trained on synthetic data, not the original midterm fitted model.")
    a,b,c,d=st.columns(4)
    a.metric("Accuracy",f"{metrics['accuracy']:.1%}"); b.metric("Precision",f"{metrics['precision']:.1%}"); c.metric("Recall",f"{metrics['recall']:.1%}"); d.metric("F1 score",f"{metrics['f1']:.1%}")
elif menu=="Dataset":
    st.header("Dataset Upload and Validation")
    st.success(f"Validated {len(data)} rows and {len(data.columns)} columns.")
    st.dataframe(data.head(50),use_container_width=True)
    st.subheader("Missing values"); st.dataframe(data.isna().sum().rename("Missing count"))
    st.metric("Duplicate Request_ID values",int(data.Request_ID.duplicated().sum()))
elif menu=="Data Analysis": eda(data)
elif menu=="Prediction": prediction(data,model,metrics)
elif menu=="Dashboard": dashboard(data,model)
else:
    st.header("Systems Analysis and Design Integration")
    st.subheader("Functional Requirements")
    for x in ["FR1: Staff can upload and validate CSV records.","FR2: Staff can inspect missing and duplicate values.","FR3: Staff can explore interactive statistics and charts.","FR4: Staff can enter new request features and view model predictions.","FR5: Staff can inspect a prioritized pending-request review queue."]: st.write(x)
    st.subheader("Non-functional Requirements")
    for x in ["NFR1: Validation errors must be understandable.","NFR2: Saved model inference must not retrain on each refresh.","NFR3: Sensitive records must not be published without authorization."]: st.write(x)
    st.code("CSV upload → schema validation → data exploration → saved model → risk prediction → staff review")
    st.info("Prototype only: authentication and official decision storage are not implemented.")
