#  -*- coding:utf-8 -*-

from timeseries import bcb

def pretty_print(quotation):
    markers = ["🔽", "🔼"]
    
    print("{}: {} {} {:.3f}%".format(
        quotation['index'],
        quotation['price'],
        markers[quotation['variation'] > 0],
        round(quotation['variation']*100, 3)))


if __name__ == "__main__":
    ts = bcb.BCBTimeSeriesHandler()

    usd_brl = ts.quotation(1)
    pretty_print(usd_brl)
    