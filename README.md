# mobiliti-network

This repo lists the steps taken to transform Here Map to Mobiliti Map. 

```mermaid
graph LR;
    unidirectional_links.py-->link_attributes.py-->length_attribute.py-->filter_ferry.py-->filter_access_restriction-->internalintersection_update-->speed_update;
```