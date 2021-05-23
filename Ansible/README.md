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

#### 3. Setup database server
pull couchDB from docker hub and excute script
run *./set_dbserver.yaml*

#### 4. Upload data and add to database
run *./set_data.yaml*

#### 6. Setup backend service
run *./set_backend.yaml*

-----------------------------

