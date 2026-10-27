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

/* Main Background */
.stApp {
    background: linear-gradient(135deg, #0f1020, #17152b, #101827);
    color: #ffffff;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #292442, #191827);
    border-right: 1px solid #7048a8;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #d8b4fe !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: #ffffff !important;
}

/* Gradient Header */
.hero {
    background: linear-gradient(120deg, #4f46e5, #9333ea, #db2777);
    padding: 35px;
    border-radius: 20px;
    color: white;
    margin-bottom: 30px;
    box-shadow: 0 8px 30px rgba(168, 85, 247, 0.35);
}

.hero h1 {
    color: white !important;
    font-size: 2.5rem;
    font-weight: 800;
}

.hero p {
    color: white !important;
    font-size: 1.1rem;
}

/* Dashboard Cards */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #302650, #1b1c2b);
    border: 1px solid #8b5cf6;
    border-radius: 16px;
    padding: 22px;
    box-shadow: 0 5px 20px rgba(139, 92, 246, 0.15);
}

div[data-testid="stMetricLabel"] {
    color: #c4b5fd !important;
}

div[data-testid="stMetricValue"] {
    color: #ffffff !important;
}

/* Headings */
h1, h2, h3 {
    color: #f5f3ff;
}

/* Input Fields */
.stTextInput input,
.stTextArea textarea {
    background-color: #25243a !important;
    color: #ffffff !important;
    border: 1px solid #7c3aed !important;
    border-radius: 10px !important;
}

/* Dropdowns */
.stSelectbox [data-baseweb="select"] > div {
    background-color: #25243a;
    border-color: #7c3aed;
    color: white;
}

/* Colourful Buttons */
.stButton > button,
.stFormSubmitButton > button {
    background: linear-gradient(90deg, #6366f1, #9333ea, #db2777) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: bold !important;
    padding: 10px 20px !important;
    transition: 0.3s ease;
}

/* Button Hover */
.stButton > button:hover,
.stFormSubmitButton > button:hover {
    filter: brightness(1.2);
    box-shadow: 0 5px 20px rgba(219, 39, 119, 0.35);
    border: 1px solid white !important;
}

/* Forms */
[data-testid="stForm"] {
    background: rgba(40, 32, 65, 0.55);
    border: 1px solid #7048a8;
    border-radius: 15px;
    padding: 20px;
}

/* Radio Buttons */
.stRadio label {
    color: #e9d5ff !important;
}

/* Dividers */
hr {
    border-color: #51416f !important;
}

/* Success Messages */
[data-testid="stAlert"][kind="success"] {
    border: 1px solid #10b981;
    border-radius: 10px;
}

/* Responsive Design */
@media (max-width: 768px) {
    .hero {
        padding: 22px;
    }

    .hero h1 {
        font-size: 1.8rem;
    }
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

       
# --------------------------------------------------
# DELETE FILE
# --------------------------------------------------

elif operation == "🗑️ Delete File":

    st.header("🗑️ Delete a File")

    files = get_files()

    if not files:
        st.info("No files found. Please create a file first.")

    else:
        filename = st.selectbox(
            "Select a file to delete",
            files,
            key="delete_filename"
        )

        confirm_delete = st.checkbox(
            f"I confirm that I want to delete '{filename}'",
            key="confirm_delete"
        )

        if st.button(
            "🗑️ Delete File",
            use_container_width=True
        ):
            if not confirm_delete:
                st.warning("Please confirm before deleting the file.")
            else:
                try:
                    path = get_file(filename)
                    path.unlink()

                    st.success(f"File '{filename}' deleted successfully!")
                    st.rerun()

                except (OSError, ValueError) as error:
                    st.error(f"Unable to delete file: {error}")
