FROM docker.io/zephyrprojectrtos/ci-base:v0.29.4

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    libx11-xcb1 \
    openjdk-17-jdk-headless \
    && rm -rf /var/lib/apt/lists/*

ENV ANDROID_SDK_ROOT="/opt/android-sdk"
ENV SDK_VERSION="13114758"
RUN mkdir -p ${ANDROID_SDK_ROOT}/cmdline-tools
RUN cd ${ANDROID_SDK_ROOT}/cmdline-tools \
    && wget "https://dl.google.com/android/repository/commandlinetools-linux-${SDK_VERSION}_latest.zip" \
    && unzip commandlinetools-linux-${SDK_VERSION}_latest.zip \
    && rm commandlinetools-linux-${SDK_VERSION}_latest.zip \
    && mv cmdline-tools latest
ENV PATH="${ANDROID_SDK_ROOT}/cmdline-tools/latest/bin:${PATH}"

RUN yes | sdkmanager --licenses || true

RUN sdkmanager --install platform-tools
ENV PATH="${ANDROID_SDK_ROOT}/platform-tools:${PATH}"

RUN sdkmanager --install emulator
ENV PATH="${ANDROID_SDK_ROOT}/emulator:${PATH}"

ENV SYSTEM_IMAGE="system-images;android-36;default;x86_64"
RUN sdkmanager --install ${SYSTEM_IMAGE}

ARG KVM_GID=100
RUN groupadd -g $KVM_GID -o kvm

ENV ZEPHYR_TOOLCHAIN_VARIANT=host

RUN pip install --no-cache-dir bumble[android] uiautomator2

WORKDIR /workspace
RUN git config --global --add safe.directory '*'

ENV DEVICE="pixel_7a"

RUN avdmanager create avd -n mobile -d ${DEVICE} -k ${SYSTEM_IMAGE}
