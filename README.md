# Fitbit Data (sleep) ETL


### Purposes:
- Allows curious individuals to easily access their sleep data and store them in a database for further statistical analysis.
- Simplifies and automate the ETL processes for sleep researchers to collect their subjects' sleep data into a database for further statistical analysis.


### Featuers:
- Fully automated once the appropriate credentials are given. 
- Can be used over multiple user accounts.



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

6. Fill in the credentials for your registered Fitbit Application and target database into ```var/config.yaml```.
   If you don't already have one registered, register one from https://dev.fitbit.com/apps/new. 
   If you don't already have AWS RDS instance established for your database, do so from https://console.aws.amazon.com/rds/home. 
```
app:
   client_id: <your client id>
   client_secret: <your client secrete>
   
db:
   host: <your DB host DNS>
   port: <your DB host Port>
   databse: <your DB name>
   user_id: <your DB user_id>
   password: <your DB password>
   
```

7. Fill in one or more Fitbit user information into ```var/users.yaml```.
```
user1:
   name: <user's name>
   bod: <user's bod in "%Y-%m-%d">
   gender: <user's gender in string>
   country: <user's coutry of residence in string> 
   accountID: <user's Fitbit account ID>
   password: <user's Fitbit accound password>
   
user2:
   name: <user's name>
   bod: <user's bod in "%Y-%m-%d">
   gender: <user's gender in string>
   country: <user's coutry of residence in string> 
   accountID: <user's Fitbit account ID>
   password: <user's Fitbit accound password>
   
user3:
   ...
```

9. Automate login process over all the user accoutns by running login.py. 
   Once authenticated, there is no need to run this every time you want to extract data. 

```
python login.py 
```

10. Extract, transform, and load your sleep data into your AWS RDS database by executing sleep_ETL.py. 

```
python FETL.py
```



