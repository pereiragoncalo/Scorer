# syntax=docker/dockerfile:1
FROM python:3.12-slim-bookworm@sha256:935c3c5b12357a7e10caa9c1e6ca5692344d97cf229832ef584be2cec9fc03df
WORKDIR /work/source
RUN --mount=type=secret,id=ca_bundle,required=true \
    apt-get -o Acquire::https::CaInfo=/run/secrets/ca_bundle update && \
    apt-get -o Acquire::https::CaInfo=/run/secrets/ca_bundle install -y --no-install-recommends \
      openjdk-17-jdk-headless gcc g++ make autoconf automake libtool libtool-bin pkg-config \
      cmake ninja-build zip unzip ccache libffi-dev libssl-dev zlib1g-dev \
      libncurses-dev patch git wget xz-utils bzip2 curl ca-certificates && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*.deb && \
    PIP_CERT=/run/secrets/ca_bundle python -m pip install --no-cache-dir \
      buildozer==1.5.0 setuptools==75.8.2 Cython==0.29.37 \
      virtualenv==20.36.1 packaging==26.3 && \
    useradd --uid 1000 --home-dir /work/cache/user --no-create-home striker
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV GRADLE_USER_HOME=/work/cache/gradle
ENV XDG_CACHE_HOME=/work/cache/xdg
ENV ANDROID_USER_HOME=/work/cache/android-user
