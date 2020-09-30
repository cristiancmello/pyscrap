# pyscrap
Python Web Scraping Environment and Examples

## Requirements

* Mozilla Firefox 81.0 or above

## Setup

### X Server

```bash
export DISPLAY=$(awk '/nameserver / {print $2; exit}' /etc/resolv.conf 2>/dev/null):0
export LIBGL_ALWAYS_INDIRECT=1
```

## Conda Environment

### Create

```bash
conda env create --file environment.yml
```

### Activation/Deactivation

```bash
# for activation
conda activate pyscrapenv

# for deactivation
conda deactivate
```

### Update Packages and configurations

```bash
conda env update --file environment.yml
```

### Remove 

```bash
conda remove --name pyscrapenv --all
```