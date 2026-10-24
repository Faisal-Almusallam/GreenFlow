# GreenFlow

CS316 Introduction to AI and Data Science project, Term 261.

Faisal Almusallam (223110267) and Abdulrahaman bin Saeed (223110148)

## About

We use machine learning to predict when the main roads in Riyadh will be congested and how bad it will be, and estimate how much extra fuel and CO2 the congestion causes. Since there is no public dataset with Riyadh traffic over time, we collect our own. We also use a public US highway dataset with six years of car counts to build the volume model and to simulate moving some drivers out of the rush hour.

The project is related to SDG 11 (sustainable cities), SDG 13 (climate action), SDG 3 (health) and SDG 9 (infrastructure).

## Data

**1. Our own Riyadh data (main dataset)**, from the TomTom Traffic Flow API

Every 15 minutes `riyadh_collector.py` saves the current speed, the normal free-flow speed and the travel time on 13 main roads in Riyadh (King Fahd Rd, the four ring roads, King Abdullah Rd, Olaya St, Takhassusi St and others). The data goes into `data/riyadh_traffic.csv`, which is shared in this repository. The Riyadh Municipality open data only has monthly totals (number of roads, traffic signs and so on), so it could not be used for this.

**2. Metro Interstate Traffic Volume** (UCI Machine Learning Repository)
https://archive.ics.uci.edu/dataset/492/metro+interstate+traffic+volume

48,204 hourly records (2012 to 2018) of westbound traffic on I-94 between Minneapolis and St Paul, with weather and holiday information. A copy is in the `data` folder.

## Files

- `GreenFlow.ipynb`: all the analysis (cleaning, EDA, models, CO2 estimate, simulation, Riyadh)
- `riyadh_collector.py`: collects the Riyadh data
- `.github/workflows/collect.yml`: runs the collector every 15 minutes on GitHub
- `data/`: the datasets
- `figures/`: the figures used in the report
- `requirements.txt`: the libraries needed

## How to run the notebook

Install Python 3.10 or newer, then install the libraries:

```
pip install -r requirements.txt
```

Open `GreenFlow.ipynb` from inside the GreenFlow folder (VS Code or Jupyter) and run all cells. It takes about 1 to 2 minutes. The figures are saved in the `figures` folder. If there is no Riyadh data yet, the Riyadh section just prints a message and skips.

## How to collect the Riyadh data

1. Make a free account on https://developer.tomtom.com and copy your API key.
2. Push this folder to a GitHub repository.
3. In the repository go to Settings > Secrets and variables > Actions, and add a secret called `TOMTOM_KEY` with your key.
4. Go to the Actions tab, open "collect riyadh traffic" and click "Run workflow" once to test it.

After that it runs by itself every 15 minutes and commits the new rows to `data/riyadh_traffic.csv`. That is about 1,250 API calls a day, which is under the free limit of 2,500. Note: GitHub may run scheduled jobs a few minutes late, and on a private repository the free minutes may not be enough, so a public repository is better.

To run it once on your own computer instead:

```
set TOMTOM_KEY=your_key
python riyadh_collector.py
```

## Results (UCI data, tested on 2018)

| Task | Model | Result |
|---|---|---|
| Traffic prediction (next hour) | Hist Gradient Boosting | R2 = 0.987, MAE about 145 |
| Traffic prediction without lag features | Hist Gradient Boosting | R2 = 0.964 |
| Congestion level (4 classes) | Hist Gradient Boosting | 92.8% accuracy |
| Types of days | K-means (k = 3) | weekdays, weekends, cold/holiday/storm days |
| Moving 20% of peak drivers (smart way) | simulation | 22.9% less extra CO2 |

Using smaller data types reduced the memory of the dataset by about 90%.

The Riyadh results will be added after we finish collecting the data.

## Notes

- The UCI data is from one highway in the US, so the results may be different for other roads.
- TomTom gives speeds but not the number of cars, so for Riyadh we look at congestion and delay, and CO2 per car instead of total CO2.
- The CO2 values are estimates. They use the BPR function, a road capacity of 7,500 cars per hour and 0.4 gallons of fuel per hour of delay (our assumptions), and the EPA value of 8.887 kg CO2 per gallon. These can be changed in section 8 of the notebook.

## Use of AI

We used AI (Claude) to guide us with the code and the formatting, and to fix the English in the report.

## References

1. J. Hogue, "Metro Interstate Traffic Volume," UCI Machine Learning Repository, 2019. doi: 10.24432/C5X60B.
2. TomTom, "Traffic Flow API - Flow Segment Data." https://developer.tomtom.com/traffic-api/documentation/traffic-flow/flow-segment-data
3. United Nations, "The 17 Sustainable Development Goals." https://sdgs.un.org/goals
4. U.S. EPA, "Greenhouse Gas Emissions from a Typical Passenger Vehicle." https://www.epa.gov/greenvehicles/greenhouse-gas-emissions-typical-passenger-vehicle
5. Bureau of Public Roads, Traffic Assignment Manual, U.S. Department of Commerce, 1964.
6. F. Pedregosa et al., "Scikit-learn: Machine Learning in Python," JMLR, vol. 12, pp. 2825-2830, 2011.
