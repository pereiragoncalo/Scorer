# syntax=docker/dockerfile:1
FROM python:3.12-bookworm@sha256:14a4933e6cef421424f7a66d89a3f4eafcbd0d90e0a822251f298e05132dc735
RUN --mount=type=secret,id=ca_bundle,required=true \
    apt-get -o Acquire::https::CaInfo=/run/secrets/ca_bundle update && \
    apt-get -o Acquire::https::CaInfo=/run/secrets/ca_bundle install -y --no-install-recommends \
      openjdk-17-jdk-headless autoconf automake libtool libtool-bin pkg-config \
      cmake ninja-build zip unzip ccache libffi-dev libssl-dev zlib1g-dev \
      libncurses-dev patch git wget && rm -rf /var/lib/apt/lists/*
RUN --mount=type=secret,id=ca_bundle,required=true \
    PIP_CERT=/run/secrets/ca_bundle python -m pip install \
      buildozer==1.5.0 setuptools==75.8.2 Cython==0.29.37 \
      virtualenv==20.36.1 packaging==26.3
RUN useradd --uid 1000 --home-dir /work/cache/user --no-create-home striker
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV GRADLE_USER_HOME=/work/cache/gradle
ENV XDG_CACHE_HOME=/work/cache/xdg
ENV ANDROID_USER_HOME=/work/cache/android-user
WORKDIR /work/source
