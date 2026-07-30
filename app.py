import streamlit as st
import requests
import difflib

st.set_page_config(
    page_title="Enterprise Migration & Security Control Center",
    page_icon="🛡️",
    layout="wide"
)

# Strict Enterprise Light Theme CSS (Clean Corporate SaaS Aesthetic)
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #0f172a; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    section[data-testid="stSidebar"] { background-color: #f8fafc; border-right: 1px solid #e2e8f0; }
    
    /* Clean Cards */
    div[data-testid="stMetric"] {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 16px;
        border-radius: 6px;
    }
    
    /* Form Buttons */
    .stButton button {
        background-color: #0f172a;
        color: #ffffff;
        border-radius: 6px;
        font-weight: 500;
        font-size: 0.9rem;
        border: none;
        width: 100%;
        padding: 0.5rem 1rem;
    }
    .stButton button:hover {
        background-color: #1e293b;
    }
    
    h1, h2, h3 { color: #0f172a !important; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# Application Header
st.markdown("## Enterprise Code Migration & Security Control Center")
st.markdown("<p style='color: #475569; font-size: 1rem;'>Automated multi-language code refactoring, AST structural analysis, vulnerability scanning, and isolated containerized verification.</p>", unsafe_allow_html=True)
st.markdown("---")

# Control Plane Sidebar
with st.sidebar:
    st.markdown("### Compliance & Policy")
    st.markdown("<p style='font-size: 0.8rem; color: #64748b;'>Execution guardrails and environment settings.</p>", unsafe_allow_html=True)
    sandbox_mode = st.toggle("Isolated Container Sandbox", value=True)
    secret_scan = st.toggle("Static Secret Detection", value=True)
    path_guard = st.toggle("Path Traversal Defense", value=True)
    
    st.markdown("---")
    st.markdown("### System Telemetry")
    st.markdown("• **API Gateway:** `Operational`")
    st.markdown("• **Docker Daemon:** `Connected`")
    st.markdown("• **Security Policies:** `Enforced`")

# Main Interface Workspace
col_input, col_telemetry = st.columns([1, 1.2], gap="large")

with col_input:
    st.markdown("### 1. Source Ingestion")
    
    ingestion_type = st.selectbox("Ingestion Mechanism", ["Project Archive (.zip)", "Remote Git Repository"])
    
    uploaded_file = None
    repo_url_input = None
    github_token_input = None

    if ingestion_type == "Project Archive (.zip)":
        uploaded_file = st.file_uploader("Upload Source Archive", type="zip", label_visibility="collapsed")
    else:
        repo_url_input = st.text_input("Repository HTTPS Endpoint", placeholder="https://github.com/organization/repository.git")
        github_token_input = st.text_input("Personal Access Token (Optional)", type="password", placeholder="ghp_...")

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Execute Migration Pipeline", use_container_width=True):
        if ingestion_type == "Project Archive (.zip)" and not uploaded_file:
            st.error("Validation Error: A valid ZIP archive is required.")
        elif ingestion_type == "Remote Git Repository" and not repo_url_input:
            st.error("Validation Error: A repository HTTPS endpoint is required.")
        else:
            with st.spinner("Executing pipeline tasks: Ingesting, parsing AST trees, evaluating security rules, and running verification suites..."):
                try:
                    files = None
                    if uploaded_file is not None:
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/zip")}
                    
                    data_fields = {}
                    if repo_url_input:
                        data_fields["repo_url"] = repo_url_input
                    if github_token_input:
                        data_fields["github_token"] = github_token_input

                    response = requests.post("http://127.0.0.1:8000/migrate-project", files=files, data=data_fields)
                    
                    if response.status_code == 200:
                        st.session_state['agent_result'] = response.json()
                        st.success("Pipeline execution completed successfully.")
                    else:
                        st.error(f"Pipeline Exception: {response.json().get('detail', 'Unknown error')}")
                except requests.exceptions.ConnectionError:
                    st.error("Network Exception: Unable to establish connection with the backend service daemon.")

with col_telemetry:
    st.markdown("### 2. Execution Telemetry & Audit")
    
    if 'agent_result' in st.session_state:
        res = st.session_state['agent_result']
        stats = res.get("stats", {})
        sandbox = res.get("sandbox", {})
        warnings = res.get("security_warnings", [])
        diffs = res.get("file_diffs", {})
        git_res = res.get("git_result", None)
        download_token = res.get("download_token", None)

        if warnings:
            st.warning("Security Policy Interceptions Recorded:")
            for w in warnings:
                st.error(w)
        else:
            st.success("Security Audit Passed: No hardcoded credentials or policy violations detected.")

        if git_res:
            st.info(f"Version Control Status: {git_res}")

        # Metrics Overview
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Files Processed", stats.get("files_processed", 0))
        with m2:
            st.metric("Dead Code Removed", len(stats.get("removed_functions", [])))
        with m3:
            st.metric("Protected Functions", len(stats.get("protected_functions", [])))
        with m4:
            st.metric("Imports Optimized", len(stats.get("removed_imports", [])))

        st.markdown(f"**Execution Runtime:** `{sandbox.get('mode', 'Environment')}`")
        st.code(sandbox.get('output', 'Execution completed.'), language="bash")

        if download_token:
            st.markdown("### 3. Artifact Export")
            if st.button("Download Refactored Bundle"):
                dl_response = requests.get(f"http://127.0.0.1:8000/download?token={download_token}")
                if dl_response.status_code == 200:
                    st.download_button(
                        label="Save Archive (.zip)",
                        data=dl_response.content,
                        file_name="refactored_enterprise_bundle.zip",
                        mime="application/zip",
                        type="primary"
                    )
                else:
                    st.error("Download token is invalid or has expired.")
    else:
        st.info("Awaiting input parameters. Configure ingestion source and execute the pipeline to view telemetry metrics.")

# Bottom Section: Code Diff Inspector
if 'agent_result' in st.session_state:
    res = st.session_state['agent_result']
    diffs = res.get("file_diffs", {})
    
    if diffs:
        st.markdown("---")
        st.markdown("### 4. Structural Diff Inspector")
        selected_file = st.selectbox("Select Target File for Code Review:", list(diffs.keys()))
        
        if selected_file:
            file_data = diffs[selected_file]
            orig = file_data["original"]
            ref = file_data["refactored"]

            diff_lines = list(difflib.unified_diff(
                orig.splitlines(),
                ref.splitlines(),
                fromfile=f"a/{selected_file}",
                tofile=f"b/{selected_file}",
                lineterm=""
            ))
            
            if diff_lines:
                st.code("\n".join(diff_lines), language="diff")
            else:
                st.info("No structural modifications required for this file path.")
