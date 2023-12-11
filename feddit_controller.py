from feddit_accessor import FedditAccessor
from util.feddit_util import FedditUtil
from util.logger_util import Logger
from fastapi import HTTPException

# Get logger for the current module
logger = Logger().get_logger(__name__)

class SubfedditController:
    """This controller class with entire business logic
    """

    def __init__(self) -> None:
        """Initialise class instance
        """
        self.fedditAccessor = FedditAccessor()

    def process_request_recent_comments(self, title: str) -> dict:
        """Method to process API request

        Args:
            title (str): Input title 

        Returns:
            dict: Response dictionary
        """

        # fetch id list for the title
        id_list = self.fedditAccessor.fetch_subfeddit_ids_from_title(title)

        # fetch all the coments for given ids
        total_comment_list = self.fedditAccessor.get_total_comment_list_for_subfeddit_ids(id_list)

        # add polarity
        updated_comment_list = self.comment_with_polarity_info(total_comment_list)
            
        # Sort the list of dictionaries based on the 'created_at' timestamp
        sorted_list = sorted(updated_comment_list, key=lambda x: x['created_at'], reverse=True)
            
        # Passing only required fields in the list
        selected_fields = ['id', 'text','score','classification']
        result_comment_list = []
        for item in sorted_list:
            result_dict = FedditUtil.select_fields(item, selected_fields)
            result_comment_list.append(result_dict)
                
        return {"title": title, "comments": result_comment_list[:25]}

    def process_request_comments_date_range(self, title:str, start_time:str, end_time:str) -> dict:
        """process request for comment with date range api

        Args:
            title (str): Input Titile
            start_time (str): Input start date
            end_time (str): Input end date

        Returns:
            dict: Response dictionary
        """
        
        # perform required validations 
        # Curretly performing only date validation. Similarly we can add more.
        FedditUtil.date_validation(start_time, end_time)

        # fetch id list for the title
        id_list = self.fedditAccessor.fetch_subfeddit_ids_from_title(title)

        # fetch all the coments for given ids
        total_comment_list = self.fedditAccessor.get_total_comment_list_for_subfeddit_ids(id_list)

        # add polarity
        updated_comment_list = self.comment_with_polarity_info(total_comment_list)

        # fetch comment within date range
        req_comment_list = self.result_comments_filtered_by_date_range(updated_comment_list, start_time, end_time)
        
        # sort on polarity
        sorted_list_on_score = sorted(req_comment_list, key=lambda x: x['score'], reverse=True)

        # Passing only required fields in the list
        selected_fields = ['id', 'text','score','classification']
        result_comment_list = list()
        for item in sorted_list_on_score:
            result_dict = FedditUtil.select_fields(item, selected_fields)
            print(f'result_dict is {result_dict}')
            result_comment_list.append(result_dict)
        
        return {"title": title, "start_time": 
                start_time, "end_time": end_time, 
                "comment": result_comment_list}


    def result_comments_filtered_by_date_range(self, comment_list: list, start_time: str, end_time: str) -> list:
        """Function to filter the comments by given date range

        Args:
            comment_list (list): Input comment list to be filtered
            start_time (str): Input start date of date range
            end_time (str): Input end date of date range

        Returns:
            list: Returns filtered comment list 
        """
        # Get epoch date for given dates
        starts = FedditUtil.get_epoch_from_date(start_time)
        ends = FedditUtil.get_epoch_from_date(end_time)
        filtered_comment_list = [comment for comment in comment_list if starts <= comment['created_at'] <= ends]
        return filtered_comment_list

    def comment_with_polarity_info(self, comment_list: list) -> list:
        """Function to fetch polarity information and classification of comments

        Args:
            comment_list (list): Input comment list

        Returns:
            list: Return comments list with polarity information and classification
        """
        comment_list_score = []
        for item in comment_list:
            score_res = FedditUtil.get_polarity_score(item['text'])
            item['score'] = score_res['score']
            item['classification'] = score_res['classification']
            comment_list_score.append(item)
        return comment_list_score
    
