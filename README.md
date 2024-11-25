# FPL-AI

This is my Fantasy Premier League AI. It is a Python project that combines **data science, machine learning, and optimization techniques** to enhance FPL team management. The project uses:

- **Historical data** from FPL and Understat.
- **Machine learning models** to predict player points.
- **Optimization algorithms** to determine the best possible fantasy team for each gameweek.

---

### Features
- Predict player scores for upcoming gameweeks using machine learning.
- Optimize transfers, captain choices, and starting lineups for maximum points.
- Integrates with your FPL team using your user ID.
- Uses historical data from FPL and Understat for predictions.

---

### How to Use
1. **Download Repository**
   ```bash
   git clone https://github.com/Jakob-F/FPL-AI.git
   ```

2. **Combine Previous Seasons Data**  
   Run `combine_previous_seasons.py` to combine FPL and Understat data from all previous seasons into one large DataFrame.

3. **Update with Current Season Data**  
   Run `combine_new_gameweek.py` to scrape the newest FPL and Understat data for the current season and combine it with the data from previous seasons.

4. **Create Training and Test Data**  
   Run `create_train_test_data.py` to create training and test datasets. It is possible to select which features/stats to use for the data in this script.

5. **XGBoost Model**  
   The `XGBoost.ipynb` Notebook trains an XGBoost model to predict the players' scores for the next gameweek(s). You can then use your FPL user ID to load your own team. The Notebook creates an optimization problem using PuLP to determine:
   - Which transfers to perform.
   - The optimal starting XI and Captain to maximize points for the next gameweek.

---

### Example Output
After running the optimization on your team, you might get an output like this:

```
Transfers in: ['Andreas', 'Gvardiol']
Transfers out: ['Foden', 'Evans']

Starting 11
+-------------+-----------------+--------+------------------+-------------------+
| Player Name | Predicted Score | FPL xP | Sum next 5 games | Chance of playing |
+-------------+-----------------+--------+------------------+-------------------+
| --- GK ---  |                 |        |                  |                   |
|    Raya     |      5.78       |  2.70  |      28.92       |        100        |
| --- DEF --- |                 |        |                  |                   |
|   Gabriel   |      6.22       |  2.70  |      31.12       |        100        |
|  Gvardiol   |      6.78       |  7.30  |      33.52       |        100        |
|  Aït-Nouri  |      5.89       |  3.50  |      29.46       |        100        |
| --- MID --- |                 |        |                  |                   |
|    Saka     |      6.41       |  4.00  |      32.05       |        75         |
|   Mbeumo    |      6.42       |  5.80  |      31.65       |        75         |
|   Andreas   |      6.60       |  2.70  |      33.02       |        100        |
|   M.Salah   |      6.81       | 12.70  |      34.05       |       None        |
| --- FWD --- |                 |        |                  |                   |
|   Welbeck   |      6.40       |  4.70  |      31.98       |        100        |
|    Wood     |      6.53       |  6.20  |      32.63       |        100        |
|   Solanke   |      6.53       |  6.20  |      32.18       |        100        |
+-------------+-----------------+--------+------------------+-------------------+

Expected points next gameweek: 77.18
```
---


### Roadmap
- Add support for chip optimization (Wildcard, Bench Boost, Free Hit, Triple Captain).
- Improve model accuracy with feature selection and feature optimization to better identify the most impactful predictors of player performance.
- Implement more advanced machine learning techniques. (WIP: Neural Network)
- Create a web-based interface for easier usage.
- Automate FPL data scraping.

---

### Acknowledgements

I would like to thank **vaastav** for providing FPL data from previous seasons, as well as for creating data-scraping functions for both FPL and Understat data. Their repository can be found [here](https://github.com/vaastav/Fantasy-Premier-League/tree/master).
