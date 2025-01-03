import pandas as pd
import streamlit as st

# Load dataset from the uploaded file
data_cleaned = pd.read_csv("C:/Users/Yuval/Desktop/SEM-5/Vittles/CopiedFile.csv")

# Function to recommend recipes
def recommend_recipes(user_input, time_filter, top_n=5):
    filtered_data = data_cleaned.copy()
    for key, value in user_input.items():
        if key in filtered_data.columns and value:
            filtered_data = filtered_data[filtered_data[key].str.contains(value, case=False, na=False)]
    if time_filter['prep_time'] is not None:
        filtered_data = filtered_data[filtered_data['prep_time (in mins)'] <= time_filter['prep_time']]
    if time_filter['cook_time'] is not None:
        filtered_data = filtered_data[filtered_data['cook_time (in mins)'] <= time_filter['cook_time']]
    recommended = filtered_data.sort_values(by='rating', ascending=False)
    return recommended.head(top_n)

# Streamlit UI
st.title("Recipe Recommendation System with Images")

st.sidebar.header("Select Your Preferences")

# Dropdowns for user input
cuisine = st.sidebar.selectbox("Select Cuisine", options=[''] + data_cleaned['cuisine'].dropna().unique().tolist())
diet = st.sidebar.selectbox("Select Diet", options=[''] + data_cleaned['diet'].dropna().unique().tolist())
course = st.sidebar.selectbox("Select Course", options=[''] + data_cleaned['course'].dropna().unique().tolist())

# Sliders for time filters
max_prep_time = st.sidebar.slider("Maximum Prep Time (mins)", min_value=0, max_value=60, value=60)
max_cook_time = st.sidebar.slider("Maximum Cook Time (mins)", min_value=0, max_value=60, value=60)

user_preferences = {'cuisine': cuisine, 'diet': diet, 'course': course}
time_filters = {'prep_time': max_prep_time, 'cook_time': max_cook_time}

if st.sidebar.button("Recommend Recipes"):
    recommendations = recommend_recipes(user_preferences, time_filters)
    if not recommendations.empty:
        st.write("Top Recommendations Based on Your Preferences:")
        
        # Display detailed recipe information in a separate section
        for _, row in recommendations.iterrows():
            st.markdown(f"<h2 id='recipe-{row.name}'>{row['name']}</h2>", unsafe_allow_html=True)
            st.image(row['image_url'], caption=row['name'], use_column_width=True)
            st.write(f"**Cuisine:** {row['cuisine']}")
            st.write(f"**Diet:** {row['diet']}")
            st.write(f"**Course:** {row['course']}")
            st.write(f"**Prep Time:** {row['prep_time (in mins)']} mins")
            st.write(f"**Cook Time:** {row['cook_time (in mins)']} mins")
            st.write(f"**Rating:** {row['rating']}/10")
            st.write(f"**Description:** {row['description']}")
            st.write(f"**Ingredients:** {row['ingredients_name']}")
            st.write(f"**Instructions:** {row['instructions']}")
            st.markdown("---")
    else:
        st.write("No recipes found matching your preferences.")
