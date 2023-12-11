from textblob import TextBlob
from datetime import datetime

class FedditUtil:
    """This is utility class containing reusable utility methods
    """
    API_INPUT_FORMAT = "%Y-%m-%d"

    @staticmethod
    def get_polarity_score(comment: dict) -> dict :
        """Method to get text polrity

        Args:
            comment (dict): dictonary containig text for whcih ploarity is required

        Returns:
            dict: response dictionary
        """
        # Create a TextBlob object
        blob = TextBlob(comment)
        # Get the polarity score (-1 to 1, where -1 is negative, 1 is positive)
        polarity_score = blob.sentiment.polarity

        if polarity_score >= 0:
            classification = 'Positive'
        else:
            classification = 'Negative'   
        return {'score':polarity_score,'classification':classification}
    
    @staticmethod
    def get_epoch_from_date(mydate: str) -> int:
        """Get epoch int from date string

        Args:
            mydate (str): _description_

        Returns:
            _type_: _description_
        """
        # Convert date to datetime
        my_datetime = datetime.strptime(mydate, FedditUtil.API_INPUT_FORMAT)

        # Convert datetime to epoch
        epoch_time = int(my_datetime.timestamp())
        return epoch_time
    
    @staticmethod
    def select_fields(input_dict: dict, selected_fields: list) -> dict:
        """Method to select required key froma  dictionary

        Args:
            input_dict (_type_): _description_
            selected_fields (_type_): _description_

        Returns:
            _type_: _description_
        """
        return {key: input_dict[key] for key in selected_fields if key in input_dict}


    @staticmethod
    def date_validation(start:str , end: str) -> None:
        """Perform required date validation

        Args:
            start (str): Date string
            end (str): Date string

        Raises:
            Exception: Bad Input Date
        """
        # correct dat format
        is_start_valid = FedditUtil.is_valid_date(start, FedditUtil.API_INPUT_FORMAT)
        is_end_valid = FedditUtil.is_valid_date(end, FedditUtil.API_INPUT_FORMAT)

        # is end greater than start
        is_end_greater = (FedditUtil.get_epoch_from_date(end) >= FedditUtil.get_epoch_from_date(start))

        if (not is_end_valid or not is_start_valid or not is_end_greater):
            raise Exception("Invalid Input Dates: Start and End date must follow YYYY-MM-DD. Also, End date should be greater than Start Date")

    @staticmethod
    def is_valid_date(mydate: str, format:str) -> bool:
        """Check if date string is valid as per given format

        Args:
            mydate (str): input date string
            format (str): date format

        Returns:
            bool: validation pased or failed
        """
        try:
            datetime.strptime(mydate, format)
            return True
        except Exception:
            return False    