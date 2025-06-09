# Vagrant Boxes for Hyper-V

I use Vagrant with the Hyper-V provider. This repo documents the steps in creating these image templates.

In the future it would be nice to have some kind of pipeline to automatically create these images. Unfortunately Vagrant used with the Hyper-V provider is not the friendliest setup, and image template creation is difficult to automate.

There are only 4 boxes (at the time of writing) and I don't plan any more tweaking of the template, I think maintiaing them manually is fine. So for now I've opted to simply record the steps in a README with convenience scripts used where possible (and reliable). 

## `build-conf.yml`
There is a `build-conf.yml` file for each of the Vagrant boxes which may help future automation. Currently they just contain the 'type' of box it is, and the base image/box it is based on. 

For my purposes, there are two types. `cloud-config` are the boxes created by starting a Hyper-V VM with cloud init and saving it as a Vagrant box. `cloud-catalog-fork` are boxes which are bascically just lightly modified versions of boxes from the cloud catalog. 

Base images and base boxes are in the S3 bucket directory `s3://hayeseoin-homelab-resources-images/base-images/`

Examples:
```yaml
type: cloud-config
base_image: al2023-hyperv-2023.7.20250527.1-kernel-6.1-x86_64.xfs.gpt.vhdx.zip
```
```yaml
type: cloud-catalog-fork
base_box: generic-VAGRANTSLASH-alpine317.tar.gz
``` 

## Requirements for automation

The internet tells me Packer would be good for this, but I have my doubts, since Vagrant and Hyper-V has been an uphill struggle from the start. Being able to entirely configure a Hyper-V VM with powershell commands will probably open the door to automating the `cloud-config` type.

The [`Box factory`](https://raw.githubusercontent.com/hayeseoin/vagrant-labs/refs/heads/main/box-factory/Vagrantfile) is useful for creating custom boxes, and is almost automation ready. 