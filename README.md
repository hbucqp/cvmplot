# cvmplot
![PyPI - Version](https://img.shields.io/pypi/v/cvmplot)
![Static Badge](https://img.shields.io/badge/OS-_Windows_%7C_Mac_%7C_Linux-steelblue)

## Table of content

- [Overview](#overview)
- [Installation](#installation)
- [API Examples](#api-examples)




## Overview
cvmplot is a data visualization python package for SZQ lab used in TransposonSequencing/cgMLST/wgMLST data analysis based on matplotlib.

## Installation
`Python 3.9 or later` is required for installation.

**Install PyPI package:**

    pip3 install cvmplot

## API Examples

Jupyter notebooks containing code examples below is available [here](https://github.com/hbucqp/cvmplot/blob/main/demo/tnseqplot_demo.ipynb).

### General plot
```python
import random
from cvmplot.cvmplot import cvmplot as cvmplot

# prepare cds data
gene_data = [
    {"start": 11120, "end": 13800, "strand": 1, "name": "gene1", 'color':'red'},
    {"start": 14231, "end": 15286, "strand": -1, "name": "gene2", 'color':'lightblue'},
    {"start": 16868, "end": 18212, "strand": 1, "name": "gene3", 'color':'green'},
    {"start": 18500, "end": 19863, "strand": -1, "name": "gene4", 'color':'blue'},
    {"start": 20123, "end": 24632, "strand": 1, "name": "gene5", 'color':'#d1af3f'},
    {"start": 25159, "end": 27000, "strand": -1, "name": "gene6", 'color':'cyan'},
    {"start": 27360, "end": 29888, "strand": 1, "name": "gene7", 'color':'#f9d9d9'},
]


bar_positions = np.random.randint(10000, 30000, size=1000) # Bar x-axis positions
bar_data = np.random.randint(50,100, size=1000) # Bar plot values


fig, cds_ax, bar_ax = cvmplot.tnseqplot(inspos=bar_positions, inscount=bar_data, cds=gene_data, track_length=20000,
                                   cds_label=True, cds_labelsize=7, cds_labrotation=45, track_start=10000, cds_color='lightblue'
                                  )

bar_ax.set_ylabel('Insert frequency')
plt.show()

fig.savefig('general_plot.png', bbox_inches='tight')
```
![general_plot.png](https://github.com/hbucqp/cvmplot/blob/main/demo/general_plot.png)

### Add CDS track name using track_label
```python
fig, cds_ax, bar_ax = cvmplot.tnseqplot(inspos=bar_positions, inscount=bar_data, cds=gene_data, track_length=20000,
                                   cds_label=True, cds_labelsize=7, cds_labrotation=45, track_start=10000, track_label='GENEs'
                                  )

bar_ax.set_ylabel('Insert frequency')
plt.show()
fig.savefig('tracklabel_plot.png', bbox_inches='tight')
```
![tracklabel_plot.png](https://github.com/hbucqp/cvmplot/blob/main/demo/tracklabel_plot.png)


### Change CDS track label size using track_labsize
```python
fig, cds_ax, bar_ax = cvmplot.tnseqplot(inspos=bar_positions, inscount=bar_data, cds=gene_data, track_length=20000,
                                   cds_label=True, cds_labelsize=7, cds_labrotation=45, track_start=10000, track_label='GENEs',
                                   track_labelsize=8
                                  )

bar_ax.set_ylabel('Insert frequency')
plt.show()
fig.savefig('tracklabelsize_plot.png', bbox_inches='tight')
```
![tracklabelsize_plot.png](https://github.com/hbucqp/cvmplot/blob/main/demo/tracklabelsize_plot.png)



### Change the height of CDS track using track_height
```python
fig, cds_ax, bar_ax = cvmplot.tnseqplot(inspos=bar_positions, inscount=bar_data, cds=gene_data, track_length=20000,
                                   cds_label=True, cds_labelsize=7, cds_labrotation=45, track_start=10000, track_label='GENEs',
                                   track_labelsize=8, track_height=0.3,
                                  )

bar_ax.set_ylabel('Insert frequency')
plt.show()
fig.savefig('trackheight_plot.png', bbox_inches='tight')
```
![trackheight_plot.png](https://github.com/hbucqp/cvmplot/blob/main/demo/trackheight_plot.png)


### Adjust the space between CDS track and insertion bar plot using bax_bottompos


```python
fig, cds_ax, bar_ax = cvmplot.tnseqplot(inspos=bar_positions, inscount=bar_data, cds=gene_data, track_length=20000,
                                   cds_label=True, cds_labelsize=7, cds_labrotation=45, track_start=10000, track_label='GENEs',
                                   track_labelsize=8, track_height=0.3, bax_bottompos=2
                                  )

bar_ax.set_ylabel('Insert frequency')
plt.show()
fig.savefig('bax_bottompos.png',  bbox_inches='tight')
```
![bax_bottompos.png](https://github.com/hbucqp/cvmplot/blob/main/demo/bax_bottompos.png)


### Display gene labels or not using cds_label
```python
fig, cds_ax, bar_ax = cvmplot.tnseqplot(inspos=bar_positions, inscount=bar_data, cds=gene_data, track_length=20000,
                                   cds_label=False, cds_labelsize=7, cds_labrotation=45, track_start=10000, track_label='GENEs',
                                   track_labelsize=8, track_height=0.3, bax_bottompos=2
                                  )

bar_ax.set_ylabel('Insert frequency')
plt.show()
fig.savefig('cds_label.png',  bbox_inches='tight')
```

![cds_label.png](https://github.com/hbucqp/cvmplot/blob/main/demo/cds_label.png)


### Adjust the CDS track name using track_labelsize

```python
fig, cds_ax, bar_ax = cvmplot.tnseqplot(inspos=bar_positions, inscount=bar_data, cds=gene_data, track_length=20000,
                                   cds_label=False, cds_labelsize=7, cds_labrotation=45, track_start=10000, track_label='GENEs',
                                   track_height=0.3, bax_bottompos=2, track_labelsize=15
                                  )

bar_ax.set_ylabel('Insert frequency')
plt.show()
fig.savefig('tracklabelsize.png', bbox_inches='tight')
```

![tracklabelsize.png](https://github.com/hbucqp/cvmplot/blob/main/demo/tracklabelsize.png)


### Change the track sublabel using track_sublabelpos
```python
fig, cds_ax, bar_ax = cvmplot.tnseqplot(inspos=bar_positions, inscount=bar_data, cds=gene_data, track_length=20000,
                                   cds_label=False, cds_labelsize=7, cds_labrotation=45, track_start=10000, track_label='GENEs',
                                   track_height=0.3, bax_bottompos=2.2, track_labelsize=8, track_sublabelpos='top-right'
                                  )

bar_ax.set_ylabel('Insert frequency')
plt.show()
fig.savefig('track_sublabelpos_plot.png', bbox_inches='tight')

```
![track_sublabelpos_plot.png](https://github.com/hbucqp/cvmplot/blob/main/demo/track_sublabelpos_plot.png)

### Change the insertion frequency barplot color using bar_color

```python
fig, cds_ax, bar_ax = cvmplot.tnseqplot(inspos=bar_positions, inscount=bar_data, cds=gene_data, track_length=20000,
                                   cds_label=False, cds_labelsize=7, cds_labrotation=45, track_start=10000, track_label='GENEs',
                                   track_height=0.3, bax_bottompos=2.2, track_labelsize=8, track_sublabelpos='top-right',
                                   bar_color='lightblue'
                                  )

bar_ax.set_ylabel('Insert frequency')
plt.show()
fig.savefig('barcolor_plot.png', bbox_inches='tight')
```
![barcolor_plot.png](https://github.com/hbucqp/cvmplot/blob/main/demo/barcolor_plot.png)

### Change the insertion frequency barplot height using bax_height
```python

fig, cds_ax, bar_ax = cvmplot.tnseqplot(inspos=bar_positions, inscount=bar_data, cds=gene_data, track_length=20000,
                                   cds_label=False, cds_labelsize=7, cds_labrotation=45, track_start=10000, track_label='GENEs',
                                   track_height=0.3, bax_bottompos=2.2, track_labelsize=8, track_sublabelpos='top-right',
                                   bar_color='lightblue', bax_height=7
                                  )

bar_ax.set_ylabel('Insert frequency')
plt.show()
fig.savefig('bax_height_plot.png', bbox_inches='tight')

```
![bax_height_plot.png](https://github.com/hbucqp/cvmplot/blob/main/demo/bax_height_plot.png)


### Change the cds arrow using cds_arrowshaftratio
```python
fig, cds_ax, bar_ax = cvmplot.tnseqplot(inspos=bar_positions, inscount=bar_data, cds=gene_data, track_length=20000,
                                   cds_label=False, cds_labelsize=7, cds_labrotation=45, track_start=10000, track_label='GENEs',
                                   track_height=0.3, bax_bottompos=2.2, track_labelsize=8, track_sublabelpos='top-right',
                                   bar_color='lightblue', bax_height=4, cds_arrowshaftratio=1
                                  )

bar_ax.set_ylabel('Insert frequency')
plt.show()
fig.savefig('cds_arrowshaftratio_plot.png', bbox_inches='tight')
```


![cds_arrowshaftratio_plot.png](https://github.com/hbucqp/cvmplot/blob/main/demo/cds_arrowshaftratio_plot.png)


### Generate gene data from genbank file

**gb2cds('GENEBANKE_FILE.gb')** function will return a dict with contigs name as key and a list as value including the CDS 'start, end, strand, name, color' used in tnseqplot funtion


```python
cds_data = cvmplot.gb2cds('HA3S26.gbff')
gene_data = cds_data['NODE_1_length_1210584_cov_117.87540']

# Simulate the insertion data in the range of 1-20000
bar_positions = np.random.randint(1, 20000, size=500) # Bar x-axis positions
bar_data = np.random.randint(50,100, size=500) # Bar plot values


fig, cds_ax, bar_ax = cvmplot.tnseqplot(inspos=bar_positions, inscount=bar_data, cds=gene_data, track_start=1,
                                   track_length=20000, cds_label=False, track_height=0.3, bax_bottompos=2
                                  )

bar_ax.set_ylabel('Insert frequency')
plt.show()
fig.savefig('genbank_plot.png', bbox_inches='tight')
```

![genbank_plot.png](https://github.com/hbucqp/cvmplot/blob/main/demo/genbank_plot.png)
