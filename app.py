from pathlib import Path
import streamlit as st

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="File Handling Manager",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: #f5f5f5;
}

[data-testid="stSidebar"] {
    background-color: #262730;
}

[data-testid="stSidebar"] h1 {
    color: white;
}

.hero {
    background: linear-gradient(
        120deg,
        #4f46e5,
        #7c3aed,
        #db2777
    );
    padding: 35px;
    border-radius: 20px;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 10px 30px rgba(124, 58, 237, 0.2);
}

.hero h1 {
    color: white;
    font-size: 2.4rem;
    margin-bottom: 12px;
}

.hero p {
    color: white;
    font-size: 1.1rem;
}

div[data-testid="stMetric"] {
    background-color: #1b1c23;
    border: 1px solid #393a45;
    padding: 22px;
    border-radius: 15px;
}

div[data-testid="stMetricLabel"],
div[data-testid="stMetricValue"] {
    color: white;
}

.stButton > button {
    background: linear-gradient(90deg, #6366f1, #db2777);
    color: white;
    border: none;
    border-radius: 9px;
    padding: 10px 20px;
    font-weight: bold;
    transition: 0.2s;
}

.stButton > button:hover {
    border: 1px solid #ffffff;
    color: white;
    filter: brightness(1.15);
}

.stTextInput input,
.stTextArea textarea {
    background-color: #262730;
    color: white;
    border-radius: 8px;
}

h1, h2, h3 {
    color: #f5f5f5;
}

hr {
    border-color: #393a45;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# FILE STORAGE
# --------------------------------------------------

DATA_DIR = Path("user_files")
DATA_DIR.mkdir(exist_ok=True)


def get_file(filename):
    """Return a validated path inside the storage directory."""

    filename = filename.strip()

    if not filename or filename in (".", ".."):
        raise ValueError("Please enter a valid file name.")

    if Path(filename).name != filename:
        raise ValueError("Please enter a file name without folder paths.")

    base = DATA_DIR.resolve()
    path = (DATA_DIR / filename).resolve()

    if path.parent != base:
        raise ValueError("Invalid file path.")

    return path


def get_files():
    """List files stored in the project directory."""

    return sorted(
        file.name
        for file in DATA_DIR.iterdir()
        if file.is_file()
    )


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<div class="hero">
    <h1>📁 File Handling Manager</h1>
    <p>Create • Read • Update • Delete files</p>
    <p>Built with Python and Streamlit</p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

files = get_files()

total_files = len(files)

total_size = sum(
    (DATA_DIR / filename).stat().st_size
    for filename in files
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📄 Total Files", total_files)

with col2:
    if total_size < 1024:
        size_display = f"{total_size} B"
    elif total_size < 1024 * 1024:
        size_display = f"{total_size / 1024:.2f} KB"
    else:
        size_display = f"{total_size / (1024 * 1024):.2f} MB"

    st.metric("💾 Storage Used", size_display)

with col3:
    st.metric("⚙️ File Operations", 4)

st.divider()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("⚙️ Operations")

operation = st.sidebar.radio(
    "Choose an operation",
    [
        "➕ Create File",
        "📖 Read File",
        "✏️ Update File",
        "🗑️ Delete File"
    ]
)

st.sidebar.divider()

st.sidebar.markdown("### 👨‍💻 About")
st.sidebar.write("Made by Rishu Kumar")
st.sidebar.caption("Python • pathlib • Streamlit")

# --------------------------------------------------
# CREATE FILE
# --------------------------------------------------

if operation == "➕ Create File":

    st.header("➕ Create a New File")

    with st.form("create_file_form"):

        filename = st.text_input(
            "File name",
            placeholder="notes.txt"
        )

        content = st.text_area(
            "File content",
            placeholder="Write something..."
        )

        create_button = st.form_submit_button(
            "➕ Create File",
            use_container_width=True
        )

    if create_button:

        try:
            path = get_file(filename)

            if path.exists():
                st.error("A file with this name already exists.")

            else:
                with path.open("x", encoding="utf-8") as file:
                    file.write(content)

                st.success(
                    f"File '{filename}' created successfully!"
                )

                st.rerun()

        except (OSError, ValueError) as error:
            st.error(f"Unable to create file: {error}")

# --------------------------------------------------
# READ FILE
# --------------------------------------------------

elif operation == "📖 Read File":

    st.header("📖 Read a File")

    files = get_files()

    if not files:

        st.info("No files found. Please create a file first.")

    else:

        filename = st.selectbox(
            "Select a file",
            files,
            key="read_filename"
        )

        if st.button(
            "📖 Read File",
            use_container_width=True
        ):

            try:
                path = get_file(filename)

                with path.open("r", encoding="utf-8") as file:
                    content = file.read()

                st.success(f"Opened '{filename}' successfully.")

                st.text_area(
                    "File Content",
                    value=content,
                    height=250,
                    disabled=True
                )

            except (OSError, UnicodeError, ValueError) as error:
                st.error(f"Unable to read file: {error}")

# --------------------------------------------------
# UPDATE FILE
# --------------------------------------------------

elif operation == "✏️ Update File":

    st.header("✏️ Update a File")

    files = get_files()

    if not files:

        st.info("No files found. Please create a file first.")

    else:

        filename = st.selectbox(
            "Select a file to update",
            files,
            key="update_filename"
        )

        update_type = st.radio(
            "Choose an operation",
            [
                "Rename File",
                "Append Content",
                "Overwrite Content"
            ],
            horizontal=True
        )

        # RENAME FILE

        if update_type == "Rename File":

            new_name = st.text_input(
                "New file name",
                placeholder="new_notes.txt"
            )

            if st.button(
                "✏️ Rename File",
                use_container_width=True
            ):

                try:
                    old_path = get_file(filename)

                    if not new_name.strip():

                        st.error("Please enter a new file name.")

                    else:

                        new_path = get_file(new_name)

                        if new_path.exists():

                            st.error(
                                "A file with the new name already exists."
                            )

                        else:

                            old_path.rename(new_path)

                            st.success("File renamed successfully!")

                            st.rerun()

                except (OSError, ValueError) as error:
                    st.error(f"Unable to rename file: {error}")

        # APPEND CONTENT

        elif update_type == "Append Content":

            new_content = st.text
