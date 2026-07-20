from dotenv import load_dotenv
from pydantic import BaseModel , Field
load_dotenv()

class JenkinsURL(BaseModel):

    job_base_url : str = Field(
        description = 'Base url of the jenkins job',
    )
    job_name : str = Field(
        description='Name of the Job'
    )
    job_number : str = Field(
        description='Number of the job executed'
    )

def parse_jenkins(url : str) -> JenkinsURL :

    """
        Returns the job_path and build_number when passed an entire Jenkins URL
    """

    job_base_url = url.split('/')[0] + "//" + url.split('/')[2]
    job_name = url.split('job/')[1].split('/')[0]
    job_number = url.split('job/')[1].split('/')[1]

    jenkins_info = JenkinsURL(
        job_base_url= job_base_url,
        job_name=job_name,
        job_number=job_number
    )

    return jenkins_info


if __name__ == "__main__":

    info = parse_jenkins(url = "http://chipd007.chennai.visteon.com:9090/job/Ford_ACM_Klocwork/1688/")
    print(info)