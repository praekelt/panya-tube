import unittest

from tube.models import ClipBase
class ClipBaseTestCase(unittest.TestCase):
    def test_duration_as_hours_minute_seconds(self):
        
        # 0 duration. All should be 0.
        clip_base = ClipBase(duration=0)
        result = clip_base.duration_as_hours_minute_seconds
        self.failUnless(result['hours']==0, result)
        self.failUnless(result['minutes']==0, result)
        self.failUnless(result['seconds']==0, result)
        
        # Random tests. XXX: Flesh out with considered cases.
        clip_base = ClipBase(duration=3660)
        result = clip_base.duration_as_hours_minute_seconds
        self.failUnless(result['hours']==1, result)
        self.failUnless(result['minutes']==1, result)
        self.failUnless(result['seconds']==0, result)
        
        clip_base = ClipBase(duration=3665)
        result = clip_base.duration_as_hours_minute_seconds
        self.failUnless(result['hours']==1, result)
        self.failUnless(result['minutes']==1, result)
        self.failUnless(result['seconds']==5, result)
        
        clip_base = ClipBase(duration=74564376)
        result = clip_base.duration_as_hours_minute_seconds
        self.failUnless(result['hours']==20712, result)
        self.failUnless(result['minutes']==19, result)
        self.failUnless(result['seconds']==36, result)
