
import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="GST Rate Finder",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}
h1 {
    color: #17365d;
}
.stButton>button {
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# Load database
@st.cache_data
def load_data():
    try:
        return pd.read_csv(
            "gst_data.csv",
            dtype={"hsn_code": str}
        ).fillna("")
    except Exception:
        return pd.DataFrame()

df = load_data()

# Header
st.title("📊 GST RATE FINDER")
st.caption("Smart GST Information and HSN Classification System")

st.info(
    "Search products by name or HSN code and explore "
    "officially verified GST information."
)

# Sidebar
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose Section",
    [
        "Home",
        "Product Search",
        "Category Browsing",
        "GST Calculator",
        "About Project"
    ]
)

st.sidebar.divider()
st.sidebar.caption("BBA FinTech Practical Project")

# HOME PAGE
if page == "Home":

    st.header("Welcome to GST Rate Finder")

    st.write("""
    This application helps users understand GST rates,
    HSN classifications and tax treatment of goods.

    Users can search using a product name or HSN code.
    """)

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Records", len(df))

    if not df.empty and "verification_status" in df:
        verified = (
            df["verification_status"].astype(str)
            .str.strip().str.lower() == "verified"
        ).sum()
    else:
        verified = 0

    c2.metric("Verified Products", int(verified))
    c3.metric("Database", "CSV")

    st.subheader("Application Features")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        - 🔍 Product Name Search
        - 🔢 HSN Code Search
        - 📋 Product Description
        - 📊 GST Rate Information
        """)

    with col2:
        st.markdown("""
        - 🧮 GST Calculator
        - 🏷️ Tax Classification
        - 📁 CSV Download
        - 📚 Official References
        """)

    st.warning(
        "Only records marked Verified with official evidence "
        "are displayed as confirmed GST information."
    )

# PRODUCT SEARCH
elif page == "Product Search":

    st.header("🔍 Search GST Information")

    search_type = st.radio(
        "Search By",
        ["Product Name", "HSN Code"],
        horizontal=True
    )

    query = st.text_input(
        "Enter Product Name or HSN Code",
        placeholder="Example: Enter a product name or code"
    )

    if st.button("Search", type="primary"):

        if not query.strip():
            st.warning("Please enter a search value.")

        elif df.empty:
            st.error("GST database is currently empty.")
            st.info(
                "Add officially verified product records "
                "to gst_data.csv first."
            )

        else:
            if search_type == "Product Name":

                results = df[
                    df["product_name"].astype(str).str.contains(
                        query.strip(),
                        case=False,
                        na=False,
                        regex=False
                    )
                ]

            else:

                results = df[
                    df["hsn_code"].astype(str).str.strip()
                    == query.strip()
                ]

            if results.empty:
                st.error("No matching product found.")

            else:
                for _, row in results.iterrows():

                    st.divider()

                    st.subheader(
                        str(row.get("product_name", ""))
                    )

                    status = str(
                        row.get("verification_status", "")
                    ).strip().lower()

                    if status != "verified":

                        st.warning(
                            "This product is not officially verified. "
                            "Do not rely on its GST rate or HSN."
                        )

                        st.write(
                            "Verification Status:",
                            row.get("verification_status", "Pending")
                        )

                        st.write(
                            "Remarks:",
                            row.get("remarks", "")
                        )

                        continue

                    col1, col2 = st.columns(2)

                    with col1:
                        st.write(
                            "**Description:**",
                            row.get("description", "")
                        )

                        st.write(
                            "**HSN Code:**",
                            row.get("hsn_code", "")
                        )

                        st.write(
                            "**Category:**",
                            row.get("category", "")
                        )

                        st.write(
                            "**Composition:**",
                            row.get("composition", "")
                        )

                    with col2:

                        st.write(
                            "**CGST:**",
                            str(row.get("cgst_rate", "")) + "%"
                        )

                        st.write(
                            "**SGST:**",
                            str(row.get("sgst_rate", "")) + "%"
                        )

                        st.write(
                            "**IGST:**",
                            str(row.get("igst_rate", "")) + "%"
                        )

                        st.write(
                            "**Cess:**",
                            str(row.get("cess_rate", "")) + "%"
                        )

                        st.write(
                            "**Tax Status:**",
                            row.get("tax_status", "")
                        )

                    st.write(
                        "**Official Notification:**",
                        row.get("notification_number", "")
                    )

                    st.write(
                        "**Effective From:**",
                        row.get("effective_from", "")
                    )

                    source = str(row.get("source_url", "")).strip()

                    if source.startswith("https://") or source.startswith("http://"):
                        st.link_button(
                            "View Official Source",
                            source
                        )
                    else:
                        st.write("Official Source:", row.get("official_source", ""))

                    st.success("Official verification recorded.")

                if not results.empty:

                    st.download_button(
                        "⬇️ Download Search Results",
                        data=results.to_csv(index=False).encode("utf-8"),
                        file_name="gst_search_results.csv",
                        mime="text/csv"
                    )

# CATEGORY BROWSING
elif page == "Category Browsing":

    st.header("🏷️ Browse Products by Category")

    if df.empty or "category" not in df.columns:

        st.warning("No product categories available.")

    else:

        categories = sorted([
            str(x) for x in df["category"].unique()
            if str(x).strip()
        ])

        if not categories:
            st.info("Add product categories to your database.")

        else:

            selected = st.selectbox(
                "Select Category",
                categories
            )

            category_data = df[
                df["category"].astype(str) == selected
            ]

            st.dataframe(
                category_data[
                    ["product_name", "description",
                     "hsn_code", "tax_status",
                     "verification_status"]
                ],
                use_container_width=True
            )

# GST CALCULATOR
elif page == "GST Calculator":

    st.header("🧮 GST Calculator")

    st.write(
        "Enter a GST rate only after verifying it from "
        "the applicable official notification."
    )

    amount = st.number_input(
        "Enter Taxable Product Value (₹)",
        min_value=0.0,
        value=1000.0,
        step=100.0
    )

    rate = st.number_input(
        "Enter GST Rate (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.5
    )

    supply = st.radio(
        "Supply Type",
        ["Intra-State", "Inter-State"]
    )

    if st.button("Calculate GST", type="primary"):

        total_tax = amount * rate / 100

        if supply == "Intra-State":
            cgst = total_tax / 2
            sgst = total_tax / 2
            igst = 0

        else:
            cgst = 0
            sgst = 0
            igst = total_tax

        st.divider()

        a, b = st.columns(2)

        with a:
            st.metric("Original Value", f"₹{amount:,.2f}")
            st.metric("CGST", f"₹{cgst:,.2f}")
            st.metric("SGST", f"₹{sgst:,.2f}")

        with b:
            st.metric("IGST", f"₹{igst:,.2f}")
            st.metric("Total GST", f"₹{total_tax:,.2f}")

        st.success(
            f"Final Amount: ₹{amount + total_tax:,.2f}"
        )

        st.caption(
            "Illustrative calculation. Actual tax treatment, "
            "cess and applicable conditions must be checked separately."
        )

# ABOUT PROJECT
elif page == "About Project":

    st.header("📚 About the Project")

    st.write("""
    Project Name: GST Rate Finder Application

    Course: BBA FinTech

    Technology:
    - Python
    - Pandas
    - Streamlit
    - CSV Database
    - GitHub
    - Streamlit Community Cloud

    Main Objective:

    To develop a user-friendly application that helps users
    search products by name or HSN code and understand
    applicable GST classification and rates.
    """)

    st.subheader("Official Government Sources")

    st.markdown("""
    - [CBIC GST Rates](https://cbic-gst.gov.in/hindi/gst-goods-services-rates.html)
    - [CBIC Tax Information Portal](https://taxinformation.cbic.gov.in/)
    - [GST Council](https://www.gstcouncil.gov.in/)
    - [India Code](https://www.indiacode.nic.in/)
    """)

    st.subheader("Educational Disclaimer")

    st.warning("""
    This application is developed for educational and
    informational purposes.

    GST rates and HSN classifications may change through
    government notifications and amendments.

    Always verify the latest applicable official notification
    before using the information for commercial or tax purposes.

    This application is not a substitute for professional
    tax or legal advice.
    """)

st.sidebar.divider()
st.sidebar.caption("Developed for BBA FinTech Practical Project")
