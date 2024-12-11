import mysql.connector
import streamlit as st
import pandas as pd
from PIL import Image
import time
import matplotlib.pyplot as plt
import altair as alt
import seaborn as sns

# Database connection details
def connect_to_db():
    return mysql.connector.connect(
        host='localhost',       
        user='root',       
        password='',  
        database='sportradar'    
    )

st.set_page_config(page_title="Competitor Dashboard", layout="wide")

# Sidebar navigation
menu = st.sidebar.radio(
    "Navigate",
    ("Home","Competitor Details", "Rank Range", "Country Filter", "Competition Type", "Category", "Venues by Country","Leadership Board")
)
# Home page coding

if menu == "Home":
    st.title('Tennis Rankings:tennis:')
    st.divider()
    image = Image.open('C:/Users/Merlin/Downloads/tennis_img.webp')
    resized_image = image.resize((900, 300))  # Set width and height
    st.image(resized_image)
    #st.image('C:/Users/Merlin/Downloads/tennis_img.webp',caption="Responsive and Custom Width", width=400,height=100, use_container_width=False)
    st.write("""**Tennis** is a popular sport played between two individuals (singles) or two teams of two players each (doubles),
 where the objective is to hit a ball over a net into the opponent's side of the court in such a way that they cannot return it within the rules of the game.
""")
    st.subheader("Basic Overview:")
    st.write("**Players**: Tennis can be played as a singles game (one player per side) or as a doubles game (two players per side).")
    st.write("**Court**: The game is typically played on a rectangular court divided by a net. The surface of the court can be made of grass, clay, or hard materials, each of which affects the style of play.")
    st.write("**Equipment**: Players use a racket to hit a rubber ball. Tennis rackets are lightweight and designed for a strong, controlled grip, while the ball is typically made of rubber covered with felt.")
    st.subheader("Objective of the Game:")
    st.write("""The goal in tennis is to win points by hitting the ball in such a way that your opponent cannot return it. 
         A match is played in a series of games, and a game is won by the first player to score four points, 
         with a two-point advantage. Matches are divided into sets, and typically, 
         the player who wins six games (with at least a two-game advantage) wins the set.
          A match can be played as a best-of-three or best-of-five sets, depending on the tournament rules. """)
    st.subheader("Key Rules:")
    st.write("**1** **Scoring**: Tennis uses a unique scoring system: 15, 30, 40, and game point. If both players reach 40, it's called a 'deuce.' After deuce, a player must win two consecutive points to win the game.")
    st.write("**2** **Serving**: The server must stand behind the baseline and serve the ball into the diagonal service box. Players alternate serves every game.")
    st.write("**3** **Rallies**: A rally begins when the ball is served, and players hit the ball back and forth, attempting to outmaneuver each other by making their shots difficult to return.")
    st.write("**4** **Faults**: If the ball lands outside the designated playing area or if the player fails to return it correctly, it results in a fault or loss of point.")
    st.subheader("Types of Tennis:")
    st.write("**Singles**: One-on-one match between two players.")
    st.write("**Doubles**: A match between two teams of two players each, requiring more coordination and teamwork.")

    st.video("C:/Users/Merlin/Downloads/tennisvideo.mp4")

# competitor Details coding

elif menu == "Competitor Details":
    st.title("Competitor Details")
    st.divider()
    st.write("**Select a competitor from the sidebar to view their details.**")
    
    def get_selectbox_options():
        conn = connect_to_db()
        cursor = conn.cursor()
# SQL query to fetch name  from a competitors table
        cursor.execute("select name from competitors order by name ASC")
        options = [row[0] for row in cursor.fetchall()]

        cursor.close()
        conn.close()

        return options
# Function to execute the SQL query based on the selected option
    def execute_query_for_selection(selected_option):
        conn = connect_to_db()
        cursor = conn.cursor()

# SQL query to fetch data based on the selected option
        query = "select co.name,cr.rank,cr.movement,cr.points,cr.competitions_played,co.country from competitors co join competitor_rankings cr on cr.competitor_id=co.competitor_id where name = %s"
        cursor.execute(query, (selected_option,))  
        results = cursor.fetchall()

        df = pd.DataFrame(results, columns=['name', 'rank', 'movement', 'points', 'competitions_played', 'country']) 
        cursor.close()
        conn.close()
        return df
# Get options for the selectbox
    options = get_selectbox_options()

# Show the selectbox in the UI
    selected_option = st.sidebar.selectbox("Select Competitor Name", options)
# If an option is selected, execute the SQL query
    if selected_option:
        st.write(f"**Details of competitor**: {selected_option}")
        data = execute_query_for_selection(selected_option)
        st.write(data)

# coding for rank range

elif menu == "Rank Range":

    progress = st.progress(0)      # time loading
    for i in range(10):
        time.sleep(0.1)
        progress.progress((i + 1) * 100 // 10)
    
    st.title("Competitor Rank Range")
    st.divider()
    def execute_query_for_rank_range(rank_range):
        conn = connect_to_db()
        cursor = conn.cursor()

# SQL query to fetch data based on the selected option

        query_rank = "select cr.rank,co.name,cr.movement,cr.points,cr.competitions_played,co.country from competitor_rankings cr join competitors co on cr.competitor_id=co.competitor_id where rank between %s and %s order by rank"
        cursor.execute(query_rank, (rank_range[0], rank_range[1]))  # Pass the first and second values of the tuple
        rank_results = cursor.fetchall()

        df_rank = pd.DataFrame(rank_results, columns=['rank', 'name', 'movement', 'points', 'competitions_played', 'country'])  

        cursor.close()
        conn.close()

        return df_rank
    rank_range = st.sidebar.slider("Rank Range", min_value=1, max_value=500, value=(1, 500), step=1)
# If an option is selected, execute the SQL query
    if rank_range:
        st.write(f"**Details of rank range**: {rank_range}")
        rank_data = execute_query_for_rank_range(rank_range)
        st.write(rank_data)
    
# scatter plot for rank and competition played
    plot=sns.relplot(x='rank', y='competitions_played', data=rank_data, kind="scatter")
    fig = plot.fig
    st.pyplot(fig)


# players details based on country
elif menu == "Country Filter":
    st.title("Country Filter")
    st.divider()
    
    def get_country_selectbox_options():
        conn = connect_to_db()
        cursor = conn.cursor()
# SQL query to fetch unique country names from a competitors table
        cursor.execute("SELECT DISTINCT country from competitors order by country asc")
        country_options = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return country_options


# Function to execute the SQL query based on the selected option
    def execute_query_for_country_selection(selected_country_options):
        conn = connect_to_db()
        cursor = conn.cursor()

# SQL query to fetch data based on the selected option
        country_query = "SELECT count(name) as Total_no_of_competitors,(points) as Average_points,co.Country from competitor_rankings cr join competitors co on cr.competitor_id=co.competitor_id where country = %s"
        cursor.execute(country_query, (selected_country_options,)) 
        country_results = cursor.fetchall()
        country_df = pd.DataFrame(country_results, columns=['Total_no_of_competitors', 'Average_points', 'Country']) 
    
        cursor.close()
        conn.close()
        return country_df

    country_options = get_country_selectbox_options()

    selected_country_options = st.sidebar.selectbox("Select Country", country_options)
# If an option is selected, execute the SQL query
    if selected_country_options:
        st.write(f"**Details of country**: {selected_country_options}")
        country_data = execute_query_for_country_selection(selected_country_options)
        st.write(country_data)

        conn = connect_to_db()
        cursor = conn.cursor()
# SQL query to fetch details of competitors based on country selection
        details_query ="SELECT co.name,cr.points,co.Country from competitor_rankings cr join competitors co on cr.competitor_id=co.competitor_id where country = %s"
        cursor.execute(details_query, (selected_country_options,))  
        details_results = cursor.fetchall()
        details_df = pd.DataFrame(details_results, columns=['name', 'points', 'Country']) 
        st.write(details_df)

        cursor.close()
        conn.close()
# competition type (single,double,mixed)
elif menu == "Competition Type":
# time loading   
    progress = st.progress(0)
    for i in range(10):
        time.sleep(0.1)
        progress.progress((i + 1) * 100 // 10)

    st.header("Competition Type")
    st.divider()

    def execute_query_for_competition_type(competition_type):
        conn = connect_to_db()
        cursor = conn.cursor()

# SQL query to fetch data based on the selected option
        query_type = "select competition_id,competition_name,type from competitions where type = %s limit 200"
        cursor.execute(query_type, (competition_type,)) 
        type_results = cursor.fetchall()

        df_type = pd.DataFrame(type_results, columns=['competition_id', 'competition_name', 'type']) 

        cursor.close()
        conn.close()

        return df_type
    competition_type = st.sidebar.radio("Competition Type",['Singles','Doubles','mixed'])
# If an option is selected, execute the SQL query
    if competition_type:
        st.write(f"**Competition Type**: {competition_type}")
        type_data = execute_query_for_competition_type(competition_type)
        st.write(type_data)

# competitions based on category
elif menu == "Category":
    st.header("Category")
    st.divider()
    
    def get_category_options():
        conn = connect_to_db()
        cursor = conn.cursor()
# SQL query to fetch unique categories from a table
        cursor.execute("SELECT category_name as category from categories")
        cetegory = [row[0] for row in cursor.fetchall()]

        cursor.close()
        conn.close()

        return cetegory
# Function to execute the SQL query based on the selected option
    def execute_query_for_category(category_option):
        conn = connect_to_db()
        cursor = conn.cursor()

# SQL query to fetch data based on the selected option
        category_query = "select co.competition_name as competition from competitions co JOIN categories ca on co.category_id=ca.category_id where category_name= %s "
        cursor.execute(category_query, (category_option,)) 
        category_results = cursor.fetchall()

        category_df = pd.DataFrame(category_results, columns=['competition']) 
        cursor.close()
        conn.close()
        return category_df
# Get options for the selectbox
    category_options = get_category_options()

# Show the selectbox in the UI
    category_option = st.sidebar.selectbox("Select Category", category_options)
# If an option is selected, execute the SQL query
    if category_option:
        st.write(f"**Details of category**: {category_option}")
        category_data = execute_query_for_category(category_option)
        st.write(category_data)

# details of venues in all country
elif menu == "Venues by Country":
    st.header("Venues by Country")
    st.divider()
# time loading
    progress = st.progress(0)
    for i in range(10):
        time.sleep(0.1)
        progress.progress((i + 1) * 100 // 10)

    def get_venues_options():
        conn = connect_to_db()
        cursor = conn.cursor()
# SQL query to fetch unique country from a venues table
        cursor.execute("SELECT DISTINCT country_name from venues")
        cetegory = [row[0] for row in cursor.fetchall()]

        cursor.close()
        conn.close()

        return cetegory
# Function to execute the SQL query based on the selected option
    def execute_query_for_venue(venue_option):
        conn = connect_to_db()
        cursor = conn.cursor()

# SQL query to fetch data based on the selected option
        venue_query = "select v.venue_id,v.venue_name,c.complex_name,v.city_name from venues v join complexes c on v.complex_id=c.complex_id WHERE country_name= %s limit 500"
        cursor.execute(venue_query, (venue_option,))  # Use the selected option as a parameter
        venue_results = cursor.fetchall()

        venue_df = pd.DataFrame(venue_results, columns=['venue_id','venue_name','complex','city'])  # Adjust column names
        cursor.close()
        conn.close()
        return venue_df
# Get options for the selectbox
    venue_country_options = get_venues_options()

# Show the selectbox in the UI
    venue_option = st.sidebar.selectbox("Venues by country", venue_country_options)
# If an option is selected, execute the SQL query
    if venue_option:
        st.write(f"**Details of venues**: {venue_option}")
        venue_data = execute_query_for_venue(venue_option)
        st.write(venue_data)

# details of top 5 rank
elif menu == "Leadership Board":

    st.header("Leadership Board")
    st.divider()

    def execute_query_for_leader_board():
        conn = connect_to_db()
        cursor = conn.cursor()

# SQL query to fetch data based on the selected option
        query_leader = "select cr.rank,c.name,cr.points from competitor_rankings cr join competitors c on cr.competitor_id=c.competitor_id where cr.rank <= 5 ORDER BY cr.rank ASC,cr.points DESC"
        cursor.execute(query_leader) 
        leader_results = cursor.fetchall()

        df_leader = pd.DataFrame(leader_results, columns=['Rank', 'Name', 'Points']) 

        cursor.close()
        conn.close()

        return df_leader
    
    st.write(f"**Top 5 Rank:**")
    leader_data = execute_query_for_leader_board()
    st.write(leader_data)

# area chart for rank and points
    st.area_chart(leader_data,x='Rank',y='Points')




