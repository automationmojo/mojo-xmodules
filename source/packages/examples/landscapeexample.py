
import os

from mojo.xmods.landscaping.landscapeparameters import LandscapeActivationParams
from mojo.xmods.landscaping.landscape import startup_landscape

from mojo.xmods.xcollections.context import Context, ContextPaths

def landscape_example_main():

    output_dir = os.path.expanduser("~/mjr/configs/results/examples/landscaping")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    config_dir = os.path.expanduser("~/mjr/configs/landscapes")
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    landscape_files = [
        os.path.join(config_dir, "default-landscape.yaml")
    ]

    ctx = Context()
    ctx.insert(ContextPaths.CONFIG_LANDSCAPE_FILES, landscape_files)
    ctx.insert(ContextPaths.OUTPUT_DIRECTORY, output_dir)

    activation_params = LandscapeActivationParams()

    startup_landscape(activation_params=activation_params)

    return

if __name__ == "__main__":
    landscape_example_main()
