# COMP90024_Project2

### Ansible
#### 1. Make instances on MRC
direct to *Ansible/* directory and run *./mkins.sh* script, use openstack pwd:
```
YTVmMmRkMzU4MDM0NzNh
```

#### 2. Set enviornment on remote servers
including set proxy and mount volume to filesystem
run *./set_env.sh*

### Access instance via SSH
```
ssh -i group-68-key.pem ubuntu@<instance-ip>
```
make sure:
* use cisco Anyconnect VPN to connect internal uom network
* set file permission of the private key to 600
