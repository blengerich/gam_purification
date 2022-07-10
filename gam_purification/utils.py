import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
import numpy as np


def find_bin(val, ar):
    # Find the first bin which has left index geq the query.
    # The query belongs in the bin to the left of this one.
    # Assumes the bins are right-inclusive.
    return np.argmin(ar < val)


def only_finite(ar):
    return ar[np.isfinite(ar)]


def get_feat_vals(ebm_global, feat_id):
    good_vals = only_finite(np.array(ebm_global.data(feat_id)['names'])).tolist()
    return good_vals


def calc_density(use_density, feat_vals1, feat_vals2,
                 feat_id1, feat_id2, X_train, laplace=0):
    if use_density:
        density = np.zeros((len(feat_vals1), len(feat_vals2))) + laplace
        for x in X_train:
            idx1 = find_bin(x[feat_id1], feat_vals1)
            idx2 = find_bin(x[feat_id2], feat_vals2)
            density[idx1, idx2] += 1
        return density
    else:
        return None


def plot_interaction(val_names1, val_names2,
                     before, after, dataset_name, feat_name1, feat_name2, model_name, move_name):
    # Plots an interaction effect before and after purification.
    # Set up figure and image grid
    fig = plt.figure(figsize=(9.75, 3))
    grid = ImageGrid(fig, 111,          # as in plt.subplot(111)
                     nrows_ncols=(1, 2),
                     axes_pad=0.15,
                     share_all=True,
                     cbar_location="right",
                     cbar_mode="single",
                     cbar_size="7%",
                     cbar_pad=0.15,
                     )

    # Add data to image grid
    extent = (val_names2[0],
              val_names2[-1],
              val_names1[0],
              val_names1[-1])

    aspect = float(extent[3] - extent[2]) / float(extent[1] - extent[0])
    aspect = 1/aspect

    im = grid[0].imshow(before, aspect=aspect, origin='lower',
                        interpolation='none', extent=extent)
    im = grid[1].imshow(after, aspect=aspect, origin='lower',
                        interpolation='none', extent=extent)

    # Colorbar
    ax = grid[-1]
    ax.cax.colorbar(im)
    ax.cax.toggle_label(True)

    grid[0].set_ylabel(feat_name1, fontsize=22)
    grid[0].set_xlabel(feat_name2, fontsize=22)
    grid[1].set_xlabel(feat_name2, fontsize=22)
    grid[0].tick_params(axis='both', which='major', labelsize=16)
    grid[0].tick_params(axis='both', which='minor', labelsize=12)
    grid[1].tick_params(axis='both', which='major', labelsize=16)
    grid[1].tick_params(axis='both', which='minor', labelsize=12)
    ax.cax.tick_params(axis='both', which='major', labelsize=16)
    ax.cax.tick_params(axis='both', which='minor', labelsize=12)

    plt.savefig("figs/{}/interactions/{}_{}_{}".format(
        dataset_name, feat_name1, feat_name2, model_name, move_name))
