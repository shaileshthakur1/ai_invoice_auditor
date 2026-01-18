import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000"

# ======================================================
# Page Config
# ======================================================
st.set_page_config(
    page_title="AI Invoice Auditor",
    page_icon="🧾",
    layout="wide"
)

# ======================================================
# Theme-Safe, Audit-Grade Styles
# ======================================================
st.markdown("""
<style>
html, body {
    background-color: #020617;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #020617;
    border-right: 1px solid #1e293b;
}
section[data-testid="stSidebar"] * {
    color: #e5e7eb !important;
}

/* Section title */
.section-title {
    font-size: 16px;
    font-weight: 600;
    color: #f8fafc;
    margin-bottom: 8px;
}

/* Report rows */
.report-row {
    display: flex;
    justify-content: space-between;
    font-size: 14px;
    padding: 6px 0;
    border-bottom: 1px solid #1e293b;
}
.report-key {
    color: #94a3b8;
}
.report-value {
    color: #e5e7eb;
    font-weight: 500;
}

/* Chat - User */
.chat-user {
    background: #1e293b;
    color: #f8fafc;
    padding: 12px 16px;
    border-radius: 14px;
    margin-bottom: 10px;
    font-size: 15px;
}

/* Chat - AI */
.chat-ai {
    background: #020617;
    color: #e5e7eb;
    padding: 16px 18px;
    border-radius: 14px;
    margin-bottom: 18px;
    border: 1px solid #1e293b;
    line-height: 1.6;
}

/* Markdown inside AI */
.chat-ai ul {
    padding-left: 18px;
}
.chat-ai li {
    margin-bottom: 6px;
}

/* Source */
.chat-source {
    margin-top: 10px;
    font-size: 12px;
    color: #94a3b8;
}

/* Scroll */
.scroll {
    max-height: 320px;
    overflow-y: auto;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# Session State
# ======================================================
st.session_state.setdefault("invoice_id", None)
st.session_state.setdefault("chat_log", [])
st.session_state.setdefault("show_edit", False)

# ======================================================
# API Helpers
# ======================================================
def api_get(path):
    return requests.get(f"{BACKEND_URL}{path}")

def api_post(path, json=None, files=None):
    return requests.post(f"{BACKEND_URL}{path}", json=json, files=files)

# ======================================================
# Sidebar — Upload, Select, History
# ======================================================
with st.sidebar:
    st.markdown("## 🧾 AI Invoice Auditor")
    st.caption("Invoice audit workspace")

    st.divider()
    st.markdown("### Upload Invoices")
    st.caption("PDF / Image • Max 200 MB")

    uploaded_files = st.file_uploader(
        "Select files",
        type=["pdf", "png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

    if uploaded_files and st.button("Process Files", use_container_width=True):
        for f in uploaded_files:
            api_post("/upload/", files={"file": f})
        st.success("Invoices processed")

    st.divider()
    st.markdown("### Select Invoice")

    inv_res = api_get("/invoice/list")
    if inv_res.status_code == 200 and inv_res.json():
        selected = st.selectbox(
            "Invoice ID",
            options=[i["id"] for i in inv_res.json()]
        )
        st.session_state.invoice_id = selected

    if st.session_state.invoice_id:
        st.divider()
        st.markdown("### Query History")

        history = api_get(f"/chat/history/{st.session_state.invoice_id}")
        if history.status_code == 200:
            st.markdown("<div class='scroll'>", unsafe_allow_html=True)
            for h in history.json():
                st.markdown(f"- {h['question']}")
            st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# Main Content
# ======================================================
if st.session_state.invoice_id:

    # -------- TOP ROW --------
    left, right = st.columns([2, 1.3])

    # -------- Extracted Invoice Info --------
    with left:
        with st.expander("Extracted Invoice Information", expanded=False):
            fields = api_get(f"/chat/fields/{st.session_state.invoice_id}")
            if fields.status_code == 200 and fields.json():
                for k, v in fields.json().items():
                    st.markdown(
                        f"""
                        <div class="report-row">
                            <div class="report-key">{k.replace('_',' ').title()}</div>
                            <div class="report-value">{v}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.info("No extracted invoice data available")

    # -------- Review & Actions --------
    with right:
        with st.expander("Review & Actions", expanded=False):
            c1, c2, c3 = st.columns(3)

            with c1:
                if st.button("Approve", use_container_width=True):
                    api_post(f"/review/{st.session_state.invoice_id}/approve")
                    st.success("Invoice approved")

            with c2:
                if st.button("Reject", use_container_width=True):
                    api_post(
                        f"/review/{st.session_state.invoice_id}/flag",
                        json={"note": "Invoice rejected"}
                    )
                    st.error("Invoice rejected")

            with c3:
                if st.button("Edit", use_container_width=True):
                    st.session_state.show_edit = not st.session_state.show_edit

            if st.session_state.show_edit:
                st.divider()
                fname = st.text_input("Field name", placeholder="total_amount")
                fval = st.text_input("New value")

                if st.button("Save Changes", use_container_width=True):
                    api_post(
                        f"/review/{st.session_state.invoice_id}/edit-field",
                        json={"field": fname, "value": fval}
                    )
                    st.success("Field updated")
                    st.session_state.show_edit = False

    st.divider()

    # -------- AI Assistant --------
    st.markdown("<div class='section-title'>AI Assistant</div>", unsafe_allow_html=True)

    st.markdown("<div class='scroll'>", unsafe_allow_html=True)

    with st.container():
        for m in st.session_state.chat_log:
            st.markdown(
                f"<div class='chat-user'><b>You</b><br>{m['q']}</div>",
                unsafe_allow_html=True
            )

            st.markdown("<div class='chat-ai'>", unsafe_allow_html=True)
            st.markdown(m["a"])
            st.markdown(
                f"<div class='chat-source'>Source: {m['source']}</div>",
            unsafe_allow_html=True
        )
        st.markdown("</div>", unsafe_allow_html=True)


    st.markdown("</div>", unsafe_allow_html=True)

    question = st.text_input(
        "Ask a question about this invoice",
        placeholder="e.g. Summarize the invoice or list key details"
    )

    if st.button("Submit Question") and question:
        res = api_post(
            "/chat/",
            json={"invoice_id": st.session_state.invoice_id, "question": question}
        )
        if res.status_code == 200:
            data = res.json()
            st.session_state.chat_log.append({
                "q": question,
                "a": data["answer"],
                "source": data["source"]
            })
            st.rerun()

else:
    st.info("Upload and select an invoice to begin.")
