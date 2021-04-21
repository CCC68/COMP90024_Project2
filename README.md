# COMP90024_Project2

### Ansible
#### Make instances on MRC
direct to *Ansible/* directory and run *./mkins.sh* script, use openstack pwd:
'''
YTVmMmRkMzU4MDM0NzNh
'''

### Access instance via SSH
'''
ssh -i group-68-key.pem ubuntu@<instance-ip>
'''
make sure:
* use cisco Anyconnect VPN to connect internal uom network
* set file permission of the private key to 600
