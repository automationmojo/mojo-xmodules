
from mojo.xmods.interfaces.icommandcontext import ICommandContext
from mojo.xmods.landscaping.landscapedeviceextension import LandscapeDeviceExtension

class SerialAgentBase(LandscapeDeviceExtension, ICommandContext):
    """
    """
    def __init__(self):
        LandscapeDeviceExtension.__init__(self)
        return