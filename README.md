# onchain

Experimenting with on-chain data

## Installation Instructions

Clone the repo:

```{bash}
git clone https://github.com/akan72/onchain
cd onchain
```

To set up our virtual environment for the first time, run `make install` or the following:

```{bash}
python3 -m venv env
source env/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

For future runs, we only need to execute `source env/bin/activate`.

Set up your Project ID for using Infura's API:

```{bash}
export INFURA_PROJECT_ID=<INFURA_PROJECT_ID>
```

or add it to the INFURA_PROJECT_ID variable in `onchain/config.py`

Deactivate the venv when we're done:

```{bash}
deactivate
```
