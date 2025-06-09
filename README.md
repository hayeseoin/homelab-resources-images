# homelab-resources
resrouces for homelab

## Generating seed.iso Files

```sh
genisoimage -output seed.iso -volid cidata -joliet -rock user-data meta-data
```
To generate a seed.iso file, run this command in the same directory as the user-data and meta-data
