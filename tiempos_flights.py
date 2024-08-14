"""Import libraries"""
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
    
    def filter_data_by_year(self, data: pd.DataFrame, year: int) -> pd.DataFrame:
        """
        Filters data by the given year.

        Parameters:
        data (pd.DataFrame): DataFrame.
        year (int): Year to filter the data by.

        Returns:
        pd.DataFrame: DataFrame filtered by the given year.
        """
        data['year'] = data["Partida.Prevista"].dt.year
        data_year = data[data['year'] == year].copy()
        return data_year
    
    def detect_overlap(self, sample: pd.DataFrame) -> (int, list): # type: ignore
        """
        Detects overlaps in the given DataFrame.

        Parameters:
        sample (pd.DataFrame): DataFrame with the conditioned and filtered data.

        Returns:
        int: Number of overlaps found.
        list: List of tuples with the overlap times.
        """
        overlaps: int = 0
        overlap_times: list = []

        for i in range(len(sample)):
            timestamp_i_start = sample["Partida.Real"].iloc[i]
            timestamp_i_end = sample["Chegada.Real"].iloc[i]

            # Check for overlaps only with flights that start after the current flight has ended
            for j in range(i + 1, len(sample)):
                timestamp_j_start = sample["Partida.Real"].iloc[j]
                
                # If the next flight starts after the current one ends, no overlap is possible
                if timestamp_j_start >= timestamp_i_end:
                    break
            
                timestamp_j_end = sample["Chegada.Real"].iloc[j]
                
                if timestamp_j_start < timestamp_i_end and timestamp_j_end > timestamp_i_start:
                    overlaps += 1
                    overlap_times.append((timestamp_i_start, timestamp_i_end, timestamp_j_start, timestamp_j_end))

        return overlaps, overlap_times

if __name__ == "__main__":

    file = "./data/br_flights.csv"
    year = 2015

    detector = OverlapDetector()

    # Open and process the file
    data = detector.open_file(file)
    data.dropna(inplace=True)
    
    data["Partida.Prevista"] = pd.to_datetime(data["Partida.Prevista"])
    data["Partida.Real"] = pd.to_datetime(data["Partida.Real"])
    data["Chegada.Prevista"] = pd.to_datetime(data["Chegada.Prevista"])
    data["Chegada.Real"] = pd.to_datetime(data["Chegada.Real"])

    # Filter data by year
    data_year = detector.filter_data_by_year(data, year)

    # Create a new DataFrame with the relevant columns
    sample = data_year[["Voos", "Partida.Prevista", "Partida.Real", "Chegada.Prevista", "Chegada.Real", "Situacao.Voo"]].copy()

    # Sort times
    sample.sort_values(by="Partida.Real", inplace=True)
    sample.reset_index(drop=True, inplace=True)

    # Detect overlaps
    num_overlaps, overlap_times = detector.detect_overlap(sample)

    print("Number of overlaps: ", num_overlaps)
    print("Overlap times: ", overlap_times[:10])  # Show the first 10 overlaps