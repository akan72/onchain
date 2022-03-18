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

Set up your Project ID for using [Alchemy's API](https://docs.alchemy.com/alchemy/) (multiple options):

- Add it to the ALCHEMY_API_KEY variable in `onchain/config.py`

- For use within scripts:

```{bash}
export ALCHEMY_API_KEY=<ALCHEMY_API_KEY>
```

- For use in Jupyter Notebooks

```{bash}
os.environ['ALCHEMY_API_KEY'] = '<ALCHEMY_API_KEY>'
```

Deactivate the venv when we're done:

```{bash}
deactivate
```
