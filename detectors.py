from math import pi
import random


# Detector Materials
water = {"molecular_density": 3.343e+22, # molecules per gram (18.0153 g/mol)
         "channel_weights": {"ibd": 2, "es": 10, "o16e": 1, "o16eb": 1}
}

# liquid scintillator: approximated here as CH_2
ls = {"molecular_density": 4.293e+22, # 14.0266 g/mol
      "channel_weights": {"ibd": 2, "es": 8, "c12e": 1}
      # TODO: add interactions on carbon: {"c12nc": 1, "c12eb": 1}
}


# List of supported detector configurations
supported_detectors = ["HyperK", "SuperK", "WATCHMAN", "WATCHMAN-LS"]

class Detector(object):
    """A neutrino detector."""
    def __init__(self, name):
        self.name = name
        if name == "HyperK": # 2019 optimized design
            self.height = 6580.
            self.radius = 6480./2
            # 2018 Design Report: radius = 7080./2; height = 5480.
            self.material = water
        elif name == "SuperK":
            self.height = 3620.
            self.radius = 3368.15/2
            self.material = water
        elif name == "WATCHMAN": # arXiv:1502.01132
            self.height = 1280.
            self.radius = 1280./2
            self.material = water
        elif name == "WATCHMAN-LS":
            self.height = 1280.
            self.radius = 1280./2
            self.material = ls
        else:
            raise ValueError("Unknown detector name: %s" % name)

        # volume in cm^3, assuming cylindrical detector shape
        self.volume = pi * self.radius**2 * self.height

    def __repr__(self):
        return "Detector('%s')" % self.name

    def __setattr__(self, attr, value):
        if attr == "volume" and hasattr(self, attr):
            raise AttributeError('Volume is determined by height and radius. It cannot be changed.')
        object.__setattr__(self, attr, value)

    def generate_random_vertex(self):
        while True:
            x = random.uniform(-self.radius, self.radius)
            y = random.uniform(-self.radius, self.radius)
            if x**2 + y**2 < self.radius**2:
                break
        z = random.uniform(-self.height/2, self.height/2)
        return x, y, z
