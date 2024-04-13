import pandas as pd 
import numpy as np
import datetime
import quandl as ql


def yields_data():
    yields = ql.get("USTREASURY/YIELD")
    return yields