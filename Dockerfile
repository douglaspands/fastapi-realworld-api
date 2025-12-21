ARG USERNAME=nonroot
ARG PYTHON_VERSION=3.14.2-slim-trixie

FROM python:${PYTHON_VERSION} AS python_base
ARG USERNAME
RUN apt update -qq && \ 
    apt install --no-install-recommends -y locales git curl && \ 
    apt autoclean && rm -rf /var/lib/apt/lists/* && \ 
    sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen && \ 
    dpkg-reconfigure --frontend=noninteractive locales && \ 
    useradd -m ${USERNAME}
ENV LC_ALL=pt_BR.UTF-8 \ 
    LANG=pt_BR.UTF-8 \ 
    LANGUAGE=pt_BR.UTF-8 \ 
    PYTHONUNBUFFERED=1 \ 
    PYTHONDONTWRITEBYTECODE=1 \ 
    PIP_NO_CACHE_DIR=1 \ 
    PIP_DISABLE_PIP_VERSION_CHECK=1 \ 
    PATH=/home/${USERNAME}/.local/bin:$PATH 

FROM python:${PYTHON_VERSION} AS requirements_gen
WORKDIR /app 
COPY pyproject.toml . 
COPY poetry.lock . 
RUN pip install poetry && \
    poetry self add poetry-plugin-export && \
    poetry export -f requirements.txt --without-hashes --output requirements.txt

FROM python_base AS python_app
ARG USERNAME
USER ${USERNAME} 
WORKDIR /home/${USERNAME} 
EXPOSE 8000 
ENV LOG_LEVEL=INFO
COPY --from=requirements_gen --chown=${USERNAME}:${USERNAME} /app/requirements.txt . 
RUN pip install --user --upgrade --no-cache-dir --requirement requirements.txt
COPY main.py .
COPY app app 
