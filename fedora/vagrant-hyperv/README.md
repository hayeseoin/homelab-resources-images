# Vagrant Box for Fedora Cloud 42 on Hyper-V

These steps create a Vagrant box for Hyper-V of Fedroa Cloud 42. The user data also installs Ansible.

## Requirements
- The `Fedora-Cloud-Base-Azure-42-1.1.x86_64.vhdfixed.xz` image
- The [`vagrant-seed.iso`](vagrant-seed.iso) file for adding the Vagrant user/key and bootstrapping the box
- A known working directory e.g. `C:\Users\eoaha\dev\hyperv\vagrant-boxing\`

## Steps

### 1. Unarchive the image
Download the image to your working directory.

> Note: It would be good to keep a temporary backup of the base image, in case you make a mistake and need to revert. 

Unarchive and rename the image. Hyper-V requires the image to have extension `.vhd`. 

```sh
xz -d Fedora-Cloud-Base-Azure-42-1.1.x86_64.vhdfixed.xz
mv Fedora-Cloud-Base-Azure-42-1.1.x86_64.vhdfixed Fedora-Cloud-Base-Azure-42-1.1.x86_64.vhd
```

### 2. Create Hyper-V VM
Create a new Generation 1 VM for Hyper-V using the above iamge and the [`vagrant-seed.iso`](vagrant-seed.iso)

This Powershell command will create a 1GB 1 core VM using the default switch
```ps
New-VM -Name "fedora-cloud-42" -Generation 1 -MemoryStartupBytes 1GB -SwitchName "Default Switch"
```
Configure as follows:
- Memory: 1GB
- Processors: 1
- IDE Controller 0: 
    - Hard drive: `C:\Users\eoaha\dev\hyperv\vagrant-boxing\Fedora-Cloud-Base-Azure-42-1.1.x86_64.vhd`
    - DVD drive: `C:\Users\eoaha\dev\hyperv\vagrant-boxing\vagrant-seed.iso`
> (note, there may be an empty DVD drive on IDE controller 1 - I remove this and put both the DVD and Hard Drive on IDE controller 0)
- Network Adapter: Default Switch
- Checkpoints: Disabled 

> Notes: It should be possible to SSH in as vagrant@<_vm_ip_address> at this point if you need to check the instance works.

### 3. Export VM

Shut down the VM. **Important: REMOVE the DVD drive.**

> Note: The vagrant box will not load properly if the DVD drive is still attached when you export it.

Once the VM is shut down and the DVD drive is removed export the VM to your working directory

```ps
Export-VM -Name "Your-VM-Name" -Path "C:\Users\eoaha\dev\hyperv\vagrant-boxing\"
```
This will export the VM in the following structure to `C:\Users\eoaha\dev\hyperv\vagrant-boxing\fedora-cloud-42`

```sh
$ tree fedora-cloud-42/
fedora-cloud-42/
├── Snapshots
├── Virtual Hard Disks
└── Virtual Machines

```
### 4. Add Vagrantfile and metadata.json 
Add the following Vagrantfile and metadata.json file to directory your VM was exported to. 

Vagrantfile:
```ruby
Vagrant.configure("2") do |config|
  config.vm.provider "hyperv"
end
```
metadata.json
```json
{ "provider": "hyperv" }
```
The exported VM's folder structure will now look like this

```sh
$ tree fedora-cloud-42/
fedora-cloud-42/
├── metadata.json   	# new metadata.json
├── Snapshots
├── Vagrantfile         # new Vagrantfile
├── Virtual Hard Disks
└── Virtual Machines
```
### 5. Create Vagrantbox

A Vagrant box is basically just a TAR file. Arhive the exported VM **in Powershell**
```ps
tar -cvf fedora-cloud-42.box metadata.json Vagrantfile "Virtual Machines" "Virtual Hard Disks" "Snapshots" 
```
Add the box to Vagrant
```ps
 vagrant box add .\fedora-cloud-42.box --name hayeseoin/fedora-cloud-42-hyperv
 ==> box: Box file was not detected as metadata. Adding it directly...
 ==> box: Adding box 'hayeseoin/fedora-cloud-42-hyperv' (v0) for provider:
 box: Unpacking necessary files from: file://C:/Users/eoaha/dev/hyperv/vagrant-boxing/fedora-cloud-42/fedora-cloud-42.box
 box:
 ==> box: Successfully added box 'hayeseoin/fedora-cloud-42-hyperv' (v0) for ''! 
 ```
