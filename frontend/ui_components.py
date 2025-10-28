import streamlit as st

# Version number
VERSION = "0.0.5"


def display_project_info():
    """Display project information including author and repository link."""
    st.markdown(
        """
        <style>
        .project-info {
            background-color: rgba(240, 242, 246, 0.5);
            border-left: 4px solid #1E90FF;
            padding: 0.75rem 1rem;
            margin: 1rem 0;
            border-radius: 0 0.25rem 0.25rem 0;
            font-size: 0.9rem;
        }
        .project-info a {
            text-decoration: none;
            color: #1E90FF;
        }
        .project-info a:hover {
            text-decoration: underline;
        }
        .project-separator {
            color: #666;
        }
        @media (prefers-color-scheme: dark) {
            .project-info {
                background-color: rgba(33, 37, 41, 0.3);
                border-left-color: #3498DB;
            }
            .project-info a {
                color: #3498DB;
            }
            .project-separator {
                color: #999;
            }
        }
        </style>
        <div class="project-info">
            <div style="display: flex; align-items: center; gap: 1rem; flex-wrap: wrap;">
                <span>
                    <strong>🚀 Open Source Project</strong> by
                    <a href="https://github.com/i-richardwang" target="_blank">
                        <strong>Richard Wang</strong>
                    </a>
                </span>
                <span class="project-separator">•</span>
                <a href="https://github.com/i-richardwang/LLM-TextKit" target="_blank"
                   style="display: flex; align-items: center; gap: 0.3rem;">
                    <span>📁</span> <strong>GitHub Repository</strong>
                </a>
                <span class="project-separator">•</span>
                <span class="project-separator">⭐ Star if you find it useful!</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_sidebar():
    """
    Display the application sidebar.
    """
    with st.sidebar:
        _render_sidebar_content()
        _add_version_info()


def _render_sidebar_content():
    """
    Render the main content of the sidebar.
    """
    st.markdown(_get_sidebar_style(), unsafe_allow_html=True)


def _get_sidebar_style():
    """
    Return CSS styles for the sidebar.
    """
    return """
    <style>
    [data-testid="stSidebarNav"] {
        background-image: none;
        padding-top: 0;
        max-height: none;
    }
    [data-testid="stSidebarNav"] > ul {
        max-height: none;
        overflow-y: visible;
    }
    .sidebar-content {
        padding: 1rem 0;
    }
    .sidebar-title {
        color: #4F8BF9;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    </style>
    """



def _add_version_info():
    """
    Add version information to the sidebar.
    """
    st.caption(f"Version {VERSION}")


def show_footer():
    """
    Display the application footer.
    """
    st.markdown(_get_footer_style() + _get_footer_content(), unsafe_allow_html=True)


def _get_footer_style():
    """
    Return CSS styles for the footer.
    """
    return """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f0f2f6;
        color: #31333F;
        text-align: center;
        padding: 10px 0;
        font-size: 0.8rem;
    }
    .footer a {
        color: #4F8BF9;
        text-decoration: none;
    }
    .footer a:hover {
        text-decoration: underline;
    }
    </style>
    """


def _get_footer_content():
    """
    Return HTML content for the footer.
    """
    return """
    <div class="footer">
        <span>© 2024 Richard Wang</span> &nbsp;|&nbsp; 
        <a href="https://github.com/i-richardwang/LLM-TextKit" target="_blank">GitHub</a> &nbsp;|&nbsp; 
        <a href="mailto:contact@xmail.ing">contact@xmail.ing</a>
    </div>
    """


def apply_common_styles():
    """
    Apply common CSS styles.
    """
    st.markdown(_get_common_styles(), unsafe_allow_html=True)


def _get_common_styles():
    """
    Return common CSS styles.
    """
    return """
    <style>
    .stTextInput>div>div>input {
        border-color: #E0E0E0;
    }
    .stProgress > div > div > div > div {
        background-color: #4F8BF9;
    }
    h2, h3, h4 {
        border-bottom: 2px solid !important;
        padding-bottom: 0.5rem !important;
        margin-bottom: 1rem !important;
    }
    h2 {
        color: #1E90FF !important;
        border-bottom-color: #1E90FF !important;
        font-size: 1.8rem !important;
        margin-top: 1.5rem !important;
    }
    h3 {
        color: #16A085 !important;
        border-bottom-color: #16A085 !important;
        font-size: 1.5rem !important;
        margin-top: 1rem !important;
    }
    h4 {
        color: #E67E22 !important;
        border-bottom-color: #E67E22 !important;
        font-size: 1.2rem !important;
        margin-top: 0.5rem !important;
    }
    .workflow-container {
        background-color: rgba(248, 249, 250, 0.05);
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(0, 0, 0, 0.125);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    @media (prefers-color-scheme: dark) {
        .workflow-container {
            background-color: rgba(33, 37, 41, 0.05);
            border-color: rgba(255, 255, 255, 0.125);
        }
        h2 {
            color: #3498DB !important;
            border-bottom-color: #3498DB !important;
        }
        h3 {
            color: #2ECC71 !important;
            border-bottom-color: #2ECC71 !important;
        }
        h4 {
            color: #F39C12 !important;
            border-bottom-color: #F39C12 !important;
        }
    }
    .workflow-step {
        margin-bottom: 1rem;
    }
    </style>
    """

