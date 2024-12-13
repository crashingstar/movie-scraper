import os
from datetime import datetime
import pandas as pd

class IMDbRankTracker:
    def __init__(self, data_dir='imdb_data'):
        """
        Initialize data processor with a specific directory for storing data
        
        :param data_dir: Directory to store CSV files
        """
        # Create data directory if it doesn't exist
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)

    def save_to_csv(self, movies):
        """
        Save movies data to a CSV file with timestamp
        
        :param movies: List of movie dictionaries
        :return: Path to the saved CSV file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"imdb_top_movies_{timestamp}.csv"
        filepath = os.path.join(self.data_dir, filename)

        try:
            df = pd.DataFrame(movies)
            
            # Save to CSV
            df.to_csv(filepath, index=False)
        
            return filepath
        except Exception as e:
            raise

    def compare_rank_changes(self, current_movies):
        """
        Compare the rank changes of the current movies compared to the previous day's movies
        and save the rank change to a CSV file.
        
        :param current_movies: List of current movie dictionaries
        :return: Rank change results (up/down or no change)
        """
        try:
            # Get all previous CSV files
            csv_files = sorted([f for f in os.listdir(self.data_dir) if f.startswith('imdb_top_movies_') and f.endswith('.csv')])
            
            if not csv_files:
                print("No previous data found for comparison of ranks, saving current data with ranks")
                self.save_to_csv(current_movies)
                return {}

            previous_filepath = os.path.join(self.data_dir, csv_files[-1])
            previous_df = pd.read_csv(previous_filepath)
            
            current_df = pd.DataFrame(current_movies)

            previous_rank_map = {row['title']: idx for idx, row in previous_df.iterrows()}
            current_rank_map = {row['title']: idx for idx, row in current_df.iterrows()}

            rank_changes = []
            for idx, movie in current_df.iterrows():
                title = movie['title']
                if title in previous_rank_map:
                    previous_rank = previous_rank_map[title]
                    current_rank = current_rank_map[title]
                    
                    if current_rank < previous_rank:
                        rank_changes.append({'title': title, 'rank_change': 'up'})
                    elif current_rank > previous_rank:
                        rank_changes.append({'title': title, 'rank_change': 'down'})
                    else:
                        rank_changes.append({'title': title, 'rank_change': 'no change'})
                else:
                    rank_changes.append({'title': title, 'rank_change': 'new'})

            current_df['rank_change'] = current_df['title'].map(lambda title: next(change['rank_change'] for change in rank_changes if change['title'] == title))

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"imdb_top_movies_{timestamp}.csv"
            filepath = os.path.join(self.data_dir, filename)
            current_df.to_csv(filepath, index=False)

            return rank_changes

        except Exception as e:
            raise
       