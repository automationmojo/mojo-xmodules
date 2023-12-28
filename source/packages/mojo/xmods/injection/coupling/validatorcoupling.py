from typing import Any

from mojo.errors.exceptions import NotOverloadedError

class ValidatorCoupling:
    """
        Base type for Validator objects used to verify return types of validator factory methods.
    """

    def attach_to_test(self, testscope: Any, suffix: str):
        """
            The 'attach_to_test' method is called by the sequencer in order to attach the validator to its partner
            test scope.
        """
        raise NotOverloadedError("'ValidatorCoupling' derived objects must overload the 'attach_to_test' method.")