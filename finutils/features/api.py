import pandas as pd


def MACD(ser, ema_1=12, ema_2=26, signal_line=9):
    '''Returns the MACD line and the signal line
    Args:
        ema_1: (int) window for for short-term EWMA
        ema_2: (int) window for long-term EWMA
        singal_line: (int) window for singal line EWMA
    '''
    ema_1_ser = ser.ewm(span=ema_1).mean()
    ema_2_ser = ser.ewm(span=ema_2).mean()
    macd = pd.DataFrame(ema_1_ser - ema_2_ser)
    signal = macd.ewm(span=signal_line).mean()
    df = pd.concat([macd, signal], axis=1)
    df.columns = ['MACD({}, {})'.format(ema_1, ema_2), 'Signal ({})'.format(signal_line)]
    return df
