import pandas as pd
from pathlib import Path

def loadcsv():
    file_path = Path.cwd() / 'data' / 'EURUSD1.csv'
    if not file_path.exists():
        raise FileNotFoundError(f"file and folder not found: {file_path}\n")

    df = pd.read_csv(
        file_path, 
        sep='\t', 
        header=None, 
        names=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'],
        usecols=['Timestamp', 'Open', 'High', 'Low', 'Close']
    )
    
    return df  # This is now explicitly 4 spaces in, clean of hidden characters
