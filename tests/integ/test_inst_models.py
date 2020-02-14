import numpy
import pandas
from fbprophet import Prophet
from pmdarima import AutoARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAXResultsWrapper

from hts.model.p import FBProphetModel
from hts.model.ar import AutoArimaModel, SarimaxModel
from hts.model import TimeSeriesModel


def test_instantiate_fb_model_uv(uv_tree):
    fb = FBProphetModel(
        node=uv_tree
    )
    assert isinstance(fb, TimeSeriesModel)
    fb = FBProphetModel(
        node=uv_tree,
        capacity_max=1
    )
    assert isinstance(fb, TimeSeriesModel)
    fb = FBProphetModel(
        node=uv_tree,
        capacity_min=1
    )
    assert isinstance(fb, TimeSeriesModel)


def test_instantiate_fb_model_mv(mv_tree):
    fb = FBProphetModel(
        node=mv_tree
    )
    assert isinstance(fb, TimeSeriesModel)


def test_fit_predict_fb_model_uv(uv_tree):
    fb = FBProphetModel(
        node=uv_tree
    )
    fb.fit()
    assert isinstance(fb.model, Prophet)
    fb.predict(uv_tree)
    assert isinstance(fb.forecast, pandas.DataFrame)
    assert isinstance(fb.residual, numpy.ndarray)
    assert isinstance(fb.mse, float)


def test_fit_predict_ar_model_uv(uv_tree):
    ar = AutoArimaModel(
        node=uv_tree,

    )
    ar.fit(max_iter=1)
    assert isinstance(ar.model, AutoARIMA)
    ar.predict(uv_tree)
    assert isinstance(ar.forecast, numpy.ndarray)
    assert isinstance(ar.residual, numpy.ndarray)
    assert isinstance(ar.mse, float)


def test_fit_predict_sarimax_model_uv(uv_tree):
    sar = SarimaxModel(
        node=uv_tree,
        max_iter=1,
    )
    fitted_sar = sar.fit()
    assert isinstance(fitted_sar, SARIMAXResultsWrapper)
    sar.predict(uv_tree)
    assert isinstance(sar.forecast, numpy.ndarray)
    assert isinstance(sar.residual, numpy.ndarray)
    assert isinstance(sar.mse, float)



