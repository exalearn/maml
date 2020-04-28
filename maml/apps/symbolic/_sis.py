"""
Sure Independence Screening

https://orfe.princeton.edu/~jqfan/papers/06/SIS.pdf

"""
from typing import Optional, Dict
import logging

import numpy as np

from ._selectors import BaseSelector


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class SIS:
    """
    Sure independence screening method.
    The method consists of two steps:
        1. Screen
        2. Select

    """

    def __init__(self, gamma=0.1, selector: Optional[BaseSelector] = None,
                 verbose: bool = True):
        """
        Sure independence screening

        Args:
            gamma (float): ratio between selected features and original feature sizes
            selector (BaseSelector): selector after the screening
            verbose (bool): whether to output information along the way

        """
        self.gamma = gamma
        self.selector = selector
        self.verbose = verbose

    def run(self, x, y, select_options=None):
        """
        Run the SIS with selector
        Args:
            x (np.ndarray): MxN input data array
            y (np.ndarray): M output targets
            select_options (dict): options in the optimizations provided
                to scipy.optimize.minimize. If the selector is using cvxpy
                optimization package, this option is fed into cp.Problem.solve

        Returns: selected feature indices

        """
        screened_indices = self.screen(x, y)
        if self.verbose:
            logger.info(f"After the screening step, {len(screened_indices)}/{x.shape[1]} features remains")
        x_screen = x[:, screened_indices]

        final_selected = self.select(x_screen, y, select_options)

        if self.verbose:
            logger.info(f"After the selection step, {len(final_selected)}/{x.shape[1]} features remains")
        return screened_indices[final_selected]

    def screen(self, x, y):
        """
        Simple screening method by comparing the correlation between features
        and the target

        Args:
            x (np.ndarray): input array
            y (np.ndarray): target array

        Returns: top indices

        """
        n = x.shape[1]
        omega = x.T.dot(y)
        sorted_omega = np.argsort(omega)[::-1]
        d = int(n * self.gamma)
        top_indices = sorted_omega[:d]
        return top_indices

    def select(self, x, y, options=None):
        """
        Select features using selectors
        Args:
            x (np.ndarray): input array
            y (np.ndarray): target array
            options (dict): options for the optimization

        Returns:

        """
        return self.selector.select(x, y, options)

    def set_selector(self, selector: BaseSelector):
        """
        Set new selector
        Args:
            selector (BaseSelector): a feature selector

        Returns:

        """
        self.selector = selector



