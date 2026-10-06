import os
import pytest
import subprocess
import time
import uiautomator2

IP = "127.0.0.1"
PORT = 9001


@pytest.fixture(scope="session", autouse=True)
def zephyr_ble_options(device_object):
    device_object.generate_command()
    device_object.command += [f"--bt-dev={IP}:{PORT}"]


@pytest.fixture(scope="session")
def android_emulator(avd_name="mobile"):
    emulator = subprocess.Popen(
        [
            "emulator",
            "-avd",
            avd_name,
            "-no-metrics",
            "-packet-streamer-endpoint",
            "default",
        ]
        + (["-no-window"] if os.path.exists("/.dockerenv") else [])
    )
    subprocess.run(["adb", "wait-for-device"], check=True)
    subprocess.run(
        [
            "adb",
            "shell",
            "-x",
            "while [[ -z $(getprop dev.bootcomplete) ]]; do sleep 1; done",
        ],
        check=True,
    )
    time.sleep(2)
    subprocess.run(
        ["adb", "shell", "-x", "while ! settings list global; do sleep 1; done"],
        check=True,
    )
    subprocess.run(
        ["adb", "shell", "settings", "put", "secure", "anr_show_background", "0"],
        check=True,
    )
    for setting in [
        "window_animation_scale",
        "transition_animation_scale",
        "animator_duration_scale",
    ]:
        subprocess.run(
            ["adb", "shell", "settings", "put", "global", setting, "0"],
            check=True,
        )
    yield
    emulator.terminate()
    emulator.wait()


@pytest.fixture(scope="session")
def hci_bridge(android_emulator):
    bridge = subprocess.Popen(
        ["bumble-hci-bridge", f"tcp-server:{IP}:{PORT}", "android-netsim"]
    )
    yield
    bridge.terminate()
    bridge.wait()


@pytest.fixture(scope="session")
def phone(hci_bridge):
    return uiautomator2.connect()


@pytest.fixture(scope="session")
def app(
    phone,
    apk="https://github.com/nordicsemi/Android-nRF-Connect/releases/download/version_4.29.1/nRF.Connect.4.29.1.apk",
    package_name="no.nordicsemi.android.mcp",
):
    phone.app_install(apk)
    phone.app_clear(package_name)
    phone.app_auto_grant_permissions(package_name)
    phone.app_start(package_name)
    phone(text="Welcome").wait()
    phone.press("back")
    return phone


def test_temperature_notification(shell, app):
    app(text="SCAN").click()
    assert app(text="ESP peripheral").wait()
    app(text="CONNECT").click()

    assert app(text="CONNECTED").wait()
    app(text="Environmental Sensing").click()
    time.sleep(1)
    app(description="Enable notifications").click()

    assert app(text="Value: 0.00℃").wait()

    shell.exec_command("adc_emul adc mv 0 1000")
    assert app(text="Value: 25.00℃").wait()
