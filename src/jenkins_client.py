from dotenv import load_dotenv
from pydantic import BaseModel , Field
from typing import List
load_dotenv()

class JenkinsURL(BaseModel):

    job_base_url : str = Field(
        description = ''
    )

def parse_jenkins(url : str) -> dict :

    """
        Returns the job_path and build_number when passed an entire Jenkins URL
    """

    job_base_url = url.split('/')[0] + "//" + url.split('/')[2]
    job_name = url.split('job/')[1].split('/')[0]
    job_number = url.split('job/')[1].split('/')[1]

    url_info = {
        'base_url' : job_base_url,
        'job_name' : job_name,
        'job_number' : job_number
    }

    return url_info


print(parse_jenkins(url="http://chipd007.chennai.visteon.com:9090/view/all/job/Ford_ACM_Klocwork/1688/"))