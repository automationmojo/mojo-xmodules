
import unittest


from mojo.xmods.xfeature import FeatureAttachedObject, FeatureTag

class Hardware(FeatureTag):
    class Processor(FeatureTag):
        class DualCore(FeatureTag):
            "Dual core processor is attached"
    class Connectors(FeatureTag):
        class HDMI(FeatureTag):
            class Micro(FeatureTag):
                "Micro HDMI connector attached."

class Missing(FeatureTag):
    class Blah(FeatureTag):
        "The 'Blah' feature"

class TestObject(FeatureAttachedObject):

    FEATURE_TAGS = [
        Hardware.Processor.DualCore,
        Hardware.Connectors.HDMI.Micro
    ]


class FeatureAttachmentTests(unittest.TestCase):

    def setUp(self) -> None:
        self.testobj = TestObject()
        return

    def test_feature_tag_str(self):
        sr = str(Hardware.Processor.DualCore)
        assert sr == "hardware/processor/dualcore", f"UnExpected Feature Tag conversion to str sr={sr}."
    
    def test_feature_tag_repr(self):
        sr = repr(Hardware.Processor.DualCore)
        assert sr == "'hardware/processor/dualcore'", f"UnExpected Feature Tag conversion to str sr={sr}."

    def test_has_all_feature(self):
        check_features = [
            Hardware.Processor.DualCore,
            Hardware.Connectors.HDMI.Micro
        ]
        result = self.testobj.has_all_features(check_features)
        assert result, "has_all_features: should have found {}".format(check_features)

        check_features = [
            Hardware.Processor.DualCore,
            Missing.Blah
        ]
        result = self.testobj.has_all_features(check_features)
        assert not result, "has_all_features: should have not found {}".format(Missing.Blah)


    def test_has_any_feature(self):
        check_features = [
            Hardware.Processor.DualCore,
            Missing.Blah
        ]
        result = self.testobj.has_any_feature(check_features)
        assert result, "has_any_feature: should have found {}".format(Hardware.Processor.DualCore)
    
    def test_has_feature(self):
        result = self.testobj.has_feature(Hardware.Processor.DualCore)
        assert result, "has_feature: should have found {}".format(Hardware.Processor.DualCore)
        
        result = self.testobj.has_feature(Hardware.Connectors.HDMI.Micro)
        assert result, "has_feature: should have found {}".format(Hardware.Processor.DualCore)


if __name__ == '__main__':
    unittest.main()
