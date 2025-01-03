import os
import sys
import time
import warnings

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram, complete, to_tree
from scipy.spatial.distance import squareform
from tabulate import tabulate
from io import StringIO


# genbank file read/parse/plot
from Bio import SeqIO
from Bio import GenBank
from pygenomeviz import GenomeViz


# matplotlib
import matplotlib
import matplotlib as mpl
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, FancyArrow
from matplotlib.transforms import Affine2D
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.collections as mpcollections
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from typing import Optional, List, Dict, Union, Tuple

# data process
import dask.array as da

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['svg.fonttype'] = 'none'


class cvmplot():
    pass

    @staticmethod
    def tnseqplot(
        inspos=None,
        inscount=None,
        cds=None,
        fig_width=10,
        track_start=1,
        track_length=None,
        track_height=0.6,
        track_label=None,
        track_labelsize=None,
        track_sublabelpos='bottom-right',
        track_sublabelsize=6,
        cds_plotstyle='bigarrow',
        cds_color='lightblue',
        cds_label=False,
        cds_labelsize=6,
        cds_labvpos='bottom',
        cds_labhpos='center',
        cds_labrotation=0,
        cds_arrowshaftratio=0.5,
        bax_bottompos=1.5,
        bax_height=4,
        bax_ylabel=None,
        bax_ylabelsize=10,
        bax_xticklabelsize=8,
        bax_yticklabelsize=8,
        bar_width=1,
        bar_color='grey',
        bar_alpha=0.7
    ):
        """
        Drawing transposon insertion frequence on genes.

        Parameters
        -----------
        inspos, inscount : names of variables in `data` or vector data
            Inputs for plotting insertion position and frequency data.
        cds: cds dictionary, genbank file
            A list of dictionary. The dictionary of CDS should use "start,
            end, name, strand, color as corresponding keys".
            Such as:
            [{"start": 10, "end": 50, "strand": 1, "name": "gene1"},
             {"start": 60, "end": 100, "strand": -1, "name": "gene2"},
             {"start": 120, "end": 180, "strand": 1, "name": "gene3"}]
        fig_width : float
            The width of cds arrows axes. Default is 10.
        track_start : int
            The start position of track.
        track_length: int
            The length of track
        track_height: float
            The height of the cds arrows axes.
        track_label : string
            The label text of CDS track.
        track_labelsize : float
            The labelsize of the cds arrows axes.
        track_sublabelpos : string
            Label position ([`top`|`bottom`]-[`left`|`center`|`right`]), Default is "top-left".
        track_sublabelsize: float
            Text size.
        cds_plotstyle : string
            CDS plot style (`bigarrow`|`arrow`|`bigbox`|`box`|`bigrbox`|`rbox`).
        cds_color : matplotlib color
            Single color for the CDS in the plot.
        cds_label : bool
            Whether or not display the CDS label. Default is False.
        cds_labelsize : float
            CDS label size. Default is 6.
        cds_labvpos : string
            Vertical alignment position of CDS label ('top'|'center'|'bottom')
        cds_labhpos : string
            Horizontal alignment posistion of CDS label ('left'|'center'|'right')
        cds_labrotation: float
            The angle of the CDS label.
        cds_arrowshaftratio: float
            The CDS arrow shaft.
        bar_bottompos: float
            The y origin of insert frequency barplot coordinates. Default value is 1.5
        bax_height : float
            The height of the barplot. if the "trackheight" was set to 1 and bax_height is 4,
            then the actual bax_height is 1 * 4. Default value is 4.
        bax_ylabel : string
            The label text.
        bax_ylabelsize : float
            The size of ylabel text.
        bax_xticklabelsize : float
            The size of xticklabel text.
        bax_yticklabelsize : float
            The size of ylabel text.
        bar_width : float
            The width of the insert frequency bar. Default value is 1.
        bar_color : matplotlib color
            The color of the insert frequency bar. Default is 'grey'
        bar_alpha : float
            The transcrepancy of bar.

        Returns
        -------
        Raises
        ------
        Notes
        -----
        References
        ----------
        See Also
        --------
        Examples
        --------

        """

        # Initialize a CDS track
        if track_length is None:
            print("The CDS track length is not set, exit ...")
            sys.exit(1)

        gv = GenomeViz(fig_width=fig_width, fig_track_height=track_height)

        # Set CDS track length
        track = gv.add_feature_track(track_label, labelsize=track_labelsize, segments=(
            int(track_start), int(track_start) + int(track_length) - 1))
        track.add_sublabel(pos=track_sublabelpos, size=float(
            track_sublabelsize))  # add sublabel

        # Get tracklength
        # track_len = int(track.total_seg_size) + 1

        track_end = int(track_start + track_length - 1)

        # Plot CDS
        if cds is None:
            print('No CDS list was passed, exit ...')
            sys.exit(1)
        else:
            for gene in cds:
                if (gene['start'] >= track_start) and (gene['end'] <= track_end):
                    if 'color' in gene.keys():
                        if cds_label and 'name' in gene.keys():
                            track.add_feature(
                                # gene["start"], gene["end"], strand=gene["strand"], label=gene["name"]
                                gene["start"], gene["end"], label=gene["name"], strand=gene['strand'], plotstyle=cds_plotstyle, color=gene['color'],
                                text_kws=dict(vpos=cds_labvpos, hpos=cds_labhpos, rotation=float(cds_labrotation), size=cds_labelsize), arrow_shaft_ratio=float(cds_arrowshaftratio))
                        else:
                            track.add_feature(
                                # gene["start"], gene["end"], strand=gene["strand"], label=gene["name"]
                                gene["start"], gene["end"], label='', strand=gene['strand'], plotstyle=cds_plotstyle, color=gene['color'],
                                text_kws=dict(vpos=cds_labvpos, hpos=cds_labhpos, rotation=float(cds_labrotation), size=cds_labelsize), arrow_shaft_ratio=float(cds_arrowshaftratio))
                    else:
                        if cds_label and 'name' in gene.keys():
                            track.add_feature(
                                # gene["start"], gene["end"], strand=gene["strand"], label=gene["name"]
                                gene["start"], gene["end"], label=gene["name"], strand=gene['strand'], plotstyle=cds_plotstyle, color=cds_color,
                                text_kws=dict(vpos=cds_labvpos, hpos=cds_labhpos, rotation=float(cds_labrotation), size=cds_labelsize), arrow_shaft_ratio=float(cds_arrowshaftratio))
                        else:
                            track.add_feature(
                                # gene["start"], gene["end"], strand=gene["strand"], label=gene["name"]
                                gene["start"], gene["end"], label='', strand=gene['strand'], plotstyle=cds_plotstyle, color=cds_color,
                                text_kws=dict(vpos=cds_labvpos, hpos=cds_labhpos, rotation=float(cds_labrotation), size=cds_labelsize), arrow_shaft_ratio=float(cds_arrowshaftratio))
                else:
                    next

        # Plot CDS track and get the CDS axes
        fig = gv.plotfig()
        cds_ax = fig.axes[0]

        # Add a bar axex aligned with the genome x-axis sharing the x-axis
        bar_ax = fig.add_axes([0, float(bax_bottompos), 1, float(
            bax_height)], sharex=cds_ax)  # [left, bottom, width, height]

        # Plot the bar data
        # change inspos and inscount to numpy array
        inspos_array = np.array(inspos)
        inscount_array = np.array(inscount)
        # filter out insert location less than track_start
        filtered_inspos = inspos_array[inspos_array >= track_start]
        filtered_inspos_index = np.where(inspos_array >= track_start)
        filtered_inscount = inscount_array[filtered_inspos_index]

        # set y_start array
        y_start = list(np.zeros(len(filtered_inspos)))

        # caliberate the insert position with track
        filtered_inspos = filtered_inspos - track_start + 1

        bar_ax.plot([filtered_inspos, filtered_inspos], [y_start, filtered_inscount],
                    linewidth=bar_width,
                    color=bar_color, alpha=bar_alpha)

        bar_ax.set_ylabel(bax_ylabel, fontsize=bax_ylabelsize)
        new_ticklabels = [int(tick + track_start)
                          for tick in bar_ax.get_xticks()]
        # Synchronize tick labels
        xticks = bar_ax.get_xticks()  # Get the current tick positions
        bar_ax.set_xticks(xticks)  # Re-set the ticks to ensure they're fixed
        bar_ax.set_xticklabels(new_ticklabels, fontsize=bax_xticklabelsize)
        # Synchronize tick labels
        # yticks = bar_ax.get_yticks()
        # bar_ax.set_yticks(yticks)
        bar_ax.set_yticklabels(bar_ax.get_yticklabels(),
                               fontsize=bax_yticklabelsize)

        # Step 4: Adjust x-axis ticks to match the genome plot
        # bar_ax.set_xlim(ax.get_xlim())  # Ensure x-limits match
        # Ensure x-limits match
        # bar_ax.set_xlim(track_start, int(track_length) - 1, auto=True)
        bar_ax.spines['top'].set_visible(False)
        bar_ax.spines['right'].set_visible(False)

        plt.tight_layout()
        # plt.show()
        return fig, cds_ax, bar_ax

    def is_genbank(filename):
        """
        Check if the file is a valid genbank file
        """
        try:
            with open(filename, 'r') as file:
                # 尝试解析文件
                record = SeqIO.read(file, "genbank")
                # print("The file is a GenBank file.")
                return True
        except ValueError:
            print("The file is not a GenBank file.")
            return False
        except FileNotFoundError:
            print("File not found.")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    @staticmethod
    def gb2cds(filename):
        """
        Convert genbank to cds list
        [{"start": 10, "end": 50, "strand": 1, "name": "gene1"},
         {"start": 60, "end": 100, "strand": -1, "name": "gene2"},
         {"start": 120, "end": 180, "strand": 1, "name": "gene3"}]
        """
        # initialize a empty list
        parsed_data = {}
        for record in SeqIO.parse(filename, 'genbank'):
            sequence_name = record.id
            parsed_data[sequence_name] = []
            # print(sequence_name)
            for feature in record.features:
                if feature.type == "CDS":  # Extract CDS feature
                    start = int(feature.location.start) + \
                        1  # Start position (1-based)
                    end = int(feature.location.end)  # End position
                    strand = feature.location.strand  # Strand (+1 or -1)
                    gene_name = feature.qualifiers.get(
                        "gene", ["unknown"])[0]  # Gene name

                    # Append the data to the list
                    parsed_data[sequence_name].append({
                        # "sequence_name": sequence_name,
                        "start": start,
                        "end": end,
                        "strand": strand,
                        "name": gene_name,
                    })
        return parsed_data

    @staticmethod
    def _auto_ticks(ax, labels, axis, shape):
        """Determine ticks and ticklabels that minimize overlap."""
        transform = ax.figure.dpi_scale_trans.inverted()
        bbox = ax.get_window_extent().transformed(transform)
        size = [bbox.width, bbox.height][axis]

        axis_tag = axis
        shape.reverse()
        start = shape[axis_tag]
        if axis_tag == 1:
            start = 0
        axis = [ax.xaxis, ax.yaxis][axis_tag]
        tick, = axis.set_ticks([0])
        fontsize = tick.label1.get_size()
        max_ticks = int(size // (fontsize / 72))
        if max_ticks < 1:
            return [], []
        tick_every = len(labels) // max_ticks + 1
        tick_every = 1 if tick_every == 0 else tick_every
        ticks, labels = cvmplot._skip_ticks(
            labels, tick_every, start, axis_tag)
        return ticks, labels

    def rectree(matrix,
                figsize: Optional[Tuple]=None,
                labels: Optional[List]=None,
                no_labels: bool=False,
                scale_max: float=10,
                ax=None):
        """
        Drawing a rectangular dendrogram using scipy dendrogram function.
        Parameters
        -----------
        matrix: linkage matrix
            A matrix returned by scipy.cluster.hierarchy.linkage.
        figsize: (x, y) tuple-like
            1D tuple-like of floats to specify the figure size.
        labels: list
            The list of the sample's name.
        scale_max: float
            The maximum value of the scale.
        ax : matplotlib Axes, optional
            Axes in which to draw the plot, otherwise use the currently-active Axes.


        Returns
        -------
        Raises
        ------
        Notes
        -----
        References
        ----------
        See Also
        --------
        Examples
        --------
        """
        if figsize == None:
            figsize = (15, 15)

        if ax is None:
            ax = plt.gca()
        else:
            ax = ax

        # MatrixS = matrix.shape

        # fig, ax = plt.subplots(1, 1, figsize=figsize)
        dendro_info = dendrogram(
            matrix, ax=ax, orientation='left', no_plot=False, labels=labels, no_labels=no_labels)
        order = dendro_info['ivl']

        # set intervals on axis
        xticklabels = np.arange(0, scale_max, 1)
        ax.set_xticks(ticks=np.arange(0, scale_max, 1), labels=xticklabels)
        ax.set_xlim(scale_max, 0)

        # move spines of ax
        ax.spines[['bottom', 'right', 'left']].set_visible(False)

        # move scale bar on top
        ax.xaxis.tick_top()
        ax.xaxis.set_label_position('top')

        # save plot
        # plt.tight_layout()
        # plt.show()
        return order, ax

    def circulartree(Z2,
                     fontsize: float=8,
                     open_angle: float=0,
                     start_angle: float=0,
                     # figsize: Optional[Tuple]=None,
                     addpoints: bool=False,
                     pointsize: float=15,
                     point_colors: Optional[dict]=None,
                     point_legend_title: str='Category',
                     palette: str="gist_rainbow",
                     addlabels: bool=True,
                     label_colors: Optional[dict]=None,
                     show: bool=True,
                     branch_color: bool=False,
                     sample_classes: Optional[dict]=None,
                     ax=None,

                     colorlabels: Optional[dict]=None,
                     colorlabels_legend: Optional[dict]=None) -> plt.Axes:
        """
        Drawing a radial dendrogram from a scipy dendrogram output.
        Parameters
        ----------
        Z2 : dictionary
            A dictionary returned by scipy.cluster.hierarchy.dendrogram
        fontsize : float
            A float to specify the font size
        palette : string
            Matplotlib colormap name.
        branch_color: bool
            whether or not render branch with colors.
        add_points: bool
            whether or not render leaf point with colors.
        point_colors: dict
            A dictionary to set the color of the leaf point. The Key is the name of the leaflabel.
            The value is the hex color.
            e.g., {'label1':{'#ffffff':'Category1'}, 'label2':{'##f77124':'Catogory2'}...}
        point_legend_title: str
            The title of leaf point legend.
        pointsize: float
            A float to specify the leaf point size
        sample_classes : dict
            A dictionary that contains lists of sample subtypes or classes. These classes appear
            as color labels of each leaf. Colormaps are automatically assigned. Not compatible
            with options "colorlabels" and "colorlabels_legend".
            e.g., {"color1":["Class1","Class2","Class1","Class3", ....]}
        start_angle : float
            The angle of the start point of the circular plot.
            e.g., range from 0 to 360.
        open_angle : float
            The angle of the endpoint of the circular plot.
            e.g., range from 0 to 360.
        addlabels: bool
            A bool to choose if labels are shown.
        label_colors: dict
            A dictionary to set the color of the leaf label. The Key is the name of the leaflabel.
            The value is the hex color.
            e.g., {'label1':'#ffffff', 'label2':'##f77124'...}
        colorlabels_legend : dict
            A nested dictionary to generate the legends of color labels. The key is the name of
            the color label. The value is a dictionary that has two keys "colors" and "labels".
            The value of "colors" is the list of RGB color codes, each corresponds to the class of a leaf.
            e.g., {"color1":{"colors":[[1,0,0,1], ....], "labels":["label1","label2",...]}}
        show : bool
            Whether or not to show the figure.
        Returns
        -------
        Raises
        ------
        Notes
        -----
        References
        ----------
        See Also
        --------
        Examples
        --------
        """
        # if figsize == None and colorlabels != None:
        #     figsize = [7, 5]
        # elif figsize == None and sample_classes != None:
        #     figsize = [7, 5]
        # elif figsize == None:
        #     figsize = [10, 10]

        if ax == None:
            ax = plt.gca()
        else:
            ax = ax
        linewidth = 0.5
        R = 1
        width = R * 0.1
        space = R * 0.05
        if colorlabels != None:
            offset = width * len(colorlabels) / R + space * \
                (len(colorlabels) - 1) / R + 0.05
            print(offset)
        elif sample_classes != None:
            offset = width * len(sample_classes) / R + \
                space * (len(sample_classes) - 1) / R + 0.05
            print(offset)
        else:
            offset = 0

        xmax = np.amax(Z2['icoord'])
        ymax = np.amax(Z2['dcoord'])

        ucolors = sorted(set(Z2["color_list"]))
        # print(f'ucolors is {ucolors}')
        #cmap = cm.gist_rainbow(np.linspace(0, 1, len(ucolors)))
        cmp = plt.get_cmap(palette, len(ucolors))
        # print(cmp)
        if type(cmp) == LinearSegmentedColormap:
            cmap = cmp(np.linspace(0, 1, len(ucolors)))
        else:
            cmap = cmp.colors
        # fig, ax = plt.subplots(figsize=figsize)
        i = 0
        label_coords = []
        leaf_coords = []
        check_coords = []

        # Get the xtick position and create iv_ticks array
        iv_ticks = np.arange(5, len(Z2['ivl']) * 10 + 5, 10)

        for x, y, c in sorted(zip(Z2['icoord'], Z2['dcoord'], Z2["color_list"])):
            if not branch_color:
                _color = 'black'
            else:
                _color = cmap[ucolors.index(c)]
            # _color = 'black'

            # np.abs(_xr1)<0.000000001 and np.abs(_yr1) <0.000000001:
            if c == "C0":
                # print('test')
                _color = "black"

            # transforming original x coordinates into relative circumference positions and y into radius
            # the rightmost leaf is going to [1, 0]
            r = R * (1 - np.array(y) / ymax)
            # _x=np.cos(2*np.pi*np.array([x[0],x[2]])/xmax) # transforming original x coordinates into x circumference positions
            _x = np.cos((2 * np.pi * (360 - open_angle) / 360)
                        * np.array([x[0], x[2]]) / xmax)
            _xr0 = _x[0] * r[0]
            _xr1 = _x[0] * r[1]
            _xr2 = _x[1] * r[2]
            _xr3 = _x[1] * r[3]
            # _y=np.sin(2*np.pi*np.array([x[0],x[2]])/xmax) # transforming original x coordinates into y circumference positions
            # transforming original x coordinates into y circumference positions
            _y = np.sin(2 * np.pi * (360 - open_angle) /
                        360 * np.array([x[0], x[2]]) / xmax)
            _yr0 = _y[0] * r[0]
            _yr1 = _y[0] * r[1]
            _yr2 = _y[1] * r[2]
            _yr3 = _y[1] * r[3]

            # calculate the new coordinate
            new_xr0, new_yr0 = cvmplot.rotate_point(_xr0, _yr0, start_angle)
            new_xr1, new_yr1 = cvmplot.rotate_point(_xr1, _yr1, start_angle)
            new_xr2, new_yr2 = cvmplot.rotate_point(_xr2, _yr2, start_angle)
            new_xr3, new_yr3 = cvmplot.rotate_point(_xr3, _yr3, start_angle)

            # plotting radial lines
            ax.plot([new_xr0, new_xr1], [new_yr0, new_yr1],
                    c=_color, linewidth=linewidth, rasterized=True)
            ax.plot([new_xr2, new_xr3], [new_yr2, new_yr3],
                    c=_color, linewidth=linewidth, rasterized=True)

            # plotting circular links between nodes
            if new_yr1 >= 0 and new_yr2 >= 0:
                link = np.sqrt(
                    r[1]**2 - np.linspace(new_xr1, new_xr2, 10000)**2)
                ax.plot(np.linspace(new_xr1, new_xr2, 10000), link,
                        c=_color, linewidth=linewidth, rasterized=True)
                # ax.plot(link, np.linspace(new_xr1, new_xr2, 10000),
                #         c=_color, linewidth=linewidth, rasterized=True)

            elif new_yr1 <= 0 and new_yr2 <= 0:
                link = -np.sqrt(r[1]**2 -
                                np.linspace(new_xr1, new_xr2, 10000)**2)

                ax.plot(np.linspace(new_xr1, new_xr2, 10000), link,
                        c=_color, linewidth=linewidth, rasterized=True)
            elif new_yr1 >= 0 and new_yr2 <= 0:
                _r = r[1]
                if new_xr1 < 0 or new_xr2 < 0:
                    _r = -_r
                link = np.sqrt(r[1]**2 -
                               np.linspace(new_xr1, _r, 10000)**2)
                # print(link)
                # print(dict(zip(np.linspace(_xr1, _r, 10000), link)))
                ax.plot(np.linspace(new_xr1, _r, 10000), link,
                        c=_color, linewidth=linewidth, rasterized=True)
                link = -np.sqrt(r[1]**2 -
                                np.linspace(_r, new_xr2, 10000)**2)
                # print(link)
                # print(dict(zip(np.linspace(_xr1, _r, 10000), link)))
                ax.plot(np.linspace(_r, new_xr2, 10000), link,
                        c=_color, linewidth=linewidth, rasterized=True)

            else:
                _r = r[1]
                if new_xr1 > 0 or new_xr2 > 0:
                    _r = r[1]
                link = -np.sqrt(r[1]**2 - np.linspace(new_xr1, _r, 10000)**2)

                ax.plot(np.linspace(new_xr1, _r, 10000), link,
                        c=_color, linewidth=linewidth, rasterized=True)
                link = np.sqrt(r[1]**2 - np.linspace(_r, new_xr2, 10000)**2)
                ax.plot(np.linspace(_r, new_xr2, 10000), link,
                        c=_color, linewidth=linewidth, rasterized=True)

                # Calculating the x, y coordinates and rotation angles of labels and the leaf points coordinates

            if y[0] == 0 and x[0] in iv_ticks:
                # print(f'{x[0]},{y[0]}')
                leaf_loc = [x[0], y[0]]
                if leaf_loc not in check_coords:
                    check_coords.append([x[0], y[0]])
                    leaf_coords.append([new_xr0, new_yr0])
                    # test_coords.append([x[0], y[0]])
                    label_coords.append(
                        [(1.05 + offset) * new_xr0, (1.05 + offset) * new_yr0, (360 - open_angle) * x[0] / xmax])
            if y[3] == 0 and x[3] in iv_ticks:
                leaf_loc = [x[3], y[3]]
                # print(f'{x[3]},{y[3]}')
                if leaf_loc not in check_coords:
                    check_coords.append([x[3], y[3]])
                    leaf_coords.append([new_xr3, new_yr3])
                    # test_coords.append([x[3], y[3]])
                    label_coords.append(
                        [(1.05 + offset) * new_xr3, (1.05 + offset) * new_yr3, (360 - open_angle) * x[2] / xmax])
        # a = len(label_coords)
        # b = len(leaf_coords)
        # c = len(check_coords)
        # print(f'label_coords is {a}')
        # print(f'leaf_coords is {b}')
        # print(f'check_coords is {c}')
        # # if y[0] == 0:
        #     label_coords.append(
        #         [(1.05 + offset) * new_xr0, (1.05 + offset) * new_yr0, (360 - open_angle) * x[0] / xmax])
        #     leaf_coords.append([new_xr0, new_yr0])
        #     #plt.text(1.05*_xr0, 1.05*_yr0, Z2['ivl'][i],{'va': 'center'},rotation_mode='anchor', rotation=360*x[0]/xmax)
        #     i += 1
        #     # print('Label_coords')
        #     # print(label_coords)
        # if y[3] == 0:
        #     label_coords.append(
        #         [(1.05 + offset) * new_xr3, (1.05 + offset) * new_yr3, (360 - open_angle) * x[2] / xmax])
        #     leaf_coords.append([new_xr3, new_yr3])
        #     #plt.text(1.05*_xr3, 1.05*_yr3, Z2['ivl'][i],{'va': 'center'},rotation_mode='anchor', rotation=360*x[2]/xmax)
        #     i += 1
        # print(label_coords)

        # print(label_coords)
        if addlabels == True:
            assert len(Z2['ivl']) == len(label_coords), "Internal error, label numbers " + \
                str(len(Z2['ivl'])) + " and " + \
                str(len(label_coords)) + " must be equal!"
            if label_colors != None:
                assert len(Z2['ivl']) == len(label_colors), "Internal error, label numbers " + str(
                    len(Z2['ivl'])) + " and " + str(len(label_colors)) + " must be equal!"
                # Adding labels
                for (_x, _y, _rot), label in zip(label_coords, Z2['ivl']):
                    ax.text(_x, _y, label, {'va': 'center'}, rotation_mode='anchor', color=list(
                        label_colors[label].keys())[0], rotation=_rot + start_angle, fontsize=fontsize)
            else:
                for (_x, _y, _rot), label in zip(label_coords, Z2['ivl']):
                    ax.text(_x, _y, label, {
                            'va': 'center'}, rotation_mode='anchor', rotation=_rot + start_angle, fontsize=fontsize)
        if addpoints == True:
            assert len(Z2['ivl']) == len(label_coords), "Internal error, point numbers " + \
                str(len(Z2['ivl'])) + " and " + \
                str(len(label_coords)) + " must be equal!"
            if point_colors != None:
                assert len(Z2['ivl']) == len(point_colors), "Internal error, label numbers " + str(
                    len(Z2['ivl'])) + " and " + str(len(point_colors)) + " must be equal!"
                for (_x, _y), label in zip(leaf_coords, Z2['ivl']):
                    point = ax.scatter(_x, _y, color=list(
                        point_colors[label].keys())[0], s=pointsize)
                    legend_elements = cvmplot.point_legend(
                        point_colors, fontsize + 2)
                    plt.legend(handles=legend_elements,
                               loc='upper left',
                               bbox_to_anchor=(1.04, 1),
                               title=point_legend_title,
                               fontsize=fontsize + 2, title_fontsize=fontsize + 3, frameon=False)
                    plt.gca().add_artist(point)

            else:
                for (_x, _y), label in zip(leaf_coords, Z2['ivl']):
                    point = ax.scatter(_x, _y, color='g', s=pointsize)
                    plt.gca().add_artist(point)

        # developing...
        # plt.draw()
        # # Plot strip
        # num_samples = 150
        # open_angle = 30
        # num_remove = math.floor(num_samples * open_angle /(360-open_angle))

        # all_samples = num_samples+num_remove
        # all_samples

        # ax.pie(np.ones(all_samples),radius=1.3,startangle=0)
        # circle = plt.Circle((0,0),1.2, fc='white', rasterized=True)
        # plt.gca().add_patch(circle)

        # if colorlabels != None:
        #     assert len(Z2['ivl'])==len(label_coords), "Internal error, label numbers "+str(len(Z2['ivl'])) +" and "+str(len(label_coords))+" must be equal!"

        #     j=0
        #     outerrad=R*1.05+width*len(colorlabels)+space*(len(colorlabels)-1)
        #     # print(outerrad)
        #     #sort_index=np.argsort(Z2['icoord'])
        #     #print(sort_index)
        #     intervals=[]
        #     for i in range(len(label_coords)):
        #         _xl,_yl,_rotl =label_coords[i-1]
        #         _x,_y,_rot =label_coords[i]
        #         if i==len(label_coords)-1:
        #             _xr,_yr,_rotr =label_coords[0]
        #         else:
        #             _xr,_yr,_rotr =label_coords[i+1]
        #         d=((_xr-_xl)**2+(_yr-_yl)**2)**0.5
        #         intervals.append(d)
        #     colorpos=intervals#np.ones([len(label_coords)])
        #     labelnames=[]
        #     for labelname, colorlist in colorlabels.items():
        #         colorlist=np.array(colorlist)[Z2['leaves']]
        #         if j!=0:
        #             outerrad=outerrad-width-space
        #         innerrad=outerrad-width
        #         patches, texts =plt.pie(colorpos, colors=colorlist,
        #                 radius=outerrad,
        #                 counterclock=True,
        #                 startangle=label_coords[0][2]*0.5)
        #         circle=plt.Circle((0,0),innerrad, fc='white')
        #         plt.gca().add_patch(circle)
        #         labelnames.append(labelname)
        #         j+=1

        #     if colorlabels_legend!=None:
        #         for i, labelname in enumerate(labelnames):
        #             print(colorlabels_legend[labelname]["colors"])
        #             colorlines=[]
        #             for c in colorlabels_legend[labelname]["colors"]:
        #                 colorlines.append(Line2D([0], [0], color=c, lw=4))
        #             leg=plt.legend(colorlines,
        #                        colorlabels_legend[labelname]["labels"],
        #                    bbox_to_anchor=(1.5+0.3*i, 1.0),
        #                    title=labelname)
        #             plt.gca().add_artist(leg)
        # elif sample_classes!=None:
        #     assert len(Z2['ivl'])==len(label_coords), "Internal error, label numbers "+str(len(Z2['ivl'])) +" and "+str(len(label_coords))+" must be equal!"

        #     j=0
        #     outerrad=R*1.05+width*len(sample_classes)+space*(len(sample_classes)-1)
        #     print(f'outerrad: {outerrad}')
        #     #sort_index=np.argsort(Z2['icoord'])
        #     #print(sort_index)
        #     intervals=[]
        #     for i in range(len(label_coords)):
        #         _xl,_yl,_rotl =label_coords[i-1]
        #         _x,_y,_rot =label_coords[i]
        #         if i==len(label_coords)-1:
        #             _xr,_yr,_rotr =label_coords[0]
        #         else:
        #             _xr,_yr,_rotr =label_coords[i+1]
        #         d=((_xr-_xl)**2+(_yr-_yl)**2)**0.5
        #         intervals.append(d)
        #     print(f'intervals:{intervals}')
        #     print(f'label_coord:{label_coords}')
        #     colorpos=intervals#np.ones([len(label_coords)])
        #     labelnames=[]
        #     colorlabels_legend={}
        #     for labelname, colorlist in sample_classes.items():
        #         ucolors=sorted(list(np.unique(colorlist)))
        #         type_num=len(ucolors)
        #         _cmp=plt.get_cmap(colormap_list[j])
        #         _colorlist=[_cmp(ucolors.index(c)/(type_num-1)) for c in colorlist]
        #         # print(f'_colorlist0:{_colorlist}')
        #         #rearange colors based on leaf index
        #         _colorlist=np.array(_colorlist)[Z2['leaves']]
        #         # print(f'_colorlist:{_colorlist}')
        #         if j!=0:
        #             outerrad=outerrad-width-space
        #         innerrad=outerrad-width
        #         # print(outerrad, innerrad)
        #         patches, texts =plt.pie(colorpos, colors=_colorlist,
        #                 radius=outerrad,
        #                 counterclock=True,
        #                 startangle=label_coords[0][2]*0.5)
        #         circle=plt.Circle((0,0),innerrad, fc='white')
        #         plt.gca().add_patch(circle)
        #         labelnames.append(labelname)
        #         colorlabels_legend[labelname]={}
        #         colorlabels_legend[labelname]["colors"]=_cmp(np.linspace(0, 1, type_num))
        #         colorlabels_legend[labelname]["labels"]=ucolors
        #         j+=1

        #     if colorlabels_legend!=None:
        #         for i, labelname in enumerate(labelnames):
        #             print(colorlabels_legend[labelname]["colors"])
        #             colorlines=[]
        #             for c in colorlabels_legend[labelname]["colors"]:
        #                 colorlines.append(Line2D([0], [0], color=c, lw=4))
        #             leg=plt.legend(colorlines,
        #                        colorlabels_legend[labelname]["labels"],
        #                    bbox_to_anchor=(1.1, 1.0-0.3*i),
        #                    title=labelname)
        #             plt.gca().add_artist(leg)
                # breakf
        ax.spines.right.set_visible(False)
        ax.spines.top.set_visible(False)
        ax.spines.left.set_visible(False)
        ax.spines.bottom.set_visible(False)
        ax.set_rasterization_zorder(None)
        plt.xticks([])
        plt.yticks([])

        if colorlabels != None:
            maxr = R * 1.05 + width * \
                len(colorlabels) + space * (len(colorlabels) - 1)
        elif sample_classes != None:
            maxr = R * 1.05 + width * \
                len(sample_classes) + space * (len(sample_classes) - 1)
        else:
            maxr = R * 1.05
        ax.set(xlim=(-maxr, maxr), ylim=(-maxr, maxr))

        # plt.legend(loc="upper right")
        plt.subplots_adjust(left=0.05, right=0.85)
        # plt.show()
        return ax

    def heatmap(data,
                order: Optional[List]=None,
                # figsize=None,
                cmap=None,
                yticklabel: bool=True,
                cbar: bool=False,
                vmin: float=0,
                vmax: float=100,
                center=None,
                ax=None):
        """
        Drawing a heatmap that could concatenate to dendrogram.
        Parameters
        -----------
        data : rectangular dataset
            2D dataset that can be coerced into an ndarray. If a Pandas DataFrame
            is provided, the index/column information will be used to label the
            columns and rows.
        order: list
            A list that reindex the input 2D dataset.
        vmin, vmax : floats, optional
            Values to anchor the colormap, otherwise they are inferred from the
            data and other keyword arguments.
        cmap : matplotlib colormap name or object, or list of colors, optional
            The mapping from data values to color space. If not provided, the
            default will depend on whether ``center`` is set.
        yticklabel : bool, optional
            Whether to draw yticklabels.
        cbar : bool, optional
            Whether to draw a colorbar.
        center : float, optional
            The value at which to center the colormap when plotting divergant data.
            Using this parameter will change the default ``cmap`` if none is
            specified.
        ax : matplotlib Axes, optional
            Axes in which to draw the plot, otherwise use the currently-active Axes.

        """
        # We always want to have a DataFrame with semantic information
        # and an ndarray to pass to matplotlib

        # if figsize == None:
        #     figsize = (10, 6)
        # else:
        #     figsize = figsize

        if ax is None:
            ax = plt.gca()

        # process dataframe or ndarray
        if isinstance(data, pd.DataFrame):
            plot_data = data.values
        else:
            plot_data = np.asarray(data)
            data = pd.DataFrame(plot_data)

        # reindex the data frame using the list returned by scipy.cluster.hierarchy.dendrogram
        if order is not None:
            data = data.reindex(order)

        # process colormap
         # Choose default colormaps if not provided
        if cmap is None:
            if center is None:
                cmap = mpl.cm.get_cmap('rocket')
            else:
                cmap = mpl.cm.get_cmap('icefire')
        elif isinstance(cmap, str):
            cmap = cvmplot.get_colormap(cmap)
        elif isinstance(cmap, list):
            cmap = mpl.colors.ListedColormap(cmap)
        else:
            cmap = cmap

        # Recenter a divergent colormap
        if center is not None:

            # Copy bad values
            # in mpl<3.2 only masked values are honored with "bad" color spec
            # (see https://github.com/matplotlib/matplotlib/pull/14257)
            bad = cmap(np.ma.masked_invalid([np.nan]))[0]

            # under/over values are set for sure when cmap extremes
            # do not map to the same color as +-inf
            # under = cmap(-np.inf)
            # over = cmap(np.inf)
            under = '#c8c8c8'
            over = '#c8c8c8'
            under_set = under != cmap(0)
            over_set = over != cmap(cmap.N - 1)

            vrange = max(vmax - center, center - vmin)
            normlize = mpl.colors.Normalize(center - vrange, center + vrange)
            cmin, cmax = normlize([vmin, vmax])
            cc = np.linspace(cmin, cmax, 256)
            cmap = mpl.colors.ListedColormap(cmap(cc))
            cmap.set_bad(bad)
            if under_set:
                cmap.set_under(under)
            if over_set:
                cmap.set_over(over)
        else:
            normlize = mpl.colors.Normalize(vmin, vmax)
            cmin, cmax = normlize([vmin, vmax])
            cc = np.linspace(cmin, cmax, 256)
            cmap = mpl.colors.ListedColormap(cmap(cc))
            under = '#c8c8c8'
            over = '#c8c8c8'
            cmap.set_under(under)
            cmap.set_over(over)

        # get the data shape
        shape = list(data.shape)
        # print(data)

        xticklabels = list(data.columns)
        yticklabels = list(data.index)

        num_xlabels = len(xticklabels)
        num_ylabels = len(yticklabels)
        # print(f'num_ylabels is {num_ylabels}')

        # init a fig and ax
        # fig, ax = plt.subplots(1,1,figsize=figsize)

        # set pcolormesh x and y
        x = np.arange(num_xlabels + 1)
        y = np.arange(0, num_ylabels * 10 + 10, 10)
        # print(x)
        # print(y)
        if cbar == True:
            heatmap = ax.pcolormesh(
                x, y, plot_data, cmap=cmap, vmin=vmin, vmax=vmax, edgecolor='white')
            # axins = inset_axes(ax,
            #                    width="5%",
            #                    height="100%",
            #                    loc='upper left',
            #                    borderpad=0,
            #                    bbox_to_anchor=(1.2, 0., 1, 1),
            #                    bbox_transform=ax.transAxes,
            #                   )
            # axins = ax.inset_axes([0, -0.5, 1, 0.1], zorder=5)
            axins = inset_axes(ax,
                               width="100%",
                               height="10%",
                               loc='lower center',
                               borderpad=-3,
                               axes_kwargs={'zorder': 5},
                               bbox_to_anchor=(0, 0., 1, 1),
                               bbox_transform=ax.transAxes
                               )
            plt.colorbar(heatmap, cax=axins, orientation="horizontal")
        else:
            heatmap = ax.pcolormesh(
                x, y, plot_data, cmap=cmap, vmin=vmin, vmax=vmax, edgecolor='white')

        # adjust the axes and set x,y lim
        ax.set(xlim=(0, data.shape[1]), ylim=(0, data.shape[0] * 10))

        xticks, xticklabels = cvmplot._auto_ticks(ax, xticklabels, 0, shape)
        yticks, yticklabels = cvmplot._auto_ticks(ax, yticklabels, 1, shape)
        ax.set(xticks=xticks, yticks=yticks)
        print(yticks)
        print(yticklabels)
        ax.yaxis.tick_right()
        ax.set_xticklabels(xticklabels)
        if yticklabel:
            ax.set_yticklabels(yticklabels)
        else:
            ax.tick_params(axis='y', right=False, labelright=False)
        return ax

    @staticmethod
    def rotate_point(x: float, y: float, theta: float):
        """
        rotate the given point a angle based on origin (0,0)
        Parameters
        ----------
        x: float
            The x value
        y: float
            The y value
        theta: float
            The rotate angle, range is (0, 360).
        """
        angle = 2 * np.pi * theta / 360

        new_x = x * np.cos(angle) - y * np.sin(angle)
        new_y = x * np.sin(angle) + y * np.cos(angle)
        return new_x, new_y

    @staticmethod
    def point_legend(point_colors: Optional[dict]=None,
                     markersize: float=10):
        """
        Return legend elements.
        Parameters
        ----------
        point_colors: dict
            A dictionary to set the color of the leaf point. The Key is the name of the leaflabel.
            The value is the hex color.
            e.g., {'label1':{'#ffffff':'Category1'}, 'label2':{'##f77124':'Catogory2'}...}
        markersize: float
            A float to specify the markerpoint size.
        Returns
        -------
        Raises
        ------
        Notes
        -----
        References
        ----------
        See Also
        --------
        Examples
        --------
        """
        df = pd.DataFrame.from_dict(point_colors, orient='columns')
        new_df = df.melt(var_name='Labels', value_name='Cate',
                         ignore_index=False)
        new_df.index.name = 'Color'
        new_df.reset_index(inplace=True)
        new_df.dropna(inplace=True)
        new_df.drop_duplicates(subset=['Color', 'Cate'], inplace=True)
        # print(new_df)
        Cate_dict = dict(zip(new_df['Cate'], new_df['Color']))
        legend_element = [Line2D([0], [0], marker='o', color='w', markerfacecolor=Cate_dict[key],
                                 label=key, markersize=markersize) for key in Cate_dict.keys()]
        return legend_element

    @staticmethod
    def get_diff_matrix(array,
                        chunks: Optional[Tuple]=None):
        """
        Function to count the number of differences of values between rows, default ignoring NaN
        Parameters
        ----------
        array: numpy.array
            The array format of the input table
        chunks: (x, y)
            1D tuple-like of floats to specify the chunks size

        Returns
        -------
        A matrix store the number of differenct values between rows.

        Raises
        ------
        Notes
        -----
        References
        ----------
        See Also
        --------
        Examples
        --------
        """
        darray = da.from_array(array, chunks=(100, 100))
        valid_mask = da.logical_and(
            ~da.isnan(darray[:, None]), ~da.isnan(darray))
        diff_count = da.sum(valid_mask, axis=-1) - \
            da.sum(da.equal(darray[:, None], darray), axis=-1)
        diff_matrix = diff_count.compute()
        return diff_matrix

    @staticmethod
    def get_diff_df(df):
        """
        Function to count the number of differences of values between rows, default ignoring NaN
        The index of input dataframe should be your sample name.

        Parameters
        -------------
        df: pandas.dataframe
            The data frame store the MLST/cgMLST or other data

        Returns
        -------
        A dataframe store the number of differenct values between rows with sample name as the dataframe columns or index.

        Raises
        ------
        Notes
        -----
        References
        ----------
        See Also
        --------
        Examples
        --------
        """
        df = df.astype('float')
        labels = list(df.index)
        matrix = df.values
        diff_matrix = cvmplot.get_diff_matrix(matrix)
        diff_df = pd.DataFrame(diff_matrix, index=labels, columns=labels)
        return diff_df

    @staticmethod
    def _skip_ticks(labels, tickevery, startpoint, axis):
        """Return ticks and labels at evenly spaced intervals."""
        n = len(labels)
        if axis == 0:
            startpoint = 0
            if tickevery == 0:
                ticks, labels = [], []
            elif tickevery == 1:
                ticks, labels = np.arange(n) + .5 + startpoint, labels
            else:
                start_tick, end_tick, step_tick = startpoint, startpoint + n, tickevery
                ticks = np.arange(start_tick, end_tick, end_tick) + .5
                start_label, end_label, setp_label = 0, n, tickevery
                labels = labels[start_label:end_label:setp_label]
        else:
            if tickevery == 0:
                ticks, labels = [], []
            elif tickevery == 1:
                ticks, labels = np.arange(
                    0, n * 10, 10) + 5 + startpoint, labels
            else:
                start_tick, end_tick, step_tick = startpoint, startpoint + n * 10, tickevery
                ticks = np.arange(start_tick, end_tick, step_tick) + 5
                start_label, end_label, setp_label = 0, n, tickevery
                labels = labels[start_label:end_label:setp_label]
        return ticks, labels

    def get_colormap(name):
        """Handle changes to matplotlib colormap interface in 3.6."""
        try:
            return mpl.colormaps[name]
        except AttributeError:
            return mpl.cm.get_cmap(name)

    def get_x_positions(tree):
        """Create a mapping of each clade to its horizontal position.

        Dict of {clade: x-coord}
        """
        depths = tree.depths()
        # If there are no branch lengths, assume unit branch lengths
        if not max(depths.values()):
            depths = tree.depths(unit_branch_lengths=True)
        return depths

    def get_y_positions(tree):
        """Create a mapping of each clade to its vertical position.

        Dict of {clade: y-coord}.
        Coordinates are negative, and integers for tips.
        """
        maxheight = tree.count_terminals()
        # Rows are defined by the tips
        heights = {
            tip: maxheight - i for i, tip in enumerate(reversed(tree.get_terminals()))
        }

        # Internal nodes: place at midpoint of children
        def calc_row(clade):
            for subclade in clade:
                if subclade not in heights:
                    calc_row(subclade)
            # Closure over heights
            heights[clade] = (
                heights[clade.clades[0]] + heights[clade.clades[-1]]
            ) / 2.0

        if tree.root.clades:
            calc_row(tree.root)
        return heights

    def phylotree(tree,
                  show_label: bool =True,
                  align_label: bool = False,
                  labelsize: float=8,
                  color: str='k',
                  lw: float=1,
                  ax=None
                  ):
        """
        Plot the given tree using matplotlib

        Parameters
        ----------
        tree: linkage matrix
            tree object from Bio.Phylo.read
        show_label: bool
            Weather or not show the tree leaf labels.
        align_label: book
            Weather or not align the tree leaf labels.
        labelsize: float
            The fontsize of the tree leaf labels.
        color: str
            The line color of the vertical and horizontal lines in the tree.
        lw: float
            the line with of the vertical and horizontal lines in the tree.
        ax : matplotlib Axes, optional
            Axes in which to draw the plot, otherwise use the currently-active Axes.
        """

        def draw_clade(clade, x_start, color, lw, x_posns, y_posns):
            """Recursively draw a tree, down from the given clade."""

            # phyloXML-only graphics annotations
            # if hasattr(clade, "color") and clade.color is not None:
            #     color = clade.color.to_hex()
            # if hasattr(clade, "width") and clade.width is not None:
            #     lw = clade.width * plt.rcParams["lines.linewidth"]

            x_here = x_posns[clade]
            y_here = y_posns[clade] - 0.5

            # recalculate the x,y coordinates
            horizontal_linecollections.append(mpcollections.LineCollection(
                [[(x_start, y_here * 10), (x_here, y_here * 10)]], color=color, lw=lw))
            # horizontal_points.append((x_start,x_here, y_here))
            # horizontal_linecollections.append(mpcollections.LineCollection([[(x_start, y_here), (x_here, y_here)]]))

            # Draw a horizontal line from start to here
            # draw_clade_lines(
            #     use_linecollection=True,
            #     orientation="horizontal",
            #     y_here=y_here,
            #     x_start=x_start,
            #     x_here=x_here,
            #     color=color,
            #     lw=lw,
            # )
            label = str(clade)
            # print(f'The label is {label}')
            # print(f'The class name is {clade.__class__.__name__}')
            if label not in (None, clade.__class__.__name__):
                label_text = f' {label}'
                leaf_coords[y_here * 10] = label
                if show_label and not align_label:
                    label_list.append(
                        (x_here, y_here * 10, label_text, 'center'))
                    # ax.text(
                    #     x_here,
                    #     y_here,
                    #     f" {label}",
                    #     verticalalignment="center",
                    #     # color=get_label_color(label),
                    # )
                elif show_label and align_label:
                    label_list.append(
                        (1.16 * xmax, y_here * 10, label_text, 'center'))
                    dashed_line.append(mpcollections.LineCollection(
                        [[(x_here, y_here * 10), (1.15 * xmax, y_here * 10)]], color='grey', lw=lw, linestyle='dashed'))
                elif not show_label and align_label:
                    assert show_label, "align_label could not be used without show_lable parameter."
                # elif not show_label and not align_label
                else:
                    label_list.append(
                        (xmax, y_here * 10, label_text, 'center'))

            if clade.clades:
                y_top = y_posns[clade.clades[0]] - 0.5
                y_bot = y_posns[clade.clades[-1]] - 0.5
                # print(f'The vertical line is ({x_here}, {y_bot*10})({x_here},{y_top*10})')
                vertical_linecollections.append(mpcollections.LineCollection(
                    [[(x_here, y_bot * 10), (x_here, y_top * 10)]], color=color, lw=lw))
                # vertical_points.append((x_here, y_bot, y_top))
                # vertical_linecollections.append(mpcollections.LineCollection([[(x_here, y_bot), (x_here, y_top)]]))
                for child in clade.clades:
                    # print(f'The key is {child}, the x_here is {x_posns[child]}')
                    draw_clade(child, x_here, color, lw, x_posns, y_posns)
        # get the x and y posns
        x_posns = cvmplot.get_x_positions(tree)
        y_posns = cvmplot.get_y_positions(tree)

        # set xlim and y_lim
        xmax = max(x_posns.values())
        ymax = max(y_posns.values())
        if ax is None:
            ax = plt.gca()
        else:
            ax = ax
        ax.set(xlim=(-0.05 * xmax, 1.25 * xmax), ylim=(0, ymax * 10))
        # set intervals on axis
        xticklabels = np.arange(0, 1.25 * xmax + 0.5, 0.5)
        ax.set_xticks(ticks=np.arange(
            0, 1.25 * xmax + 0.5, 0.5), labels=xticklabels)

        # tree plot
        tree = tree
        color = color
        lw = lw
        align_label = align_label
        show_label = show_label
        labelsize = labelsize
        # set h_line and v_line list
        horizontal_linecollections = []
        vertical_linecollections = []

        # set dashed line list for aligned labels
        dashed_line = []

        # horizontal_points = []
        # vertical_points = []

        # set labels list
        label_list = []
        leaf_coords = {}

        # get horizontal or vertical line
        draw_clade(clade=tree.root, x_start=0, color='k',
                   lw=1, x_posns=x_posns, y_posns=y_posns)

        # def inner functions

        # get the order or the leaf label
        order_label = []
        for key in sorted(leaf_coords.keys()):
            order_label.append(leaf_coords[key])

        # draw phylogenetic tree
        for hline in horizontal_linecollections:
            ax.add_collection(hline)
        for vline in vertical_linecollections:
            ax.add_collection(vline)
        if show_label:
            if align_label:
                for dash in dashed_line:
                    ax.add_collection(dash)
                for label in label_list:
                    ax.text(x=label[0], y=label[1], s=label[2],
                            verticalalignment=label[-1], fontsize=labelsize)
            else:
                for label in label_list:
                    ax.text(x=label[0], y=label[1], s=label[2],
                            verticalalignment=label[-1], fontsize=labelsize)

        # move spines of ax
        ax.spines[['bottom', 'right', 'left']].set_visible(False)

        # move scale bar on top
        ax.xaxis.tick_top()
        ax.xaxis.set_label_position('top')

        # move yticks
        ax.tick_params(axis='y', left=False, labelleft=False)

        return ax, order_label

    def _arrow_patch(
        y_loc: float,
        arrowlabel: str,
        start: float=0,
        end: float=5000,
        strand: int=1,
        color: str="#ec9631",
        ylim: Optional[Tuple]=(-3, 3),
        max_track_size: float=5000,
        no_head_length: bool = False,
        label_track: str='all'
    ) -> FancyArrow:
        """Arrow patch

        Parameters
        ----------
        y_loc: float
            The y coord of the arrow tail.
        start : int
            Start position
        end : int
            End position
        strand: int
            1: forward strand, -1: reverse strand.
        color: str
            The color or the arrow
        ylim : tuple[float, float]
            height of the track limit (Used for calculation of the arrow head width).
        max_track_size : int
            Max track size (Use for head length calculation)
        no_head_length : bool, optional
            If True, set head length as 0

        Returns
        -------
        arrow_patch : FancyArrow
            Arrow patch
        label_coords: tuple
            (label_xcoords, label_ycoords, label)
        """
        # x, y
        x = end if strand == -1 else start

        # for y_loc in np.arange(5, len(order)*10+5, 10):
        y = y_loc

        assert start < end, f"The end position:{end} should great than start:{start} position"
        length = end - start
        dx, dy = length * strand, 0

        # head width
        max_width = ylim[1] - ylim[0]
        head_width = max_width

        # lable coords
        label_x = x + length * strand / 2
        label_y = y_loc + max_width / 2 + 1

        label_coords = (label_x, label_y, arrowlabel)

        # print(label_coords)

        # if self.is_bigstyle:
        #     head_width = max_width
        # else:
        #     head_width = max_width / 2
        # shaft_width
        shaft_width = head_width * 0.5
        # head length
        head_length = max_track_size * 0.015
        if length < head_length:
            head_length = length

        if no_head_length:
            head_length = 0
            head_width = shaft_width
        # print(f'head_width is {head_width}')
        # print(f'head_length is {head_length}')

        if color == None:
            color = "#ec9631"

        arrow = FancyArrow(
            x,
            y,
            dx,
            dy,
            width=shaft_width,
            length_includes_head=True,
            head_width=head_width,
            head_length=head_length,
            color=color
        )

        return arrow, label_coords

    def get_arrows(dc: Optional[Dict],
                   order: Optional[List],
                   label_track: str='all',
                   ylim: Optional[Tuple]=(-3, 3)
                   ):
        """
        Parameter
        ---------
        dc: Dict
            The Dict of the arrow corresponding info.
            {'yticklabel':[(start, end, strand, arrowlabel, color), (start, end, strand, arrowlabel, color)...]}
        order: list
            The list or the yticklabels (Used for the y coordinates of arrow tail).
        label_track: {'all', 'top', 'bottom'}, default: 'all'
            The track that the label should be showed.

        Returns
        ------
        arrow_patches : list of FancyArrow
            Arrow patch list
        label_coords: list
            [(label_xcoords, label_ycoords, label1), (label_xcoords, label_ycoords, label2), ...]
        """
        arrows = []
        arrowlabels = []
        if isinstance(order, list):
            num_yticks = len(order)
            ticks_order = np.arange(5, 10 * num_yticks + 5, 10)
        # get the top and bottom track
        max_track = ticks_order[-1]
        min_track = ticks_order[0]

        # check label_track
        assert label_track in ['top', 'bottom',
                               'all'], f'{label_track} not in the choosable list]'

        if isinstance(dc, dict):
            for yticklabel, ytick in zip(order, ticks_order):
                for arrow in dc[yticklabel]:
                    start, end, strand, arrowlabel, color = arrow['START'], arrow[
                        'END'], arrow['STRAND'], arrow['LABEL'], arrow['COLOR']
                    arrows.append(cvmplot._arrow_patch(
                        start=start, end=end, strand=strand, arrowlabel=arrowlabel, color=color, y_loc=ytick, ylim=ylim)[0])
                    if label_track == 'all':
                        arrowlabels.append(cvmplot._arrow_patch(
                            start=start, end=end, strand=strand, arrowlabel=arrowlabel, color=color, y_loc=ytick, ylim=ylim)[1])
                    elif label_track == 'top':
                        if ytick == max_track:
                            arrowlabels.append(cvmplot._arrow_patch(
                                start=start, end=end, strand=strand, arrowlabel=arrowlabel, color=color, y_loc=ytick, ylim=ylim)[1])
                        else:
                            next
                    if label_track == 'bottom':
                        if ytick == min_track:
                            arrowlabels.append(cvmplot._arrow_patch(
                                start=start, end=end, strand=strand, arrowlabel=arrowlabel, color=color, y_loc=ytick, ylim=ylim)[1])
                        else:
                            next

        return arrows, arrowlabels

    def plotgenes(dc=Optional[Dict],
                  order=Optional[List],
                  addlabels: bool=False,
                  ax=None,
                  max_track_size: int=5000,
                  trackname_size: int = 18,
                  label_track: str='all',
                  label_rot: int=45,
                  label_size: int=12,
                  ylim: Optional[Tuple]=(-3, 3)
                  ) -> plt.Axes:
        """
        Drawing the gene environment.

        Paramters
        ---------
        dc: dict
            The Dict of the arrow corresponding info.
            {'yticklabel':[("START":0, "END":1000, "STRAND":1, "ARROWLABEL":'test', "COLOR":'#ec9631'),
                           ("START":1500, "END":2500, "STRAND":-1, "ARROWLABEL":'test1', "COLOR":'#ec9631'),...]}.
        order: list
            The yticklabels order
        ax : matplotlib Axes, optional
            Axes in which to draw the plot, otherwise use the currently-active Axes.
        max_track_size: int.
            Max track size (Use for head length calculation).
        label_track: {'all', 'top', 'bottom'}, default: 'all'
            The track that the label should be showed.
        label_rot: float
            The rotation angle of the label.
        label_size: float
            The label size of the labels.
        ylim : tuple[float, float]. Default:(-3,3)
            height of the track limit (Used for calculation of the arrow head width).


        Returns
        ---------
        plt.Axes
        """
        # arrows, labels = cvmplot.get_arrows(arrow_dict, order)
        if ax is None:
            ax = plt.gca()
        else:
            ax = ax
        arrows, labels = cvmplot.get_arrows(
            dc=dc, order=order, label_track=label_track, ylim=ylim)
        # print(labels)

        if addlabels:
            for label in labels:
                ax.text(x=label[0], y=label[1], s=label[2], fontdict={'rotation': label_rot, 'ha': 'left',
                                                                      'fontsize': label_size
                                                                      })

        # add arrows
        for arrow in arrows:
            ax.add_patch(arrow)

        # add tracks or hlines
        for y_loc in np.arange(5, 10 * len(order) + 5, 10):
            ax.hlines(y=y_loc, xmin=0, xmax=max_track_size,
                      zorder=0, color='#757575', linewidth=1)

        # ax settings
        ax.set_yticks(np.arange(5, 10 * len(order) + 5, 10),
                      labels=order, fontsize=trackname_size)
        # ax.set_yticklables(ax.get_yticklabels(), fontsize=trackname_size)
        ax.set_xlim(0, max_track_size)
        ax.set_ylim(0, 10 * len(order))
        ax.spines[['top', 'left', 'right']].set_visible(False)
        ax.tick_params(axis='y', right=False)
        ax.yaxis.tick_right()
        return ax
