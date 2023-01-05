"""
This script plot the QC M3C2 results
"""
#%% Import modules
import numpy as np
import pandas as pd

from lidar_platform import cc, global_shifts

#%% Function


def func(filepath, distance_filter):
    pc, sf, config = cc.read_sbf(filepath)

    # SF1 = Npoints_cloud1
    # SF2 = Npoints_cloud2
    # SF3 = STD_cloud1
    # SF4 = STD_cloud2
    # SF5 = significant change
    # SF6 = distance uncertainty
    # SF7 = M3C2 distance

    uncertainty = sf[:, 5]
    distance = sf[:, 6]

    select = ~np.isnan(uncertainty)
    select &= (uncertainty < distance_filter)
    select &= ~np.isnan(distance)
    select &= (distance < 1)

    m3c2_dist = distance[select]

    if len(m3c2_dist) > 100:
        line_select = np.unique(np.random.randint(0, len(m3c2_dist), int(0.5 * len(m3c2_dist))))
        results = m3c2_dist[line_select]
    else:
        results = []
    return results

#%% Plot
workspace = r'G:\RENNES1\ThomasBernard\StripAlign\Multi_channel_test\results\QC\before_corr\Ardeche_01102021'
folder = 'C2'
list_filepath = glob.glob(os.path.join(workspace, folder, "*_m3c2_*.sbf"))

if True:
    max_uncertainty = 0.1
    result = Parallel(n_jobs=20, verbose=2)(delayed(func)(i, max_uncertainty) for i in list_filepath)
    np.savez_compressed(os.path.join(workspace, folder, "save_results_data_v1.npz"), np.concatenate(result))

npz = os.path.join(workspace, folder, "save_results_data_v1.npz")
f = np.load(npz)
tab = f[f.files[0]]
f.close()

print(np.mean(tab))
print(np.std(tab))

plt.figure(1)
plt.xlabel("Distance M3C2 (en cm)")
plt.ylabel("Fréquence")
plt.title('Histogramme des écarts en altitude\npour les données du canal vert')
plt.hist(tab * 100, bins=50, range=(-15, 15), edgecolor='white')
plt.ticklabel_format(axis="y", style='sci', scilimits=(0,0))
plt.text(x=-30,y=3000,s="Moyenne : -9cm\nEcart-type : 5.5cm")
out = os.path.join(workspace, folder,  "figure_C3_v1.png")
plt.savefig(out, dpi=150)
plt.show()