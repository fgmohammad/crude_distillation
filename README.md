# crude_distillation
Distillation profile model for blend of two crude oils. The data being used are obtained from crudemonitor.ca using web scraping.

# Model
The model estimates the distillation profile, i.e. the fraction of oil evaporated at temperature T, for a blend of two crude oils given their individual distillation profiles.

### Assumptions
1. The blend is an emulsion of the two crude oils rather than a new chemical compound, i.e. we assume that both oils preserve their physical and chemical properties;
2. The shrinkage effect in volume after blending is negligible;
3. Distillation profiles for each crude oil are given as discrete snapshots of an otherwise continuous fucntion. We assume that the function at intermediate points between two snapshots is locally linear;
4. We also assume the the function, that describes the distillation profile, linarly extends beyond the minimum and maximum values reported in the HSTD table on crudemonitor.ca;
