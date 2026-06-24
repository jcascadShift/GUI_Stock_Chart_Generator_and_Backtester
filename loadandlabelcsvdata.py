import sys
import pandas as pd
from pathlib import Path

def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) / relative_path

    return Path.cwd() / relative_path

def loadcsv():
    file_path =  resource_path(Path('data') / 'EURUSD1.csv')
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
