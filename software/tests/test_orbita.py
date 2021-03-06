import pytest
import numpy as np

from pyquaternion import Quaternion
from scipy.spatial.transform import Rotation as R

from mockup import mock_luos_io

mock_luos_io()

from reachy.io import SharedLuosIO  # noqa: E402
from reachy.parts.motor import OrbitaActuator  # noqa: E402


def rot(axis, deg):
    return R.from_euler(axis, np.deg2rad(deg)).as_dcm()


def test_orbita_goto():
    luos_io = SharedLuosIO.with_gate('gate', '')
    luos_disks_motor = luos_io.find_orbital_disks()

    config = {
        'Pc_z': [0, 0, 25],
        'Cp_z': [0, 0, 0],
        'R': 36.7,
        'R0': rot('z', 60),
        'pid': [8, 0.035, 0],
        'reduction': 77.35,
        'wheel_size': 62,
        'encoder_res': 3,
    }

    orb = OrbitaActuator('', 'bob', luos_disks_motor, **config)

    with pytest.raises(TypeError):
        orb.goto(Quaternion([1, 0, 0, 0]), 1, False)

    with pytest.raises(ValueError):
        orb.goto([1, 0, 0, 0], 1, False)

    with pytest.raises(ValueError):
        orb.goto([1, 0], 1, False)
