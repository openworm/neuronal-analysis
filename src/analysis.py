"""
Analyzer is for creating data analysis pipelines.
It integrates with experiment_management so each step in the analysis
of data can be annotated, etc.

If the routines implemented by Analyzer aren't suitable enough
for what you are doing, Analyzer also allows for the creation of
custom pipelines with the same annotation capabilities as native ones.

Data analysis pipelines should be easily composable,
modularizable, and shareable. Analyzer makes this standardized for
everything OpenWorm.

Additionally, once pipelines are composable they become machine-composable.
Such capabilities will be invaluable if we want to develop complex auto-experimentation
software.

"""
import timeseries as ts


class Analyzer(ts):


    def cross_correlate(timeseriesA, timeseriesB):
        if not timeseriesA.shape == timeseriesB.shape:
            raise Error('Invalid matrix dimensions')

        if not timeseriesA.neurons == timeseriesB.neurons:
            raise Error('Must be on the same neurons to correlate')

        a = timeseriesA.timeseries
        b = timeseriesB.timeseriesB

        dot = np.dot(a,b.T)

        leaves = sch.leaves_list(sch.linkage(dot))
