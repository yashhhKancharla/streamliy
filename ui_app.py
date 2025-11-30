"""
Streamlit UI for Autonomous QA Agent
Grounded_In: Assignment - 1.pdf

A user-friendly interface for the RAG-powered test generation system.
"""

import streamlit as st
import requests
import json
from datetime import datetime
import time
import os

# Page configuration
st.set_page_config(
    page_title="Autonomous QA Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Base URL - Use environment variable or default to localhost
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .status-healthy {
        color: #28a745;
        font-weight: bold;
    }
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
    }
    .test-case-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)


def check_health():
    """Check API health status."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.json() if response.status_code == 200 else None
    except:
        return None


def ingest_documents(documents, chunk_size, chunk_overlap):
    """Ingest documents via API."""
    try:
        payload = {
            "documents": documents,
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap
        }
        response = requests.post(f"{API_BASE_URL}/ingest", json=payload, timeout=30)
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500


def query_rag(query, k, generate_answer, document_filter=None):
    """Query the RAG system."""
    try:
        payload = {
            "query": query,
            "k": k,
            "generate_answer": generate_answer
        }
        if document_filter:
            payload["filters"] = {"source": document_filter}
        response = requests.post(f"{API_BASE_URL}/query", json=payload, timeout=30)
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500


def list_documents():
    """List all ingested documents."""
    try:
        response = requests.get(f"{API_BASE_URL}/list-documents", timeout=10)
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500


def generate_tests(feature, requirements, test_types, priority_levels, output_formats):
    """Generate test cases via API."""
    try:
        payload = {
            "feature": feature,
            "requirements": requirements,
            "test_types": test_types,
            "priority_levels": priority_levels,
            "output_formats": output_formats
        }
        response = requests.post(f"{API_BASE_URL}/generate-tests", json=payload, timeout=60)
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500


def run_test(test_id, base_url, headless, timeout):
    """Execute test via API."""
    try:
        payload = {
            "test_id": test_id,
            "base_url": base_url,
            "headless": headless,
            "timeout": timeout
        }
        response = requests.post(f"{API_BASE_URL}/run-test", json=payload, timeout=timeout + 20)
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500


# Sidebar
with st.sidebar:
    st.markdown("## 🤖 QA Agent")
    st.markdown("---")
    
    # Health Check
    st.markdown("### System Status")
    health_data = check_health()
    
    if health_data and health_data.get("status") == "healthy":
        st.markdown('<p class="status-healthy">✅ Healthy</p>', unsafe_allow_html=True)
        services = health_data.get("services", {})
        st.caption(f"Flask: {services.get('flask', 'unknown')}")
        st.caption(f"ChromaDB: {services.get('chroma', 'unknown')}")
        st.caption(f"OpenRouter: {services.get('openrouter', 'unknown')}")
    else:
        st.markdown('<p class="status-error">❌ Unhealthy</p>', unsafe_allow_html=True)
        st.error("Backend API is not responding. Please start the server.")
        st.code("python start_server.py", language="bash")
    
    st.markdown("---")
    st.markdown("### Navigation")
    page = st.radio(
        "Select Page",
        ["🏠 Home", "📥 Ingest Documents", "🔍 Query RAG", "🧪 Generate Tests", "▶️ Run Tests"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.caption("Version 1.0.0")
    st.caption(f"© 2025 QA Agent")


# Main Content
if "🏠 Home" in page:
    st.markdown('<p class="main-header">🤖 Autonomous QA Agent</p>', unsafe_allow_html=True)
    st.markdown("### RAG-Powered Test Generation System")
    
    st.markdown("""
    Welcome to the Autonomous QA Agent! This system uses **Retrieval-Augmented Generation (RAG)** 
    to automatically generate and execute comprehensive test cases for web applications.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("#### 📥 Ingest")
        st.markdown("Upload and process documentation into the vector database")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("#### 🔍 Query")
        st.markdown("Search documentation using semantic search powered by ChromaDB")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown("#### 🧪 Generate")
        st.markdown("Create test cases using LLM and retrieved context")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🚀 Quick Start")
    
    st.markdown("""
    1. **Ingest Documents**: Upload your documentation (specs, APIs, UI guides)
    2. **Query RAG**: Test the semantic search to find relevant information
    3. **Generate Tests**: Create comprehensive test cases for any feature
    4. **Run Tests**: Execute generated Selenium tests automatically
    """)
    
    st.markdown("---")
    st.markdown("### 📊 Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ✅ **RAG-Powered Generation**  
        ✅ **Multi-Format Output** (JSON, Markdown, Selenium)  
        ✅ **Semantic Search** with ChromaDB  
        ✅ **LLM Integration** via OpenRouter  
        """)
    
    with col2:
        st.markdown("""
        ✅ **Automated Test Execution**  
        ✅ **Real-time Health Monitoring**  
        ✅ **Comprehensive Test Coverage**  
        ✅ **Docker Ready Deployment**  
        """)


elif "📥 Ingest Documents" in page:
    st.markdown('<p class="main-header">📥 Ingest Documents</p>', unsafe_allow_html=True)
    st.markdown("Upload and process documentation into the vector database")
    
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["Single Document", "Multiple Documents"])
    
    with tab1:
        st.markdown("### Add Single Document")
        
        doc_content = st.text_area(
            "Document Content",
            height=200,
            placeholder="Paste your document content here..."
        )
        
        col1, col2 = st.columns(2)
        with col1:
            doc_source = st.text_input("Source Name", value="manual_upload.md")
        with col2:
            doc_category = st.selectbox("Category", ["documentation", "api", "ui", "legal", "specs"])
        
        col1, col2 = st.columns(2)
        with col1:
            chunk_size = st.number_input("Chunk Size", min_value=100, max_value=2000, value=800)
        with col2:
            chunk_overlap = st.number_input("Chunk Overlap", min_value=0, max_value=500, value=150)
        
        if st.button("🚀 Ingest Document", type="primary", use_container_width=True):
            if doc_content.strip():
                with st.spinner("Ingesting document..."):
                    documents = [{
                        "content": doc_content,
                        "metadata": {
                            "source": doc_source,
                            "category": doc_category,
                            "uploaded_at": datetime.now().isoformat()
                        }
                    }]
                    
                    result, status_code = ingest_documents(documents, chunk_size, chunk_overlap)
                    
                    if status_code == 200:
                        st.success("✅ Document ingested successfully!")
                        st.json(result)
                    else:
                        st.error(f"❌ Ingestion failed: {result.get('error', 'Unknown error')}")
            else:
                st.warning("⚠️ Please enter document content")
    
    with tab2:
        st.markdown("### Batch Upload Documents")
        
        num_docs = st.number_input("Number of Documents", min_value=1, max_value=10, value=2)
        
        documents = []
        for i in range(num_docs):
            with st.expander(f"Document {i + 1}"):
                content = st.text_area(f"Content {i + 1}", key=f"content_{i}", height=150)
                col1, col2 = st.columns(2)
                with col1:
                    source = st.text_input(f"Source {i + 1}", value=f"doc_{i + 1}.md", key=f"source_{i}")
                with col2:
                    category = st.selectbox(f"Category {i + 1}", 
                                          ["documentation", "api", "ui", "legal", "specs"],
                                          key=f"category_{i}")
                
                if content.strip():
                    documents.append({
                        "content": content,
                        "metadata": {
                            "source": source,
                            "category": category,
                            "uploaded_at": datetime.now().isoformat()
                        }
                    })
        
        col1, col2 = st.columns(2)
        with col1:
            chunk_size = st.number_input("Chunk Size", min_value=100, max_value=2000, value=800, key="batch_chunk_size")
        with col2:
            chunk_overlap = st.number_input("Chunk Overlap", min_value=0, max_value=500, value=150, key="batch_chunk_overlap")
        
        if st.button("🚀 Ingest All Documents", type="primary", use_container_width=True):
            if documents:
                with st.spinner(f"Ingesting {len(documents)} documents..."):
                    result, status_code = ingest_documents(documents, chunk_size, chunk_overlap)
                    
                    if status_code == 200:
                        st.success(f"✅ {len(documents)} documents ingested successfully!")
                        st.json(result)
                    else:
                        st.error(f"❌ Ingestion failed: {result.get('error', 'Unknown error')}")
            else:
                st.warning("⚠️ Please add at least one document with content")


elif "🔍 Query RAG" in page:
    st.markdown('<p class="main-header">🔍 Query RAG System</p>', unsafe_allow_html=True)
    st.markdown("Search documentation using semantic search powered by ChromaDB")
    
    st.info("""
    ### 📖 How to Use Query RAG
    
    This feature allows you to search through ingested documentation using semantic search:
    
    1. **Select a document** (optional) - Filter by specific ingested document
    2. **Enter a natural language query** (e.g., "How does authentication work?")
    3. **Adjust the number of results** you want to retrieve (1-10)
    4. **Enable AI Answer** to get a synthesized response from the LLM
    5. Click **Search** to retrieve relevant documents
    
    **Note:** Make sure you have ingested documents first using the "Ingest Documents" tab!
    """)
    
    st.markdown("---")
    
    # Fetch available documents
    with st.spinner("Loading available documents..."):
        docs_result, docs_status = list_documents()
    
    document_options = ["All Documents"]
    if docs_status == 200 and docs_result.get("documents"):
        document_sources = docs_result.get("documents", [])
        for doc in document_sources:
            source = doc.get("source", "unknown")
            chunk_count = doc.get("chunk_count", 0)
            category = doc.get("category", "unknown")
            document_options.append(f"{source} ({category}, {chunk_count} chunks)")
    
    # Document filter dropdown
    selected_doc = st.selectbox(
        "📄 Filter by Document (Optional)",
        options=document_options,
        help="Select a specific document to search within, or 'All Documents' to search everywhere"
    )
    
    # Extract source name from selection
    document_filter = None
    if selected_doc != "All Documents":
        # Extract source name before the first parenthesis
        document_filter = selected_doc.split(" (")[0] if " (" in selected_doc else selected_doc
    
    st.markdown("---")
    
    query = st.text_area(
        "Enter your query",
        height=100,
        placeholder="e.g., How does authentication work? What are the payment processing requirements?"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        k = st.slider("Number of Results (k)", min_value=1, max_value=10, value=3)
    with col2:
        generate_answer = st.checkbox("Generate AI Answer", value=True)
    
    if st.button("🔍 Search", type="primary", use_container_width=True):
        if query.strip():
            with st.spinner("Searching..."):
                result, status_code = query_rag(query, k, generate_answer, document_filter)
                
                if status_code == 200:
                    st.success("✅ Query completed successfully!")
                    
                    # Display filter info
                    if document_filter:
                        st.info(f"🔍 Filtered results from: **{document_filter}**")
                    
                    # Display answer
                    if result.get('answer'):
                        st.markdown("### 💡 AI-Generated Answer")
                        st.info(result['answer'])
                    
                    # Display results
                    st.markdown(f"### 📚 Retrieved Documents ({result.get('total_results', 0)})")
                    
                    for i, doc in enumerate(result.get('results', []), 1):
                        with st.expander(f"Result {i} - Score: {doc.get('similarity_score', 0):.2f}"):
                            st.markdown("**Content:**")
                            st.markdown(doc.get('content', 'No content'))
                            st.markdown("**Metadata:**")
                            st.json(doc.get('metadata', {}))
                    
                    # Display metrics
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Total Results", result.get('total_results', 0))
                    with col2:
                        st.metric("Retrieval Time", f"{result.get('retrieval_time_ms', 0)} ms")
                else:
                    st.error(f"❌ Query failed: {result.get('error', 'Unknown error')}")
        else:
            st.warning("⚠️ Please enter a query")


elif "🧪 Generate Tests" in page:
    st.markdown('<p class="main-header">🧪 Generate Test Cases</p>', unsafe_allow_html=True)
    st.markdown("Create comprehensive test cases using RAG + LLM")
    
    st.info("""
    ### 📖 How to Generate Test Cases
    
    This feature uses AI to generate comprehensive test cases based on your requirements:
    
    1. **Enter Feature Name** (e.g., "User Authentication", "Payment Gateway")
    2. **Describe Requirements** - Be specific about functionality, edge cases, constraints
    3. **Select Test Types** - Choose which types of tests you need
    4. **Choose Output Formats** - JSON for management tools, Selenium for automation
    5. Click **Generate** - AI will create test cases grounded in your documentation
    
    **Output Files** will be saved to:
    - JSON: `output/testcases_<feature>.json`
    - Markdown: `output/testcases_<feature>.md`  
    - Selenium: `tests/selenium/test_<feature>.py`
    
    **Note:** Results are also available in `app/testcases/` folders organized by feature!
    """)
    
    st.markdown("---")
    
    feature = st.text_input(
        "Feature Name",
        placeholder="e.g., User Login, Shopping Cart, Payment Processing",
        help="Enter the name of the feature you want to test"
    )
    
    requirements = st.text_area(
        "Requirements Description",
        height=150,
        placeholder="Describe the feature requirements, acceptance criteria, and expected behavior..."
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Test Types")
        test_types = []
        if st.checkbox("Functional", value=True):
            test_types.append("functional")
        if st.checkbox("UI/UX", value=True):
            test_types.append("ui")
        if st.checkbox("Security", value=True):
            test_types.append("security")
        if st.checkbox("Negative", value=True):
            test_types.append("negative")
        if st.checkbox("Performance"):
            test_types.append("performance")
    
    with col2:
        st.markdown("#### Priority Levels")
        priority_levels = []
        if st.checkbox("High", value=True):
            priority_levels.append("high")
        if st.checkbox("Medium", value=True):
            priority_levels.append("medium")
        if st.checkbox("Low", value=True):
            priority_levels.append("low")
    
    st.markdown("#### Output Formats")
    col1, col2, col3 = st.columns(3)
    output_formats = []
    with col1:
        if st.checkbox("JSON", value=True):
            output_formats.append("json")
    with col2:
        if st.checkbox("Markdown", value=True):
            output_formats.append("markdown")
    with col3:
        if st.checkbox("Selenium Python", value=True):
            output_formats.append("selenium")
    
    if st.button("🚀 Generate Test Cases", type="primary", use_container_width=True):
        if feature.strip() and requirements.strip():
            if not test_types:
                st.warning("⚠️ Please select at least one test type")
            elif not priority_levels:
                st.warning("⚠️ Please select at least one priority level")
            elif not output_formats:
                st.warning("⚠️ Please select at least one output format")
            else:
                with st.spinner("Generating test cases... This may take a minute."):
                    result, status_code = generate_tests(
                        feature, requirements, test_types, priority_levels, output_formats
                    )
                    
                    if status_code == 200:
                        st.success(f"✅ Generated {len(result.get('test_cases', []))} test cases!")
                        
                        # Display metrics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Test Cases", len(result.get('test_cases', [])))
                        with col2:
                            st.metric("Generation Time", f"{result.get('generation_time_ms', 0)} ms")
                        with col3:
                            st.metric("Output Files", len(result.get('output_files', [])))
                        
                        # Display test cases
                        st.markdown("### 📋 Generated Test Cases")
                        
                        for i, test in enumerate(result.get('test_cases', []), 1):
                            st.markdown(f'<div class="test-case-card">', unsafe_allow_html=True)
                            
                            col1, col2, col3 = st.columns([2, 1, 1])
                            with col1:
                                st.markdown(f"**{test.get('id', 'N/A')}**: {test.get('title', 'Untitled')}")
                            with col2:
                                priority = test.get('priority', 'medium')
                                priority_color = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}
                                st.markdown(f"{priority_color.get(priority, '⚪')} {priority.upper()}")
                            with col3:
                                st.markdown(f"📂 {test.get('type', 'N/A')}")
                            
                            if test.get('preconditions'):
                                st.markdown("**Preconditions:**")
                                for pre in test.get('preconditions', []):
                                    st.markdown(f"- {pre}")
                            
                            if test.get('steps'):
                                with st.expander("View Test Steps"):
                                    for step in test.get('steps', []):
                                        st.markdown(f"**Step {step.get('step_number', '')}:** {step.get('action', '')}")
                                        st.caption(f"Expected: {step.get('expected', '')}")
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Display output files
                        if result.get('output_files'):
                            st.markdown("### 📁 Output Files")
                            output_files = result.get('output_files', {})
                            if isinstance(output_files, dict):
                                for format_type, file_path in output_files.items():
                                    if isinstance(file_path, list):
                                        for fp in file_path:
                                            st.code(f"{format_type}: {fp}")
                                    else:
                                        st.code(f"{format_type}: {file_path}")
                            elif isinstance(output_files, list):
                                for file_info in output_files:
                                    if isinstance(file_info, dict):
                                        st.code(f"{file_info.get('format', 'unknown')}: {file_info.get('path', 'N/A')}")
                                    else:
                                        st.code(str(file_info))
                        
                        # Display full JSON
                        with st.expander("View Full JSON Response"):
                            st.json(result)
                    else:
                        st.error(f"❌ Generation failed: {result.get('error', 'Unknown error')}")
        else:
            st.warning("⚠️ Please provide both feature name and requirements")


elif "▶️ Run Tests" in page:
    st.markdown('<p class="main-header">▶️ Run Test Cases</p>', unsafe_allow_html=True)
    
    st.info("""
    ### 📖 How to Use Test Execution
    
    **Option 1: Browse Pre-Generated Test Cases**
    1. Navigate to `app/testcases/<feature-name>/` folders
    2. Open `testcases.json` to view available test cases
    3. Copy test case ID (e.g., `TC-AUTH-001`)
    4. Paste below and click "Run Test"
    
    **Option 2: Use Generated Tests**
    1. Go to "Generate Test Cases" tab
    2. Generate tests for your feature
    3. Note the test IDs in the output
    4. Return here and run them
    
    **Available Pre-Built Test Suites:**
    - `TC-AUTH-001` to `TC-AUTH-008`: Authentication tests
    - `TC-CART-001` to `TC-CART-008`: Shopping cart tests
    - `TC-PAY-001` to `TC-PAY-008`: Payment processing tests
    - `TC-USER-001` to `TC-USER-008`: User management tests
    - `TC-SEARCH-001` to `TC-SEARCH-008`: Search functionality tests
    """)
    
    st.markdown("---")
    
    test_id = st.text_input(
        "Test ID",
        placeholder="e.g., TC-AUTH-001, TC-CART-003, TC-PAY-001",
        help="Enter the test case ID from the testcases folders or generated tests"
    )
    
    base_url = st.text_input(
        "Base URL",
        value="http://localhost:3000",
        placeholder="e.g., http://localhost:3000",
        help="The base URL of your application to test against"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        headless = st.checkbox("Run in Headless Mode", value=False, 
                               help="Run browser in background without GUI")
    with col2:
        timeout = st.number_input("Timeout (seconds)", min_value=10, max_value=300, value=30,
                                  help="Maximum time to wait for test completion")
    
    if st.button("▶️ Run Test", type="primary", use_container_width=True):
        if test_id.strip():
            with st.spinner(f"Executing test {test_id}..."):
                result, status_code = run_test(test_id, base_url, headless, timeout)
                
                if status_code == 200:
                    test_status = result.get('status', 'unknown')
                    
                    if test_status == 'passed':
                        st.success(f"✅ Test {test_id} PASSED!")
                    elif test_status == 'failed':
                        st.error(f"❌ Test {test_id} FAILED")
                        
                        # Check for common ChromeDriver errors
                        error_output = result.get('stdout', '') + result.get('stderr', '')
                        if 'WinError 193' in error_output or 'OSError' in error_output:
                            st.error("""
                            ### 🔧 ChromeDriver Setup Issue Detected!
                            
                            The test failed due to ChromeDriver configuration problems.
                            
                            **Quick Fix:**
                            1. Open terminal in project folder
                            2. Run: `pip install webdriver-manager --upgrade`
                            3. Clear cache: Delete `C:\\Users\\<YourUsername>\\.wdm\\` folder
                            4. Try running test again
                            
                            **For detailed troubleshooting, see:** `SELENIUM_SETUP_GUIDE.md`
                            """)
                        
                    elif test_status == 'timeout':
                        st.warning(f"⏱️ Test {test_id} TIMEOUT")
                    else:
                        st.info(f"ℹ️ Test {test_id} status: {test_status}")
                    
                    # Display metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Test ID", result.get('test_id', 'N/A'))
                    with col2:
                        st.metric("Status", test_status.upper())
                    with col3:
                        st.metric("Execution Time", f"{result.get('execution_time_ms', 0)} ms")
                    
                    # Display logs
                    if result.get('stdout'):
                        with st.expander("📋 Standard Output"):
                            st.text(result.get('stdout', ''))
                    
                    if result.get('stderr'):
                        with st.expander("⚠️ Standard Error"):
                            st.text(result.get('stderr', ''))
                    
                    if result.get('logs'):
                        with st.expander("📜 Detailed Logs"):
                            for log in result.get('logs', [])[:50]:  # Limit to 50 logs
                                st.text(log.get('message', ''))
                    
                    # Display full JSON
                    with st.expander("View Full JSON Response"):
                        st.json(result)
                else:
                    st.error(f"❌ Test execution failed: {result.get('error', 'Unknown error')}")
        else:
            st.warning("⚠️ Please enter a test ID")


# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #6c757d; padding: 1rem;'>
        <p>🤖 Autonomous QA Agent v1.0.0 | Powered by RAG + LLM</p>
        <p>Built with ❤️ using Streamlit, Flask, ChromaDB & OpenRouter</p>
    </div>
    """,
    unsafe_allow_html=True
)
