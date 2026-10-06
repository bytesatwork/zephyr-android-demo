# Zephyr Android Emulator Demo
This repository shows how Zephyr applications can be integration tested together with the Android emulator through native_sim.

## Repository Initialization
```
west init -m https://github.com/bytesatwork/zephyr-android-demo zephyr-workspace
cd zephyr-workspace
west update
```

## Running the Tests inside a Docker Container
```
zephyr-android-demo/run.sh
```
