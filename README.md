# mobiliti-network

This repository contains the scripts to convert Here Map to Mobiliti Map. The following is the order in which these steps are executed. 

```mermaid
graph LR;
    unidirectional_links.py-->link_attributes.py-->length_attribute.py-->filter_ferry.py-->filter_access_restriction.py-->update_internalintersection.py-->update_speed.py;
```

After executing the aforementioned pipeline, a fully processed California network is generated, which can subsequently be clipped according to the specified region of interest.



