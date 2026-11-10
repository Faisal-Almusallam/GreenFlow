# GreenFlow - live demo guide

The presentation is a live run of `GreenFlow.ipynb` (no slides). The full run takes about 1.5 minutes.

## Before class

1. Open the `GreenFlow` folder in VS Code or Jupyter (the notebook must be opened from inside this folder).
2. Check the libraries once: `pip install -r requirements.txt`
3. Do one full **Restart & Run All** at home so you know it works on the laptop you will use.
4. Zoom the editor in (Ctrl +) so the class can read the code and the tables.
5. Keep the report open in a second window in case they ask about a number.

## In class (about 10 minutes)

Press **Restart & Run All** at the start, then scroll and explain while it runs. Everything up to section 5 finishes in a few seconds. The grid search (section 6) needs about 70 seconds, so the talking points for sections 4-6 cover that wait.

| Notebook section | What to show | What to say |
|---|---|---|
| Title + 1. Loading | `ry.head()`, 4,810 rows | No public Riyadh traffic data, so we collected our own from the TomTom API with GitHub Actions (show `riyadh_collector.py` and `collect.yml` if asked). 13 roads, 24 Oct - 8 Nov. |
| Runs per day | bar chart | GitHub didn't keep the 15-minute schedule: about 35 runs a day, then only 4 from 3 Nov. That is why the models use 25 Oct - 2 Nov. |
| 2. Cleaning | `describe()` | Congestion = 1 - current speed / free-flow speed. "Closed" readings were kept because the cars were still moving. |
| 3. EDA | road bar chart, map, heat map, hourly plot | Olaya St, Northern Ring Rd and Khurais Rd are the worst on average. Eastern Ring Rd at 5 PM is about 80% slower. On workdays 5 PM (29%) is about twice the morning peak. Weekends have the same average but the peak moves to 8 PM. |
| 4. Features | feature list | previous readings, yesterday, `usual` (computed on training days only, leaving out each row's own day, so there is no leakage). |
| 5. Classification | results table | Split by time, not at random. The baseline (same level as last reading) already gets 80.7%. Random forest has the best accuracy, 81.7%. Be honest: no model clearly beats the baseline on F1. |
| 6. Tuning | best params, table | GridSearchCV with TimeSeriesSplit and macro F1. The tuned forest uses balanced class weights: 80.8% accuracy, and it finds 11 of 16 severe jams (the baseline finds 9). |
| 7. Importance | bar chart | The previous reading, the road and the usual congestion matter most. |
| 8. CO2 per car | table + chart | 1 minute of delay is about 59 g CO2. Leaving 1 hour earlier or later saves 45 g per trip on average. |
| 9. UCI memory | `11.71 MB -> 1.20 MB` | category / float32 / int8 types + reading in chunks = 90% less memory (in the report appendix). |
| 10-11. UCI regression | results table, one-week plot | Gradient boosting R² = 0.987, MAE 144, against 339 for "same hour last week". Weather is from the previous hour so the model doesn't use the future. |
| 12. K-means | elbow / silhouette, clusters | k = 3: weekdays, weekends, cold days and holidays. |
| 13. Peak shift | table + chart | The busiest 25% of hours make 77% of the extra CO2. Spreading 20% of peak drivers smartly saves 23.5%. Moving everyone one hour later just makes a new peak (+53% at 30%). |
| 14. Conclusion | markdown | Limitations: only about 10 good days, the CO2 assumptions, one US highway. Ethics: not every worker can change hours. |

## If something goes wrong

- `FileNotFoundError` for `data/...` or `figures/...`: the notebook was opened from another folder. Open it from inside `GreenFlow`.
- Missing library: `pip install -r requirements.txt`, then restart the kernel.
- No time to wait for the grid search: the notebook is saved with all its outputs, so you can just scroll through it without running.

## Likely questions

- **Why not a random train/test split?** It would let the model learn from readings that come after the test readings.
- **Why is accuracy only a little above the baseline?** Traffic barely changes in 30-45 minutes, and we only have about 6 training days.
- **Why use the US data?** TomTom gives speeds but no car counts. Regression, clustering and the simulation need counts.
- **How sure are the CO2 numbers?** They are estimates (0.4 gallons per hour of delay and a capacity of 7,500 are our assumptions), so the percentages are more reliable than the grams.
