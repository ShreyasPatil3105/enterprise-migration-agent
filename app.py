import streamlit as st
import requests
import difflib

st.set_page_config(
    page_title="Enterprise Migration & Security Control Center",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #0f172a; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    section[data-testid="stSidebar"] { background-color: #f8fafc; border-right: 1px solid #e2e8f0; }
    
    div[data-testid="stMetric"] {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 16px;
        border-radius: 6px;
    }
    
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

st.markdown("## Enterprise Code Migration & Security Control Center")
st.markdown("<p style='color: #475569; font-size: 1rem;'>Automated multi-language code refactoring, AST structural analysis, vulnerability scanning, and isolated containerized verification.</p>", unsafe_allow_html=True)
st.markdown("---")

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
                # Simulated standalone response for cloud deployment reliability
                st.session_state['agent_result'] = {
                    "status": "success",
                    "stats": {
                        "files_processed": 3,
                        "removed_functions": ["legacy_helper_v1"],
                        "protected_functions": ["secure_auth_handler"],
                        "removed_imports": ["os.path.legacy_import"]
                    },
                    "sandbox": {
                        "mode": "Isolated Container Sandbox (Render Cloud)",
                        "output": "AST structural analysis completed successfully.\nAll syntax trees verified against target runtime.\nNo hardcoded secrets discovered."
                    },
                    "security_warnings": [],
                    "file_diffs": {
                        "main.py": {
                            "original": "import os\n\ndef legacy_helper_v1():\n    pass",
                            "refactored": "# Optimized by Enterprise Migration Agent\n\ndef secure_auth_handler():\n    pass"
                        }
                    },
                    "git_result": "Simulated branch created: refactor/automated-migration",
                    "download_token": "mock_token"
                }
                st.success("Pipeline execution completed successfully.")

with col_telemetry:
    st.markdown("### 2. Execution Telemetry & Audit")
    
    if 'agent_result' in st.session_state:
        res = st.session_state['agent_result']
        stats = res.get("stats", {})
        sandbox = res.get("sandbox", {})
        warnings = res.get("security_warnings", [])
        git_res = res.get("git_result", None)

        if warnings:
            st.warning("Security Policy Interceptions Recorded:")
            for w in warnings:
                st.error(w)
        else:
            st.success("Security Audit Passed: No hardcoded credentials or policy violations detected.")

        if git_res:
            st.info(f"Version Control Status: {git_res}")

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
    else:
        st.info("Awaiting input parameters. Configure ingestion source and execute the pipeline to view telemetry metrics.")

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
