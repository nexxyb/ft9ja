This is an app showing the profit and loss dashboard for traders.

Step 1: Use a random number generator to simulate the profit and loss on the $100 given to each trader.
    This is the simulate function in  main/stock/simulator.py.
    The simulated data is the data.json file in main directory.

Step 2: Create a MongoDB database for this data.
    This are implemented in  connect_to_mongo, read_from_mongo and write_to_mongo functions in 
    main/stock/simulator.py

Step 3: Create a user dashboard. The dashboard should at least include a graph of the 
    profit (or loss) vs time (data point at 1 minute intervals).

    To see this you need to run the local.yml docker compose file.
    in the root directory, run 'docker compose -f local.yml up -d build' command from the terminal
     which run the django and mongodb containers and  simulate the data to be used. navigate to 
     '127.0.0.1:800' on your browser to see a single user dasboard updated every minute.

Step 4: Create an admin dashboard.
    Click the admin dashboard link on the homepage to navigate to admin dashboard


The step 5 will be presented on interview day.
