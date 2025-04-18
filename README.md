# Company Information Search API

# Overview:
This Flask-based API enables users to search for company information on the internet. The search functionality leverages the Google search engine and integrates seamlessly with Gemini for advanced queries. Data sources will be used:
- masothue.com
- bocaodientu.dkkd.gov.vn

# Environment Configuration:
- API_KEY (string, required with dkkd search): Gemini API key for authentication.
- PROMPT (string, required with dkkd search): Custom prompt used to interact with Gemini.
<!-- - PROXIES (string, optional): Comma-separated list of proxy URLs to use for searching with Google, to prevent bot detection errors. -->
- PROXY_SERVER (string, optional): URL of the proxy server to route requests through, useful for bypassing restrictions or avoiding bot detection.
- POOL_SIZE (integer, default 2): Number of concurrent threads or processes to use for handling requests, optimizing performance for high traffic.

# Endpoints:
[GET] /search
Retrieve company details based on the specified parameters.

Query Parameters:
- company_name (string, required): Name of company to search for.
- engine (string, optional): Search engine [google (default), dkkd].
- type (string, optional): Search type [quick (default), full].
- ann_type (string, optional): Announcement type on dkkd.gov.vn [NEW, AMEND (default), CORP, OTHER, CHANTC, REVOKE].