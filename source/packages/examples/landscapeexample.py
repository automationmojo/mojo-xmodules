
from mojo.xmods.landscaping.landscapeparameters import LandscapeActivationParams
from mojo.xmods.landscaping.landscape import startup_landscape

def landscape_example_main():

    activation_params = LandscapeActivationParams()

    startup_landscape(activation_params=activation_params)

    return

if __name__ == "__main__":
    landscape_example_main()
