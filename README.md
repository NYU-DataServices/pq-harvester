# pq-harvester
Harvester for the licensed text as data content from PQ

## Considerations

 - Does PQ use any relative links in their anchor tags?
 - Do the anchor tags contain useful contents that can be used to structure containing folders?
 - What IDs are embedded in the links/anchor contents that need to be extracted to name files?
 - Any advantage to adding a readme doc in each folder that aggregates any metadata from the xml, or re-crawl downloaded xml and create that later?
 - How exactly to respond in case of a 403 or 404 error? Shut down script or record the URL that didn't work and keep going? 
