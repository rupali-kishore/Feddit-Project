import requests
import sys
sys.path.append("/Users/rajat/Documents/Rupali/MyProjects/Python/FedditProject")

class FedditAccessor:
    """
    FedditAccessor class is responsible for fetching required info from Feddit APIs
    Provided in the sue-case
    """

    def fetch_subfeddit_ids_from_title(self, titile: str) -> list:
        """Method to fetch the subfeddit id from given subfeddit title.

        Args:
            titile (str): Input title

        Returns:
            list: Returns list of ids
        """
        skip = 0
        limit = 10
        result = list()
        while True:
            response = requests.get('http://0.0.0.0:8080/api/v1/subfeddits/?skip='+str(skip)+'&limit='+str(limit))
            subfeddits = response.json()['subfeddits']
            if not subfeddits:
                return result
            else:
                for items in subfeddits:
                    if items['title']==titile:
                        result.append(items['id'])
            skip = skip + limit
        return result
    
    def get_total_comment_list_for_subfeddit_ids(self, id_list: list) -> list:
        """Method to fetch all comments list for input subfeddit ids

        Args:
            id_list (list): Input id list

        Returns:
            list: Returns comments list
        """
        comment_list = list()
        for item in id_list:
            response = requests.get('http://0.0.0.0:8080/api/v1/subfeddit/?subfeddit_id='+str(item))
            comments = response.json()['comments']
            for item in comments:
                comment_list.append(item)
        return comment_list