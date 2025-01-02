# Description:
This Flask API allows you to search for company information by name on the website masothue.com, bocaodientu.dkkd.gov.vn using google engine. 

# Route:
[GET] /search

Query Parameters:
- company_name (string, required): Name of company to search.
- engine (string, optional): Search engine [google, dkkd], default google.
- type (string, optional): Search type [quick, full], default quick.