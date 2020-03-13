COVID19 UK tracker
==================

This software checks the UK government's online tracker for COVID19
cases, and calculates the growth factor of the disease.

The tracker relates only to cases which have been confirmed by tests,
which may lag true cases by an order of magnitude.

Operation
---------

To start:

    $ make initdb

To update, to be done some time after 2pm each day:

    $ ./scrape_cases

The updater script is designed such that it *could* be run from cron
or a similar service.

To calculate the growth factor

    $ ./growth

Weakness
--------

The system currently relies on capturing data each day, and doesn't deal
with missing values. Historical data is cached in a file called `seed.csv`,
which is used to initialise the database. There's currently no good
mechanism for updating this file, and the gov.uk website doesn't seem
to have a good log of the historical data.

