import logging

import numpy

from hts.hierarchy import HierarchyTree
from hts._t import Model
from hts.model import TimeSeriesModel, BaseArModel

logger = logging.getLogger(__name__)

try:
    from pmdarima import AutoARIMA
except ImportError:
    logger.error('pmdarima not installed, so HierarchicalArima won\'t work. Install it with: \npip install pmdarima')


class AutoArimaModel(BaseArModel):
    def __init__(self, node: HierarchyTree, **kwargs):
        super().__init__(Model.auto_arima.name, node, **kwargs)

    def predict(self, node, steps_ahead=10, alpha=0.05):
        if self.node.exogenous:
            ex = node.item
        else:
            ex = None
        self.forecast = self.model.predict(exogenous=ex, alpha=alpha, n_periods=steps_ahead)
        in_sample_preds = self.model.predict_in_sample()
        self.residual = in_sample_preds - self._reformat(self.node.item)[self.node.key].values
        self.mse = numpy.mean(numpy.array(self.residual) ** 2)
        return self.model


class SarimaxModel(BaseArModel):
    def __init__(self, node: HierarchyTree, **kwargs):
        super().__init__(Model.sarimax.name, node, **kwargs)

    def fit(self, **fit_args) -> 'TimeSeriesModel':
        as_df = self._reformat(self.node.item)
        end = as_df[self.node.key]
        if self.node.exogenous:
            ex = as_df[self.node.exogenous]
        else:
            ex = None
        sar_model = self.model(endog=end, exog=ex, **fit_args)
        self.model = sar_model.fit(disp=0)
        return self.model

    def predict(self, node, steps_ahead=10, alpha=0.05):
        if self.node.exogenous:
            ex = node.item
        else:
            ex = None
        self.forecast = self.model.forecast(steps=steps_ahead, exog=ex).values
        in_sample_preds = self.model.get_prediction(dynamic=False, exog=ex)
        self.residual = (in_sample_preds.predicted_mean - self._reformat(self.node.item)[self.node.key].values).values
        self.mse = numpy.mean(numpy.array(self.residual) ** 2)
        return self.model


