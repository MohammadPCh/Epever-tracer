# Epever-tracer
Trace **EPsolar** and **UPower** with **rapberry pi**.
# Step 1: Prepare Driver

follow these steps:
- ## Install required packages

you should install driver of your device.
install these before:
```
sudo apt install dkms raspberrypi-kernel-headers
```

- ## remove default driver

Remove the CDC-ACM driver and install the driver:
```
rmmod cdc-acm
```
```
modprobe -r usbserial
```
```
modprobe usbserial
```

Ensure that thecdc-acm module is not loaded:
```
echo blacklist cdc-acm > /etc/modprobe.d/blacklist-cdc-acm.conf 
```
if it says you have not permission, go to the `/etc/modprobe.d/` and create a file with `blacklist-cdc-acm.conf` and add `blacklist cdc-acm` to it.

then run this line:

```
update-initramfs -u
```

- ## Install driver

go to the xr_usb_serial_common-1a folder and install via DKMS:
```
cp -a ../xr_usb_serial_common-1a /usr/src/
```
```
dkms add -m xr_usb_serial_common -v 1a
```
```
dkms build -m xr_usb_serial_common -v 1a
```
```
dkms install -m xr_usb_serial_common -v 1a
```

- ## Plug USB and Check
Plug the device into the USB host. You should see up to four devices created,typically `/dev/ttyXRUSB[0-3]`.