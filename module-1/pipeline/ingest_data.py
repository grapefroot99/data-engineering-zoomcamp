#!/usr/bin/env python
# coding: utf-8

import click                            # for parameters/props in cli docker run
import pandas as pd                     # read csv and manipulate data
from sqlalchemy import create_engine    # connects to postgres database
from tqdm.auto import tqdm              # chunking the data

# lists all data types on unclean csv
dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

# same as above but for dates
parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]


# click command line interface to run the script with parameters
@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--target-table', default='yellow_taxi_data', help='Target table name')

# actual ingestion function
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, target_table):
    year = 2021             # arbitrary for taxi data file
    month = 1               # arbitrary for taxi data file

    chunksize = 100000      # arbitrary for iterating and chucking the data

    # data source prefix and url
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow'
    url = f'{prefix}/yellow_tripdata_{year}-{month:02d}.csv.gz'

    # connects to the postgres database using sqlalchemy and parameters from click
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')    

    # reads the csv in chunks
    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator = True,
        chunksize = chunksize,
    )

    # iterates through the chunks and writes them to the postgres database
    first = True
    
    for df_chunk in tqdm(df_iter):
        # first chunk creates the table and headers
        if first:
            df_chunk.head(0).to_sql(name=target_table, con=engine, if_exists='replace')
            first = False

        # actual rows of data
        df_chunk.to_sql(name=target_table, con=engine, if_exists='append')

if __name__ == '__main__':
    run()





