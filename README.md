# pygeek-stellar

![pygeek-stellar-logo](resources/pygeek-stellar-logo.png)

**pygeek-stellar** is a CLI Python tool to manage Stellar accounts and interact with the Stellar network. With this tool you can check account balances, check transactions history, send payments and a lot more.. everything using the terminal like a true geek! It requires Python 3.7.


## Installing

You can install from Pypi using: 

```bash
pip install -U pygeek-stellar
```

## Warning

This tool is still in development mode so it is using the Stellar Testnet by default.
Also the private key of the generated Stellar addresses is being saved in plain text in a configuration file. This is a severe security issue and it should be fixed in the future.