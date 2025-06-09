# Homelab Images
Manifest of my default homelab base images, and procedures for creating them.

## ['Manifest`](manifest.yml)

Manifest of images can be found at [`manifest.yml](manifest.yml)

## Generating seed.iso Files
Some of these images require cloud-init. To generate a seed.iso file, run this command in the same directory as the user-data and meta-data.

```sh
genisoimage -output seed.iso -volid cidata -joliet -rock user-data meta-data
```
A `generate-seed-iso.sh` script will be included anywhere it's needed.
