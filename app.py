import streamlit as st
from crew import run_tone_crew 

# 1. Page Configuration
st.set_page_config(
    page_title="Tone Adaptive Writer Agent",
    page_icon="✍️",
    layout="wide" 
)

# 2. Custom Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: gray;
        border-radius: 5px 5px 0 0;
        gap: 1px;
        padding: 10px;
    }
    .stTabs [aria-selected="true"] { background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

def main():
    # Header Section
    st.title("✍️ Tone Adaptive Writer Agent")
    st.markdown("### Generate specialized content for Academic, Conversational, and Corporate audiences.")
    st.divider()

    # Layout: Sidebar for info
    with st.sidebar:
        st.header("Project Info")
        st.write("This multi-agent system uses specialized writers to adapt core research into distinct voices.")
        st.info("Each tab below contains a unique rewrite of the same factual data.")

    # 3. Input Section
    st.subheader("Configuration")
    user_input = st.text_area(
        "Enter your topic or raw content:",
        height=150,
        placeholder="e.g., Write a LinkedIn post announcing a new product launch..."
    )

    if st.button("Generate Adaptive Content 🚀"):
        if not user_input.strip():
            st.warning("⚠️ Please provide a topic or prompt to begin.")
        else:
            with st.spinner("🤖 The Crew is researching and writing three versions..."):
                try:
                    # run_tone_crew now returns a dictionary: {'academic': '...', 'conversational': '...', 'corporate': '...'}
                    results = run_tone_crew(user_input)
                    
                    st.success("✅ All versions generated successfully!")
                    st.divider()

                    # 4. Output Section using Tabs
                    st.subheader("📄 Generated Results")
                    tab1, tab2, tab3 = st.tabs(["🎓 Academic", "💬 Conversational", "🏢 Corporate"])

                    with tab1:
                        st.markdown("#### Scholarly Analysis")
                        st.info("Tone: Formal, objective, and technical.")
                        st.write(results['academic'])
                        st.download_button("Download Academic (.txt)", results['academic'], file_name="academic_tone.txt")
                    
                    with tab2:
                        st.markdown("#### Friendly Perspective")
                        st.info("Tone: Engaging, simple, and relatable.")
                        st.write(results['conversational'])
                        st.download_button("Download Conversational (.txt)", results['conversational'], file_name="conversational_tone.txt")
                        
                    with tab3:
                        st.markdown("#### Executive Summary")
                        st.info("Tone: Professional, concise, and impact-oriented.")
                        st.write(results['corporate'])
                        st.download_button("Download Corporate (.txt)", results['corporate'], file_name="corporate_tone.txt")

                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()