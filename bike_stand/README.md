Survey123 URL Info
I am going to do my best to document everything I have figured out about the url format so that if things change you are able to figure things out

Survey link: `https://survey123.arcgis.com/share/<SURVEY_ID>`

Survey Results Dashboard: `https://survey123.arcgis.com/share/<SURVEY_ID>/result`
  - This should take you to a dashboard that allows you to see aggregated responses over some time period

The next thing to figure out is the organization id. This can be found by going to the `/result` dashboard,
inspecting element and then going to the network tab and then refreshing the page. You will see a lot of network
requests. You care about network requests with the following url format:
`https://services.arcgis.com/<ORG_ID>/arcgis/rest/services/survey123_<SURVEY_ID>_results/FeatureServer/0/...`
you can add ?f=json to the end of the url to get the raw data


To get use information about a survey, go to the following url (as in enter this url into your browser):
`https://services.arcgis.com/<ORG_ID>/arcgis/rest/services/survey123_<SURVEY_ID>_results/FeatureServer/0`

The most important info is the fields section which should tell you the names of the fields asked in the survey.
I think this is the documentation link: `https://developers.arcgis.com/rest/services-reference/enterprise/layer-feature-service/`
for the above url.

To query for results, I use the url format:
- `https://services.arcgis.com/<ORG_ID>/arcgis/rest/services/survey123_<SURVEY_ID>_results/FeatureServer/0/query`
- documentation: https://developers.arcgis.com/rest/services-reference/enterprise/query-feature-service-layer/

To get the attachments related to a specific survey response, the url format is:
- `https://services.arcgis.com/<ORG_ID>/arcgis/rest/services/survey123_<SURVEY_ID>_results/FeatureServer/0/<OBJECT_ID>/attachments`
where <OBJECT_ID> is the "objectid" field from an individual response
- documentation: https://developers.arcgis.com/rest/services-reference/enterprise/attachment-infos-feature-service/

For attachment urls (photos, files, etc uploaded by the user in the survey), the link format to the resource is:
- `https://services.arcgis.com/<ORG_ID>/arcgis/rest/services/survey123_<SURVEY_ID>_results/FeatureServer/0/<OBJECT_ID>/attachments/<attachmentId>`
where the attachment id comes from the above api call.
- documentation: https://developers.arcgis.com/rest/services-reference/enterprise/attachment-feature-service/

Finally, the url format to view a specific response is:
- `https://survey123.arcgis.com/share/<SURVEY_ID>?mode=view&globalId=<GLOBAL_ID>`
where global id comes from a specific response.
- documentation: https://doc.arcgis.com/en/survey123/get-started/integrate-launchwebapp.htm