Linear and Bilinear Forms
~~~~~~~~~~~~~~~~~~~~~~~~~

FElupe requires a pre-evaluated array for the definition of a bilinear :class:`felupe.IntegralForm` object on interpolated field values or their gradients. While this has two benefits, namely a fast integration of the form is easy to code and the array may be computed in any programming language, sometimes numeric representations of analytic linear and bilinear form expressions may be easier in user-code and less error prone compared to the calculation of explicit second or fourth-order tensors. Therefore, FElupe provides a function decorator :func:`felupe.Form` as an easy-to-use high-level interface, similar to what `scikit-fem <https://github.com/kinnala/scikit-fem>`_ offers. The :func:`felupe.Form` decorator handles a field container. The form class is similar, but not identical in its usage compared to :class:`felupe.IntegralForm`. It requires a callable function (with optional arguments and keyword arguments) instead of a pre-computed array to be passed. The bilinear form of linear elasticity serves as a reference example for the demonstration on how to use this feature of FElupe. The stiffness matrix is assembled for a unit cube out of hexahedrons.

..  code-block:: python

    import felupe as fe
    
    mesh = fe.Cube(n=11)
    region = fe.RegionHexahedron(mesh)
    displacement = fe.Field(region, dim=3)
    field = fe.FieldContainer([displacement])

The bilinear form of linear elasticity is defined as

..  math::
    
    a(v, u) = \int_\Omega 2 \mu \ \delta\boldsymbol{\varepsilon} : \boldsymbol{\varepsilon} + \lambda \ \text{tr}(\delta\boldsymbol{\varepsilon}) \ \text{tr}(\boldsymbol{\varepsilon}) \ dV

with

..  math::

    \delta\boldsymbol{\varepsilon} &= \text{sym}(\text{grad}(\boldsymbol{v}))
    
    \boldsymbol{\varepsilon} &= \text{sym}(\text{grad}(\boldsymbol{u})) 
    
and implemented in FElupe closely to the analytic expression. The first two arguments for the callable *weak-form* function of a bilinear form are always arrays of field (gradients) ``(v, u)`` followed by arguments and keyword arguments. Optionally, the integration/assembly may be performed in parallel (threaded). Please note that this is only faster for relatively large systems. Contrary to :class:`felupe.IntegralForm`, :func:`felupe.Form` does not offer a Just-In-Time (JIT) compilation by Numba for integration/assembly. The weak-form function is decorated by :func:`felupe.Form` where the appropriate fields are linked to ``v`` and ``u`` along with the gradient flags for both fields. Arguments as well as keyword arguments of the weak-form may be defined inside the decorator or as part of the assembly arguments.

..  code-block:: python

    from felupe.math import ddot, trace, sym
    
    @fe.Form(v=field, u=field, grad_v=[True], grad_u=[True], kwargs={"mu": 1.0, "lmbda": 2.0})
    def bilinearform():
        "A container for a bilinear form."
        
        def linear_elasticity(gradv, gradu, mu, lmbda):
            "Linear elasticity."
        
            de, e = sym(gradv), sym(gradu)
            return 2 * mu * ddot(de, e) + lmbda * trace(de) * trace(e)
        
        return [linear_elasticity,]

    K = bilinearform.assemble(v=field, u=field, parallel=False)