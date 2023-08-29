import requests, json, dateutil, datetime
from typing import ByteString, Union, List


class Redfin:
    def __init__(self, headers: dict = {"user-agent": ""}):
        """
        Args:
            headers (dict, optional): Default header for the requests. If you do not include user-agent, Redfin will block all requests. Defaults to {"user-agent": ""}.
        """
        self.base = "https://redfin.com/stingray/"
        self.headers = headers

    def redfin_request(self, url: str, params: dict = {}) -> requests.Response:
        """
        Used to make basic requests to Redfin's API. This is intended as a helper function; however, this is usable as long as you know the full API endpoint you would like to use.

        Args:
            url (str): The endpoint for your API request.
            params (dict, optional): Query parameters for the request. Defaults to {}.

        Returns:
            requests.Response:
        """
        response = requests.get(self.base + url, params=params, headers=self.headers)
        response.raise_for_status()
        return response

    def request_property_data(self, url: str, params: dict, page: bool = False) -> dict:
        """
        Used to make basic requests to Redfin's API endpoint that begins with 'api/home/details/'. This is intended as a helper function; however, this is usable as long as you know the full API endpoint you would like to use.

        Args:
            url (str): The endpoint for your API request.
            params (dict): Query parameters for the request.
            page (bool, optional): Not really sure what this does. Defaults to False.

        Returns:
            dict: Returns a dictionary of the requested data.
        """
        if page:
            params["pageType"] = 3
        response = self.redfin_request(
            url="api/home/details/" + url, params={"accessLevel": 1, **params}
        )
        return_dict = self._format_response(response)
        return return_dict

    def request_region_data(
        self,
        url: str,
        region_type: Union[str, int],
        region_id: Union[str, int],
        property_type: Union[str, int] = "",
    ) -> dict:
        """_summary_

        Args:
            url (str): _description_
            region_type (Union[str, int]): _description_
            region_id (Union[str, int]): _description_
            property_type (Union[str, int], optional): _description_. Defaults to "".

        Returns:
            dict: _description_
        """
        if property_type == "":
            request_url = f"api/region/{region_type}/{region_id}/{url}"
        else:
            request_url = f"api/region/{region_type}/{region_id}/{property_type}/{url}"
        response = self.redfin_request(url=request_url)
        return_dict = self._format_response(response)
        return return_dict

    def _format_response(self, response: requests.Response) -> dict:
        """
        Takes a response from a Redfin endpoint and formats it into a dict.

        Args:
            response (requests.Response): A response from a self.redfin_request or self.request_property_data

        Returns:
            dict: A formatted response from Redfin
        """
        return_dict = json.loads(response.text[4:])
        return return_dict

    def search(self, query: str, **kwargs) -> dict:
        """
        A transformed response from a standard search in at redfin.com

        Args:
            query (str): the search you would enter in at redfin.com

        Returns:
            dict: A transformed response from Redfin's search endpoint. Redfin returns a string
            that needs to be transformed to be useful.
        """
        response = self.redfin_request(
            url="do/location-autocomplete", params={"location": query, "v": 2, **kwargs}
        )
        return_dict = self._format_response(response)
        return return_dict

    def get_region_id(self, search_response: dict) -> str:
        """
        Takes a Redfin.search() dict and returns the region_id associated with the search

        Args:
            search_response (dict): A dictionary response from Redfin.search()

        Returns:
            str: A string for the region id needed to download houses related to your given
            search criteria.
        """
        region_id = search_response["payload"]["sections"][0]["rows"][0]["id"].rsplit(
            "_"
        )[1]
        return region_id

    def get_search_results_table(
        self,
        region_id: Union[str, int],
        region_type: Union[str, int],
        al: int = 1,
        has_deal: bool = False,
        has_dishwasher: bool = False,
        has_laundry_facility: bool = False,
        has_laundry_hookups: bool = False,
        has_parking: bool = False,
        has_pool: bool = False,
        has_short_term_lease: bool = False,
        include_pending_homes: bool = False,
        is_rentals: bool = False,
        is_furnished: bool = False,
        market: str = "dc",
        num_homes: int = 5000,
        ord: str = "redfin-recommended-asc",
        page_number: int = 1,
        sold_within_days: int = 1825,
        status: int = 9,
        travel_with_traffic: bool = False,
        travel_within_region: bool = False,
        uipt: str = "1,2,3,4,5,6,7,8",
        utilities_included: bool = False,
        v: int = 8,
    ) -> ByteString:
        """_summary_

        Args:
            region_id (Union[str,int]): Redfin unique id for the region associated with your search. The value is
            obtained by using self.get_region_id.
            region_type (Union[str,int]): Redfin region type for your query:  1-neighborhood, 2-ZIP code, 5-County, 6-City.
            al (int, optional): _description_. Defaults to 1.
            has_deal (bool, optional): _description_. Defaults to False.
            has_dishwasher (bool, optional): property must have dishwasher. Defaults to False.
            has_laundry_facility (bool, optional): Property must have laundry facility. Defaults to False.
            has_laundry_hookups (bool, optional): Property must have laundry hookups. Defaults to False.
            has_parking (bool, optional): Property must have parking. Defaults to False.
            has_pool (bool, optional): Property must have pool. Defaults to False.
            has_short_term_lease (bool, optional): Property must allow short term leases. Defaults to False.
            include_pending_homes (bool, optional): Include pending sales in search results. Defaults to False.
            is_rentals (bool, optional): Include rental properties. Defaults to False.
            is_furnished (bool, optional): Property must be furnished. Defaults to False.
            market (str, optional): _description_. Defaults to "dc".
            num_homes (int, optional): Total number of homes downloaded when returning search results. Defaults to 5000.
            ord (str, optional): _description_. Defaults to "redfin-recommended-asc".
            page_number (int, optional): _description_. Defaults to 1.
            sold_within_days (int, optional): Number of days since homes were sold. Defaults to 1825 (5 years).
            status (int, optional): _description_. Defaults to 9.
            travel_with_traffic (bool, optional): _description_. Defaults to False.
            travel_within_region (bool, optional): _description_. Defaults to False.
            uipt (str, optional): Property tye, you can included as many valid property types as you would like. Defaults to "1,2,3,4,5,6,7,8".
            utilities_included (bool, optional): Property must include utilities. Defaults to False.
            v (int, optional): _description_. Defaults to 8.

        Returns:
            ByteString: Returns a bytestring of the csv that makes up the download button from a Redfin search.
        """
        params = {
            "al": al,
            "has_deal": has_deal,
            "has_dishwasher": has_dishwasher,
            "has_laundry_facility": has_laundry_facility,
            "has_laundry_hookups": has_laundry_hookups,
            "has_parking": has_parking,
            "has_pool": has_pool,
            "has_short_term_lease": has_short_term_lease,
            "include_pending_homes": include_pending_homes,
            "isRentals": is_rentals,
            "is_furnished": is_furnished,
            "market": market,
            "num_homes": num_homes,
            "ord": ord,
            "page_number": page_number,
            "region_id": region_id,
            "region_type": region_type,
            "sold_within_days": sold_within_days,
            "status": status,
            "travel_with_traffic": travel_with_traffic,
            "travel_within_region": travel_within_region,
            "uipt": uipt,
            "utilities_included": utilities_included,
            "v": v,
        }
        response = self.redfin_request(url="api/gis-csv", params=params)
        return response.content

    def primary_region(self, url: str) -> requests.Response:
        """
        example url '/NY/New-Windsor/1615-State-Route-94-12553/home/54921952'
        """
        response = self.redfin_request(
            "api/home/details/primaryRegionInfo", {"path": url}
        )
        return response

    def shared_region(self, table_id: Union[str, int], **kwargs) -> requests.Response:
        """_summary_

        Args:
            table_id (Union[str,int]): _description_

        Returns:
            requests.Response: _description_
        """
        response = self.redfin_request(
            "api/region/shared-region-info",
            {"tableId": table_id, "regionTypeId": 2, "mapPageTypeId": 1, **kwargs},
        )
        return response

    def get_recently_sold(
        self, region_type: Union[str, int], region_id: Union[str, int]
    ) -> dict:
        response = self.redfin_request(
            "api/gis/recently-sold",
            {"region_type": region_type, "region_id": region_id},
        )
        return response

    def get_property_information(
        self, property_id: Union[int, str], listing_id: Union[int, str] = ""
    ) -> dict:
        """
        Returns all the information for a given property id. You may provide a listing id if the property is still for sale; however, it is not needed.

        Args:
            property_id (Union[int, str]): Redfin's unique property id
            listing_id (Union[int, str], optional): The property's listing id. Defaults to "".

        Returns:
            dict: Returns a nested dictionary with all the information for the property; however, it will need to be transformed to make it more useful for analysis.
        """
        response = self.request_property_data(
            url="belowTheFold",
            params={"propertyId": property_id, "listingId": listing_id},
        )
        return response

    def get_property_images(
        self, property_id: Union[int, str], listing_id: Union[int, str] = ""
    ) -> List[str]:
        """
        Returns a list of all url's for the images of the property.

        Args:
            property_id (Union[int, str]): Redfin's unique property id.
            listing_id (Union[int, str], optional): The property's listing id. Defaults to "".

        Returns:
            List[str]: A list of all url's for the images of the property.
        """
        response = self.request_property_data(
            url="aboveTheFold",
            params={"propertyId": property_id, "listingId": listing_id},
        )
        image_list = []
        for i in response["payload"]["mediaBrowserInfo"]["photos"]:
            image_list.append(i["photoUrls"]["nonFullScreenPhotoUrlCompressed"])
        return image_list

    def get_property_timeseries_estimate(
        self, property_id: Union[int, str], listing_id: Union[int, str] = ""
    ) -> dict:
        """
        Returns a monthly time series for the estimate of the house

        Args:
            property_id (Union[int, str]): Redfin's unique property id.
            listing_id (Union[int, str], optional): The property's listing id. Defaults to "".

        Returns:
            dict: time series dict with {'Mmm yy':'property estimate'} with monthly estimates of the property for the past 5 years from query time.
        """
        response = self.request_property_data(
            url="avmHistoricalData",
            params={"propertyId": property_id, "listingId": listing_id},
        )
        estimate_list = response["payload"]["propertyTimeSeries"]
        month_range = list(range(-1, 12 * 5))
        month_list = [
            (
                datetime.datetime.today()
                - dateutil.relativedelta.relativedelta(months=i - 1)
            ).strftime("%b %y")
            for i in month_range
        ][::-1]
        ts = {month_list[i]: estimate_list[i] for i in range(len(estimate_list))}
        return ts

    def get_similar_homes(
        self, property_id: Union[int, str], listing_id: Union[int, str] = ""
    ) -> dict:
        """_summary_

        Args:
            property_id (Union[int, str]): _description_
            listing_id (Union[int, str], optional): _description_. Defaults to "".

        Returns:
            dict: _description_
        """
        response = self.request_property_data(
            url="avm",
            params={"propertyId": property_id, "listingId": listing_id},
        )
        return response

    def get_offer_insights(
        self,
        region_type: Union[str, int],
        region_id: Union[str, int],
        property_type: Union[str, int] = "",
    ) -> dict:
        """_summary_

        Args:
            region_type (Union[str, int]): Redfin region type for your query:  1-neighborhood, 2-ZIP code, 5-County, 6-City
            region_id (Union[str, int]): Redfin unique id for the region associated with your search. The value is
            obtained by using self.get_region_id.
            property_type (Union[str, int], optional): Redfin property type for your query:  1-House, 2-Condo, 3-Townhouse, 4-Multi-family, 5-Land, 6-Other. Defaults to "".
        Returns:
            dict: _description_
        """
        response = self.request_region_data(
            url="offer-insights",
            region_type=region_type,
            region_id=region_id,
            property_type=property_type,
        )
        return response

    def get_best_schools(
        self,
        region_type: Union[str, int],
        region_id: Union[str, int],
        property_type: Union[str, int] = "",
    ) -> dict:
        """_summary_

        Args:
            region_type (Union[str, int]): Redfin region type for your query:  1-neighborhood, 2-ZIP code, 5-County, 6-City
            region_id (Union[str, int]): Redfin unique id for the region associated with your search. The value is
            obtained by using self.get_region_id.
            property_type (Union[str, int], optional): Redfin property type for your query:  1-House, 2-Condo, 3-Townhouse, 4-Multi-family, 5-Land, 6-Other. Defaults to "".

        Returns:
            dict: _description_
        """
        response = self.request_region_data(
            url="best-schools",
            region_type=region_type,
            region_id=region_id,
            property_type=property_type,
        )
        return response

    def get_walk_score_data(
        self,
        region_type: Union[str, int],
        region_id: Union[str, int],
        property_type: Union[str, int] = "",
    ) -> dict:
        """_summary_

        Args:
            region_type (Union[str, int]): Redfin region type for your query:  1-neighborhood, 2-ZIP code, 5-County, 6-City
            region_id (Union[str, int]): Redfin unique id for the region associated with your search. The value is
            obtained by using self.get_region_id.
            property_type (Union[str, int], optional): Redfin property type for your query:  1-House, 2-Condo, 3-Townhouse, 4-Multi-family, 5-Land, 6-Other. Defaults to "".

        Returns:
            dict: _description_
        """
        response = self.request_region_data(
            url="walk-score-data",
            region_type=region_type,
            region_id=region_id,
            property_type=property_type,
        )
        return response

    def get_region_trends(
        self,
        region_type: Union[str, int],
        region_id: Union[str, int],
        property_type: Union[str, int] = "",
    ) -> dict:
        """_summary_

        Args:
            region_type (Union[str, int]): Redfin region type for your query:  1-neighborhood, 2-ZIP code, 5-County, 6-City
            region_id (Union[str, int]): Redfin unique id for the region associated with your search. The value is
            obtained by using self.get_region_id.
            property_type (Union[str, int], optional): Redfin property type for your query:  1-House, 2-Condo, 3-Townhouse, 4-Multi-family, 5-Land, 6-Other. Defaults to "".

        Returns:
            dict: _description_
        """
        response = self.request_region_data(
            url="trends",
            region_type=region_type,
            region_id=region_id,
            property_type=property_type,
        )
        return response

    def get_flood_risk_data(
        self,
        region_type: Union[str, int],
        region_id: Union[str, int],
    ) -> dict:
        """_summary_

        Args:
            region_type (Union[str, int]): Redfin region type for your query:  1-neighborhood, 2-ZIP code, 5-County, 6-City
            region_id (Union[str, int]): Redfin unique id for the region associated with your search. The value is
            obtained by using self.get_region_id.

        Returns:
            dict: _description_
        """
        response = self.request_region_data(
            url="floodRisk-data", region_type=region_type, region_id=region_id
        )
        return response

    def get_market_insights_interlinks(
        self,
        region_type: Union[str, int],
        region_id: Union[str, int],
    ) -> dict:
        """_summary_

        Args:
            region_type (Union[str, int]): Redfin region type for your query:  1-neighborhood, 2-ZIP code, 5-County, 6-City
            region_id (Union[str, int]): Redfin unique id for the region associated with your search. The value is
            obtained by using self.get_region_id.

        Returns:
            dict: _description_
        """
        response = self.request_region_data(
            url="market-insights-interlinks",
            region_type=region_type,
            region_id=region_id,
        )
        return response

    def get_env_risk_data(
        self,
        region_type: Union[str, int],
        region_id: Union[str, int],
    ) -> dict:
        """_summary_

        Args:
            region_type (Union[str, int]): Redfin region type for your query:  1-neighborhood, 2-ZIP code, 5-County, 6-City
            region_id (Union[str, int]): Redfin unique id for the region associated with your search. The value is
            obtained by using self.get_region_id.

        Returns:
            dict: _description_
        """
        response = self.request_region_data(
            url="envRisk-data", region_type=region_type, region_id=region_id
        )
        return response

    def get_home_feature_trends(
        self,
        region_type: Union[str, int],
        region_id: Union[str, int],
    ) -> dict:
        """_summary_

        Args:
            region_type (Union[str, int]): Redfin region type for your query:  1-neighborhood, 2-ZIP code, 5-County, 6-City
            region_id (Union[str, int]): Redfin unique id for the region associated with your search. The value is
            obtained by using self.get_region_id.

        Returns:
            dict: _description_
        """
        response = self.request_region_data(
            url="home-feature-trends/entrypoint",
            region_type=region_type,
            region_id=region_id,
        )
        return response

    def get_compete_score(
        self,
        region_type: Union[str, int],
        region_id: Union[str, int],
    ) -> dict:
        """_summary_

        Args:
            region_type (Union[str, int]): Redfin region type for your query:  1-neighborhood, 2-ZIP code, 5-County, 6-City
            region_id (Union[str, int]): Redfin unique id for the region associated with your search. The value is
            obtained by using self.get_region_id.

        Returns:
            dict: _description_
        """
        response = self.request_region_data(
            url="compete-score", region_type=region_type, region_id=region_id
        )
        return response

    def get_nearby_compete_scores(
        self,
        region_type: Union[str, int],
        region_id: Union[str, int],
    ) -> dict:
        """_summary_

        Args:
            region_type (Union[str, int]): Redfin region type for your query:  1-neighborhood, 2-ZIP code, 5-County, 6-City
            region_id (Union[str, int]): Redfin unique id for the region associated with your search. The value is
            obtained by using self.get_region_id.

        Returns:
            dict: _description_
        """
        response = self.request_region_data(
            url="nearby-compete-scores", region_type=region_type, region_id=region_id
        )
        return response

    # http://www.redfin.com/stingray/api/home/details/initialInfo?path=[REPLACE with redfin house URL (no http://www.redfin.com)]

    # offer insights
    # https://www.redfin.com/stingray/api/region/2/8729/1/offer-insights


# other apis
#  ['stingray/api/region/2/8729/1/offer-insights', DONE
#  'stingray/api/region/2/8729/1/best-schools', DONE
#  'stingray/api/region/2/8729/floodRisk-data', DONE
#  'stingray/api/region/2/8729/market-insights-interlinks', DONE
#  'stingray/api/region/2/8729/envRisk-data', DONE
#  'stingray/api/market-insights-page?region_id=22030&region_type=2',
#  'stingray/api/region/2/8729/home-feature-trends/entrypoint', DONE
#  'stingray/api/graph/2/8729/All/regional-housing-market/home_prices', ## Always has to be All and region type and region id must match.
#  'stingray/api/gis/recently-sold?region_type=2&region_id=8729',
#  'stingray/do/gis-school?region_id=8729&region_type=2',
#  'stingray/api/graph/2/8729/All/regional-housing-market/demand', # Always has to be All and region type and region id must match.
#  'stingray/api/region/2/8729/1/walk-score-data', DONE
#  'stingray/api/region/2/8729/compete-score', DONE
#  'stingray/api/region/2/8729/1/trends', DONE
#  'stingray/api/region/2/8729/nearby-compete-scores'] DONE


###All api calls on a property page

# [{'url': '/stingray/api/home/details/homeDetailsPageHeaderInfo',
#   'requestData': {'urlPath': '/stingray/api/home/details/homeDetailsPageHeaderInfo',
#    'method': 'GET',
#    'queryParams': [{'propertyId': '9701815'}]}},
#  {'url': '/stingray/api/region/shared-region-info',
#   'requestData': {'urlPath': '/stingray/api/region/shared-region-info',
#    'method': 'GET',
#    'queryParams': [{'tableId': '8729',
#      'regionTypeId': '2',
#      'mapPageTypeId': '1'}]}},
#  {'url': '/stingray/api/home/details/marketInsightsInfo',
#   'requestData': {'urlPath': '/stingray/api/home/details/marketInsightsInfo',
#    'method': 'GET',
#    'queryParams': [{'propertyId': '9701815', 'listingId': '104431105'}]}},
#  {'url': '/stingray/api/home/details/listingStatusBannerInfo/v1',
#   'requestData': {'urlPath': '/stingray/api/home/details/listingStatusBannerInfo/v1',
#    'method': 'GET',
#    'queryParams': [{'propertyId': '9701815', 'listingId': '104431105'}]}},
#  {'url': '/stingray/api/home/details/banner-data/p1',
#   'requestData': {'urlPath': '/stingray/api/home/details/banner-data/p1',
#    'method': 'GET',
#    'queryParams': [{'propertyId': '9701815',
#      'accessLevel': '1',
#      'listingId': '104431105'}]}},
#  {'url': '/stingray/api/home/details/tourInsights',
#   'requestData': {'urlPath': '/stingray/api/home/details/tourInsights',
#    'method': 'GET',
#    'queryParams': [{'listingId': '104431105',
#      'propertyId': '9701815',
#      'accessLevel': '1',
#      'pageType': '3'}]}},
#  {'url': '/stingray/api/home/details/mainHouseInfoPanelInfo',
#   'requestData': {'urlPath': '/stingray/api/home/details/mainHouseInfoPanelInfo',
#    'method': 'GET',
#    'queryParams': [{'propertyId': '9701815',
#      'accessLevel': '1',
#      'listingId': '104431105',
#      'pageType': '3'}]}},
#  {'url': '/stingray/api/home/details/moreResourcesInfo',
#   'requestData': {'urlPath': '/stingray/api/home/details/moreResourcesInfo',
#    'method': 'GET',
#    'queryParams': [{'propertyId': '9701815'}]}},
#  {'url': '/stingray/api/building/details-page/v1',
#   'requestData': {'urlPath': '/stingray/api/building/details-page/v1',
#    'method': 'GET',
#    'queryParams': [{'propertyId': '9701815'}]}},
#  {'url': '/stingray/api/region/2/8729/nearby-compete-scores',
#   'requestData': {'urlPath': '/stingray/api/region/2/8729/nearby-compete-scores',
#    'method': 'GET',
#    'queryParams': []}},
#  {'url': '/stingray/api/home/details/similars/listings',
#   'requestData': {'urlPath': '/stingray/api/home/details/similars/listings',
#    'method': 'GET',
#    'queryParams': [{'propertyId': '9701815',
#      'accessLevel': '1',
#      'listingId': '104431105',
#      'marketId': '5'}]}},
#  {'url': '/stingray/api/home/details/listing/floorplans',
#   'requestData': {'urlPath': '/stingray/api/home/details/listing/floorplans',
#    'method': 'GET',
#    'queryParams': [{'listingId': '104431105'}]}},
#  {'url': '/stingray/api/home/details/descriptiveParagraph',
#   'requestData': {'urlPath': '/stingray/api/home/details/descriptiveParagraph',
#    'method': 'GET',
#    'queryParams': [{'propertyId': '9701815',
#      'accessLevel': '1',
#      'listingId': '104431105'}]}},
#  {'url': '/stingray/api/home/details/propertyParcelInfo?propertyId=9701815&pageType=3',
#   'requestData': {'urlPath': '/stingray/api/home/details/propertyParcelInfo?propertyId=9701815&pageType=3',
#    'method': 'GET',
#    'queryParams': []}},
#  {'url': '/stingray/api/home/details/rental-estimate',
#   'requestData': {'urlPath': '/stingray/api/home/details/rental-estimate',
#    'method': 'GET',
#    'queryParams': [{'propertyId': '9701815',
#      'accessLevel': '1',
#      'listingId': '104431105'}]}},
#  {'url': '/stingray/api/home/details/initialInfo',
#   'requestData': {'urlPath': '/stingray/api/home/details/initialInfo',
#    'method': 'GET',
#    'queryParams': [{'path': 'NY/Albany/363-Elk-St-12206/home/97942731'}]}}, this give listing id
#  {'url': '/stingray/api/home/details/similars/solds',
#   'requestData': {'urlPath': '/stingray/api/home/details/similars/solds',
#    'method': 'GET',
#    'queryParams': [{'propertyId': '9701815',
#      'accessLevel': '1',
#      'listingId': '104431105',
#      'marketId': '5'}]}},
#  {'url': '/stingray/api/home/details/owner-estimate',
#   'requestData': {'urlPath': '/stingray/api/home/details/owner-estimate',
#    'method': 'GET',
#    'queryParams': [{'propertyId': '9701815'}]}},
#  {'url': '/stingray/do/chat/omdpChatPromptEligibility',
#   'requestData': {'urlPath': '/stingray/do/chat/omdpChatPromptEligibility',
#    'method': 'GET',
#    'queryParams': [{'propertyId': '9701815'}]}},
#  {url:/stingray/api/home/details/compHomeTags/compHomeTagsInfo,
#   'requestData':{'urlPath': '/stingray/api/home/details/compHomeTags/compHomeTagsInfo',
#   'method': 'GET',
#   'queryParams': [{'property_id': '9701815',
#     'comp_property_ids':[9700684,9701700,9701826,180482505,9701373,9735639],
#     'predicted_value': '789135.01',
#     'display_level': 1}]}},
#  {'url': '/stingray/do/chat/omdpChatPromptEligibility',
#   'requestData': {'urlPath': '/stingray/do/chat/omdpChatPromptEligibility',
#    'method': 'GET',
#    'queryParams': [{'propertyId': '9701815'}]}},
#  {'url': '/stingray/api/home/details/aroundThisHomeSectionInfo',
#   'requestData': {'urlPath': '/stingray/api/home/details/aroundThisHomeSectionInfo',
#    'method': 'GET',
#    'queryParams': [{'propertyId': '9701815', 'listingId': '104431105'}]}},
#  {'url': '/stingray/api/v1/home/details/propertyCommentsInfo',
#   'requestData': {'urlPath': '/stingray/api/v1/home/details/propertyCommentsInfo',
#    'method': 'GET',
#    'queryParams': [{'propertyId': '9701815'}]}},
#  {'url': '/stingray/api/home/details/activityInfo',
#   'requestData': {'urlPath': '/stingray/api/home/details/activityInfo',
#    'method': 'GET',
#    'queryParams': [{'propertyId': '9701815',
#      'accessLevel': '1',
#      'listingId': '104431105'}]}},
#  {'url': '/stingray/api/home/details/v1/pagetagsinfo',
#   'requestData': {'urlPath': '/stingray/api/home/details/v1/pagetagsinfo',
#    'method': 'GET',
#    'queryParams': [{'path': 'NY/Albany/363-Elk-St-12206/home/97942731'}]}},
#  {'url': '/stingray/opendoor/api/estimate/forProperty/9701815?placement=omdp',
#   'requestData': {'urlPath': '/stingray/opendoor/api/estimate/forProperty/9701815?placement=omdp',
#    'method': 'GET',
#    'queryParams': []}},
#  {'url': '/stingray/api/home/details/primaryRegionInfo',
#   'requestData': {'urlPath': '/stingray/api/home/details/primaryRegionInfo',
#    'method': 'GET',
#    'queryParams': [{'path': 'NY/Albany/363-Elk-St-12206/home/97942731'}]}}, gives you the region type and region id {"regionType":2,"tableId":8729}}
#  {'url': '/stingray/do/api/costOfHomeOwnershipDetails',
#   'requestData': {'urlPath': '/stingray/do/api/costOfHomeOwnershipDetails',
#    'method': 'GET',
#    'queryParams': [{'propertyId': '9701815'}]}}, # mortgage information for the home
#  {'url': '/stingray/api/home/details/propertyParcelInfo',
#   'requestData': {'urlPath': '/stingray/api/home/details/propertyParcelInfo',
#    'method': 'GET',
#    'queryParams': [{'listingId': '104431105',
#      'propertyId': '9701815',
#      'accessLevel': '1',
#      'pageType': '3'}]}},
