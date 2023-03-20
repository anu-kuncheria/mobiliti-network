# mobiliti-network

This repository enumerates the procedures undertaken to convert Here Map to Mobiliti Map. 

```mermaid
graph LR;
    unidirectional_links.py-->link_attributes.py-->length_attribute.py-->filter_ferry.py-->filter_access_restriction-->internalintersection_update-->speed_update;
```

After executing the aforementioned pipeline, a fully processed California network is generated, which can subsequently be clipped according to the specified region of interest.

