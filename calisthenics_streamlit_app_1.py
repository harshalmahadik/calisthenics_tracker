import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# --- Helper: Find image file automatically ---
def find_image(base_name):
    img_dir = "images"
    possible_exts = [".avif", ".webp", ".png", ".jpg", ".jpeg", ".gif"]
    for ext in possible_exts:
        path = os.path.join(img_dir, base_name + ext)
        if os.path.exists(path):
            return path
    return None

# --- Exercise details (only description; image auto-detected) ---
exercise_info = {
    "Push-ups": {"desc": "Standard push-up for chest and arms."},
    "Squats": {"desc": "Bodyweight squat for legs & glutes."},
    "Plank": {"desc": "Static hold for core activation."},
    "Lunges": {"desc": "Alternating lunge for legs & balance."},
    "Burpees": {"desc": "Full-body explosive movement."},
    "Mountain Climbers": {"desc": "Dynamic cardio and core."},
    "Pike Push-ups": {"desc": "Shoulder-focused push-up."},
    "Leg Raises": {"desc": "Targets lower abs and hip flexors."},
    "Tricep Dips": {"desc": "Bench/Chair dips for triceps."},
    "Glute Bridges": {"desc": "Glute and hamstring activation."}
}


def get_data():
    workout_schedule = pd.DataFrame({
        'Day': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        'Workout Type': ['Upper Body', 'Lower Body', 'Rest/Light Cardio', 'Full Body', 'Upper Body Focus', 'Lower Body Focus', 'Rest'],
        'Duration (min)': [30, 30, 20, 35, 30, 30, 0],
        'Primary Focus': ['Push/Pull', 'Legs/Glutes', 'Recovery', 'Compound', 'Strength', 'Power', 'Recovery']
    })

    exercises = pd.DataFrame({
        'Exercise': list(exercise_info.keys()),
        'Week 1': ['3x8-12', '3x15-20', '3x30-45s', '3x10 each leg', '3x20', '3x5', '3x5-8', '3x10-15', '3x8-12', '3x15-20'],
        'Week 4': ['3x15-20', '3x25-30', '3x60-90s', '3x15 each leg', '3x30', '3x10', '3x12-15', '3x15-20', '3x15-20', '3x25-30'],
        'Muscles': [info['desc'] for info in exercise_info.values()],
        'Difficulty': ['Beginner', 'Beginner', 'Beginner', 'Beginner', 'Beginner-Intermediate',
                       'Intermediate', 'Intermediate', 'Beginner', 'Beginner-Intermediate', 'Beginner']
    })

    # --- Day-wise meal plan ---
    meal_plan = {
        'Monday': [
            'Breakfast: Oats, milk, almonds (25g protein, 400 kcal)',
            'Lunch: Brown rice, dal, paneer, veggies (30g protein, 600 kcal)',
            'Dinner: Chapati, dal, vegetables, curd (25g protein, 500 kcal)',
        ],
        'Tuesday': [
            'Breakfast: Poha with peas, curd (20g protein, 350 kcal)',
            'Lunch: Jeera rice, rajma, salad (28g protein, 580 kcal)',
            'Dinner: Kadhi, khichdi, roasted peanuts (24g protein, 450 kcal)',
        ],
        'Wednesday': [
            'Breakfast: Moong dosa, chutney, sprouts (22g protein, 370 kcal)',
            'Lunch: Paratha, chole, buttermilk (27g protein, 600 kcal)',
            'Dinner: Idli, sambhar, paneer bhurji (25g protein, 480 kcal)',
        ],
        'Thursday': [
            'Breakfast: Peanut butter bread, milk, banana (20g protein, 400 kcal)',
            'Lunch: Rice, mixed dal, tofu curry (28g protein, 600 kcal)',
            'Dinner: Roti, palak-paneer, salad (28g protein, 520 kcal)',
        ],
        'Friday': [
            'Breakfast: Vegetable upma, curd, sprouts (18g protein, 350 kcal)',
            'Lunch: Lemon rice, dal, soya chunks (30g protein, 620 kcal)',
            'Dinner: Stuffed paratha, curd, salad (24g protein, 450 kcal)',
        ],
        'Saturday': [
            'Breakfast: Oats, fruit smoothie, peanuts (22g protein, 370 kcal)',
            'Lunch: Veg biryani, dal makhani, salad (29g protein, 590 kcal)',
            'Dinner: Whole wheat pasta, soya chilli (27g protein, 550 kcal)',
        ],
        'Sunday': [
            'Breakfast: Paneer sandwich, milk (21g protein, 340 kcal)',
            'Lunch: Mix veg curry, rice, dal (28g protein, 580 kcal)',
            'Dinner: Besan chilla, curd, vegetables (25g protein, 500 kcal)',
        ]
    }

    # --- Nutrition reference plan ---
    nutrition = pd.DataFrame({
        'Meal': ['Early Morning', 'Breakfast', 'Mid-Morning', 'Lunch', 'Pre-Workout', 'Post-Workout', 'Dinner', 'Before Bed'],
        'Food': ['Soaked almonds (10-12) + 1 glass milk',
                 'Oats with banana, nuts, protein powder',
                 'Buttermilk + handful of nuts',
                 'Brown rice + dal + paneer + vegetables',
                 'Banana + dates (2-3)',
                 'Protein shake + banana',
                 'Chapati + dal + vegetables + curd',
                 'Warm milk + soaked almonds'],
        'Protein (g)': [12, 25, 8, 30, 2, 28, 25, 10],
        'Calories': [250, 400, 150, 600, 120, 300, 500, 180]
    })
    return workout_schedule, exercises, nutrition, meal_plan


def extract_reps(rep_string):
    try:
        rep_string = rep_string.lower()
        if 'each leg' in rep_string:
            return int(rep_string.split('x')[1].split()[0])
        if 's' in rep_string:
            return int(rep_string.split('x')[1].replace('s', '').split('-')[0])
        return int(rep_string.split('x')[1].split('-')[0])
    except:
        return 0


def main():
    st.set_page_config(page_title="Calisthenics Tracker", layout="centered")
    st.title("🏋️ Calisthenics Muscle & Weight Gain Tracker (Local Image Version)")

    workout_schedule, exercises, nutrition, meal_plan = get_data()
    days = workout_schedule['Day'].tolist()
    today_idx = datetime.today().weekday() % 7

    st.subheader("Day Navigation")
    if 'current_day_idx' not in st.session_state:
        st.session_state.current_day_idx = today_idx

    col1, col2, col3 = st.columns([1,3,1])
    with col1:
        if st.button("< Previous"):
            st.session_state.current_day_idx = (st.session_state.current_day_idx - 1) % 7
    with col3:
        if st.button("Next >"):
            st.session_state.current_day_idx = (st.session_state.current_day_idx + 1) % 7

    selected_day = days[st.session_state.current_day_idx]
    st.markdown(f"### **Today: {selected_day}**")

    ws_row = workout_schedule.loc[workout_schedule['Day'] == selected_day].squeeze()
    st.info(f"**Workout Type**: {ws_row['Workout Type']} | Duration: {ws_row['Duration (min)']} min | Primary Focus: {ws_row['Primary Focus']}")

    # --- Meal Plan Section ---
    st.subheader("Today's Vegetarian Meal Plan")
    for meal in meal_plan[selected_day]:
        st.write(f"• {meal}")

    # --- Exercise Section ---
    if ws_row['Duration (min)'] == 0:
        st.success("This is a rest or recovery day! Hydrate and stretch.")
    else:
        st.subheader("Today's Recommended Exercises")
        for i, row in exercises.iterrows():
            ex = row['Exercise']
            st.markdown(f"#### {ex}")
            # Find local image (supports .avif, .webp, etc.)
            image_path = find_image(ex.replace(" ", "-")) or find_image(ex.replace(" ", "_"))
            if image_path:
                st.image(image_path, width=340, caption=exercise_info[ex]['desc'])
            else:
                st.warning(f"Image not found for: {ex}")
            st.write(f"**Start:** {row['Week 1']} | **Progress Week 4:** {row['Week 4']}")

    # --- Charts & Tables ---
    with st.expander("Show full weekly chart and nutrition plan"):
        st.write("#### Weekly Workout Duration")
        fig1, ax1 = plt.subplots(figsize=(8,3))
        ax1.bar(workout_schedule['Day'], workout_schedule['Duration (min)'], color='dodgerblue')
        st.pyplot(fig1)

        st.write("#### Exercise Progression")
        ex_week1 = [extract_reps(e) for e in exercises['Week 1']]
        ex_week4 = [extract_reps(e) for e in exercises['Week 4']]
        fig2, ax2 = plt.subplots(figsize=(10,4))
        ax2.barh(exercises['Exercise'], ex_week1, color='lightcoral', label='Week 1')
        ax2.barh(exercises['Exercise'], ex_week4, left=ex_week1, color='seagreen', label='Week 4')
        ax2.legend()
        st.pyplot(fig2)

        st.dataframe(exercises, use_container_width=True)
        st.write("#### Daily Vegetarian Nutrition Plan (Reference)")
        st.dataframe(nutrition, use_container_width=True)

        fig3, ax3 = plt.subplots(figsize=(10,3))
        ax3.bar(nutrition['Meal'], nutrition['Calories'], color='mediumorchid', label='Calories')
        ax3.bar(nutrition['Meal'], nutrition['Protein (g)'], alpha=0.5, color='limegreen', label='Protein (g)')
        ax3.legend()
        st.pyplot(fig3)

        total_calories = nutrition['Calories'].sum()
        total_protein = nutrition['Protein (g)'].sum()
        st.success(f"Total Daily Calories: {total_calories} kcal | Total Daily Protein: {total_protein} g")


if __name__ == "__main__":
    main()
