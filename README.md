# GreenFlow

CS316 Introduction to AI and Data Science project, term 261.

Faisal Almusallam (223110267) and Abdulrahaman bin Saeed (223110148)

## About

We predict how congested the main roads in Riyadh get and estimate how much extra CO2 the congestion causes. There is no public dataset with Riyadh traffic over time, so we collected our own from TomTom. We also used a public US highway dataset with car counts for the parts that need the number of cars (regression, clustering and the peak shift simulation).

Related to SDG 11 (sustainable cities), SDG 13 (climate action), SDG 3 (health) and SDG 9 (infrastructure).

## Data

**1. Riyadh (our own data)** - `data/riyadh_traffic.csv`

`riyadh_collector.py` asks the TomTom Traffic Flow API about one point on 13 main roads (King Fahd Rd, the four ring roads, Makkah Rd, Khurais Rd, Olaya St, Takhassusi St and others) and saves the current speed, free-flow speed and travel times. GitHub Actions ran it for us.

We set it to every 15 minutes but GitHub ran it every 30-45 minutes, and from 3 November only about 4 times a day. In total we have 4,810 rows from 24 Oct to 8 Nov 2026. The models use 25 Oct - 2 Nov. We stopped the collection after 8 November (the schedule in `collect.yml` is turned off) and the notebook only reads data up to 8 November, so the results always match the report.

The Riyadh Municipality open data only has monthly totals (number of roads, signs etc.) so we couldn't use it for this.

**2. Metro Interstate Traffic Volume** (UCI) - https://archive.ics.uci.edu/dataset/492/metro+interstate+traffic+volume

48,204 hourly rows (2012-2018) from the I-94 highway in the US with weather and holidays. A copy is in `data/`.

## Files

- `GreenFlow.ipynb` - all the analysis (commented code + explanations)
- `riyadh_collector.py` - collects the Riyadh data
- `.github/workflows/collect.yml` - runs the collector on GitHub (manual run only now)
- `data/` - the two datasets
- `figures/` - figures used in the report and slides
- `CS316_Report_...docx` - the IEEE report
- `DEMO_GUIDE.md` - what we show when we run the notebook in the presentation
- `requirements.txt`

## How to run

```
pip install -r requirements.txt
```

Then open `GreenFlow.ipynb` from inside this folder and run all cells (Restart & Run All, about 1.5 minutes; the grid search alone takes about 70 seconds). The figures are saved in `figures/`.

To collect the Riyadh data yourself: get a free key from https://developer.tomtom.com, add it as a repository secret called `TOMTOM_KEY` (Settings > Secrets and variables > Actions), then run the "collect riyadh traffic" workflow from the Actions tab. To run it every 15 minutes again, uncomment the `schedule` lines in `collect.yml`. Or run it once on your computer:

```
set TOMTOM_KEY=your_key
python riyadh_collector.py
```

## Results

Riyadh:

- most congested on average: Olaya St (22%), Northern Ring Rd at KAFD (21%), Khurais Rd (18%)
- on workdays the evening is much worse than the morning (29% at 5 PM vs 15% at 9 AM). Weekends have almost the same average but the peak is at 8 PM
- worst road and hour: Eastern Ring Rd at 5 PM, about 80% slower than normal
- congestion level (4 classes), test days 31 Oct - 2 Nov:

| Model | Accuracy | Macro F1 | Severe found |
|---|---|---|---|
| Baseline (same as last reading) | 80.7% | 0.685 | 9 of 16 |
| Random forest | 81.7% | 0.661 | 9 of 16 |
| Random forest (tuned, balanced) | 80.8% | 0.679 | 11 of 16 |

  The baseline is hard to beat because traffic changes little in 30-45 minutes. The tuned forest has almost the same F1 and finds more severe jams.
- 1 minute of delay is about 59 g CO2 per car. Leaving 1 hour earlier or later saves 45 g per trip on average

UCI (tested on 2018):

| Task | Model | Result |
|---|---|---|
| Next hour traffic | Gradient boosting | R2 = 0.987, MAE = 144 (baseline "same hour last week": MAE = 339) |
| Types of days | K-means (k = 3) | weekdays, weekends, cold/holiday days |
| Moving 20% of peak drivers (smart way) | simulation | 23.5% less extra CO2 |

Smaller data types and reading in chunks reduced the memory of the UCI data from 11.7 MB to 1.2 MB.

## Notes

- only about 10 good days of Riyadh data, so no Ramadan, summer or rain
- TomTom gives speed but not car counts, so for Riyadh we only have CO2 per car
- the CO2 values are estimates (0.4 gallons per hour of delay and a road capacity of 7,500 cars/hour are our assumptions, 8.887 kg CO2 per gallon is from the EPA)

## Use of AI

We used AI (Claude) to guide us with parts of the code (for example the time-based validation and the peak shift simulation), to help find bugs, and to help with the formatting and the English of the report. We wrote, ran and checked all the analysis ourselves and all the results come from running the notebook.

## References

1. J. Hogue, "Metro Interstate Traffic Volume," UCI Machine Learning Repository, 2019. doi: 10.24432/C5X60B.
2. TomTom, "Traffic Flow API - Flow Segment Data." https://developer.tomtom.com/traffic-api/documentation/traffic-flow/flow-segment-data
3. U.S. EPA, "Greenhouse Gas Emissions from a Typical Passenger Vehicle." https://www.epa.gov/greenvehicles/greenhouse-gas-emissions-typical-passenger-vehicle
4. Bureau of Public Roads, Traffic Assignment Manual, 1964.
5. L. Breiman, "Random forests," Machine Learning, vol. 45, no. 1, pp. 5-32, 2001.
6. F. Pedregosa et al., "Scikit-learn: Machine Learning in Python," JMLR, vol. 12, pp. 2825-2830, 2011.
