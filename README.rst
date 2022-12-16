=====
Swype
=====


Wave-Pay is a Python package that seamlessly allow merchants accept payments
on their Python based web apps.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Install Swype::

    pip install swype

2. It is preferred that you store your API Keys as an environment variable then import Wave gateway instance and instantiate::

    from swype.core import Swype
    swype = Swype(secret_key="<YOUR_SECRET_KEY>", public_key="<YOUR_PUBLIC_KEY>")

3. start using the API::

    gateway = Swype.gateway()
    transaction = gateway.Card.initiate("<PAYLOAD>")

