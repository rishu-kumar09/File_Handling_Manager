from pathlib import Path
import streamlit as st

# Configure the application
st.set_page_config(
    page_title="File Handling Manager",
    page_icon="📁",
    layout="wide"
)

# Store project files in a separate directory
DATA_DIR = Path("user_files")
DATA_DIR.mkdir(exist_ok=True)


def get_file(name):
    """Return a safe path for a file inside the storage directory."""
    name = name.strip()

    if not name or name in (".", "..") or Path(name).name != name:
        raise ValueError("Please enter a valid file name.")

    path = (DATA_DIR / name).resolve()

    if path.parent != DATA_DIR.resolve():
        raise ValueError("Invalid file name.")

    return path


def get_files():
    """Return files stored in the project directory."""
    return sorted(
        file.name for file in DATA_DIR.iterdir()
        if file.is_file()
    )


# Header
st.title("📁 File Handling Manager")
st.write("Create, read, update, and delete files easily using Python and Streamlit.")

# Dashboard
files = get_files()
total_size = sum(
    (DATA_DIR / name).stat().st_size for name in files
)

col1, col2, col3 = st.columns(3)

col1.metric("📄 Total Files", len(files))
col2.metric("💾 Storage Used", f"{total_size} bytes")
col3.metric("🛠️ Operations", 4)

st.divider()

# Sidebar menu
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
st.sidebar.caption("Made by Rishu Kumar")
st.sidebar.caption("Python • pathlib • Streamlit")


# CREATE FILE
if operation == "➕ Create File":

    st.header("➕ Create a New File")

    with st.form("create_form"):
        filename = st.text_input(
            "File name",
            placeholder="notes.txt"
        )

        content = st.text_area(
            "File content",
            placeholder="Write something..."
        )

        submitted = st.form_submit_button("Create File")

    if submitted:
        try:
            path = get_file(filename)

            if path.exists():
                st.error("A file with this name already exists.")
            else:
                with path.open("x", encoding="utf-8") as file:
                    file.write(content)

                st.success(f"File '{filename}' created successfully!")
                st.rerun()

        except (OSError, ValueError) as error:
            st.error(f"Unable to create file: {error}")


# READ FILE
elif operation == "📖 Read File":

    st.header("📖 Read a File")

    files = get_files()

    if not files:
        st.info("No files found. Create a file first.")
    else:
        filename = st.selectbox("Select a file", files)

        if st.button("Read File"):
            try:
                path = get_file(filename)

                with path.open("r", encoding="utf-8") as file:
                    content = file.read()

                st.success(f"Reading file: {filename}")
                st.text_area(
                    "File content",
                    value=content,
                    height=250,
                    disabled=True
                )

            except (OSError, UnicodeError, ValueError) as error:
                st.error(f"Unable to read file: {error}")


# UPDATE FILE
elif operation == "✏️ Update File":

    st.header("✏️ Update a File")

    files = get_files()

    if not files:
        st.info("No files found. Create a file first.")
    else:
        filename = st.selectbox("Select a file to update", files)

        update_type = st.radio(
            "Choose an operation",
            ["Rename File", "Append Content", "Overwrite Content"]
        )

        if update_type == "Rename File":
            new_name = st.text_input("New file name")

            if st.button("Rename File"):
                try:
                    old_path = get_file(filename)
                    new_path = get_file(new_name)

                    if not new_name.strip():
                        st.error("Please enter a new file name.")
                    elif new_path.exists():
                        st.error("A file with the new name already exists.")
                    else:
                        old_path.rename(new_path)
                        st.success("File renamed successfully!")
                        st.rerun()

                except (OSError, ValueError) as error:
                    st.error(f"Unable to rename file: {error}")

        elif update_type == "Append Content":
            new_content = st.text_area(
                "Content to append",
                placeholder="Enter additional content..."
            )

            if st.button("Append Content"):
                try:
                    path = get_file(filename)

                    with path.open("a", encoding="utf-8") as file:
                        if new_content:
                            file.write("\n" + new_content)

                    st.success("Content appended successfully!")

                except (OSError, ValueError) as error:
                    st.error(f"Unable to update file: {error}")

        else:
            new_content = st.text_area(
                "New file content",
                placeholder="Enter the new content..."
            )

            if st.button("Overwrite File"):
                try:
                    path = get_file(filename)

                    with path.open("w", encoding="utf-8") as file:
                        file.write(new_content)

                    st.success("File content overwritten successfully!")

                except (OSError, ValueError) as error:
                    st.error(f"Unable to update file: {error}")


# DELETE FILE
elif operation == "🗑️ Delete File":

    st.header("🗑️ Delete a File")

    files = get_files()

    if not files:
        st.info("No files found. Create a file first.")
    else:
        filename = st.selectbox("Select a file to delete", files)

        confirm = st.checkbox(
            f"I confirm that I want to delete '{filename}'."
        )

        if st.button("Delete File", type="primary"):
            if not confirm:
                st.warning("Please confirm before deleting the file.")
            else:
                try:
                    path = get_file(filename)
                    path.unlink()

                    st.success(f"File '{filename}' deleted successfully!")
                    st.rerun()

                except (OSError, ValueError) as error:
                    st.error(f"Unable to delete file: {error}")


st.divider()
st.caption("File Handling Manager | Built with Python and Streamlit")
