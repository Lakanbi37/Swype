### **Wave Pay**

**Wave-Pay is a Python package that seamlessly allow merchants accept payments
on their Python based web apps.**

**Detailed documentation is in the "docs" directory.**

### **Quick start**

1. Install wave-pay


    pip install wave-pay

   
2. It is preferred that you store your API Keys as an environment variable then import Wave gateway instance and instantiate


    from wave_pay import WaveGateway
    wave = WaveGateway(secret_key="<YOUR_SECRET_KEY>", public_key="<YOUR_PUBLIC_KEY>")

3. start using the API


    new_transaction = wave.Card.initiate("<ENCRYPTED_PAYLOAD>")