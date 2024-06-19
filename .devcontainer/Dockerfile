FROM mcr.microsoft.com/devcontainers/python:3.11-bookworm

RUN python -m pip install --upgrade pip \
    && python -m pip install 'flit>=3.8.0'

ENV FLIT_ROOT_INSTALL=1

COPY pyproject.toml .
RUN touch README.md \
    && mkdir -p src/tbot \
    && python -m flit install --only-deps --deps develop \
    && rm -r pyproject.toml README.md src