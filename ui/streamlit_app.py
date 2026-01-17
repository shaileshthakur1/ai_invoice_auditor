import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000"

# ======================================================
# Page Config
# ======================================================
st.set_page_config(
    page_title="Invoice Auditor",
    page_icon="🧾",
    layout="wide"
)

# ======================================================
# Theme-Safe, High-Contrast Styles
# ======================================================
st.markdown("""
<style>
html, body {
    background-color: #f8fafc;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0f172a;
}
section[data-testid="stSidebar"] * {
    color: #e5e7eb !important;
}

/* Section title */
.section-title {
    font-size: 15px;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 6px;
}

/* Report rows */
.report-row {
    display: flex;
    justify-content: space-between;
    font-size: 14px;
    padding: 3px 0;
    border-bottom: 1px solid #e5e7eb;
}
.report-key { color: #334155; }
.report-value { color: #1e3a8a; font-weight: 500; }

/* Chat bubbles */
.chat-user {
    background: #e2e8f0;
    color: #020617;
    padding: 10px 14px;
    border-radius: 12px;
    margin-bottom: 6px;
}

.chat-ai {
    background: #f1f5f9;
    color: #020617;
    padding: 10px 14px;
    border-radius: 12px;
    margin-bottom: 12px;
    border-left: 4px solid #6366f1;
}

/* Scroll */
.scroll {
    max-height: 260px;
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
    st.markdown("## Invoice Auditor")
    st.caption("Audit workspace")

    st.divider()
    st.markdown("### Upload Invoices")
    st.caption("PDF / Image • Up to 200 MB")

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
            "Invoice",
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

    # -------- Extracted Info --------
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
                st.info("No extracted data")

    # -------- Review & Actions --------
    with right:
        with st.expander("Review & Actions", expanded=False):
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("Approve", use_container_width=True):
                    api_post(f"/review/{st.session_state.invoice_id}/approve")
                    st.success("Invoice approved")

            with col2:
                if st.button("Reject", use_container_width=True):
                    api_post(
                        f"/review/{st.session_state.invoice_id}/flag",
                        json={"note": "Invoice rejected"}
                    )
                    st.error("Invoice rejected")

            with col3:
                if st.button("Edit", use_container_width=True):
                    st.session_state.show_edit = not st.session_state.show_edit

            # ---- Conditional Edit ----
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
    for m in st.session_state.chat_log:
        st.markdown(f"<div class='chat-user'><b>You:</b> {m['q']}</div>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='chat-ai'><b>System:</b> {m['a']}<br><small>Source: {m['source']}</small></div>",
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)

    question = st.text_input("Ask a question about this invoice")

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
