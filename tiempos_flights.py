import pandas as pd

class OverlapDetector:
    """Class to detect overlaps in a DataFrame"""
    
    def open_file(self, file: str, encoding: str = 'latin-1') -> pd.DataFrame:
        """
        Opens the file and returns a DataFrame.

        Parameters:
        file (str): Path to the file to open.
        encoding (str): File encoding format.

        Returns:
        pd.DataFrame: DataFrame with the file's data.
        """
        data: pd.DataFrame = pd.read_csv(file, encoding=encoding)
        return data
    
    def filter_data_by_year(self, data: pd.DataFrame, date_column: str, year: int) -> pd.DataFrame:
        """
        Filters data by the given year.

        Parameters:
        data (pd.DataFrame): DataFrame.
        date_column (str): The name of the column containing date information.
        year (int): Year to filter the data by.

        Returns:
        pd.DataFrame: DataFrame filtered by the given year.
        """
        data['year'] = pd.to_datetime(data[date_column]).dt.year
        data_year = data[data['year'] == year].copy()
        return data_year
    
    def detect_overlap(self, sample: pd.DataFrame, start_column: str, end_column: str) -> (int, list): # type: ignore
        """
        Detects overlaps in the DataFrame.

        Parameters:
        sample (pd.DataFrame): DataFrame with the conditioned and filtered flight data.
        start_column (str): The name of the column containing the start time.
        end_column (str): The name of the column containing the end time.

        Returns:
        int: Number of overlaps found.
        list: List of tuples with the overlap times.
        """
        overlaps: int = 0
        overlap_times: list = []

        for i in range(len(sample)):
            timestamp_i_start = sample[start_column].iloc[i]
            timestamp_i_end = sample[end_column].iloc[i]

            # Check for overlaps only with flights that start after the current flight has ended
            for j in range(i + 1, len(sample)):
                timestamp_j_start = sample[start_column].iloc[j]
                
                # If the next timestamp is outside the overlap window, break the loop
                if timestamp_j_start >= timestamp_i_end:
                    break
                
                timestamp_j_end = sample[end_column].iloc[j]
                if timestamp_j_start < timestamp_i_end and timestamp_j_end > timestamp_i_start:
                    overlaps += 1
                    overlap_times.append((timestamp_i_start, timestamp_i_end, timestamp_j_start, timestamp_j_end))

        return overlaps, overlap_times

if __name__ == "__main__":

    file = "./data/BrFlights2.csv"
    year = 2015
    date_column = "Partida.Prevista"
    start_column = "Partida.Real"
    end_column = "Chegada.Real"

    detector = OverlapDetector()

    data = detector.open_file(file)
    #data.dropna(inplace=True)
    data[date_column] = pd.to_datetime(data[date_column])
    data[start_column] = pd.to_datetime(data[start_column])
    data[end_column] = pd.to_datetime(data[end_column])

    #Data exploration:
    print("Info: ", data.info())
    print("Head: ", data.head())
    print("Describe: ", data.describe())
    
    situation = data["Situacao.Voo"].value_counts()    
    print("Situation: ", situation)
    
    company = data["Companhia.Aerea"].value_counts()
    print("Company: ", company)
    
    country_o = data["Pais.Origem"].value_counts()
    print("Country of origin: ", country_o)
    
    country_d = data["Pais.Destino"].value_counts()
    print("Country of destination: ", country_d)
    
    # Filter data by year
    data_year = detector.filter_data_by_year(data, date_column, year)

    # Create a new DataFrame with the relevant columns
    sample = data_year[["Voos", date_column, start_column, end_column, "Situacao.Voo"]].copy()

    # Sort times
    sample.sort_values(by=start_column, inplace=True)
    sample.reset_index(drop=True, inplace=True)

    # Detect overlaps
    num_overlaps, overlap_times = detector.detect_overlap(sample, start_column, end_column)

    print("Number of overlaps: ", num_overlaps)
    print("Overlap times: ", overlap_times[:10])  # Show the first 10 overlaps
