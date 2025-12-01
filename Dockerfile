# Image Base With OS Dependencies 
FROM python:3.13-slim-bookworm AS python_base 
RUN apt update -qq && \ 
    apt install --no-install-recommends -y locales git curl && \ 
    apt autoclean && rm -rf /var/lib/apt/lists/* && \ 
    sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen && \ 
    dpkg-reconfigure --frontend=noninteractive locales && \ 
    useradd -m app 
ENV LC_ALL=pt_BR.UTF-8 \ 
    LANG=pt_BR.UTF-8 \ 
    LANGUAGE=pt_BR.UTF-8 \ 
    PYTHONUNBUFFERED=1 \ 
    PYTHONDONTWRITEBYTECODE=1 \ 
    PIP_NO_CACHE_DIR=1 \ 
    PIP_DISABLE_PIP_VERSION_CHECK=1 \ 
    PATH=/home/app/.local/bin:$PATH 

# Python Base Image With Dependencies 
FROM python_base AS python_deps 
USER app 
WORKDIR /home/app 
RUN pip install --user -U pip poetry && \ 
    poetry config virtualenvs.create false 
COPY pyproject.toml . 
COPY poetry.lock . 
RUN poetry install --only main 

# Image Python Production 
FROM python_deps AS python_production 
USER app 
WORKDIR /home/app 
EXPOSE 8000 
COPY app app 
COPY main.py .
