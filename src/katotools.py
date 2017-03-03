"""
KatoAnalyzer provides a comprehensive toolkit to make asking and answering
questions about the kato dataset much easier.
"""

import data_config as dc
import neurontimeseries as nts
wd = dc.kato.data()

def integrated(timeseriestype):
    allowed_series = ['deltaFOverF', 'deltaFOverF_bc','deltaFOverF_deriv']
    if not timeseriestype in allowed_series:
        raise LookupError("""
            Invalid timeseriestype passed\n
            Must be one of\n{0}
            """.format(allowed_series))
    datasets  = [ \
        nts.NeuronTimeSeries(
            timeseries=wd[i][timeseriestype],
            nnames=wd[i]['NeuronIds'])
        for i in range(5) \
        ]          
    set( datasets[0].nnames )
    return nts.NeuronTimeSeriesIntegrator(datasets)
