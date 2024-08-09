import os
import streamlit as st
from file_checker import checkFile
from blockchain import Blockchain

# Initialize the blockchain
blockchain = Blockchain()

# Ensure the 'malwares' directory exists
malwares_dir = 'malwares'
if not os.path.exists(malwares_dir):
    os.makedirs(malwares_dir)

# Streamlit Sidebar with Icons
st.sidebar.title("Navigation")
selected_option = st.sidebar.radio(
    "Choose an option",
    ["🏠 Home", "📁 Upload & Detect", "🔗 View Blockchain"]
)

# Home Section
if selected_option == "🏠 Home":
    st.title("Welcome to the Malware Detection & Blockchain Viewer")
    st.markdown("""
    This application allows you to:
    
    - **Upload files** and detect if they are malware.
    - If the file is malware, it will be **stored securely in a blockchain**.
    - **View the entire blockchain** and track all the malware that has been detected.
    """)
    st.image("https://images.unsplash.com/photo-1515974251951-8a2b84b3e5ca", use_column_width=True)
    st.markdown("Made with 💻 and Streamlit", unsafe_allow_html=True)

# Upload & Detect Section
if selected_option == "📁 Upload & Detect":
    st.title("Malware Detection and Blockchain Addition")
    st.markdown("""
    ### Upload a file to check if it's malware and store it on the blockchain if necessary.
    """)
    
    uploaded_file = st.file_uploader("Upload a file", type=["exe", "bin", "dll", "jar", "py", "zip", "rar"])
    
    if uploaded_file is not None:
        file_path = os.path.join(malwares_dir, uploaded_file.name)
        
        # Save the uploaded file
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getvalue())
    
        # Check if the file is malware
        is_legitimate = checkFile(file_path)
        
        # Remove the temporary file
        os.remove(file_path)
        
        if is_legitimate:
            st.success(f"✅ The file '{uploaded_file.name}' seems to be legitimate.")
        else:
            st.error(f"🚨 The file '{uploaded_file.name}' is probably malware!")
            new_block = blockchain.add_block(uploaded_file.name)
            st.success("📦 The file has been added to the blockchain!")
            with st.expander("View Block Details"):
                st.json({
                    "index": new_block.index,
                    "previous_hash": new_block.previous_hash,
                    "timestamp": new_block.timestamp,
                    "data": new_block.data,
                    "hash": new_block.hash
                })

# View Blockchain Section
if selected_option == "🔗 View Blockchain":
    st.title("Blockchain")
    st.markdown("### Here are the blocks currently in the blockchain:")

    # Fetch blockchain data directly from MongoDB
    blocks = list(blockchain.collection.find().sort("index", 1))
    
    if len(blocks) > 0:
        for block in blocks:
            with st.expander(f"🔗 Block {block['index']}"):
                st.json({
                    "index": block["index"],
                    "previous_hash": block["previous_hash"],
                    "timestamp": block["timestamp"],
                    "data": block["data"],
                    "hash": block["hash"]
                })
    else:
        st.warning("⚠️ No blocks in the blockchain yet.")
