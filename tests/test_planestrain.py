# -*- coding: utf-8 -*-
"""
 _______  _______  ___      __   __  _______  _______ 
|       ||       ||   |    |  | |  ||       ||       |
|    ___||    ___||   |    |  | |  ||    _  ||    ___|
|   |___ |   |___ |   |    |  |_|  ||   |_| ||   |___ 
|    ___||    ___||   |___ |       ||    ___||    ___|
|   |    |   |___ |       ||       ||   |    |   |___ 
|___|    |_______||_______||_______||___|    |_______|

This file is part of felupe.

Felupe is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Felupe is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Felupe.  If not, see <http://www.gnu.org/licenses/>.

"""

import felupe as fem
import pytest


def test_planestrain():

    m = fem.Rectangle(n=6)
    r = fem.RegionQuad(m)
    f = fem.FieldsMixed(r, n=1, planestrain=True)
    u = fem.NeoHooke(mu=1, bulk=2)
    b = fem.SolidBody(u, f)
    loadcase = fem.dof.uniaxial(f, clamped=True)[-1]
    res = fem.newtonrhapson(items=[b], **loadcase)

    assert res.success


def test_planestrain_mixed():

    m = fem.Rectangle(n=6)
    r = fem.RegionQuad(m)
    f = fem.FieldsMixed(r, n=3, planestrain=True)
    u = fem.ThreeFieldVariation(fem.NeoHooke(mu=1, bulk=5000))
    b = fem.SolidBody(u, f)
    loadcase = fem.dof.uniaxial(f, clamped=True)[-1]
    res = fem.newtonrhapson(items=[b], **loadcase)

    assert res.success


if __name__ == "__main__":
    test_planestrain()
    test_planestrain_mixed()
