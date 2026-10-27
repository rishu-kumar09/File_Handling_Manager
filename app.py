import streamlit as st
from pathlib import Path
from datetime import datetime

# ---------- Setup ----------
BASE_DIR = Path("workspace")  # all files live here (safe sandbox)
BASE_DIR.mkdir(exist_ok=True)

st.set_page_config(page_title="File Handling Manager", page_icon="📁", layout="wide")

# ---------- Custom CSS ----------
st.markdown(
    """
    <style>
    .hero {
        background: linear-gradient(120deg, #4f46e5, #7c3aed 55%, #db2777);
        padding: 2rem 2.2rem; border-radius: 18px; color: white;
        margin-bottom: 1.4rem; box-shadow: 0 10px 30px rgba(79,70,229,.30);
    }
    .hero h1 { margin: 0; font-size: 2.1rem; }
    .hero p  { margin: .4rem 0 0; opacity: .9; }
    .stat {
        background: rgba(128,128,128,.10); border: 1px solid rgba(128,128,128,.25);
        border-radius: 14px; padding: 1rem 1.2rem; text-align: center;
    }
    .stat h2 { margin: 0; font-size: 1.8rem; }
    .stat span { opacity: .7; font-size: .85rem; }
    div.stButton > button {
        border-radius: 10px; font-weight: 600; padding: .5rem 1.4rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- Helpers ----------
def get_path(name: str):
    """Return a safe path inside workspace (blocks ../ tricks)."""
    name = Path(name.strip()).name
    return BASE_DIR / name if name else None


def list_files():
    return sorted(p for p in BASE_DIR.iterdir() if p.is_file())


def human_size(n: int) -> str:
    return f"{n} B" if n < 1024 else f"{n / 1024:.1f} KB"


# ---------- Header ----------
st.markdown(
    """
    <div class="hero">
        <h1>📁 File Handling Manager</h1>
        <p>Create • Read • Update • Delete files — built with Python &amp; Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True,
)

files = list_files()
total_size = sum(f.stat().st_size for f in files)

c1, c2, c3 = st.columns(3)
c1.markdown(f'<div class="stat"><h2>{len(files)}</h2><span>Total Files</span></div>', unsafe_allow_html=True)
c2.markdown(f'<div class="stat"><h2>{human_size(total_size)}</h2><span>Storage Used</span></div>', unsafe_allow_html=True)
c3.markdown(f'<div class="stat"><h2>{datetime.now():%H:%M}</h2><span>Current Time</span></div>', unsafe_allow_html=True)

st.write("")

# ---------- Sidebar ----------
with st.sidebar:
    st.title("⚙️ Operations")
    choice = st.radio(
        "Choose an action",
        ["➕ Create File", "📖 Read File", "✏️ Update File", "🗑️ Delete File"],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("Made by Rishu Srivastava")
    st.caption("Python • pathlib • Streamlit")

# ---------- 1. CREATE ----------
if choice == "➕ Create File":
    st.subheader("➕ Create a New File")
    name = st.text_input("File name", placeholder="notes.txt")
    data = st.text_area("File content", height=200, placeholder="Write something...")

    if st.button("Create File", type="primary"):
        path = get_path(name)
        if path is None:
            st.warning("Please enter a file name.")
        elif path.exists():
            st.error(f"'{path.name}' already exists.")
        else:
            path.write_text(data, encoding="utf-8")
            st.success(f"File '{path.name}' created successfully!")
            st.balloons()

# ---------- 2. READ ----------
elif choice == "📖 Read File":
    st.subheader("📖 Read a File")
    if not files:
        st.info("No files yet. Create one first!")
    else:
        selected = st.selectbox("Select a file", [f.name for f in files])
        path = BASE_DIR / selected
        content = path.read_text(encoding="utf-8")
        st.text_area("Content", content, height=250, disabled=True)
        st.download_button("⬇️ Download", content, file_name=selected)

# ---------- 3. UPDATE ----------
elif choice == "✏️ Update File":
    st.subheader("✏️ Update a File")
    if not files:
        st.info("No files yet. Create one first!")
    else:
        selected = st.selectbox("Select a file", [f.name for f in files])
        path = BASE_DIR / selected
        mode = st.radio("What do you want to do?", ["Rename", "Append", "Overwrite"], horizontal=True)

        if mode == "Rename":
            new_name = st.text_input("New file name")
            if st.button("Rename", type="primary"):
                new_path = get_path(new_name)
                if new_path is None:
                    st.warning("Enter a new name.")
                elif new_path.exists():
                    st.error("A file with that name already exists.")
                else:
                    path.rename(new_path)
                    st.success(f"Renamed to '{new_path.name}'")
                    st.rerun()

        elif mode == "Append":
            extra = st.text_area("Text to append", height=150)
            if st.button("Append", type="primary"):
                with open(path, "a", encoding="utf-8") as fs:
                    fs.write("\n" + extra)
                st.success("Content appended successfully!")

        else:  # Overwrite
            new_data = st.text_area("New content (old content will be replaced)", height=150)
            if st.button("Overwrite", type="primary"):
                path.write_text(new_data, encoding="utf-8")
                st.success("File overwritten successfully!")

# ---------- 4. DELETE ----------
else:
    st.subheader("🗑️ Delete a File")
    if not files:
        st.info("Nothing to delete.")
    else:
        selected = st.selectbox("Select a file", [f.name for f in files])
        sure = st.checkbox(f"Yes, I want to permanently delete '{selected}'")
        if st.button("Delete File", type="primary", disabled=not sure):
            (BASE_DIR / selected).unlink()
            st.success(f"'{selected}' deleted successfully!")
            st.rerun()

# ---------- File Explorer ----------
st.divider()
st.subheader("🗂️ File Explorer")
files = list_files()
if files:
    st.dataframe(
        [
            {
                "File": f.name,
                "Size": human_size(f.stat().st_size),
                "Modified": datetime.fromtimestamp(f.stat().st_mtime).strftime("%d %b %Y, %H:%M"),
            }
            for f in files
        ],
        use_container_width=True,
        hide_index=True,
    )
else:
    st.caption("Workspace is empty.")