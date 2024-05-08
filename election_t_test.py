from scipy import stats

# Extract the voter participation data for before and after periods
before_congressional = avg_voter_participation_before['votes_per_capita']
after_congressional = avg_voter_participation_after['votes_per_capita']

before_austin = before_austin_data['Ballots to Population Ratio']
after_austin = after_austin_data['Ballots to Population Ratio']

# Perform t-test for congressional districts
t_stat_congressional, p_val_congressional = stats.ttest_ind(before_congressional, after_congressional)

# Perform t-test for Austin City Council elections
t_stat_austin, p_val_austin = stats.ttest_ind(before_austin, after_austin)

# Print the results
print("T-test results for congressional districts:")
print(f"T-statistic: {t_stat_congressional}")
print(f"P-value: {p_val_congressional}")
print("\n")

print("T-test results for Austin City Council elections:")
print(f"T-statistic: {t_stat_austin}")
print(f"P-value: {p_val_austin}")