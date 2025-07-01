import streamlit as st
import pandas as pd

st.title("📊 ISW Grade Tracker")

# Upload file
uploaded_file = st.file_uploader("📤 Upload your Excel grade list", type=["xlsx"])

if uploaded_file:
    # Load uploaded Excel file
    try:
        df = pd.read_excel(uploaded_file)
        # Check required columns exist
        required_cols = {"Course Name", "Grade", "EC"}
        if not required_cols.issubset(df.columns):
            st.error("❌ Excel must contain columns: 'Course Name', 'Grade', 'EC'")
        else:
            st.success("✅ File uploaded and read successfully.")

            st.subheader("📘 Current Courses")
            st.dataframe(df)

            # Calculate weighted average
            def calculate_weighted_average(data):
                weighted_sum = (data["Grade"] * data["EC"]).sum()
                total_ec = data["EC"].sum()
                return weighted_sum / total_ec if total_ec > 0 else 0

            current_avg = calculate_weighted_average(df)
            st.metric("🎓 Current Weighted Average", f"{current_avg:.2f}")

            st.divider()

            # Add new courses
            st.subheader("➕ Add New Courses")
            num_courses = st.number_input("How many courses do you want to add?", min_value=1, max_value=20, value=1, step=1)

            new_courses = []

            with st.form("multi_course_form"):
                for i in range(num_courses):
                    st.markdown(f"**Course {i+1}**")
                    col1, col2, col3 = st.columns([4, 2, 2])
                    with col1:
                        name = st.text_input(f"Course name {i+1}", key=f"name_{i}")
                    with col2:
                        grade = st.number_input(f"Grade {i+1}", min_value=1.0, max_value=10.0, step=0.1, key=f"grade_{i}")
                    with col3:
                        ec = st.number_input(f"EC {i+1}", min_value=0.5, max_value=30.0, step=0.5, key=f"ec_{i}")
                    new_courses.append({"Course Name": name, "Grade": grade, "EC": ec, "Category": "User Added"})

                submitted = st.form_submit_button("Add and Recalculate")

            if submitted:
                new_df = pd.DataFrame(new_courses)
                df = pd.concat([df, new_df], ignore_index=True)

                updated_avg = calculate_weighted_average(df)
                st.success(f"✅ Courses added! New weighted average: **{updated_avg:.2f}**")

                st.subheader("📘 Updated Course List")
                st.dataframe(df)

    except Exception as e:
        st.error(f"❌ Failed to read Excel file: {e}")
else:
    st.info("Please upload your Excel grade list to begin.")
