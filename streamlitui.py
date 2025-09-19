import streamlit as st
import json
from datetime import datetime
import time
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the AI agent directly
try:
    import sys
    sys.path.append(".")
    from app.agent import run_analysis
    AGENT_AVAILABLE = True
except ImportError:
    AGENT_AVAILABLE = False

# Streamlit App Config
st.set_page_config(
    page_title="Misinformation Detection System", 
    layout="wide",
    page_icon="🔍",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .result-box {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .credible {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
    }
    .suspicious {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
    }
    .misinformation {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
    }
    .analysis-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🔍 DetectAI: Misinformation Detection System</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Powered by Google Gemini AI - Analyze text content for credibility and misinformation</p>', unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # AI Configuration
    st.subheader("🔑 API Configuration")
    
    # Try to get API key from secrets first, then environment, then user input
    api_key_from_secrets = None
    try:
        api_key_from_secrets = st.secrets.get("GEMINI_API_KEY", None)
    except:
        pass
    
    api_key_from_env = os.getenv("GEMINI_API_KEY", "")
    
    if api_key_from_secrets:
        st.success("✅ API Key loaded from Streamlit secrets")
        gemini_api_key = api_key_from_secrets
        os.environ["GEMINI_API_KEY"] = gemini_api_key
    elif api_key_from_env and api_key_from_env != "your-gemini-api-key-here":
        st.success("✅ API Key loaded from environment")
        gemini_api_key = api_key_from_env
    else:
        st.warning("⚠️ API Key required for analysis")
        gemini_api_key = st.text_input(
            "Enter your Gemini API Key", 
            value="",
            type="password",
            help="Get your API key from: https://makersuite.google.com/app/apikey",
            placeholder="Enter your Gemini API key here..."
        )
        
        if gemini_api_key:
            os.environ["GEMINI_API_KEY"] = gemini_api_key
            st.success("✅ API Key configured for this session")
        else:
            st.info("💡 For deployment, add GEMINI_API_KEY to your Streamlit secrets")
    
    st.markdown("---")
    
    # Analysis settings
    st.subheader("Analysis Settings")
    max_claims = st.slider("Max Claims to Analyze", 1, 10, 5)
    analysis_timeout = st.slider("Analysis Timeout (seconds)", 10, 60, 30)
    
    st.markdown("---")
    
    # Security note
    st.subheader("🔒 Security")
    st.info("""
    **API Key Security:**
    • Keys entered here are only stored for this session
    • For deployment, use Streamlit secrets
    • Never share your API key publicly
    """)
    
    st.markdown("---")
    
    # About section
    st.subheader("About")
    st.info("""
    This system uses Google Gemini AI to analyze text content and detect potential misinformation by:
    
    • Extracting key claims
    • Fact-checking against reliable sources
    • Analyzing credibility indicators
    • Providing detailed explanations
    """)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📝 Text Analysis")
    
    # Text input options
    input_method = st.radio(
        "Choose input method:",
        ["Type/Paste Text", "Upload Text File"],
        horizontal=True
    )
    
    user_text = ""
    
    if input_method == "Type/Paste Text":
        user_text = st.text_area(
            "Enter text to analyze:",
            placeholder="Paste news article, social media post, or any text content here...",
            height=200,
            help="Enter the text you want to analyze for misinformation"
        )
    else:
        uploaded_file = st.file_uploader(
            "Upload a text file",
            type=["txt", "md", "rtf"],
            help="Upload a text file to analyze"
        )
        if uploaded_file:
            user_text = str(uploaded_file.read(), "utf-8")
            st.text_area("File content:", value=user_text, height=200, disabled=True)
    
    # Analysis button
    analyze_button = st.button(
        "🔍 Analyze for Misinformation",
        type="primary",
        use_container_width=True,
        disabled=not user_text.strip()
    )

with col2:
    st.subheader("📊 Quick Stats")
    
    if user_text:
        word_count = len(user_text.split())
        char_count = len(user_text)
        
        st.metric("Word Count", word_count)
        st.metric("Character Count", char_count)
        
        # Text preview
        st.subheader("📄 Text Preview")
        preview_text = user_text[:200] + "..." if len(user_text) > 200 else user_text
        st.text_area("Preview:", value=preview_text, height=100, disabled=True)

# Analysis Results Section
if analyze_button and user_text.strip():
    st.markdown("---")
    st.subheader("🔬 Analysis Results")
    
    with st.spinner("🤖 AI is analyzing the content... This may take a few moments."):
        try:
            if not AGENT_AVAILABLE:
                st.error("❌ AI agent not available. Please check your installation.")
                st.stop()
            
            if not gemini_api_key:
                st.error("❌ Please provide your Gemini API key in the sidebar.")
                st.stop()
            
            # Run analysis directly
            start_time = time.time()
            
            # Run the async function
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(run_analysis(user_text.strip()))
            loop.close()
            
            end_time = time.time()
            
            if result:
                
                # Display overall credibility score
                credibility_score = result.get("credibility_score", 0)
                overall_assessment = result.get("overall_assessment", "Unknown")
                
                # Determine result styling based on credibility
                if credibility_score >= 0.7:
                    result_class = "credible"
                    icon = "✅"
                elif credibility_score >= 0.4:
                    result_class = "suspicious"
                    icon = "⚠️"
                else:
                    result_class = "misinformation"
                    icon = "❌"
                
                # Main result display
                st.markdown(f"""
                <div class="result-box {result_class}">
                    <h3>{icon} Overall Assessment: {overall_assessment}</h3>
                    <p><strong>Credibility Score:</strong> {credibility_score:.2f}/1.00</p>
                    <p><strong>Analysis Time:</strong> {end_time - start_time:.2f} seconds</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Detailed analysis
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("🎯 Key Claims Analysis")
                    st.markdown("*Individual claims extracted from the text and their credibility assessment*")
                    
                    claims = result.get("claims", [])
                    
                    if claims and len(claims) > 0:
                        for i, claim in enumerate(claims, 1):
                            claim_text = claim.get('text', 'No claim text available')
                            claim_credibility = claim.get('credibility', 'Unknown')
                            claim_evidence = claim.get('evidence', 'No evidence provided')
                            
                            # Determine claim credibility color
                            if claim_credibility.lower() in ['high', 'credible', 'accurate']:
                                claim_color = "🟢"
                            elif claim_credibility.lower() in ['medium', 'moderate', 'mixed']:
                                claim_color = "🟡"
                            else:
                                claim_color = "🔴"
                            
                            with st.expander(f"{claim_color} Claim {i}: {claim_text[:60]}{'...' if len(claim_text) > 60 else ''}"):
                                st.markdown(f"**📝 Full Claim:**")
                                st.write(claim_text)
                                
                                st.markdown(f"**🎯 Credibility Assessment:** {claim_credibility}")
                                
                                st.markdown(f"**🔍 Evidence & Analysis:**")
                                st.write(claim_evidence)
                                
                                # Add explanation of credibility levels
                                if claim_credibility.lower() in ['high', 'credible', 'accurate']:
                                    st.success("✅ This claim appears to be well-supported by evidence")
                                elif claim_credibility.lower() in ['medium', 'moderate', 'mixed']:
                                    st.warning("⚠️ This claim has mixed or limited supporting evidence")
                                else:
                                    st.error("❌ This claim appears to lack credible supporting evidence")
                    else:
                        st.info("""
                        **No specific claims were extracted from the text.**
                        
                        This could happen when:
                        • The text is too short or vague
                        • The content doesn't contain factual assertions
                        • The AI couldn't identify distinct claims to analyze
                        
                        The overall assessment above still provides a general credibility evaluation.
                        """)
                
                with col2:
                    st.subheader("📋 Analysis Summary")
                    st.markdown("*Overall assessment and key findings from the AI analysis*")
                    
                    # Summary information
                    summary = result.get("summary", "")
                    explanation = result.get("explanation", "")
                    
                    # Display summary or explanation
                    analysis_text = summary or explanation or "No detailed summary available"
                    
                    if analysis_text and analysis_text != "No detailed summary available":
                        st.markdown(f"""
                        <div class="analysis-card">
                            <strong>🔍 Detailed Analysis:</strong><br><br>
                            {analysis_text}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Add interpretation guide
                        st.markdown("---")
                        st.markdown("**📖 How to interpret this analysis:**")
                        if credibility_score >= 0.7:
                            st.success("• The content appears reliable and well-supported")
                            st.info("• Cross-reference with additional sources for complete verification")
                        elif credibility_score >= 0.4:
                            st.warning("• The content has mixed reliability - some parts may be accurate")
                            st.info("• Verify specific claims independently before sharing")
                        else:
                            st.error("• The content shows signs of potential misinformation")
                            st.info("• Exercise caution and seek authoritative sources")
                    else:
                        st.info("""
                        **Analysis summary not available.**
                        
                        The AI analysis completed but didn't provide a detailed summary. 
                        Check the raw API response below for technical details.
                        """)
                    
                    # Analysis metrics
                    st.markdown("---")
                    st.markdown("**📊 Analysis Metrics:**")
                    
                    # Create metrics display
                    metrics_col1, metrics_col2 = st.columns(2)
                    with metrics_col1:
                        st.metric("Credibility Score", f"{credibility_score:.2f}", 
                                help="Scale: 0.0 (Highly Questionable) to 1.0 (Highly Credible)")
                    with metrics_col2:
                        claims_count = len(claims) if claims else 0
                        st.metric("Claims Analyzed", claims_count,
                                help="Number of distinct factual claims identified and evaluated")
                    
                    # Additional metadata
                    if "metadata" in result:
                        metadata = result["metadata"]
                        st.markdown("**🔧 Technical Metadata:**")
                        st.json(metadata)
                
                # Recommendations
                if "recommendations" in result:
                    st.subheader("💡 Recommendations")
                    recommendations = result["recommendations"]
                    for rec in recommendations:
                        st.info(f"• {rec}")
                
                # Raw response (collapsible)
                with st.expander("🔍 View Raw API Response"):
                    st.markdown("""
                    **📋 About the Raw API Response:**
                    
                    This section shows the complete, unprocessed response from the AI analysis API. 
                    It includes all technical details and data structures returned by the system.
                    
                    **Key fields explained:**
                    - `overall_assessment`: The AI's final verdict on content credibility
                    - `credibility_score`: Numerical score from 0.0 (least credible) to 1.0 (most credible)
                    - `summary/explanation`: Detailed reasoning behind the assessment
                    - `claims`: Individual factual assertions found and analyzed
                    - `recommendations`: Suggested actions based on the analysis
                    - `metadata`: Technical information about the analysis process
                    
                    ---
                    """)
                    st.json(result)
                    
            else:
                st.error("❌ Analysis failed: No results returned")
                
        except Exception as e:
            st.error(f"⚡ Analysis error: {str(e)}")
            st.error("Please check your Gemini API key and internet connection.")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🚀 Quick Start")
    st.info("1. Enter or upload text\n2. Click 'Analyze'\n3. Review results")

with col2:
    st.subheader("⚡ Features")
    st.info("• AI-powered analysis\n• Claim extraction\n• Credibility scoring\n• Evidence checking")

with col3:
    st.subheader("🛠️ Status")
    # AI Service check
    current_api_key = os.getenv("GEMINI_API_KEY", "")
    if AGENT_AVAILABLE and current_api_key and current_api_key != "your-gemini-api-key-here":
        st.success("✅ AI Service Ready")
    elif AGENT_AVAILABLE and not current_api_key:
        st.warning("⚠️ API Key Needed")
    else:
        st.error("❌ AI Service Unavailable")

# Add timestamp
st.markdown(f"<small>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small>", unsafe_allow_html=True)
