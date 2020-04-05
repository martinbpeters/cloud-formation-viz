# Find the latest link from the following page:
#    https://aws.amazon.com/architecture/icons/

cd icons
wget https://d1.awsstatic.com/webteam/architecture-icons/AWS-Architecture-Icons_PNG_20200131.361768486d709f4d0ffca86995b4bf8a7cf5b5ac.zip
unzip AWS-Architecture-Icons_PNG_20200131.361768486d709f4d0ffca86995b4bf8a7cf5b5ac.zip
cp AWS-Architecture-Icons_PNG_20200131/PNG\ Light/*/*.png .
rm AWS-Architecture-Icons_PNG_20200131
cd ../
