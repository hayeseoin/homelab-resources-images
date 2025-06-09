# Vagrant box of Alpine for Hyper-V

This box is just a fork of the `generic/alpine317` box from Vagrant Cloud.

## Overview

This is mostly the same as the default box. Additions include Ansible and and alias for `ls -l`.

## Steps

### 1. Initialize box
Add the following [`Vagrantfile`](Vagrantfile) to a new directory and run `vagrant up`. 

This Vagrantfile updates the packages, installs Ansible and adds a few convenience aliases. 

> Note: the following line must be included:
> ```ruby
> config.ssh.insert_key = false
> ```

### 2. Save as new box

Stop the VM.
```ps
vagrant halt
```
Repackage as a new box.
```ps
vagrant package --output alpine317-hyperv.box 
```
Add the new box to vagrant (use `--force` flag at end if nescessary).
```ps
vagrant box add ./alpine317-hyperv.box --name hayeseoin/alpine317-hyperv
```