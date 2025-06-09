# Vagrant Box for Fedora Cloud 42 on Hyper-V

These steps create a Vagrant box for Hyper-V of Fedroa Cloud 42. The user data also installs Ansible.

## Requirements
- The `al2023-hyperv-2023.7.20250527.1-kernel-6.1-x86_64.xfs.gpt.vhdx.zip` image
- The [`vagrant-seed.iso`](../seed-iso/vagrant/amazon-linux-2023/vagrant-seed.iso) file for adding the Vagrant user/key and bootstrapping the box
- A known working directory e.g. `C:\Users\eoaha\dev\hyperv\vagrant-boxing\`

## Steps

### 1. Unarchive the image
Download the image to your working directory.

> Note: It would be good to keep a temporary backup of the base image, in case you make a mistake and need to revert. 

Unarchive the image. The result is a folder with the VHDX file inside of it.

```sh
gzip -d al2023-hyperv-2023.7.20250527.1-kernel-6.1-x86_64.xfs.gpt.vhdx.zip
```

### 2. Create Hyper-V VM
Create a new Generation 2 VM for Hyper-V using the above iamge and the [`vagrant-seed.iso] 

This Powershell command will create a 1GB 1 core VM using the default switch
```ps
New-VM -Name "amazon-linux-2023" -Generation 2 -MemoryStartupBytes 1GB -SwitchName "Default Switch"
```
Configure as follows:
- Secure Boot: Disabled
- Memory: 1GB
- Processors: 1
- SCSI Controller: 
    - Hard drive: `C:\Users\eoaha\dev\hyperv\vagrant-boxing\al2023-hyperv-2023.7.20250527.1-kernel-6.1-x86_64.xfs.gpt.vhdx\al2023-hyperv-2023.7.20250527.1-kernel-6.1-x86_64.xfs.gpt.vhdx`
    - DVD drive: `"C:\Users\eoaha\dev\hyperv\vagrant-boxing\seed.iso"`
- Network Adapter: Default Switch
- Checkpoints: Disabled 

Start the VM.

> Notes: It should be possible to SSH in as vagrant@<_vm_ip_address> at this point if you need to check the instance works.

### 3. Export VM

Shut down the VM. **Important: REMOVE the DVD drive.**

> Note: The vagrant box will not load properly if the DVD drive is still attached when you export it.

Once the VM is shut down and the DVD drive is removed export the VM to your working directory

```ps
Export-VM -Name "amazon-linux-2023" -Path "C:\Users\eoaha\dev\hyperv\vagrant-boxing\"
```
This will export the VM in the following structure to `C:\Users\eoaha\dev\hyperv\vagrant-boxing\amazon-linux-2023`

```sh
$ tree amazon-linux-2023/
amazon-linux-2023/
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
$ tree amazon-linux-2023/
amazon-linux-2023/
├── metadata.json   	# new metadata.json
├── Snapshots
├── Vagrantfile         # new Vagrantfile
├── Virtual Hard Disks
└── Virtual Machines
```
### 5. Create Vagrantbox

A Vagrant box is basically just a TAR file. Arhive the exported VM **in Powershell**
```ps
tar -cvf amazon-linux-2023.box metadata.json Vagrantfile "Virtual Machines" "Virtual Hard Disks" "Snapshots" 
```
Add the box to Vagrant
```ps
 vagrant box add .\amazon-linux-2023.box --name hayeseoin/al2023-hyperv
 ==> box: Box file was not detected as metadata. Adding it directly...
 ==> box: Adding box 'hayeseoin/al2023-hyperv' (v0) for provider:
 box: Unpacking necessary files from: file://C:/Users/eoaha/dev/hyperv/vagrant-boxing/amazon-linux-2023/al2023-hyperv.box
 box:
 ==> box: Successfully added box 'hayeseoin/al2023-hyperv' (v0) for ''! 
 ```
