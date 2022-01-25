# crude_distillation
Distillation profile model for blend of two crude oils. The data being used are obtained from crudemonitor.ca using web scraping.

## Requirements
bs4<br>
pandas<br>
requests<br>

## Usage
- `$ python 01-get_crudes_list.py` will scrape the list of crudes from crudemonitor.ca and save it to `crudes_list.csv`
- `$ python 02-scrape_htsd_data.py` will read the list of crudes from `crudes_list.csv`, scrape their High-Temperature Simulated Distillation (HTSD) tables from crudemonitor.ca and save them into individual `.csv` files in `./data/`
- `$ python 03-blend_distillation.py --name_a 'name_crude_a' --name_b 'name_crude_b' --frac_a frac_a --fname 'PathTo_crudes_list.csv'` will read crudes abbreviations from `crudes_list.csv` HTSD data for crude_a and crude_b from `./data/` and generate the distillation profile for the blend of crude_a with fractional volume frac_a and crude_b with fractional volume (1-frac_a)
- `03-blend_distillation_notebook.ipynb` is the interactive version of `03-blend_distillation.py` and also includes some tests of the model.

__If you clone the repository then you can skip `$ python 01-get_crudes_list.py` and `$ python 02-scrape_htsd_data.py`__

## Model
The model estimates the distillation profile, i.e. the fraction of oil evaporated at temperature T, for a blend of two crude oils given their individual distillation profiles.

### Assumptions
1. The blend is an emulsion of the two crude oils rather than a new chemical compound, i.e. we assume that both oils preserve their physical and chemical properties;
2. The shrinkage effect in volume after blending is negligible;
3. Distillation profiles for each crude oil are given as discrete snapshots of an otherwise continuous fucntion. We assume that the function at intermediate points between two snapshots is locally linear;
4. We also assume the the function, that describes the distillation profile, linarly extends beyond the minimum and maximum values reported in the HSTD table on crudemonitor.ca;
5. During distillation the density of each crude oil (not evaporated) is constant;

### Derivation

* <img src="https://render.githubusercontent.com/render/math?math=V">   -> Volume of the blend<br>
* <img src="https://render.githubusercontent.com/render/math?math=f_{V,a}"> -> Crude a fractional volume in the blend<br>
* <img src="https://render.githubusercontent.com/render/math?math=f_{V,b}"> -> Crude b fractional volume in the blend<br>
with the constraint that:
<p align='center'> <img src="https://render.githubusercontent.com/render/math?math=f_{V,a}%2Bf_{V,b} = 1"> </p>
<br>

* <img src="https://render.githubusercontent.com/render/math?math=\alpha_a(T)"> -> Fraction of Crude a evaporated at T<br>
* <img src="https://render.githubusercontent.com/render/math?math=\alpha_b(T)"> -> Fraction of Crude b evaporated at T<br>
<br>
At temperature T the blend volume evaporated:<br>
    <p align='center'><img src="https://render.githubusercontent.com/render/math?math=V(T)=\left[\alpha_a(T)f_{V,a}%2B\alpha_b(T)(1-f_{V,a})\right]V"><br></p>
This gives the final model:<br>
    <p align='center'><img src="https://render.githubusercontent.com/render/math?math=\alpha(T)=\left[\alpha_a(T)f_{V,a}%2B\alpha_b(T)(1-f_{V,a})\right]"><br></p>
<br>

