import requests
import streamlit as st

from src.fix_generator import generate_fix_snippet

# FastAPI backend URL (defaults to local development server)
API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="CommitMetrics | GitHub Portfolio Auditor",
    layout="wide",
)

# GitHub Primer Dark Theme Styling (Zero icons, authentic GitHub UI look)
st.markdown(
    """
    <style>
    /* GitHub Dark Canvas & Global Font */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    
    /* GitHub Card Containers */
    .metric-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
        transition: border-color 0.2s ease;
    }
    .metric-card:hover {
        border-color: #8b949e;
    }
    
    /* Typography & Badges */
    .card-title {
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #8b949e;
        margin-bottom: 8px;
    }
    .grade-badge {
        font-size: 40px;
        font-weight: 700;
        color: #58a6ff;
        line-height: 1.1;
    }
    .score-badge {
        font-size: 36px;
        font-weight: 700;
        color: #3fb950;
        line-height: 1.1;
    }
    .count-badge {
        font-size: 36px;
        font-weight: 700;
        color: #d2a8ff;
        line-height: 1.1;
    }
    
    /* GitHub Primary Green Button */
    .stButton > button {
        background-color: #238636 !important;
        color: #ffffff !important;
        border: 1px solid rgba(240, 246, 252, 0.1) !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        width: 100%;
        padding: 8px 16px;
        transition: background-color 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #2ea043 !important;
        border-color: #8b949e !important;
    }
    
    /* Input Fields styling */
    .stTextInput input {
        background-color: #0d1117 !important;
        color: #c9d1d9 !important;
        border: 1px solid #30363d !important;
        border-radius: 6px !important;
    }
    .stTextInput input:focus {
        border-color: #58a6ff !important;
        box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.3);
    }
    
    /* Dividers */
    hr {
        border-color: #30363d;
        margin: 32px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# App Header
st.title("Commit Metrics")
st.markdown("### Automated GitHub Repository Health & Portfolio Auditor")
st.write("Scan your public GitHub profile, evaluate core engineering standards, and get actionable recommendations to level up your portfolio.")

st.markdown("---")

# Sidebar for controls
with st.sidebar:
    st.header("Configuration")
    username_input = st.text_input("GitHub Username", placeholder="e.g. mhdhamka")
    custom_token = st.text_input("GitHub Token (Optional)", type="password", placeholder="ghp_...")
    
    st.markdown("---")
    st.info("Tip: Adding a GitHub Token prevents API rate-limit errors when scanning large portfolios.")
    
    run_audit = st.button("Run Portfolio Audit")

# Main Content Area
if run_audit:
    if not username_input.strip():
        st.warning("Please enter a valid GitHub username.")
    else:
        with st.spinner(f"Scanning public repositories for `{username_input}`... This may take a few seconds."):
            try:
                # Call FastAPI backend endpoint
                params = {}
                if custom_token:
                    params["token"] = custom_token
                    
                response = requests.get(f"{API_BASE_URL}/audit/{username_input}", params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    summary = data["audit_summary"]
                    
                    # --- Dashboard Summary Section ---
                    st.success(f"Successfully audited {summary['total_repos']} public repositories for **{username_input}**.")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(
                            f"""
                            <div class="metric-card">
                                <div class="card-title">Portfolio Health Grade</div>
                                <div class="grade-badge">{summary['grade']}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        
                    with col2:
                        st.markdown(
                            f"""
                            <div class="metric-card">
                                <div class="card-title">Overall Health Score</div>
                                <div class="score-badge">{summary['overall_score']}%</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        
                    with col3:
                        st.markdown(
                            f"""
                            <div class="metric-card">
                                <div class="card-title">Active Repositories</div>
                                <div class="count-badge">{summary['total_repos']}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        
                    st.markdown("---")
                    
                    # --- High-Level Recommendations ---
                    st.markdown("### Portfolio Insights & Recommendations")
                    for rec in summary["recommendations"]:
                        st.markdown(f"- {rec}")
                        
                    st.markdown("---")
                    
                    # --- Individual Repository Breakdown ---
                    st.markdown("### Repository Health Breakdown")
                    
                    for repo in summary["repositories"]:
                        tech_stack_str = ", ".join(repo.get('tech_stack', ['Generic']))
                        with st.expander(f"{repo['name']} ({repo['language']} | Stack: {tech_stack_str}) — Grade: **{repo['grade']}** ({repo['health_score']}%)"):
                            rc1, rc2 = st.columns([1, 2])
                            
                            with rc1:
                                st.write(f"**[View Repository]({repo['html_url']})**")
                                st.markdown("##### Dimension Scores:")
                                st.write(f"- Documentation: **{repo['breakdown']['documentation']}%**")
                                st.write(f"- CI/CD Workflows: **{repo['breakdown']['ci_cd']}%**")
                                st.write(f"- Maintenance: **{repo['breakdown']['maintenance']}%**")
                                st.write(f"- Security / `.gitignore`: **{repo['breakdown']['security']}%**")
                                st.write(f"- Stale Branches (>60 days): **{repo.get('zombie_branches', 0)}**")
                                
                            with rc2:
                                st.markdown("##### Actionable Fixes:")
                                if repo["suggestions"]:
                                    for suggestion in repo["suggestions"]:
                                        st.markdown(f"- {suggestion}")
                                        
                                    # One-Click Fix Generators based on repository issues
                                    st.markdown("##### Quick Configuration Snippets:")
                                    for suggestion in repo["suggestions"]:
                                        if "README.md" in suggestion:
                                            with st.expander("View Suggested README Template"):
                                                st.code(generate_fix_snippet("missing_readme"), language="markdown")
                                        elif "GitHub Actions" in suggestion:
                                            primary_stack = repo.get("tech_stack", ["Python"])[0]
                                            with st.expander("View Suggested CI/CD Workflow"):
                                                st.code(generate_fix_snippet("missing_ci", primary_stack), language="yaml")
                                        elif ".gitignore" in suggestion:
                                            with st.expander("View Suggested .gitignore"):
                                                st.code(generate_fix_snippet("missing_gitignore"), language="text")
                                else:
                                    st.markdown("*No improvements needed! This repo meets elite standards.*")
                                    
                else:
                    err_detail = response.json().get("detail", "Unknown server error.")
                    st.error(f"Error from API: {err_detail}")
                    
            except requests.exceptions.ConnectionError:
                st.error(f"Could not connect to the FastAPI backend at `{API_BASE_URL}`. Make sure your FastAPI server is running (`uvicorn api.main:app --reload`)!")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e!s}")
else:
    st.info("Enter a GitHub username in the sidebar and click **Run Portfolio Audit** to begin.")