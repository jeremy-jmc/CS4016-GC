
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('benchmark.csv')
point_number = df['Points'].unique()

distributions = df['Distribution'].unique()
for distribution in distributions:
    for algorithm in ['graham_scan']:   # , 'jarvis_march'
        plt.figure(figsize=(5, 5))
        plt.title(f'{algorithm} - {distribution}')
        for point_elimination in [True, False]:
            df_filtered = df[(df['Algorithm'] == algorithm) & (df['Distribution'] == distribution) & (df['Point Elimination'] == point_elimination)]
            plt.plot(df_filtered['Points'], df_filtered['Runtime'], label=point_elimination,
                     marker='o', linestyle='--', markersize=5)

        # plt.xscale('log')
        # plt.yscale('log')
        plt.xticks(point_number, rotation=45)
        plt.xlabel('Number of Points')
        plt.ylabel('Runtime (seconds)')
        plt.legend()
        plt.show()

# display(df)
