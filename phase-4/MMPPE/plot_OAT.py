from pyexpat import model

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_OAT_scatter(data, var, model, ppename, ref_diff=False, width=9, height=3):
    '''
    ref_diff: True for for relative diff (in %) of global mean;  False for just global mean 
    '''
    plt.figure(figsize=(width, height))

    base_val = data.get(f'base', np.nan)

    # Collect values by grouping L and H under the same base label
    grouped_data = {}
    for key, val in data.items():
        label = key
        if label == 'base':
            continue
        if label.endswith(('L', 'H')):
            base_label = label[:-2]  # Remove '_L' or '_H'
            suffix = label[-1]
            if base_label not in grouped_data:
                grouped_data[base_label] = {}
            grouped_data[base_label][suffix] = ((float(val) - base_val) / base_val * 100) if ref_diff else float(val) 
            

    x_labels = list(grouped_data.keys())
    x_pos = range(len(x_labels))

    # Scatter plot values
    for i, label in enumerate(x_labels):
        values = grouped_data[label]
        if 'L' in values:
            plt.scatter(i, values['L'], color='blue', label='Low' if i == 0 else "", zorder=3, alpha=0.7, marker='s')
        if 'H' in values:
            plt.scatter(i, values['H'], color='orange', label='High' if i == 0 else "", zorder=3, alpha=0.7)
    

    plt.axhline(0 if ref_diff else base_val, color='red', linestyle='--', linewidth=1, label='Base')

    plt.xticks(ticks=x_pos, labels=x_labels, rotation=90)
    plt.ylabel(f'{var} [%]' if ref_diff else var)
    plt.title(f'Relative difference to base run [{ppename}]' if ref_diff else 'Global Mean')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
     # Legend outside
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    plt.tight_layout(rect=[0, 0, 0.85, 1])  # Make space for the legend

    plt.savefig(f'{model}_{ppename}_{var}.png', bbox_inches='tight')

    plt.show()
    plt.close()


def main():

    model = "ICON-HAM" # your model
    ppename = "5d_OAT"

    csv_file = f"{model}_{ppename}.csv"
    df = pd.read_csv(csv_file, index_col="experiment")

    for var in df.columns:
        plot_OAT_scatter(
            data=df[var],
            var=var,
            model=model,
            ppename=ppename,
            ref_diff=True,
            width=14,
            height=4,
        )

if __name__ == "__main__":
    main()