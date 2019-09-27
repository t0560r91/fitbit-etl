# Fitbit Data (sleep) ETL


### Purposes:
- Allows curious individuals to easily access their sleep data and store them in a database for further statistical analysis.
- Simplifies and automate the ETL processes for sleep researchers to collect their subjects' sleep data into a database for further statistical analysis.


### Featuers:
- Fully automated once the appropriate credentials are given. 
- Can be used over multiple user accounts.
- Transform the data into CSV format. 


### Instruction:
If you don't already have anaconda environment manager installed on your machine,
install environment manager anaconda3 from https://www.anaconda.com/distribution/#download-section . 

Or, if you already have Anaconda Envirionment Manager follow the steps below.

1. Create an environment that will be configured for running the ETL application. 

```
conda create -n fitbitETL python=3.6
```

2. Activate the new environment.

```
conda activate fitbitETL
```

3. Download the application package.

```
git clone https://github.com/sehokim88/fitbit-etl.git 
```

4. Change directory into the package's root.

```
cd fitbit-etl 
```

5. Install required python pacakges from anaconda distribution.

```
conda install --file requirements.txt
```

6. Fill in the credentials for your registered Fitbit Application into ```var/creds/app-creds.json```.
   If you don't already have one registered, register one from https://dev.fitbit.com/apps/new. 
``` 
{
  "client_id" : your_client_id,
  "client_secret" : your_client_secrete
 }
 ```


7. Fill in the credentials for your AWS RDS into ```var/creds/rds-creds.json```. 
   If you don't already have AWS RDS instance established for your database, do so from https://console.aws.amazon.com/rds/home. 
```
{
  "host" : your_AWS_RDS_host_DNS,
  "port" : your_AWS_RDS_host_port,
  "database" : your_AWS_RDS_database_name,
  "user_id" : your_AWS_RDS_user_id,
  "password" : your_AWS_RDS_password
}
```

8. Fill in the credentials for one or more Fitbit user information into ```var/users.yaml```.
```
user1:
   name: USER1_NAME
   bod: USER1_BOD
   gender: USER1_GENDER
   country: USER1_COUNTRY
   accountID: USER1_ACCOUNTID
   password: USER1_PASSWORD
   
user2:
   name: USER2_NAME
   bod: USER2_BOD
   gender: USER2_GENDER
   country: USER2_COUNTRY
   accountID: USER2_ACCOUNTID
   password: USER2_PASSWORD
   
```
9. Automate login process over all the user accoutns by running login.py. 
   Once authenticated, there is no need to run this every time you want to extract data. 

```
python login.py 
```

10. Extract, transform, and load your sleep data into your AWS RDS database by executing sleep_ETL.py. 

```
python sleep_ETL.py
```



