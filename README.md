# Twitter Application #

Twitter Application to pick the latest 5 tweets of the users you want.


## Set Up ##

Please make sure that you have Docker installed in your computer, for the direction of downloading the application can be found [here](https://docs.docker.com/docker-for-mac/install/).

Once the Docker is downloaded, it is essential that you set up the `.env` file in your application directory because the application will be using [docker-compose](https://docs.docker.com/compose/) to boot up the application.

The requirement Environment Variable are as follows:

* `CONSUMER_KEY`: Twitter Application consumer Key to be used for your app
* `CONSUMER_SECRET`: Twitter Application consumer secret to be used for your app
* `POSTGRES_URI`: The postgresql uri for your application to connect to (this is defaulted at boot)

## Running ##

To run the program and start search through the tweets of the users you are interested in:

```shell
$ make run
```

The command will prompt you inside of the container where you will be able to execute the application without any additional set up.

The Python command is structured as following:

```shell
$ python3 ./fetch.py --user=<TWITTER USER NAME> --show --followers
```

--user      The user name you want to fetch the last 5 tweets
--show      (optional) The command to show the last 5 tweets retrieved from the Twitter API
--followers (optional) The command to retrieve followers of the user (set to just 1 page), Grabbing all users are limited due to API rate limit

## Testing ##

To run the testing of the program:

```shell
$ make test
```
